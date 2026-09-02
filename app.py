"""PairwisePM — Gradio UI (one screen, one sitting).

The whole comparison happens on ONE screen in ONE sitting because the pairwise
delta only cancels the occasion noise that both scores share (spec §1). Gradio
is imported here and only here; the package underneath is numpy-only.

This file holds ZERO math (architecture invariant): every displayed number
comes from ``pairwisepm`` engine calls, and every user-visible string is keyed
off the design leaf's constants module (``pairwisepm/strings.py``, vendored
byte-identical from ``leaves/design/strings.py``).

Honesty rules implemented in this file:
- Permanent structure-not-prediction banner whenever 0→1 mode is selected.
- No naked probabilities: every probability renders through the atomic MP-1
  token ``prob_token(p, lo, hi)`` — there is no p-only path.
- No imputation: the verdict computes only when EVERY mechanical factor is
  scored for both ideas; skipped factors are never defaulted to "average".
- Verdict clears the moment any input changes (no stale numbers on screen).
- "Too close to call" is never overridden into a winner by the UI, and picking
  against a verdict (or picking on a too-close) requires a logged rationale
  before append (Decisions C8).
- The decision log lives with the user: download/upload JSONL (uploads MERGE
  by timestamp with duplicate dedupe), nothing is stored server-side.
"""

from __future__ import annotations

import html as _html
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import gradio as gr

from pairwisepm import (
    M1_ACTIVATION_N,
    RELIABILITY_CURVE_MIN_N,
    ComparisonResult,
    DecisionLog,
    M1Fit,
    ModeConfig,
    compare,
    fit_m1,
    load_default_configs,
    make_record,
)
from pairwisepm.strings import (
    MODE_PROMISE_01,
    MODE_PROMISE_1N,
    STRINGS as S,
    prob_token,
)

def _S_n(base_id: str, n: int) -> str:
    """Count-template selection (design states.md §6.8 R-10(i) binding rule):
    a count template's singular is a DISTINCT catalogue ID with suffix
    ``_one``, selected when the interpolated count is exactly 1 — never a
    runtime "(s)" hack, never string surgery on the plural. The singular
    templates hard-code the "1" and drop that slot; call sites still pass the
    full kwarg set and str.format ignores the unused ones, so one call site
    serves both variants."""
    return S[base_id + "_one"] if n == 1 else S[base_id]


CONFIGS = load_default_configs()
N2N = CONFIGS["one_to_n"]
Z2O = CONFIGS["zero_to_one"]
MODE_BY_LABEL = {c.label: c for c in CONFIGS.values()}

# The banner text is the config's (== str.banner.01, asserted at import below).
assert Z2O.banner == S["str.banner.01"], "0→1 banner drifted from design copy"

# The primary control's label is a bare literal (the catalogue owns sentences,
# not widget nouns) — but str.verdict.stale NAMES it: "…Press Compare to
# recompute." Renaming the button without the string would leave the one copy
# line minted to state what the app actually does instructing the user to press
# a control that no longer exists, with every test green. Same shape as the
# banner assert above: bind the noun once, assert the cross-reference at import.
_COMPARE_LABEL = "Compare"
assert S["str.verdict.stale"].endswith(
    f"Press {_COMPARE_LABEL} to recompute."
), (
    "str.verdict.stale names the primary control by literal; it and "
    "_COMPARE_LABEL have drifted. Change both in one push, or neither."
)
BANNER_HTML = (
    "<div style='background:#0b7285;color:#f0fdfa;padding:10px 14px;"
    "border-radius:8px;font-size:0.95em'>"
    f"{_html.escape(Z2O.banner or '')}</div>"
)

# ---------------------------------------------------------------------------
# Canonical seeded example — leaves/gtm/seed-comparison.json (GTM leaf).
# Every demo artifact tells the SAME story: Reply Drafts vs Instant Summaries.
# ---------------------------------------------------------------------------

_SEED_KEY_MAP = {  # GTM json key -> config factor key (Decisions C3: risk is
    "impact": "impact_primary_metric",  # entered already reversed, 4 = lowest)
    "feasibility": "capability_feasibility",
    "reach": "reach",
    "unit_economics": "unit_economics",
    "data_flywheel": "data_flywheel",
    "risk_scored_reversed": "risk_surface",
    "effort": "effort",
}

_SEED_FALLBACK = {  # inlined copy of the canonical values (file may be absent
    "ideas": {  # in a stripped deployment); keep in sync with the json.
        "A": {"name": "Reply Drafts",
              "one_liner": "Agent-assist generative reply drafts in the ticket composer."},
        "B": {"name": "Instant Summaries",
              "one_liner": "LLM thread summary rendered when an agent opens a ticket."},
    },
    "raw_inputs": {
        "A": {"impact": 1.0, "feasibility": 2.9, "reach": 8400,
              "unit_economics": 2.7, "data_flywheel": 2.3,
              "risk_scored_reversed": 1.0, "effort": 9},
        "B": {"impact": 0.5, "feasibility": 2.5, "reach": 8800,
              "unit_economics": 2.0, "data_flywheel": 1.5,
              "risk_scored_reversed": 1.5, "effort": 9},
    },
    "evaluative_inputs_excluded_from_score": {
        "A": {"strategic_fit": "core to our assist strategy"},
        "B": {"strategic_fit": "adjacent - nice to have"},
    },
}


def _load_seed_example() -> dict:
    path = Path(__file__).resolve().parent / "leaves" / "gtm" / "seed-comparison.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _SEED_FALLBACK


SEED = _load_seed_example()


def _seed_raw(side: str) -> Dict[str, float]:
    d = SEED["raw_inputs"][side]
    return {_SEED_KEY_MAP[k]: float(v) for k, v in d.items() if k in _SEED_KEY_MAP}


# ---------------------------------------------------------------------------
# Rendering helpers — pure functions of engine outputs (restylable freely)
# ---------------------------------------------------------------------------

def _fmt_raw(x: float) -> str:
    return f"{x:,.0f}" if abs(x) >= 1000 else f"{x:g}"


def _winner_token(sc) -> Tuple[str, str]:
    """(winner_side, MP-1 token for the winner's probability). The interval is
    reflected with the point estimate so token and estimate always agree."""
    if sc.verdict == "A":
        return "A", prob_token(sc.p, sc.interval[0], sc.interval[1])
    return "B", prob_token(1 - sc.p, 1 - sc.interval[1], 1 - sc.interval[0])


