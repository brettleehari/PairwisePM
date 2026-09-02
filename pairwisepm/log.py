"""PairwisePM decision log — JSONL records, ζ (transitivity), Brier.

The log is LOCAL and belongs to the user (Spine: no server-side storage; the
Space stores nothing). This module never touches the network and never calls
the clock — the caller passes every timestamp in, so nothing here can invent
provenance.

Honesty rules implemented here:
- Every record carries an ``outcome`` slot that starts null: the schema is
  ready for M2/M3 outcome labeling from day one, but nothing pretends an
  outcome exists before the user labels it (spec §6).
- ζ (Kendall's coefficient of consistency, from circular triads over the
  user's own picks) and the Brier score accumulate from decision 1 — the noise
  meter runs on the judge, not just the ideas (spec §4).
- Override rationale is recorded verbatim when the user picks against the
  model: disagreement is data, not an error state.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from itertools import combinations
from typing import Dict, List, Optional, Sequence, Tuple

from .config import ModeConfig
from .engine import ComparisonResult

SCHEMA_VERSION = 1

# Decisions D4 build-meanwhile default (config, not code): the reliability
# curve unlocks at n >= 30 decisions in a mode; below that, binned reliability
# curves are themselves overconfident. The curve itself is not built in v1 —
# this constant ships so the unlock rule is already config when it is.
RELIABILITY_CURVE_MIN_N = 30


def make_record(
    timestamp: str,
    mode: str,
    name_a: str,
    name_b: str,
    raw_a: Dict[str, float],
    raw_b: Dict[str, float],
    result: ComparisonResult,
    pick: str,
    evaluative_a: Optional[Dict[str, float]] = None,
    evaluative_b: Optional[Dict[str, float]] = None,
    flags_a: Optional[Dict[str, bool]] = None,
    flags_b: Optional[Dict[str, bool]] = None,
    override_rationale: Optional[str] = None,
    config_fingerprint: Optional[str] = None,
) -> dict:
    """Build one JSONL record per spec §6.

    ``timestamp`` is supplied by the caller (ISO-8601 recommended) — this
    module deliberately has no clock. ``pick`` is "A" or "B". The record
    stores BOTH raw and z factor vectors, the evaluative (never-scored)
    inputs, both model outputs, the override rationale if any, and a null
    outcome slot awaiting later labeling.

    ``config_fingerprint`` (architecture data contract, additive v1.1 key) is
    ``ModeConfig.fingerprint`` — sha256 of the canonical loaded YAML — so
    audits can be partitioned by policy version. ``None`` (older callers,
    code-built configs) is recorded as null; readers must ignore unknown keys,
    so pre-v1.1 logs remain valid.
    """
    if pick not in ("A", "B"):
        raise ValueError("pick must be 'A' or 'B'")
    return {
        "schema_version": SCHEMA_VERSION,
        "timestamp": timestamp,
        "mode": mode,
        "config_fingerprint": config_fingerprint,
        "idea_a": {"name": name_a, "raw": dict(raw_a), "z": dict(result.z_a)},
        "idea_b": {"name": name_b, "raw": dict(raw_b), "z": dict(result.z_b)},
        "evaluative": {  # displayed, never scored (Spine scope boundary)
            "a": dict(evaluative_a or {}),
            "b": dict(evaluative_b or {}),
        },
        "flags": {"a": dict(flags_a or {}), "b": dict(flags_b or {})},
        "pick": pick,
        "model": {
            "active": result.active_model,
            "m0_p": result.m0.p,
            "m0_interval": list(result.m0.interval),
            "m0_equal_p": result.m0_equal.p,
            "m1_p": result.m1.p if result.m1 else None,
            "m1_interval": list(result.m1.interval) if result.m1 else None,
            "verdict": result.active.verdict,
        },
        "override_rationale": override_rationale or None,
        "outcome": None,  # null until the user labels it later (M2/M3 runway)
    }


@dataclass
class DecisionLog:
    """In-memory log with JSONL (de)serialization and audit statistics."""

    records: List[dict] = field(default_factory=list)

    # -- persistence --------------------------------------------------------

    def append(self, record: dict) -> None:
        self.records.append(record)

    def to_jsonl(self) -> str:
        return "\n".join(json.dumps(r, ensure_ascii=False) for r in self.records)

    @classmethod
    def from_jsonl(cls, text: str) -> "DecisionLog":
        records = []
        for i, line in enumerate(text.splitlines()):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"line {i + 1}: not valid JSON ({e.msg})") from e
            if "pick" not in rec or "idea_a" not in rec or "idea_b" not in rec:
                raise ValueError(f"line {i + 1}: not a PairwisePM record")
            records.append(rec)
        return cls(records=records)

    def merged(self, other: "DecisionLog") -> "DecisionLog":
        """Merge another log into this one (design S10c contract): the union
        of both logs, ordered by timestamp, with duplicates — same timestamp
        AND same inputs (mode, both raw vectors, pick) — kept once. Neither
        input log is mutated; a new DecisionLog is returned."""
        def dedupe_key(r: dict) -> str:
            return json.dumps(
                [r.get("timestamp"), r.get("mode"),
                 r.get("idea_a", {}).get("raw"), r.get("idea_b", {}).get("raw"),
                 r.get("pick")],
                sort_keys=True,
            )

        seen: Dict[str, dict] = {}
        for r in self.records + other.records:
            seen.setdefault(dedupe_key(r), r)
        records = sorted(seen.values(), key=lambda r: str(r.get("timestamp", "")))
        return DecisionLog(records=records)

    # -- views --------------------------------------------------------------

    def for_mode(self, mode: str) -> List[dict]:
        return [r for r in self.records if r.get("mode") == mode]

    def n(self, mode: Optional[str] = None) -> int:
        return len(self.for_mode(mode)) if mode else len(self.records)

    def training_data(
        self, cfg: ModeConfig
    ) -> Tuple[List[Dict[str, float]], List[int]]:
        """(factor-delta rows, picks) for M1 — the log IS the training set.
        pick = 1 when the user chose A. Records missing any current factor key
        are skipped (schema drift tolerance, not silent invention)."""
        rows: List[Dict[str, float]] = []
        picks: List[int] = []
        for r in self.for_mode(cfg.mode):
            za, zb = r["idea_a"]["z"], r["idea_b"]["z"]
            if all(k in za and k in zb for k in cfg.factor_keys):
                rows.append({k: za[k] - zb[k] for k in cfg.factor_keys})
                picks.append(1 if r["pick"] == "A" else 0)
        return rows, picks

    def raw_vectors(self, mode: str) -> List[Dict[str, float]]:
        """All raw factor vectors (both sides) — feeds log-derived z-scoring
        distributions once the log outgrows the seeds."""
        out = []
        for r in self.for_mode(mode):
            out.append(r["idea_a"]["raw"])
            out.append(r["idea_b"]["raw"])
        return out

    # -- audit statistics ----------------------------------------------------

    def kendall_zeta(self, mode: Optional[str] = None) -> Optional[float]:
        """ζ, Kendall's coefficient of consistency, from circular triads.

        Preference relation: the MOST RECENT pick per unordered idea pair, in
        log order (repeat comparisons update the edge, they never
        double-count — compliance T-ZETA interface note). Only triads with
        all three edges present are examined; a triad is circular when every
        node has out-degree 1.

        ζ = 1 − c/c_max. When the observed preference graph is a COMPLETE
        tournament on its n ideas, c_max is Kendall's exact maximum:
        (n³−n)/24 for odd n, (n³−4n)/24 for even n. On an incomplete graph
        c_max falls back to T·(n+1)/(4(n−2)) over the T observed complete
        triads — a close approximation. Clipped to [0, 1]. Returns None until
        at least one complete triad exists: the meter reads "insufficient
        data", it never fabricates a consistency score.
        """
        recs = self.for_mode(mode) if mode else self.records
        # Most recent pick per unordered pair wins (later records overwrite).
        beats: Dict[Tuple[str, str], bool] = {}
        for r in recs:
            a = r["idea_a"]["name"].strip()
            b = r["idea_b"]["name"].strip()
            if not a or not b or a == b:
                continue
            winner = a if r["pick"] == "A" else b
            key = tuple(sorted((a, b)))
            beats[key] = winner == key[0]  # True: key[0] beats key[1]

        items = sorted({x for pair in beats for x in pair})

        def edge(u: str, v: str) -> Optional[int]:
            key = tuple(sorted((u, v)))
            if key not in beats:
                return None
            first_beats = beats[key]
            return (1 if first_beats else -1) if u == key[0] else (-1 if first_beats else 1)

        total = circular = 0
        involved = set()
        for x, y, z in combinations(items, 3):
            exy, eyz, ezx = edge(x, y), edge(y, z), edge(z, x)
            if exy is None or eyz is None or ezx is None:
                continue
            total += 1
            involved.update((x, y, z))
            out_deg = {
                x: (exy == 1) + (ezx == -1),
                y: (eyz == 1) + (exy == -1),
                z: (ezx == 1) + (eyz == -1),
            }
            if all(d == 1 for d in out_deg.values()):
                circular += 1
        if total == 0:
            return None
        n = len(items)
        if len(beats) == n * (n - 1) // 2:  # complete tournament: exact c_max
            c_max = (n ** 3 - n) / 24.0 if n % 2 == 1 else (n ** 3 - 4 * n) / 24.0
        else:
            n_i = len(involved)
            c_max = total * (n_i + 1) / (4.0 * (n_i - 2))
        return max(0.0, min(1.0, 1.0 - circular / c_max)) if c_max > 0 else None

    def brier(self, mode: Optional[str] = None) -> Optional[float]:
        """Brier score of the active model's probability against the user's
        pick, accumulating from decision 1 (spec §4). Until outcomes exist
        this measures model–judge agreement calibration, not real-world
        accuracy — and in 0→1 mode it NEVER becomes an accuracy claim."""
        recs = self.for_mode(mode) if mode else self.records
        vals = []
        for r in recs:
            m = r.get("model", {})
            p = m.get("m1_p") if m.get("active") == "M1" and m.get("m1_p") is not None else m.get("m0_p")
            if p is None:
                continue
            y = 1.0 if r["pick"] == "A" else 0.0
            vals.append((p - y) ** 2)
        return sum(vals) / len(vals) if vals else None

    def outcome_brier(self, mode: Optional[str] = None) -> Optional[float]:
        """Brier vs. LABELED outcomes only (outcome: 'A'|'B' set by the user
        later). Returns None until at least one outcome is labeled — the M2
        runway, never conflated with the pick-agreement Brier above."""
        recs = self.for_mode(mode) if mode else self.records
        vals = []
        for r in recs:
            if r.get("outcome") not in ("A", "B"):
                continue
            m = r.get("model", {})
            p = m.get("m1_p") if m.get("active") == "M1" and m.get("m1_p") is not None else m.get("m0_p")
            if p is None:
                continue
            y = 1.0 if r["outcome"] == "A" else 0.0
            vals.append((p - y) ** 2)
        return sum(vals) / len(vals) if vals else None

    def override_rate(self, mode: Optional[str] = None) -> Optional[float]:
        """Share of decisions where the user picked against a non-too-close
        verdict. Displayed, never judged: overriding is allowed and logged."""
        recs = self.for_mode(mode) if mode else self.records
        n = disagreed = 0
        for r in recs:
            verdict = r.get("model", {}).get("verdict")
            if verdict in ("A", "B"):
                n += 1
                if r["pick"] != verdict:
                    disagreed += 1
        return disagreed / n if n else None
