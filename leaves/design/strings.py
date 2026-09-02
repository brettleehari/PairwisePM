"""PairwisePM — canonical UI copy constants (DESIGN leaf, single source of truth).

Human-readable authority: leaves/design/states.md (same IDs, with visual/state
context). This module is the assertable mirror compliance tests import
(T-VERDICT / T-PAR / T-CEIL / T-FRAG / T-NEG-04) and engineering vendors as
``pairwisepm/strings.py`` — the design leaf cannot write inside the package, so
the vendored copy must stay byte-identical to this file's constants.

Conventions
-----------
- IDs match states.md exactly (``str.verdict.headline`` -> STRINGS["str.verdict.headline"]).
- Templates are ``str.format``-style; placeholder names document what interpolates.
- Probabilities ALWAYS interpolate as the MP-1 atomic token via ``prob_token()``:
  point estimate and interval in one string, no API accepting p alone.
- No dependencies. Pure data plus two pure helpers.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# The five compliance-pinned constants (tests assert these verbatim; they also
# appear, contiguous, inside the full strings below)
# ---------------------------------------------------------------------------

PINNED_TOO_CLOSE = "too close to call — gather evidence"
PINNED_FUNDAMENTALS = "loses on fundamentals — no working-harder path flips this"
PINNED_CEILING = "high-ceiling outlier — portfolio decision, not averaged in"
PINNED_FRAGILITY_TMPL = "margin rests on the {factor} estimate — re-estimate before committing"
PINNED_BANNER_01 = (
    "0→1 mode structures your search. It does not predict product–market fit."
)


# ---------------------------------------------------------------------------
# MP-1: the atomic probability token — the ONLY way a probability renders
# ---------------------------------------------------------------------------

def _pct(x: float) -> int:
    """Percent with HALF-UP rounding (never banker's): the GTM canonical seed
    comparison (leaves/gtm/seed-comparison.json) pins p(A)=58.5% rendering as
    59%, and Python's round() would give 58."""
    return int(x * 100 + 0.5)


def prob_token(p: float, lo: float, hi: float) -> str:
    """Render ``68% (55–79%)``. There is deliberately no signature taking p alone:
    if the interval is unavailable, render STRINGS['str.mp1.nointerval'] instead
    and withhold the point estimate too."""
    return f"{_pct(p)}% ({_pct(lo)}–{_pct(hi)}%)"


def fragility_line(factor_display_name: str) -> str:
    """The compliance-pinned fragility phrase with the factor name interpolated,
    capitalized as the strip's opening sentence."""
    body = PINNED_FRAGILITY_TMPL.format(factor=factor_display_name)
    return body[0].upper() + body[1:]


# ---------------------------------------------------------------------------
# All UI strings by states.md ID
# ---------------------------------------------------------------------------

STRINGS: dict = {
    # -- S1 empty ----------------------------------------------------------
    "str.empty.headline": "Two ideas. One questionnaire. One sitting.",
    "str.empty.sub": (
        "Score both ideas together, on this screen, now. Scoring them on "
        "different days adds noise the math can't remove; scoring them side "
        "by side cancels it."
    ),
    "str.empty.verdict_placeholder": (
        "The verdict appears when every factor is scored for both ideas. It "
        "will be a win probability with an interval — never a bare number."
    ),
    "str.empty.privacy": (
        "Runs entirely in this app. No API key, no server, nothing stored "
        "anywhere but your own log file."
    ),
    # R-10(iv) mint (states.md §6.8, landed round 8): the as-built demo-path
    # button, catalogued as an S1 affordance.
    "str.empty.example_cta": "Load example (canonical seeded pair)",

    # -- S2 partial --------------------------------------------------------
    "str.partial.progress_a": "Idea A — {n_scored} of {n_total} factors scored",
    "str.partial.progress_b": "Idea B — {n_scored} of {n_total} factors scored",
    "str.partial.verdict_placeholder": (
        "{n_missing} factor scores to go before the verdict: {missing_list}."
    ),
    # R-10(i) singular variant (states.md §6.8 binding rule: a count template's
    # singular is a distinct ID with suffix ``_one``, selected when the
    # interpolated count is exactly 1 — never a runtime "(s)" hack. Mixed-count
    # templates pluralize each slot independently by the same rule.)
    "str.partial.verdict_placeholder_one": (
        "1 factor score to go before the verdict: {missing_list}."
    ),
    "str.partial.no_default": (
        "Skipped factors aren't scored as zero — that would quietly mean "
        "\"exactly average.\" The verdict waits until you've said what you "
        "actually think."
    ),
    "str.partial.eval_optional": "optional — never enters the score",

    # -- S3 verdict --------------------------------------------------------
    "str.verdict.headline": "{winner_name} wins this comparison — {prob_token}",
    "str.verdict.prob_gloss": (
        "win probability under your policy, with its 90% bootstrap interval"
    ),
    "str.verdict.model_line_m0": (
        "Computed by M0 — your stated prior weights, applied identically to "
        "both ideas."
    ),
    "str.verdict.model_line_m1": (
        "Computed by M1 — the weights your own logged picks reveal, shrunk "
        "toward your stated policy."
    ),
    "str.verdict.mode_line_1n": (
        "1→N allocation verdict. Accuracy is earned: check the Brier meter "
        "below to see how this policy has actually done."
    ),
    "str.verdict.mode_line_01": "0→1 structural verdict — consistency, not prophecy.",
    "str.verdict.log_cta": "Log this decision",
    "str.verdict.fragility": (
        "⚠ Margin rests on the {factor} estimate — re-estimate before "
        "committing. One plausible step on that factor alone flips this verdict."
    ),
    "str.verdict.ablation_toggle": (
        "Equal-weight check — rerun with all weights equal (signs kept). If "
        "the winner changes, your weights are doing the work; if not, the "
        "factors are."
    ),
    # R-10(ii) revised tail (states.md §6.8, landed round 8): the as-built flow
    # recomputes only on a manual Compare click, so the copy states exactly
    # that. If engineering ever wires auto-recompute, the tail reverts to
    # "Recomputing…" in the same change as the wiring — copy and behavior must
    # state the same thing in the same change.
    "str.verdict.stale": (
        "Inputs changed — the verdict above no longer applies. Press Compare "
        "to recompute."
    ),
    # Reserved slot (ships EMPTY in v1 per Decisions D4; layout reserves the line)
    "str.verdict.audit_footer": (
        "Your policy so far: ζ {zeta:.2f} · Brier {brier:.2f} across "
        "{n} decisions — details in audit."
    ),

    # -- S4 too close ------------------------------------------------------
    "str.tctc.headline": "Too close to call — gather evidence.",
    "str.tctc.body": (
        "Win probability {prob_token}. The interval straddles 50%, so this "
        "comparison doesn't separate these ideas — and a forced winner here "
        "would be noise wearing a number."
    ),
    "str.tctc.next": (
        "The cheapest way to break the tie is below: the lever whose "
        "real-world change moves this furthest per unit of effort."
    ),
    "str.tctc.log_cta": "Log as too-close-to-call",
    "str.tctc.force_note": (
        "You can still pick one — people ship on Tuesdays too. Your pick will "
        "be logged as your call, not the model's."
    ),

    # -- S5 ceiling routing (0→1) -----------------------------------------
    "str.ceiling.strip": (
        "High-ceiling outlier — portfolio decision, not averaged in. You "
        "flagged {idea_name} as a possible top-box outcome. Averages are "
        "exactly what destroy outliers, so this flag never enters the score. "
        "Take {idea_name} to portfolio judgment: what does the portfolio look "
        "like if it works?"
    ),
    "str.ceiling.mech_label": (
        "Mechanical comparison below, ceiling flag excluded — use it as "
        "context, not as the decision."
    ),
    "str.ceiling.both": (
        "Both ideas are flagged high-ceiling. This pair is a portfolio "
        "conversation, not a weighted average. The mechanical comparison "
        "below is context only."
    ),

    # -- S6 M0-vs-M1 disagreement -----------------------------------------
    "str.disagree.headline": "Your stated policy and your revealed policy disagree.",
    "str.disagree.row_m0": "What you say you weigh (M0): {winner_name} — {prob_token}",
    "str.disagree.row_m1": (
        "What your last {n_picks} picks reveal you weigh (M1): "
        "{winner_name} — {prob_token}"
    ),
    "str.disagree.body": (
        "Neither is automatically right. Your stated weights are your policy; "
        "your revealed weights are your behavior. Open the weight comparison "
        "to see which factors drifted — then either update your policy or "
        "admit the drift."
    ),
    "str.disagree.compare_cta": "Compare weights",
    "str.disagree.weights_caption": (
        "Revealed weights are shrunk toward your stated policy (ridge, "
        "centered on M0), so early differences are real signal, not "
        "small-sample noise."
    ),
    "str.disagree.log_note": "Whichever you pick, the log records both model outputs.",

    # -- S7 order-bias diagnostic -----------------------------------------
    "str.orderbias.headline": "Presentation-order bias measured.",
    "str.orderbias.body": (
        "Across your {n} logged decisions, the idea you entered in slot A "
        "wins more often than symmetry allows (free intercept "
        "{intercept:+.2f}, beyond noise). Your verdicts are unaffected — "
        "scoring forces this term to zero, so swapping A and B flips every "
        "probability exactly. But your raw picks lean toward whichever idea "
        "you typed first."
    ),
    "str.orderbias.advice": (
        "Cheap fix: enter the incumbent or your own idea as B sometimes. The "
        "⇄ swap button exists for this."
    ),
    "str.orderbias.clear": (
        "Order-bias no longer detectable over your current log. Kept in the "
        "audit history."
    ),

    # -- S8 permanent 0→1 banner ------------------------------------------
    "str.banner.01": (
        "0→1 mode structures your search. It does not predict product–market "
        "fit. There is no dataset of ideas like yours, so this tool makes no "
        "claim about which idea will succeed. What it does: makes your "
        "comparison explicit, applies your policy identically to both ideas, "
        "and shows you the levers. The judgment stays yours."
    ),

    # -- S9 model-of-the-judge progress ------------------------------------
    "str.m1.progress": (
        "Model of the judge activates at {threshold} decisions — you have "
        "{n}. Until then, verdicts use your stated weights (M0)."
    ),
    # R-10(i) singular variant (exactly 1 logged decision; §6.8 rule)
    "str.m1.progress_one": (
        "Model of the judge activates at {threshold} decisions — you have 1. "
        "Until then, verdicts use your stated weights (M0)."
    ),
    "str.m1.progress_zero": (
        "Model of the judge activates at {threshold} decisions — you have "
        "none yet. Every logged decision teaches it what you actually weigh."
    ),
    "str.m1.activated": (
        "Model of the judge is now active. From here, each verdict also shows "
        "M1 — the weights your own picks reveal. When it disagrees with your "
        "stated policy, you'll see both."
    ),
    "str.m1.active_chip": "M1 active · trained on your {n} picks",
    "str.m1.consistency_note": (
        "ζ and Brier don't wait for {threshold} — they accumulate from your "
        "first decision. ζ is your consistency: how often your own picks form "
        "circular contradictions (A over B over C over A)."
    ),

    # -- S10 log states ----------------------------------------------------
    "str.log.empty": (
        "No decisions logged yet. Your log is a local file you download and "
        "keep — this Space stores nothing after you leave. If you have a log "
        "from before, upload it and your history (ζ, Brier, model of the "
        "judge) comes back."
    ),
    "str.log.upload_cta": "Upload log (.jsonl)",
    "str.log.loaded": (
        "{n} decisions in the log ({n_session} from this sitting). "
        "ζ {zeta:.2f} · Brier {brier:.2f} — see audit."
    ),
    # R-10(i) singular variant (n = 1 total; §6.8 rule; n_session pluralizes
    # independently and may be 0 or 1)
    "str.log.loaded_one": (
        "1 decision in the log ({n_session} from this sitting). ζ and Brier "
        "accumulate from here — see audit."
    ),
    "str.log.download_cta": "Download log (.jsonl)",
    "str.log.unsaved_nudge": (
        "{n_session} decisions from this sitting exist only in this browser "
        "tab. Download to keep them — there is no server copy, by design."
    ),
    # R-10(i) singular variant (§6.8 rule; the session-2 defect "1 decisions"
    # is exactly what this ID exists to kill)
    "str.log.unsaved_nudge_one": (
        "1 decision from this sitting exists only in this browser tab. "
        "Download to keep it — there is no server copy, by design."
    ),
    "str.log.uploaded_ok": (
        "Log restored — {n} decisions. ζ, Brier, and the model of the judge "
        "recomputed from your history. New decisions append to this log."
    ),
    # R-10(i) singular variant (§6.8 rule)
    "str.log.uploaded_ok_one": (
        "Log restored — 1 decision. ζ, Brier, and the model of the judge "
        "recomputed from your history. New decisions append to this log."
    ),
    "str.log.uploaded_merge": (
        "Merged: {n_uploaded} uploaded + {n_session} from this sitting = "
        "{n_total} decisions, ordered by timestamp. Duplicate records (same "
        "timestamp and inputs) were kept once."
    ),
    "str.log.uploaded_bad": (
        "That file isn't a PairwisePM log ({problem}). Nothing was changed — "
        "your current session log is intact. Export a fresh log from the tool "
        "that made this one, or check the schema in the README."
    ),
    "str.log.uploaded_mode_note": (
        "{n_1n} of these decisions are 1→N and {n_01} are 0→1. Each model "
        "trains only on its own mode; ζ and Brier are reported per mode."
    ),
    # Handler messages minted at the round-2 as-built reconciliation (states.md
    # §6.4 R-2) — previously hardcoded in app.py without IDs.
    "str.log.pick_first": (
        "Run a comparison first — the log records the verdict and your pick "
        "together, so there is nothing to append yet."
    ),
    "str.log.pick_missing": (
        "Choose which idea you actually pick (A or B) before logging — the "
        "log records your call, not just the model's."
    ),
    "str.log.appended": "Logged decision #{n} — your pick: {pick_name}.",
    "str.log.export_empty": (
        "Nothing to export yet — the log is empty. Log a decision first; the "
        "download hands you the only copy."
    ),
    "str.log.upload_none": "No file received — your current log is untouched.",

    # -- S11 inline errors -------------------------------------------------
    "str.err.number": (
        "{factor} needs a number — {scale_hint}, e.g. {example}. The "
        "z-scoring can't do anything with \"lots\"."
    ),
    "str.err.range_step": (
        "{factor} is a 0–4 step ({scale_hint}). {value} is off this scale — "
        "if it feels like a {value}, the scale's anchors are in the `why?` note."
    ),
    "str.err.range_signed": (
        "{factor} is scored −2 to +2 against the named past feature. Pick the "
        "anchor that fits; the comparison feature is your ruler."
    ),
    "str.err.effort_positive": (
        "Effort needs positive person-weeks. If it's truly zero, it isn't a "
        "comparison — ship it."
    ),
    "str.err.preserved": "Everything else you've entered is untouched.",

    # -- S12 mode toggle ---------------------------------------------------
    # RETIRED (states.md S12, round-2 reconciliation): the ratified
    # retained-per-mode contract means switching destroys nothing, so the
    # confirm dialog — whose copy claims scores are cleared — would be a false
    # statement. Kept for ID stability; MUST NOT be wired into the UI.
    "str.mode.confirm": (
        "Switching to {new_mode} replaces the factor set. Kept: idea names, "
        "descriptions, and everything in the judgment panel. Cleared: the "
        "{n_scores} factor scores you've entered — {old_mode_kind} factors "
        "don't map onto {new_mode_kind} factors, and pretending they do would "
        "cook the numbers."
    ),
    "str.mode.confirm_go": "Switch to {new_mode}",
    "str.mode.confirm_stay": "Stay in {old_mode}",
    "str.mode.switched_toast": (
        "{new_mode} mode. Same two ideas, new ruler: {mode_promise}."
    ),

    # -- S13 evaluative panel + override -----------------------------------
    "str.eval.header": "Outside the math — on the record",
    "str.eval.sub": (
        "Strategic fit, brand, taste. Captured here, shown on the verdict "
        "card as labeled judgment, and never — never — inside the score. If "
        "these end up deciding it, that's allowed: it just happens in the open."
    ),
    "str.eval.card_echo": "Your judgment notes (not scored): {notes}",
    "str.override.cta": "Pick the other idea",
    "str.override.rationale_prompt": (
        "You're picking {pick_name} against the mechanical verdict "
        "({verdict_name} — {prob_token}). Say why, in a sentence. The "
        "rationale goes in the log — future-you gets to check whether this "
        "kind of call ages well."
    ),
    "str.override.rationale_placeholder": (
        "e.g. \"B unlocks the enterprise segment we've committed to for Q2 — "
        "strategic fit outweighs the score here.\""
    ),
    "str.override.logged": (
        "Logged as your call, with your rationale, alongside both model "
        "outputs. The model of the judge learns from picks — including this one."
    ),

    # -- R6 leverage-panel provenance chip ---------------------------------
    "str.leverage.provenance_m0": "weights: M0 — your stated prior policy",
    "str.leverage.provenance_m1": (
        "weights: M1 — revealed by your {n_picks} logged picks, shrunk toward "
        "your stated policy"
    ),

    # -- S14 audit view ----------------------------------------------------
    "str.audit.m1_locked": (
        "Revealed-policy panel not yet active — it activates near decision "
        "{threshold} (you have {n} in this mode). Until then verdicts use M0, "
        "your stated weights; nothing here is simulated."
    ),
    "str.audit.zeta_gloss": (
        "ζ is your consistency: how often your own picks form circular "
        "contradictions (A over B over C over A). 1.00 = perfectly transitive."
    ),
    "str.audit.brier_gloss": (
        "Brier scores the model's probabilities against your actual picks — "
        "lower is better; 0.25 is what coin-flipping earns."
    ),
    "str.audit.curve_locked": (
        "Reliability curve unlocks at {threshold} decisions in this mode (you "
        "have {n}). With fewer, the bins would be noise drawn as a line."
    ),
    # Wording constraint (compliance T-NEG-04b): 0→1-scoped strings may never
    # contain the words "accuracy" or "predictive" — not even in a negation,
    # because the test is a substring assertion. "predict(s)" as a verb is fine
    # (the pinned banner uses it).
    "str.audit.01_caption": (
        "0→1 mode: these measure the consistency of your judgments — they do "
        "not predict outcomes. No outcome data about ideas like yours exists."
    ),

    # -- Micro-patterns ----------------------------------------------------
    "str.mp1.nointerval": "interval unavailable — probability withheld",
    "str.mp2.chip": "Runner-up in this comparison",
    "str.mp2.parity": (
        "Path to parity: {parity_move} brings {loser_name} to 50/50. To 60/40 "
        "in its favor: {sixty_forty_move}."
    ),
    "str.mp2.fundamentals": (
        "{loser_name} loses on fundamentals — no working-harder path flips "
        "this comparison: every path to parity runs through facts "
        "({fact_list}) or leaves the plausible range. That's worth knowing "
        "before anyone spends a quarter trying."
    ),
    "str.mp3.lever_chip": "lever",
    "str.mp3.lever_tip": "Lever: you can move this by working — build, test, sell, de-risk.",
    "str.mp3.fact_chip": "fact",
    "str.mp3.fact_tip": (
        "Fact: it is what it is. The tool will never suggest \"improving\" "
        "this — it will tell you when a verdict rests on it."
    ),

    # -- Factor-label rules (§6.2, §6.4 R-2) -------------------------------
    "str.factor.risk_label_suffix": "4 = lowest exposure, 0 = highest",
    # Verbatim-identical to the as-built app.py checkbox label (zero-cost
    # adoption); 0→1-scoped, so covered by the T-NEG-04b wording rule.
    "str.factor.ceiling_label": (
        "Ceiling (top-box flag) — unweighted; routes to portfolio judgment, "
        "never enters the score"
    ),
}


# Banned vocabulary anywhere in UI or log-facing copy (MP-2)
BANNED_WORDS = ("rejected", "loser", "killed", "eliminated", "failed")

# 0→1-scoped strings (rendered only in 0→1 mode). Compliance T-NEG-04b asserts
# these never contain "accuracy" or "predictive" — substring match, so negations
# count too. The interpolant for str.mode.switched_toast's {mode_promise} when
# entering 0→1 is MODE_PROMISE_01 below and is covered by the same rule.
ZERO_TO_ONE_SCOPED_IDS = (
    "str.banner.01",
    "str.verdict.mode_line_01",
    "str.ceiling.strip",
    "str.ceiling.mech_label",
    "str.ceiling.both",
    "str.audit.01_caption",
    "str.factor.ceiling_label",
)
MODE_PROMISE_01 = "structure and consistency, no claim about what will succeed"
MODE_PROMISE_1N = "your stated policy, calibration earned over the log"
BANNED_01_WORDS = ("accuracy", "predictive")


def _self_check() -> None:
    """Verify the pinned constants appear contiguously in the full strings.
    Cheap invariant so an edit to one location cannot silently break the other."""
    assert PINNED_TOO_CLOSE.lower() in STRINGS["str.tctc.headline"].lower()
    assert PINNED_FUNDAMENTALS in STRINGS["str.mp2.fundamentals"].format(
        loser_name="Idea B", fact_list="Reach"
    )
    assert PINNED_CEILING.lower() in STRINGS["str.ceiling.strip"].format(
        idea_name="Idea B"
    ).lower()
    assert PINNED_FRAGILITY_TMPL.format(factor="Reach").lower() in STRINGS[
        "str.verdict.fragility"
    ].format(factor="Reach").lower()
    assert PINNED_BANNER_01 in STRINGS["str.banner.01"]
    for word in BANNED_WORDS:
        for sid, s in STRINGS.items():
            assert word not in s.lower().split(), (sid, word)
    # T-NEG-04b: 0→1-scoped copy never contains these substrings, even negated
    for sid in ZERO_TO_ONE_SCOPED_IDS:
        for word in BANNED_01_WORDS:
            assert word not in STRINGS[sid].lower(), (sid, word)
    for word in BANNED_01_WORDS:
        assert word not in MODE_PROMISE_01.lower()
    # GTM canonical rounding: 58.5% renders 59%, not banker's 58%
    assert prob_token(0.585, 0.52, 0.64) == "59% (52–64%)"


_self_check()