def render_placeholder(missing: Optional[List[str]] = None) -> str:
    """The dashed empty/partial verdict card (S1/S2): no fake verdict, no
    preview probability, and no silent defaulting of skipped factors."""
    if missing:
        body = _S_n("str.partial.verdict_placeholder", len(missing)).format(
            n_missing=len(missing), missing_list=", ".join(missing))
        note = S["str.partial.no_default"]
    else:
        body = S["str.empty.verdict_placeholder"]
        note = S["str.empty.sub"]
    return (
        "<div style='border:2px dashed #a8a29e;border-radius:8px;"
        "padding:14px 16px;background:#fafaf9;color:#57534e'>"
        f"<div style='color:#57534e'>{_html.escape(body)}</div>"
        f"<div style='margin-top:6px;font-size:0.85em;color:#57534e'>"
        f"{_html.escape(note)}</div>"
        "</div>"
    )


def render_stale() -> str:
    return (
        "<div style='border:2px dashed #a8a29e;border-radius:8px;"
        "padding:10px 14px;background:#fafaf9;color:#57534e'>"
        f"{_html.escape(S['str.verdict.stale'])}</div>"
    )


def render_verdict(res: ComparisonResult, name_a: str, name_b: str,
                   eval_notes: str = "",
                   ceiling: Tuple[bool, bool] = (False, False)) -> str:
    sc = res.active
    ea = _html.escape(name_a or "Idea A")
    eb = _html.escape(name_b or "Idea B")
    is_01 = res.mode == "zero_to_one"
    lines: List[str] = []

    # R-9b (design §6.7): gradio 6's `.prose * { color: var(--body-text-color) }`
    # rule beats CSS inheritance, so the wrapper's forced color never reaches
    # nested elements — every text-bearing element INSIDE a forced-light block
    # must carry its own inline color (inline always beats the stylesheet rule).
    if sc.verdict == "too_close":
        color = "#57534e"  # neutral stone: a withheld verdict is a calm state
        lines.append(f"<div style='font-size:1.25em;color:#1c1917'>"
                     f"<b style='color:#1c1917'>"
                     f"{_html.escape(S['str.tctc.headline'])}</b></div>")
        body = S["str.tctc.body"].format(
            prob_token=prob_token(sc.p, sc.interval[0], sc.interval[1]))
        lines.append(f"<div style='color:#1c1917'>{_html.escape(body)}</div>")
        lines.append(f"<div style='color:#57534e;margin-top:4px'>"
                     f"{_html.escape(S['str.tctc.next'])}</div>")
        lines.append(f"<div style='color:#57534e;font-size:0.85em;margin-top:4px'>"
                     f"{_html.escape(S['str.tctc.force_note'])}</div>")
    else:
        color = "#0b7285" if sc.verdict == "A" else "#b0561c"
        wname = ea if sc.verdict == "A" else eb
        lname = eb if sc.verdict == "A" else ea
        _, token = _winner_token(sc)
        head = S["str.verdict.headline"].format(
            winner_name=wname, prob_token=token)
        lines.append(f"<div style='font-size:1.25em;color:#1c1917'>"
                     f"<b style='color:#1c1917'>{head}</b></div>")
        lines.append(f"<div style='color:#57534e'>"
                     f"{_html.escape(S['str.verdict.prob_gloss'])}</div>")
        lines.append(
            f"<div style='margin-top:4px'><span style='border:1px solid #a8a29e;"
            f"border-radius:10px;padding:1px 8px;font-size:0.85em;"
            f"color:#1c1917'>"
            f"{lname}: {_html.escape(S['str.mp2.chip'])}</span></div>")

    model_line = (S["str.verdict.model_line_m1"] if sc.model == "M1"
                  else S["str.verdict.model_line_m0"])
    mode_line = (S["str.verdict.mode_line_01"] if is_01
                 else S["str.verdict.mode_line_1n"])
    eq = res.m0_equal
    lines.append(f"<div style='color:#57534e;margin-top:6px'>"
                 f"{_html.escape(model_line)}</div>")
    lines.append(f"<div style='color:#57534e'>{_html.escape(mode_line)}</div>")
    lines.append(
        f"<div style='color:#57534e;font-size:0.85em'>Equal-weight control: "
        f"P(A) = {prob_token(eq.p, eq.interval[0], eq.interval[1])}. "
        f"{_html.escape(S['str.verdict.ablation_toggle'])}</div>")

    # S5 routing strip (amber = honesty state, §6.4 R-3): the full design
    # explanation ("averages are exactly what destroy outliers") renders
    # alongside the engine's pinned note — the note asserts the exclusion
    # (T-CEIL-02), the strip makes it legible.
    flag_a, flag_b = ceiling
    if flag_a and flag_b:
        strip = S["str.ceiling.both"]
    elif flag_a or flag_b:
        strip = S["str.ceiling.strip"].format(
            idea_name=(name_a or "Idea A") if flag_a else (name_b or "Idea B"))
    else:
        strip = ""
    if strip:
        lines.append(
            "<div style='margin-top:8px;background:#fef3c7;color:#1c1917;"
            f"padding:8px 10px;border-radius:6px'>{_html.escape(strip)}</div>")
    for note in res.ceiling_notes:  # engine's pinned note (T-CEIL-02)
        lines.append(
            "<div style='margin-top:8px;background:#fef3c7;color:#1c1917;"
            f"padding:8px 10px;border-radius:6px'>{_html.escape(note)} "
            f"{_html.escape(S['str.ceiling.mech_label'])}</div>")
    if res.fragility.fragile:
        frag = S["str.verdict.fragility"].format(factor=res.fragility.factor_name)
        lines.append(
            "<div style='margin-top:8px;background:#fef3c7;color:#1c1917;"
            f"padding:8px 10px;border-radius:6px'>{_html.escape(frag)}</div>")
    if eval_notes:
        lines.append(  # S13a card echo: bordered annex, outside the math
            "<div style='margin-top:8px;border:1px solid #d6d3d1;"
            "border-radius:6px;padding:8px 10px;color:#57534e;font-size:0.9em'>"
            f"{_html.escape(S['str.eval.card_echo'].format(notes=eval_notes))}"
            "</div>")

    # The card forces a light background, so it must force its text color too:
    # in Gradio's dark theme the inherited body color is near-white, which
    # renders the MP-1 headline invisible on #fafaf9 (design §6.4 R-9). The
    # wrapper's color alone is NOT enough (R-9b): `.prose *` re-colors every
    # nested element, so each text-bearing child above carries inline color.
    return (f"<div style='border-left:6px solid {color};"
            "background:#fafaf9;color:#1c1917;"
            "padding:12px 16px;border-radius:8px'>" + "\n".join(lines) + "</div>")


