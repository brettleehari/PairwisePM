"""Loader for PairwisePM YAML factor schemas.

The factor tables are CONFIG, not code (technical-spec §2): prior weights are a
stated, editable policy pending Decisions-Leaf sign-off (D1/D2), and editing a
weight must never require touching the engine. This module is the only place
that reads the YAML files; everything downstream works with typed objects.

Honesty rules implemented here:
- The 0→1 config carries a mandatory ``banner`` (structure-not-prediction). The
  loader refuses a zero_to_one schema without one, so no packaging accident can
  strip the claim-limiting banner out of the product.
- Evaluative inputs (strategic fit, brand) are loaded into a separate list that
  the engine never sees as factors — they are excluded from the mechanical
  score by type, not by convention.
- The Ceiling flag lives in ``flags`` and carries no weight field at all: it is
  unweighted by construction and cannot enter the score.

D1/D2 RESOLUTION-ROUND PROCEDURE (owner: engineering; this is the file that
tells you the YAML is authoritative, so the procedure lives here rather than in
a packet nobody re-reads). When the Decisions record directs value changes,
engineering edits configs/*.yaml only — no code motion — citing a per-entry
``resolution_source``. Three constraints, each contributed by another leaf and
each cheaper to honor than to discover:

1. TWO EDIT CLASSES SHARE THESE FILES (design). ``prior_weight``, ``sign``,
   ``seed_mean``, ``seed_std``, ``transform`` and ``plausible_range`` are
   POLICY: they change freely under the D1/D2 record, owing nothing to the copy
   catalogue. ``label``, ``banner``, ``factors[].name`` / ``.scale`` /
   ``.rationale``, ``flags[].name`` / ``.description`` and
   ``evaluative_inputs[].name`` / ``.scale`` / ``.note``
   are COPY. Moving one of those is a
   copy change: per-line notification and a §6.12 retrigger, NOT a config
   edit. "YAML only, no code motion" has been read by five seats as "no
   rendered surface"; in these files those are different statements, and the
   two classes sit on neighbouring lines.

   SCOPE WORD ON THE RENDER CLAIM, NOT ON THE CLASS (design, round 18; each
   line grepped from this seat before it was written down; ``banner`` and
   ``evaluative_inputs[].scale`` added round 19 after architecture and
   compliance found both missing from every census of this population,
   theirs and mine). Rounds 16-17 of this docstring said all six COPY fields
   "render in the browser". There are NINE names, not six, and FIVE of them
   render:
     - RENDERS: ``label``; ``banner`` (0→1 only — configs/zero_to_one.yaml
       → app.py:91 ``BANNER_HTML`` → the gr.HTML at :854, permanent while in
       0→1; one_to_n's is null); ``factors[].name`` and ``.rationale``
       (app.py ``_factor_input``: the Textbox label and its ``info=``);
       ``factors[].scale``, WITH ONE SHADOW — for ``risk_surface`` the suffix
       is replaced by ``S['str.factor.risk_label_suffix']``.
     - NO CALL SITE TODAY: ``flags[].name`` (the ceiling checkbox label is
       ``S['str.factor.ceiling_label']``); ``flags[].description`` (the
       routing copy is the engine's pinned ``PINNED_CEILING``, T-CEIL-02);
       ``evaluative_inputs[].name`` / ``.scale`` / ``.note`` —
       ``cfg.evaluative_inputs`` is never read by app.py at all.
   THE EDIT-CLASS RULING IS UNCHANGED: all nine stay COPY and all nine still
   owe the per-line notification, because a field that is dead today is one
   call site away from live. What is narrowed is only the claim about where
   the text lands. The reason not to leave the wider wording standing: the
   field that reads most like a trust surface — ``evaluative_inputs[].note``,
   "not scored — labeled override input" — reaches no browser, while the four
   labels that DO carry the Spine's excluded-from-score refusal on screen are
   bare literals in app.py and are therefore NOT in this list at all. A
   reader doing the round at speed should not go looking for that refusal in
   these files; see ENG-COPY-EVALLABELS-01 at app.py's evaluative panel.

   ``banner`` IS THE ONE COPY FIELD THAT FAILS AT IMPORT, NOT UNDER PYTEST
   (architecture, round 19; re-derived here from the source rather than taken
   on report). It is the only field in the COPY list that has a counterpart
   in the design catalogue: app.py:73 asserts ``Z2O.banner ==
   S["str.banner.01"]`` at module import, and the two are byte-equal today.
   So a hand-edit to that one line does not surface as a red suite — THE APP
   DOES NOT START, before first paint, before any gate has anything to
   attach to, and with a traceback rather than a test name. If that fires
   during the resolution round it is the cross-reference working: the remedy
   is design's mint on leaves/design/strings.py plus a re-vendor, NEVER
   loosening or deleting the assert to make the app launch. Practical rule
   for a values round: the D1/D2 record has no reason to touch ``banner``,
   and the correct number of edits to it is zero.

   COVERAGE, AS OF ROUND 19 (this superseded a claim this docstring carried
   for three rounds — "the only coverage anywhere is non-empty
   (tests/test_engine.py), not correct" — which was true when written and is
   now false in two places). The five rendering fields have TWO authorities,
   not one, and the split is worth knowing before you edit rather than after:
     - ``banner`` — authority is the CATALOGUE's ``str.banner.01``. Design
       ruled it deliberately NOT ratified in their fixture (§6.19(i)); it is
       pinned by the import assert above and by two shipped clauses in
       tests/test_engine.py, which compliance's T-COPY-02c checks by name.
     - ``label``, ``factors[].name`` / ``.scale`` / ``.rationale`` — authority
       is design's ratified fixture, leaves/design/copy-authority.yaml,
       diffed BOTH directions by T-COPY-02 in tests/test_copy_surfaces.py.
   So a citation reading "the config copy is diffed against design's fixture"
   is four-fifths true and wrong about the field where a silent change would
   be worst. Neither instrument reads
   a policy value, so neither can red on a D1/D2 write — but both red if a
   values round moves rendered text, which is precisely the silent failure
   constraint 1 exists to catch. The per-line notification is still owed:
   a test tells you that you changed copy, it does not tell gtm's tour.

   NOTIFY BOTH DESIGN AND GTM, per line, if and only if a COPY field moves
   (gtm). Design owns the copy authority question; gtm owns the files that
   BREAK. Verified from this seat rather than taken on report: the three 1→N
   factor names occur 7 times across ``leaves/gtm/tour.html``, and the demo
   script names them aloud — so a rename lands as a presenter reading a script
   against a screen that no longer agrees with it, with the suite green, the
   mirror cmp clean and P-14/P-15 all passing, because none of those watch the
   correspondence between a factor name and a tour that quotes it. No hold, no
   deferral, no extra step in the round: one line, only on a copy edit.

2. RUN TWO COMMANDS AFTER THE WRITE AND BEFORE ANY PUSH (compliance):
   ``pytest tests/test_vendoring.py`` (gate P-14) and
   ``pytest tests/test_copy_surfaces.py`` (gate P-15).

   A SKIP IS A FAILURE OF THE CHECK, NOT A PASS (compliance, round 18). The
   pass condition for BOTH commands is ``N passed, 0 skipped`` — act on a
   red AND on a skip. pytest exits 0 on a file whose every clause skipped, so
   "green" and "nothing ran" are the same exit code; run them with ``-rs`` if
   you want the skipped ones named. Own runs this round: test_vendoring.py
   7 passed / 0 skipped, test_copy_surfaces.py 5 passed / 0 skipped, so this
   costs nothing today — which is the point, since a skip appearing later is
   exactly the event worth stopping for. T-VEND-07 now asserts structurally
   that T-VEND-04/05 can never acquire a skip predicate, so the floor holds
   even if this line is forgotten; the line is here because the person acting
   on the output is at this keyboard.

   WHERE THE GATE IS LIVE (architecture, round 18 — narrowing their own
   round-16 wording, which this file carried as "on this editable install").
   T-VEND-06 can red only where a repo checkout's ``configs/`` is present as
   the anchor AND a duplicate ``configs/`` tree is reachable on ``sys.path``.
   Off that, the guard skips (no authority to resolve against) or is absent
   entirely — the wheel target ships ``packages = ["pairwisepm"]`` plus the
   force-included ``configs`` and NO ``tests``, so on a plain install there
   is no file to run and no skip line to look for either. A green from such a
   tree asserted nothing.
   ONE CORRECTION TO THAT DEMAND'S STATED MECHANISM, measured here rather
   than transcribed: the trigger is NOT the working directory. ``ROOT`` in
   tests/test_vendoring.py is ``Path(__file__).resolve().parent.parent`` —
   the anchor is positional to the TEST FILE, not to the cwd. Run from /tmp
   against this repo's path, the file still reads 7 passed / 0 skipped
   (verified this round). So the instruction that carries the fact is: run
   THIS CHECKOUT'S copy of the file, from anywhere; a green means something
   only because the anchor beside it is the ``configs/`` you just wrote.
   And the green here is not vacuous: walking ``sys.path`` from this
   interpreter finds exactly one duplicate tree,
   ``.venv/lib/python3.11/site-packages/configs``, so the guard executes two
   byte comparisons rather than zero.

   P-14 / T-VEND-06 — EXPECT THIS ONE TO RED, on this machine, at the moment
   the write lands, with no reinstall involved (architecture; re-derived here
   rather than accepted on report). The venv is EDITABLE and its own dist-info
   nonetheless owns a second ``configs/`` tree:
   ``direct_url.json`` = {"dir_info": {"editable": true}}, while ``RECORD``
   lists ``configs/one_to_n.yaml`` and ``configs/zero_to_one.yaml`` with
   sha256 digests that I recomputed from both trees this round and found
   equal — the editable target inherits the wheel's force-include. So the
   duplicate is not waiting on some future non-editable install: it is here,
   byte-identical today, and the D1/D2 write falsifies it immediately. THAT
   RED IS THE GUARD WORKING, NOT A BROKEN ENVIRONMENT.

   The remedy is REFRESH-OR-REMOVE: re-run ``pip install -e .``, or
   ``pip uninstall pairwisepm``. NEVER hand-edit the site-packages copy, and
   NEVER delete ``[tool.hatch.build.targets.wheel.force-include]``
   ``"configs" = "configs"`` from pyproject.toml to make the red go away —
   that clause is the only reason ``pip install pairwisepm`` finds its schemas
   at all, so deleting it turns a loud correct red into a silent broken
   install path for every user. Which of refresh-or-remove pip actually
   performs is deliberately UNVERIFIED here: confirming it means mutating this
   venv, and the check is one command at the hour when it matters.

   P-15 / tests/test_copy_surfaces.py — the machine check that tells you WHICH
   EDIT CLASS you just made, so constraint 1 stops depending on anyone noticing
   mid-edit. It reds on a rendered config string left as ``TBD`` (the realistic
   failure of a fast values round), on a label that is the machine key, and on
   the four ``(not scored)`` markers going missing. Demonstrated, not assumed:
   those mutations leave ``tests/test_engine.py`` entirely green.

   This is the one hazard class that fails silently — a stale strings copy
   crashes at import; stale priors, or a rationale reading "TBD", serve a
   plausible wrong verdict with every other test green.

   ONE P-15 RED THAT DOES NOT MEAN YOU CHANGED COPY (observed live this
   round, not constructed). T-COPY-02 / T-COPY-02b read a fixture OUTSIDE
   every tree this procedure writes — ``leaves/design/copy-authority.yaml``,
   another leaf's file. Mid-round, with my own edits confined to this
   docstring and one comment in app.py, the command returned 2 failed on a
   ``yaml.scanner.ScannerError`` from the fixture being written by its owner
   at that second; re-run 40 seconds later: 10 passed. Measured rather than
   inferred, and with no repo file mutated — of the 8593 single-byte
   prefixes of that fixture, 855 fail to parse, the first at byte 2400 with
   exactly that error. An ABSENT fixture skips honestly (``_design_ratified_
   copy`` names FIXTURE as its subject); a HALF-WRITTEN one reds, and the
   failure text is pyyaml's, so it names a line in the scanner and not the
   file's owner. IF YOU SEE A SCANNER ERROR HERE: it is not a defect in
   configs/, not your write, and not a reason to touch anything — re-run.
   Only act on it if it survives a second run, and then it is design's file
   to repair, not this seat's. Nothing else in this procedure depends on a
   file another leaf owns; this one clause does, which is why it is
   written down instead of left to be rediscovered at the hour.

3. DO NOT FOLLOW THE ROUND WITH A PLAIN ``pip install .`` (architecture). That
   single command recreates A-13-01 — a second importable ``pairwisepm`` in
   site-packages whose binding depends on the working directory — and re-arms
   the force-included frozen ``configs/`` in the same step. The venv is
   editable (``pip install -e .``) and must stay that way. T-VEND-04 is what
   catches a slip here; this line exists so nobody has to rely on memory, not
   as a substitute for the guard.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import yaml

# Transforms applied to raw values before z-scoring. ``log10p`` handles
# heavy-tailed counts (e.g. Reach in users/quarter); seed mean/std for such a
# factor are stated in transform space.
_FORWARD: Dict[str, Callable[[float], float]] = {
    "identity": lambda x: float(x),
    "log10p": lambda x: math.log10(1.0 + max(float(x), 0.0)),
}
_INVERSE: Dict[str, Callable[[float], float]] = {
    "identity": lambda t: float(t),
    "log10p": lambda t: (10.0 ** float(t)) - 1.0,
}


@dataclass(frozen=True)
class Factor:
    """One scored factor: scale, prior policy weight, tag, seed distribution."""

    key: str
    name: str
    scale: str
    prior_weight: float  # magnitude; effective weight = sign * prior_weight
    sign: int  # +1 or -1
    tag: str  # "lever" | "fact"
    rationale: str
    seed_mean: float  # in transform space
    seed_std: float  # in transform space
    transform: str = "identity"
    plausible_range: Tuple[float, float] = (0.0, 4.0)

    @property
    def effective_weight(self) -> float:
        return self.sign * self.prior_weight

    def to_transform_space(self, raw: float) -> float:
        return _FORWARD[self.transform](raw)

    def from_transform_space(self, t: float) -> float:
        return _INVERSE[self.transform](t)

    def zscore(self, raw: float) -> float:
        """z-score a raw value against the seed (or log-updated) distribution."""
        return (self.to_transform_space(raw) - self.seed_mean) / self.seed_std

    def raw_from_z(self, z: float) -> float:
        """Invert a z-score back to raw units (used by path-to-parity)."""
        return self.from_transform_space(self.seed_mean + z * self.seed_std)

    def in_plausible_range(self, raw: float) -> bool:
        lo, hi = self.plausible_range
        return lo <= raw <= hi


@dataclass(frozen=True)
class EvaluativeInput:
    """Captured and displayed, NEVER scored (Spine scope boundary)."""

    key: str
    name: str
    scale: str
    note: str


@dataclass(frozen=True)
class Flag:
    """An unweighted flag (e.g. Ceiling). No weight field exists on purpose."""

    key: str
    name: str
    description: str


@dataclass(frozen=True)
class ModeConfig:
    mode: str  # "one_to_n" | "zero_to_one"
    label: str
    banner: Optional[str]
    factors: List[Factor] = field(default_factory=list)
    evaluative_inputs: List[EvaluativeInput] = field(default_factory=list)
    flags: List[Flag] = field(default_factory=list)
    # sha256 over the CANONICAL form of the loaded YAML (architecture §4.1 data
    # contract, additive v1.1 log key): stamps every log record so audits can be
    # partitioned by policy version. None only for configs built in code (tests).
    fingerprint: Optional[str] = None

    @property
    def factor_keys(self) -> List[str]:
        return [f.key for f in self.factors]

    def factor(self, key: str) -> Factor:
        for f in self.factors:
            if f.key == key:
                return f
        raise KeyError(f"unknown factor {key!r} in mode {self.mode!r}")

    def with_updated_distributions(
        self, stats: Dict[str, Tuple[float, float]]
    ) -> "ModeConfig":
        """Return a copy whose seed distributions are replaced by log-derived
        (mean, std) stats — in transform space — for the factors present in
        ``stats``. The spec ships seed distributions in config *until the log
        grows*; this is the growth path."""
        new_factors = []
        for f in self.factors:
            if f.key in stats:
                m, s = stats[f.key]
                if s > 1e-9:
                    f = Factor(
                        key=f.key, name=f.name, scale=f.scale,
                        prior_weight=f.prior_weight, sign=f.sign, tag=f.tag,
                        rationale=f.rationale, seed_mean=float(m),
                        seed_std=float(s), transform=f.transform,
                        plausible_range=f.plausible_range,
                    )
            new_factors.append(f)
        return ModeConfig(
            mode=self.mode, label=self.label, banner=self.banner,
            factors=new_factors, evaluative_inputs=self.evaluative_inputs,
            flags=self.flags,
            # The fingerprint identifies the POLICY (the YAML file), which a
            # log-derived distribution update does not change — records keep
            # partitioning by the stated policy version.
            fingerprint=self.fingerprint,
        )


def config_fingerprint(data: dict) -> str:
    """sha256 hex digest of the canonical form of a parsed config mapping.

    Canonicalization is JSON with sorted keys, so reformatting the YAML —
    whitespace, comments, key order, quoting style — never changes the
    fingerprint, while any semantic edit (a weight, a seed distribution, the
    banner) always does. This is the value stamped into every log record as
    ``config_fingerprint`` (architecture data contract; additive v1.1 key —
    readers ignore unknown keys, so old logs and old readers both survive).
    """
    canonical = json.dumps(data, sort_keys=True, ensure_ascii=False,
                           separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _parse_factor(d: dict) -> Factor:
    rng = d.get("plausible_range", [0, 4])
    sign = int(d["sign"])
    if sign not in (-1, 1):
        raise ValueError(f"factor {d.get('key')!r}: sign must be +1 or -1")
    tag = str(d["tag"])
    if tag not in ("lever", "fact"):
        raise ValueError(f"factor {d.get('key')!r}: tag must be lever|fact")
    transform = str(d.get("transform", "identity"))
    if transform not in _FORWARD:
        raise ValueError(f"factor {d.get('key')!r}: unknown transform {transform!r}")
    if float(d["seed_std"]) <= 0:
        raise ValueError(f"factor {d.get('key')!r}: seed_std must be > 0")
    return Factor(
        key=str(d["key"]),
        name=str(d["name"]),
        scale=str(d["scale"]),
        prior_weight=float(d["prior_weight"]),
        sign=sign,
        tag=tag,
        rationale=str(d["rationale"]),
        seed_mean=float(d["seed_mean"]),
        seed_std=float(d["seed_std"]),
        transform=transform,
        plausible_range=(float(rng[0]), float(rng[1])),
    )


def load_mode_config(path: str | Path) -> ModeConfig:
    """Load and validate one mode's YAML schema."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    mode = str(data["mode"])
    banner = data.get("banner") or None
    if mode == "zero_to_one" and not banner:
        # Honesty rule: 0→1 must never ship without its
        # structure-not-prediction banner (Spine success metric 4).
        raise ValueError("zero_to_one config must define a non-empty 'banner'")

    factors = [_parse_factor(f) for f in data.get("factors", [])]
    if not factors:
        raise ValueError(f"{path}: no factors defined")
    keys = [f.key for f in factors]
    if len(keys) != len(set(keys)):
        raise ValueError(f"{path}: duplicate factor keys")

    evaluative = [
        EvaluativeInput(
            key=str(e["key"]), name=str(e["name"]),
            scale=str(e.get("scale", "0–4")), note=str(e.get("note", "not scored")),
        )
        for e in (data.get("evaluative_inputs") or [])
    ]
    flags = [
        Flag(key=str(g["key"]), name=str(g["name"]),
             description=str(g.get("description", "")))
        for g in (data.get("flags") or [])
    ]
    return ModeConfig(
        mode=mode, label=str(data["label"]), banner=banner,
        factors=factors, evaluative_inputs=evaluative, flags=flags,
        fingerprint=config_fingerprint(data),
    )


def default_config_dir() -> Path:
    """The repo-root ``configs/`` directory that ships with the package."""
    return Path(__file__).resolve().parent.parent / "configs"


def load_default_configs(config_dir: str | Path | None = None) -> Dict[str, ModeConfig]:
    """Load both shipped mode schemas, keyed by mode ("one_to_n", "zero_to_one")."""
    d = Path(config_dir) if config_dir else default_config_dir()
    out: Dict[str, ModeConfig] = {}
    for fname in ("one_to_n.yaml", "zero_to_one.yaml"):
        cfg = load_mode_config(d / fname)
        out[cfg.mode] = cfg
    return out