def render_leverage(res: ComparisonResult, cfg: ModeConfig,
                    name_a: str, name_b: str,
                    m1: Optional[M1Fit] = None) -> str:
    ea = _html.escape(name_a or "Idea A")
    eb = _html.escape(name_b or "Idea B")
    # Provenance chip (R6): the panel must name which regime produced it
    # (Decisions C6: hard switch at activation, label mandatory).
    if res.active_model == "M1" and m1 is not None:
        prov = S["str.leverage.provenance_m1"].format(n_picks=m1.n_train)
    else:
        prov = S["str.leverage.provenance_m0"]
    maxc = max((abs(r.contribution) for r in res.leverage), default=1.0) or 1.0
    rows = []
    for r in res.leverage:
        w = int(100 * abs(r.contribution) / maxc)
        col = "#0b7285" if r.contribution > 0 else "#b0561c"
        side = ea if r.contribution > 0 else (eb if r.contribution < 0 else "—")
        chip = (S["str.mp3.lever_chip"] if r.tag == "lever"
                else S["str.mp3.fact_chip"])
        rows.append(
            f"<tr><td>{_html.escape(r.name)}</td>"
            f"<td style='text-align:center'><code>{chip}</code></td>"
            f"<td style='text-align:right'>{r.weight:+.2f}</td>"
            f"<td style='text-align:right'>{r.delta:+.2f}</td>"
            f"<td style='text-align:right'>{r.contribution:+.3f}</td>"
            f"<td><div style='height:10px;width:{w}%;background:{col};"
            f"border-radius:3px'></div></td><td>{side}</td></tr>")
    out = [
        "<h3>Leverage panel</h3>",
        f"<div style='font-size:0.85em;color:#57534e'>"
        f"<span style='border:1px solid #a8a29e;border-radius:10px;"
        f"padding:1px 8px'>{_html.escape(prov)}</span></div>",
        "<table style='width:100%;border-collapse:collapse;font-size:0.9em'>",
        "<tr><th style='text-align:left'>Factor</th><th>Tag</th>"
        "<th>Weight</th><th>Δz (A−B)</th><th>Contribution</th>"
        "<th style='width:25%'>|pull|</th><th>Favors</th></tr>",
        *rows, "</table>",
    ]
    if res.parity_paths:
        loser_name = eb if res.parity_paths[0].loser == "B" else ea
        if res.active.verdict == "too_close":
            # S4: on a too-close, the same lever math is "cheapest evidence".
            out.append(f"<h4>Cheapest evidence — levers for {loser_name}</h4>")
        else:
            out.append(f"<h4>Path to parity — for {loser_name}</h4>")
        if res.loses_on_fundamentals and res.active.verdict != "too_close":
            facts = ", ".join(f.name for f in cfg.factors if f.tag == "fact")
            out.append(
                "<div style='background:#fef3c7;color:#1c1917;"
                "padding:8px 10px;border-radius:6px'>"
                + _html.escape(S["str.mp2.fundamentals"].format(
                    loser_name=loser_name, fact_list=facts))
                + "</div>")
        else:
            items = []
            for p in res.parity_paths:
                if p.feasible:
                    s6040 = (
                        f"; for 60/40 in its favor: reach {_fmt_raw(p.raw_target_6040)}"
                        if p.feasible_6040 else
                        "; the 60/40 target falls outside the plausible range")
                    items.append(
                        f"<li><b>{_html.escape(p.name)}</b> "
                        f"(<code>{S['str.mp3.lever_chip']}</code>): move from "
                        f"{_fmt_raw(p.current_raw)} to <b>{_fmt_raw(p.raw_target)}</b> "
                        f"(raw units) to reach 50/50{s6040}.</li>")
                else:
                    items.append(  # off-scale target: shown and flagged, never clamped
                        f"<li>{_html.escape(p.name)}: 50/50 would need "
                        f"{_fmt_raw(p.raw_target)} — {_html.escape(p.note)}.</li>")
            out.append("<ul>" + "".join(items) + "</ul>")
            out.append(f"<div style='color:#57534e;font-size:0.85em'>"
                       f"{_html.escape(S['str.mp3.fact_tip'])} "
                       f"{_html.escape(S['str.mp3.lever_tip'])}</div>")
    return "\n".join(out)


def render_ladder(res: ComparisonResult, cfg: ModeConfig,
                  m1: Optional[M1Fit]) -> str:
    """S6: M0-vs-M1, revealed vs stated. Rendered only once M1 is active."""
    if not (m1 and m1.active and res.m1):
        return ""
    rows = []
    for f in cfg.factors:
        w0, w1 = f.effective_weight, m1.weights[f.key]
        rows.append(
            f"<tr><td>{_html.escape(f.name)}</td>"
            f"<td style='text-align:right'>{w0:+.2f}</td>"
            f"<td style='text-align:right'>{w1:+.2f}</td>"
            f"<td style='text-align:right'>{w1 - w0:+.2f}</td></tr>")
    parts = [f"<h3>{_html.escape(S['str.disagree.headline'])}</h3>"
             if res.m0.verdict != res.m1.verdict else
             "<h3>Stated vs revealed policy</h3>"]
    wa, ta = _winner_token(res.m0) if res.m0.verdict != "too_close" else ("—", prob_token(res.m0.p, *res.m0.interval))
    wb, tb = _winner_token(res.m1) if res.m1.verdict != "too_close" else ("—", prob_token(res.m1.p, *res.m1.interval))
    parts.append("<div>" + _html.escape(S["str.disagree.row_m0"].format(
        winner_name=f"Idea {wa}", prob_token=ta)) + "</div>")
    parts.append("<div>" + _html.escape(S["str.disagree.row_m1"].format(
        n_picks=m1.n_train, winner_name=f"Idea {wb}", prob_token=tb)) + "</div>")
    if res.m0.verdict != res.m1.verdict:
        parts.append(f"<div style='color:#57534e'>"
                     f"{_html.escape(S['str.disagree.body'])}</div>")
    parts += [
        "<table style='border-collapse:collapse;font-size:0.9em'>",
        "<tr><th style='text-align:left'>Factor</th><th>You say (prior)</th>"
        "<th>You reveal (fitted)</th><th>Drift</th></tr>",
        *rows, "</table>",
        f"<div style='color:#57534e;font-size:0.85em'>"
        f"{_html.escape(S['str.disagree.weights_caption'])} "
        f"{_html.escape(S['str.disagree.log_note'])}</div>",
    ]
    return "\n".join(parts)


def render_audit(log: DecisionLog, n_session: int = 0) -> str:
    """``n_session`` is the count of records APPENDED THIS SESSION only —
    never the total log size (design S10b, binding). Uploaded records already
    live in the user's own file; counting them in the custody nudge would
    falsely claim they are tab-only. When 0, the nudge does not render."""
    parts = ["<h3>Audit</h3><table style='border-collapse:collapse'>"]

    def row(k: str, v: str) -> str:
        return (f"<tr><td style='padding-right:14px;color:#57534e'>{k}</td>"
                f"<td><b>{v}</b></td></tr>")

    parts.append(row("Decisions logged", f"{log.n()} "
                     f"(1→N: {log.n('one_to_n')}, 0→1: {log.n('zero_to_one')})"))
    # THE NEXT FOUR STATISTICS ARE POOLED ACROSS MODES — ζ, Brier-vs-picks,
    # Brier-vs-outcomes and override rate are computed over the WHOLE log,
    # while every row rendered below the `for cfg in (N2N, Z2O)` loop is
    # per-mode. Compliance row F-35 owns it; owner of the fix is this seat.
    # THE FIX is to pass the mode through — each of these four takes an
    # optional `mode` (pairwisepm/log.py:180/243/259/276) — and render them
    # inside the per-mode loop.
    #
    # tests/test_audit_honesty.py's T-NEG-09b STAYS GREEN when you do. It is
    # a CENSUS of the unscoped `log.*` calls in this function, not a freeze:
    # passing a mode moves a call out of the censused population, so the fix
    # shrinks what the clause has to classify and never reds on the repair.
    # One caveat, read off that clause rather than taken on report: the
    # pooled call must be REPLACED, not joined by a scoped one. A statistic
    # rendered both pooled and per-mode in one table reds T-NEG-09b's
    # `ambiguous` assertion, and `n` above is the only sanctioned both-ways
    # row because it prints the split beside the total.
    #
    # DEFERRED DELIBERATELY, and this comment is not a step: not before the
    # M-UX-02a sitting, and not in the D1/D2 resolution round, which is
    # YAML-only with no code motion. Adding a FIFTH pooled statistic here
    # before the fix lands reds T-NEG-09b in the change that adds it.
    z = log.kendall_zeta()
    parts.append(row("ζ (consistency)",
                     f"{z:.2f}" if z is not None else "accumulating — needs 3 ideas"))
    b = log.brier()
    parts.append(row("Brier (model vs. your picks)",
                     f"{b:.3f}" if b is not None else "n/a — no decisions yet"))
    ob = log.outcome_brier()
    if ob is not None:
        parts.append(row("Brier (vs. labeled outcomes)", f"{ob:.3f}"))
    orate = log.override_rate()
    if orate is not None:
        parts.append(row("Override rate", f"{orate:.0%}"))

    for cfg in (N2N, Z2O):
        rows_, picks_ = log.training_data(cfg)
        n_mode = len(picks_)
        if n_mode >= M1_ACTIVATION_N:
            fit = fit_m1(rows_, picks_, cfg)
            chip = S["str.m1.active_chip"].format(n=fit.n_train)
            bias = (S["str.orderbias.headline"] + " " +
                    S["str.orderbias.body"].format(n=n_mode, intercept=fit.free_intercept)
                    if fit.order_bias_flagged else
                    f"free intercept {fit.free_intercept:+.2f} "
                    f"(z = {fit.order_bias_z:+.1f}) — no measured order bias")
            parts.append(row(f"Model of the judge ({cfg.label})", chip))
            parts.append(row(f"Order-bias diagnostic ({cfg.label})", bias))
        else:
            locked = S["str.audit.m1_locked"].format(
                threshold=M1_ACTIVATION_N, n=n_mode)
            parts.append(row(f"Model of the judge ({cfg.label})", locked))
        if 0 < n_mode < RELIABILITY_CURVE_MIN_N:
            parts.append(row(
                f"Reliability curve ({cfg.label})",
                S["str.audit.curve_locked"].format(
                    threshold=RELIABILITY_CURVE_MIN_N, n=n_mode)))
    parts.append("</table>")
    parts.append(f"<div style='color:#57534e;font-size:0.85em'>"
                 f"{_html.escape(S['str.audit.zeta_gloss'])} "
                 f"{_html.escape(S['str.audit.brier_gloss'])}</div>")
    if log.n("zero_to_one"):
        parts.append(f"<div style='color:#57534e;font-size:0.85em'>"
                     f"{_html.escape(S['str.audit.01_caption'])}</div>")
    if log.n() == 0:
        custody = S["str.log.empty"]
    elif n_session > 0:
        custody = _S_n("str.log.unsaved_nudge", n_session).format(
            n_session=n_session)
    else:
        custody = ""  # loaded from the user's own file; nothing tab-only
    if custody:
        parts.append(f"<div style='color:#57534e;font-size:0.85em;margin-top:6px'>"
                     f"{_html.escape(custody)}</div>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Event handlers (pure of Gradio state; testable with a gradio stub)
# ---------------------------------------------------------------------------

def _coerce_raw(v) -> Tuple[Optional[float], bool]:
    """Parse one factor Textbox payload into ``(value, ok)``.

    ``None``, ``""`` and whitespace mean legitimately unfilled → ``(None,
    True)``; a parseable number → ``(float, True)``; anything else →
    ``(None, False)``. Factor inputs are Textboxes, not gr.Number, because
    gradio 6 renders ``gr.Number(value=None)`` as a literal 0 and submits it
    (design §6.4 R-8) — an untouched field must never reach the handler as a
    value, and an empty Textbox reliably submits the empty string."""
    if v is None:
        return None, True
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v), True
    s = str(v).strip()
    if not s:
        return None, True
    try:
        return float(s), True
    except ValueError:
        return None, False


def _screen_factors(cfg: ModeConfig, raw_a: Dict, raw_b: Dict
                    ) -> Tuple[List[str], Dict[str, float], Dict[str, float]]:
    """Blocking rule (design S2) at the UI boundary: every mechanical factor,
    both ideas, a usable number inside its plausible range — or no verdict.

    Returns ``(entries, parsed_a, parsed_b)``. Non-empty ``entries`` block
    computation and feed ``str.partial.verdict_placeholder``; a factor counts
    as "to go" when unfilled, non-numeric, or outside its plausible range
    (range checks live here, not in gr.Number min/max, so violations surface
    in the S2 missing-list instead of raw Gradio error toasts). Nothing is
    ever defaulted."""
    entries: List[str] = []
    pa: Dict[str, float] = {}
    pb: Dict[str, float] = {}
    for f in cfg.factors:
        lo, hi = f.plausible_range
        problems: Dict[str, str] = {}
        for label, raw, parsed in (("Idea A", raw_a, pa), ("Idea B", raw_b, pb)):
            val, ok = _coerce_raw(raw.get(f.key))
            if not ok:
                problems[label] = "not a number"
            elif val is None:
                problems[label] = "unfilled"
            elif not f.in_plausible_range(val):
                problems[label] = f"outside {lo:g}–{hi:g}"
            else:
                parsed[f.key] = val
        if list(problems.values()) == ["unfilled", "unfilled"]:
            entries.append(f"{f.name} (both ideas)")
        else:
            for label in ("Idea A", "Idea B"):
                note = problems.get(label)
                if note == "unfilled":
                    entries.append(f"{f.name} ({label})")
                elif note:
                    entries.append(f"{f.name} ({label} — {note})")
    return entries, pa, pb


def _split_inputs(vals: List) -> Dict:
    """Slice the flat component list back into per-mode raw dicts. Values are
    Textbox strings and may be empty (unfilled) — the blocking rule handles
    those, never a default."""
    kn, kz = N2N.factor_keys, Z2O.factor_keys
    i = 0
    n2n_a = dict(zip(kn, vals[i:i + len(kn)])); i += len(kn)
    n2n_b = dict(zip(kn, vals[i:i + len(kn)])); i += len(kn)
    z2o_a = dict(zip(kz, vals[i:i + len(kz)])); i += len(kz)
    z2o_b = dict(zip(kz, vals[i:i + len(kz)])); i += len(kz)
    ceil_a, ceil_b = bool(vals[i]), bool(vals[i + 1]); i += 2
    ev = vals[i:i + 4]
    evaluative = {
        "a": {k: v for k, v in
              (("strategic_fit", ev[0]), ("brand_fit", ev[1])) if v},
        "b": {k: v for k, v in
              (("strategic_fit", ev[2]), ("brand_fit", ev[3])) if v},
    }
    return {"one_to_n": (n2n_a, n2n_b), "zero_to_one": (z2o_a, z2o_b),
            "ceiling": (ceil_a, ceil_b), "evaluative": evaluative}


def _eval_notes_text(evaluative: Dict) -> str:
    bits = []
    for side, label in (("a", "A"), ("b", "B")):
        for k, v in evaluative.get(side, {}).items():
            pretty = k.replace("_", " ").capitalize()
            bits.append(f"{label} · {pretty} — \"{v}\"")
    return " · ".join(bits)


def do_compare(mode_label: str, name_a: str, name_b: str, log: DecisionLog,
               *vals):
    cfg = MODE_BY_LABEL[mode_label]
    parts = _split_inputs(list(vals))
    raw_a, raw_b = parts[cfg.mode]

    blocking, raw_a, raw_b = _screen_factors(cfg, raw_a, raw_b)
    if blocking:
        return render_placeholder(blocking), "", "", None

    ceil_a, ceil_b = (parts["ceiling"] if cfg.mode == "zero_to_one"
                      else (False, False))

    m1: Optional[M1Fit] = None
    rows, picks = log.training_data(cfg)
    if len(picks) >= M1_ACTIVATION_N:  # gate on LOG LENGTH, not code presence
        m1 = fit_m1(rows, picks, cfg)

    res = compare(cfg, raw_a, raw_b, m1_fit=m1,
                  ceiling_a=ceil_a, ceiling_b=ceil_b)
    ctx = {"mode": cfg.mode, "name_a": name_a, "name_b": name_b,
           "raw_a": raw_a, "raw_b": raw_b, "result": res,
           "evaluative": parts["evaluative"],
           "flags": {"a": {"ceiling": ceil_a}, "b": {"ceiling": ceil_b}}
           if cfg.mode == "zero_to_one" else {"a": {}, "b": {}}}
    notes = _eval_notes_text(parts["evaluative"])
    return (render_verdict(res, name_a, name_b, notes,
                           ceiling=(ceil_a, ceil_b)),
            render_leverage(res, cfg, name_a, name_b, m1),
            render_ladder(res, cfg, m1),
            ctx)


def do_log(pick_label: str, rationale: str, ctx: Optional[dict],
           log: DecisionLog, n_session: int):
    """``n_session`` counts records appended this session (design S10b); it is
    Gradio state threaded through so the custody nudge never counts uploads."""
    if not ctx:
        return S["str.log.pick_first"], render_audit(log, n_session), log, \
            n_session
    if not pick_label:
        return S["str.log.pick_missing"], render_audit(log, n_session), log, \
            n_session
    pick = "A" if pick_label.startswith("Idea A") else "B"
    res: ComparisonResult = ctx["result"]
    verdict = res.active.verdict
    overrode = verdict == "too_close" or pick != verdict
    rationale = (rationale or "").strip()
    if overrode and not rationale:
        # Decisions C8 / design S13b: the override is honored, never fought —
        # but exactly one logged one-sentence rationale is required first.
        if verdict == "too_close":
            prompt = S["str.tctc.force_note"] + " Add a one-sentence rationale."
        else:
            wname = (ctx["name_a"] or "Idea A") if verdict == "A" else (ctx["name_b"] or "Idea B")
            pname = (ctx["name_a"] or "Idea A") if pick == "A" else (ctx["name_b"] or "Idea B")
            _, token = _winner_token(res.active)
            prompt = S["str.override.rationale_prompt"].format(
                pick_name=pname, verdict_name=wname, prob_token=token)
        return prompt, render_audit(log, n_session), log, n_session
    record = make_record(
        timestamp=datetime.now(timezone.utc).isoformat(),  # caller supplies time
        mode=ctx["mode"],
        name_a=ctx["name_a"] or "Idea A",
        name_b=ctx["name_b"] or "Idea B",
        raw_a=ctx["raw_a"], raw_b=ctx["raw_b"], result=res, pick=pick,
        evaluative_a=ctx["evaluative"]["a"], evaluative_b=ctx["evaluative"]["b"],
        flags_a=ctx["flags"]["a"], flags_b=ctx["flags"]["b"],
        override_rationale=rationale if overrode else None,
        config_fingerprint=CONFIGS[ctx["mode"]].fingerprint,
    )
    log.append(record)
    n_session += 1
    pick_name = ((ctx["name_a"] or "Idea A") if pick == "A"
                 else (ctx["name_b"] or "Idea B"))
    msg = S["str.log.appended"].format(n=log.n(), pick_name=pick_name)
    if overrode:
        msg += " " + S["str.override.logged"]
    cfg = CONFIGS[ctx["mode"]]
    n_mode = log.n(cfg.mode)
    if n_mode == M1_ACTIVATION_N:
        msg += " " + S["str.m1.activated"]
    elif n_mode < M1_ACTIVATION_N:
        msg += " " + _S_n("str.m1.progress", n_mode).format(
            threshold=M1_ACTIVATION_N, n=n_mode)
    return msg, render_audit(log, n_session), log, n_session


def do_export(log: DecisionLog):
    if log.n() == 0:
        return gr.update(visible=False), S["str.log.export_empty"]
    path = Path(tempfile.mkdtemp()) / "pairwisepm-decision-log.jsonl"
    path.write_text(log.to_jsonl() + "\n", encoding="utf-8")
    return gr.update(value=str(path), visible=True), \
        f"Exported {log.n()} decisions. " + S["str.empty.privacy"]


def do_upload(file, log: DecisionLog, n_session: int):
    """Upload MERGES with the in-session log (design S10c): ordered by
    timestamp, duplicates (same timestamp and inputs) kept once. A bad file
    changes nothing. ``n_session`` (records appended this session) passes
    through unchanged — uploads are never counted as tab-only (S10b)."""
    if file is None:
        return log, render_audit(log, n_session), S["str.log.upload_none"]
    try:
        text = Path(file.name if hasattr(file, "name") else file).read_text(
            encoding="utf-8")
        uploaded = DecisionLog.from_jsonl(text)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        return log, render_audit(log, n_session), \
            S["str.log.uploaded_bad"].format(problem=e)
    n_before = log.n()
    merged = log.merged(uploaded)
    if n_before:
        msg = S["str.log.uploaded_merge"].format(
            n_uploaded=uploaded.n(), n_session=n_before, n_total=merged.n())
    else:
        msg = _S_n("str.log.uploaded_ok", merged.n()).format(n=merged.n())
    n_1n, n_01 = merged.n("one_to_n"), merged.n("zero_to_one")
    if n_1n and n_01:
        msg += " " + S["str.log.uploaded_mode_note"].format(n_1n=n_1n, n_01=n_01)
    return merged, render_audit(merged, n_session), msg


def do_example():
    """Fill the form with the canonical seeded pair (GTM leaf). 1→N mode;
    0→1 factors stay unfilled (the blocking rule keeps them honest)."""
    vals: List = []
    ra, rb = _seed_raw("A"), _seed_raw("B")
    vals += [f"{ra[k]:g}" for k in N2N.factor_keys]
    vals += [f"{rb[k]:g}" for k in N2N.factor_keys]
    vals += [""] * (2 * len(Z2O.factor_keys))  # unfilled Textboxes are ""
    vals += [False, False]  # ceiling flags
    ev = SEED.get("evaluative_inputs_excluded_from_score", {})
    vals += [ev.get("A", {}).get("strategic_fit", ""),
             ev.get("A", {}).get("brand_fit", ""),
             ev.get("B", {}).get("strategic_fit", ""),
             ev.get("B", {}).get("brand_fit", "")]
    return [N2N.label,
            SEED["ideas"]["A"]["name"], SEED["ideas"]["B"]["name"], *vals]


def do_swap(name_a: str, name_b: str, *vals):
    """⇄ Swap A/B (design S7 hygiene control): swaps names, every factor
    value in both mode blocks, ceiling flags, and evaluative notes. The
    engine's zero-intercept symmetry guarantees the recomputed probability is
    exactly 1 − p."""
    v = list(vals)
    kn, kz = len(N2N.factor_keys), len(Z2O.factor_keys)
    i = 0
    n2n_a, n2n_b = v[i:i + kn], v[i + kn:i + 2 * kn]; i += 2 * kn
    z2o_a, z2o_b = v[i:i + kz], v[i + kz:i + 2 * kz]; i += 2 * kz
    ceil_a, ceil_b = v[i], v[i + 1]; i += 2
    ev = v[i:i + 4]
    swapped = (n2n_b + n2n_a + z2o_b + z2o_a + [ceil_b, ceil_a]
               + [ev[2], ev[3], ev[0], ev[1]])
    return [name_b, name_a, *swapped]


def do_stale():
    """Any input edit after compute clears the verdict (design S3 exit rule):
    a wrong-but-visible number is a confidence overstatement."""
    return render_stale(), "", "", None


def on_mode_change(mode_label: str):
    is_n2n = MODE_BY_LABEL[mode_label].mode == "one_to_n"
    toast = S["str.mode.switched_toast"].format(
        new_mode=mode_label,
        mode_promise=MODE_PROMISE_1N if is_n2n else MODE_PROMISE_01)
    return (gr.update(visible=is_n2n), gr.update(visible=not is_n2n),
            gr.update(visible=not is_n2n),  # banner
            gr.update(visible=not is_n2n),  # banner_spacer (height, M-UX-03)
            render_placeholder(), "", "", None, toast)


# ---------------------------------------------------------------------------
# UI construction
# ---------------------------------------------------------------------------

def _factor_input(f, side: str):
    tag_chip = (S["str.mp3.lever_chip"] if f.tag == "lever"
                else S["str.mp3.fact_chip"])
    label = f"{f.name} — {f.scale} [{tag_chip}]"
    if f.key == "risk_surface":
        label = f"{f.name} — {S['str.factor.risk_label_suffix']} [{tag_chip}]"
    # No default value, ever: a silent default of "average" would be the tool
    # guessing (design S2). The blocking rule holds the verdict until filled.
    # Textbox, not gr.Number: gradio 6 renders Number(value=None) as a literal
    # 0 and submits it, so every untouched field would arrive as a real score
    # and silently defeat the no-imputation rule (design §6.4 R-8). An empty
    # Textbox submits "", which _coerce_raw maps to unfilled; plausible-range
    # bounds are enforced in _screen_factors so violations render through the
    # S2 missing-list, not as raw Gradio error toasts or red invalid borders.
    return gr.Textbox(value="", label=label,
                      info=f.rationale if side == "a" else None)


# M-UX-03 (design S1, str.banner.01): the 0→1 banner is PERMANENT — it must
# stay on screen while the user scrolls the questionnaire.
# Mechanism history (design states.md §6.9, render session 3): position:sticky
# on this wrapper was APPLIED (browser computed sticky/top:0/z:100) yet
# structurally inert — gradio's own `.gradio-container-6-26-0` computes
# overflow:hidden while the DOCUMENT is the scroller, so sticky's nearest
# scrollport never scrolls and the banner left the viewport. Fallback is
# position:fixed — viewport-anchored regardless of ancestor overflow; §6.9
# verified zero fixed-position breakers (no transform/filter/perspective/
# contain/will-change ancestors between banner and root). left/right:0 avoid
# a fixed box's shrink-to-fit width; z-index keeps it above the cards it
# scrolls over; the inner div's opaque #0b7285 background keeps content
# unreadable-through. Fixed removes the wrapper from flow, so its height is
# reserved by BANNER_SPACER_HTML — an in-flow, invisible, content-exact
# duplicate placed FIRST in the layout (the viewport slot a top:0 fixed box
# actually covers), so the banner never overlaps the header or mode toggle.
# No magic pixel height: the duplicate tracks the real copy through edits
# and text wrapping by construction.
_CSS = "#pwpm-banner { position: fixed; top: 0; left: 0; right: 0; z-index: 100; }"

BANNER_SPACER_HTML = ("<div style='visibility:hidden' aria-hidden='true'>"
                      f"{BANNER_HTML}</div>")


def build_app() -> gr.Blocks:
    # css= on the constructor emits a gradio 6 deprecation warning but IS
    # honored, and it survives ANY launcher — python app.py, the Space runner,
    # the gradio CLI — whereas css passed only in the __main__ launch() would
    # not. Deliberate, and the delivery path is thinner than "honored" implies:
    # on the CONSTRUCTED object `demo.css` is None; _CSS survives only on the
    # private `demo._deprecated_css`, read inside launch()
    # (gradio/blocks.py:2785, `css = css if css is not None else
    # self._deprecated_css`) — re-verified this round on the installed 6.26.0.
    #
    # ENG-CSS-MIGRATION-01 (registered 2026-08-31, owner: engineering).
    # The durable fix is moving `css=` off the constructor and into
    # `launch(css=...)` at both call sites. That is a LAYOUT-RULE change and
    # fires design §6.12's bidirectional retrigger (a scoped render session),
    # so it is deliberately NOT done today, in the hours before the M-UX-02a
    # sitting. It fires on whichever comes FIRST of:
    #   (a) a gradio major bump (installed runtime leaves the 6.x line);
    #   (b) any push that widens or removes the `gradio>=6.0,<7` bound in
    #       requirements.txt or pyproject.toml [app];
    #   (c) the first release after the M-UX-02a sitting.
    # Until then compliance's T-DELIV-01b is the tripwire, not the fix: it
    # reds if the installed gradio ever loses `_deprecated_css`, before an
    # unstyled banner reaches a user. An unstyled #pwpm-banner is not cosmetic
    # — it is the Spine's "0→1 never claims predictive accuracy" disclaimer
    # scrolled out of the viewport, i.e. the accuracy claim un-disclaimed.
    with gr.Blocks(title="PairwisePM — mechanical pairwise judge",
                   css=_CSS) as demo:
        # First in the layout: the fixed banner's height reservation. A top:0
        # fixed box covers the top of the VIEWPORT, so the in-flow spacer must
        # occupy the top of the PAGE — at scroll 0 the banner sits exactly in
        # the strip the spacer vacates, and nothing hides beneath it.
        banner_spacer = gr.HTML(BANNER_SPACER_HTML, visible=False,
                                elem_id="pwpm-banner-spacer")
        gr.Markdown(
            "# PairwisePM\n"
            f"**{S['str.empty.headline']}** {S['str.empty.sub']}\n\n"
            "A mechanical pairwise judge for GenAI product decisions: winner, "
            "probability **with an interval**, and the levers that would flip "
            "it. The runtime is weights and a (zero) bias term — no LLM, no "
            "API key, no network."
        )
        mode = gr.Radio(choices=[N2N.label, Z2O.label], value=N2N.label,
                        label="Mode")  # fresh load = 1→N (Decisions C7)
        banner = gr.HTML(BANNER_HTML, visible=False,  # permanent while in 0→1
                         elem_id="pwpm-banner")  # fixed via _CSS (M-UX-03);
        # flow position is irrelevant to a fixed box — height lives in the
        # spacer above, which toggles with this component in on_mode_change.
        mode_toast = gr.Markdown()

        with gr.Row():
            name_a = gr.Textbox(label="Idea A — name", placeholder="Idea A")
            btn_swap = gr.Button("⇄ Swap A/B", size="sm")
            name_b = gr.Textbox(label="Idea B — name", placeholder="Idea B")

        # -- 1→N factor block ------------------------------------------------
        with gr.Group(visible=True) as grp_n2n:
            gr.Markdown(f"### Factors — {N2N.label}")
            with gr.Row():
                with gr.Column():
                    gr.Markdown("**Idea A**")
                    n2n_a = [_factor_input(f, "a") for f in N2N.factors]
                with gr.Column():
                    gr.Markdown("**Idea B**")
                    n2n_b = [_factor_input(f, "b") for f in N2N.factors]

        # -- 0→1 factor block ------------------------------------------------
        with gr.Group(visible=False) as grp_z2o:
            gr.Markdown(f"### Factors — {Z2O.label}")
            with gr.Row():
                with gr.Column():
                    gr.Markdown("**Idea A**")
                    z2o_a = [_factor_input(f, "a") for f in Z2O.factors]
                    ceil_a = gr.Checkbox(label=S["str.factor.ceiling_label"])
                with gr.Column():
                    gr.Markdown("**Idea B**")
                    z2o_b = [_factor_input(f, "b") for f in Z2O.factors]
                    ceil_b = gr.Checkbox(label=S["str.factor.ceiling_label"])

        # -- Evaluative panel: outside the math, on the record (S13a) --------
        with gr.Group():
            gr.Markdown(f"### {S['str.eval.header']} — "
                        f"*{S['str.partial.eval_optional']}*\n"
                        f"{S['str.eval.sub']}")
            # ENG-COPY-EVALLABELS-01 (registered 2026-08-31, owner engineering,
            # requested by design; DEFERRED ON PURPOSE). The four "(not scored)"
            # labels below are the Spine's excluded-from-score refusal made
            # visible, and they are bare literals under no copy authority. They
            # move into the design catalogue (mint + re-vendor + §6.12 retrigger)
            # at the FIRST RELEASE AFTER the M-UX-02a sitting — not before: a
            # mint and a mirror update in the hours ahead of a timed sitting is
            # the same class of risk as the CSS migration deferred in
            # requirements.txt. Firing conditions: (a) that first post-sitting
            # release, (b) any edit to these four label strings, whichever first.
            # SCOPE, BOUNDED (design answered the round-16 ask by partitioning
            # their §6.15(iii) census): this trigger fires on EXACTLY the four
            # labels below and nothing else. The 15 literals design classes as
            # structural/neutral stay bare by design and are governed, where
            # they need to be, the way _COMPARE_LABEL is — one constant plus an
            # import-time cross-reference assert, zero catalogue growth. A
            # trigger that names a set can be fired; a trigger that names a
            # 20-item census is a standing reason never to fire it.
            # WHAT THE PARAGRAPH ABOVE IS NOT A MAP OF (design, round 19;
            # verified from this seat before being written down). "The four,
            # and the structural sixteen excluded by name" reads like a
            # complete inventory of this file's uncatalogued rendered copy.
            # It is not. Both sets come from design's census, whose predicate
            # walks ``gr.*`` CONSTRUCTION calls with constant arguments — and
            # app.py paints a SECOND surface that predicate contributes zero
            # literals from: six builders (render_placeholder, render_stale,
            # render_verdict, render_leverage, render_ladder, render_audit)
            # return HTML strings that reach the screen through gr.HTML()
            # (:916-918, :940). Those bodies hold bare literals nobody has
            # censused — e.g. "accumulating — needs 3 ideas" and
            # "n/a — no decisions yet" in render_audit, and the parity
            # refusal clause "; the 60/40 target falls outside the plausible
            # range" at :349. That population is design's to enumerate
            # (DESIGN-COPY-HTMLSURFACE-01, their §6.18); it is NOT in this
            # trigger and must never be folded into it. THE SET HERE STAYS
            # EXACTLY FOUR — a trigger grows only by design's dated amendment
            # naming a literal individually, and a bound that absorbs each
            # new finding is not a bound. This clause exists so a reader at
            # speed does not conclude the two sets above are exhaustive of
            # the file and stop looking.
            # HOW THE MOVE IS MADE, when it fires (gtm, round 18): MOVE THEM
            # BYTE-IDENTICAL. The rendered strings stay exactly "A · Strategic
            # fit (not scored)" and its three siblings — no rewording, no
            # retitling, no tidy-up bundled into the mechanical push. If the
            # wording is to change, that is a copy change needing design's
            # mint plus a per-line notification to gtm, in a SEPARATE push.
            # Why the split is not ceremony: T-NEG-08 censuses the marker
            # "(not scored)", not the surrounding label text, so a move that
            # also improved the phrasing would leave the whole suite green
            # while leaves/gtm/tour.html — which makes "excluded from the
            # mechanical arithmetic" a numbered stop and badges it — points at
            # a screen that no longer reads like the script. Nothing about the
            # deferral or its firing conditions changes; this constrains only
            # how the already-planned edit is split.
            with gr.Row():
                with gr.Column():
                    ev_a_strat = gr.Textbox(label="A · Strategic fit (not scored)")
                    ev_a_brand = gr.Textbox(label="A · Brand fit (not scored)")
                with gr.Column():
                    ev_b_strat = gr.Textbox(label="B · Strategic fit (not scored)")
                    ev_b_brand = gr.Textbox(label="B · Brand fit (not scored)")

        with gr.Row():
            btn_example = gr.Button(S["str.empty.example_cta"])
            btn_compare = gr.Button(_COMPARE_LABEL, variant="primary")

        verdict_html = gr.HTML(render_placeholder())
        leverage_html = gr.HTML()
        ladder_html = gr.HTML()  # M0-vs-M1, appears once M1 is active

        # -- Decision + log --------------------------------------------------
        with gr.Group():
            gr.Markdown("### Your decision")
            with gr.Row():
                pick = gr.Radio(choices=["Idea A", "Idea B"],
                                label="Which do you actually pick?")
                rationale = gr.Textbox(
                    label="Rationale (required if you pick against the verdict "
                          "or on a too-close-to-call)",
                    placeholder=S["str.override.rationale_placeholder"])
            btn_log = gr.Button(S["str.verdict.log_cta"])
            log_status = gr.Markdown()

        with gr.Row():
            btn_export = gr.Button(S["str.log.download_cta"])
            upload = gr.File(label=S["str.log.upload_cta"],
                             file_types=[".jsonl", ".json", ".txt"])
        export_file = gr.File(label="Your decision log", visible=False)
        io_status = gr.Markdown()

        audit_html = gr.HTML(render_audit(DecisionLog(), 0))
        gr.Markdown(f"*{S['str.empty.privacy']}*")

        log_state = gr.State(DecisionLog())
        last_ctx = gr.State(None)
        # Records APPENDED this session (design S10b) — uploads excluded, so
        # the custody nudge never claims the user's own file is tab-only.
        session_n = gr.State(0)

        all_factor_inputs = (n2n_a + n2n_b + z2o_a + z2o_b
                             + [ceil_a, ceil_b]
                             + [ev_a_strat, ev_a_brand, ev_b_strat, ev_b_brand])
        verdict_outputs = [verdict_html, leverage_html, ladder_html, last_ctx]

        mode.change(on_mode_change, inputs=[mode],
                    outputs=[grp_n2n, grp_z2o, banner, banner_spacer,
                             *verdict_outputs, mode_toast])
        btn_compare.click(
            do_compare,
            inputs=[mode, name_a, name_b, log_state, *all_factor_inputs],
            outputs=verdict_outputs)
        btn_log.click(do_log,
                      inputs=[pick, rationale, last_ctx, log_state, session_n],
                      outputs=[log_status, audit_html, log_state, session_n])
        btn_export.click(do_export, inputs=[log_state],
                         outputs=[export_file, io_status])
        upload.change(do_upload, inputs=[upload, log_state, session_n],
                      outputs=[log_state, audit_html, io_status])
        btn_example.click(do_example, inputs=[],
                          outputs=[mode, name_a, name_b, *all_factor_inputs])
        btn_swap.click(do_swap, inputs=[name_a, name_b, *all_factor_inputs],
                       outputs=[name_a, name_b, *all_factor_inputs])
        # Stale-verdict rule (S3 exit): any input edit clears the verdict.
        for comp in [name_a, name_b, *all_factor_inputs]:
            comp.change(do_stale, inputs=[], outputs=verdict_outputs)
    return demo


demo = build_app()

if __name__ == "__main__":
    demo.launch()
