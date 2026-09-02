"""The AUDIT VIEW's honesty surface — the Spine refusal that renders as a NUMBER.

Registered round 19 on design's §6.18 finding (compliance rows F-34 / F-35).
Every other copy instrument on this board watches WORDS: the string catalogue
(T-VEND-01/02/05), the config text (T-COPY-01/01b/02), the four ``(not
scored)`` labels (T-NEG-08 / T-COPY-02b). The audit view is where the Spine's
hardest refusal — *"Out — refused, deliberately: … accuracy claims in 0→1
mode"* — is carried by a statistic and a caption in the same table, and
neither half was asserted by anything until this file:

* **The caption was minted and unwatched.** ``str.audit.01_caption`` ("0→1
  mode: these measure the consistency of your judgments — they do not predict
  outcomes. No outcome data about ideas like yours exists.") is in the
  catalogue, is byte-guarded by T-VEND-01/02/05, and is swept for banned words
  by T-NEG-04b — three instruments on its TEXT, none on whether it reaches a
  screen. Delete the ``if log.n("zero_to_one"):`` gate in ``render_audit`` and
  the entire suite stayed green with the refusal gone from the surface it was
  written for. That is the F-33 defect one view over, and T-NEG-09 closes it.

* **The numbers above it are POOLED ACROSS MODES.** ``render_audit`` calls
  ``log.kendall_zeta()``, ``log.brier()``, ``log.outcome_brier()`` and
  ``log.override_rate()`` with no ``mode`` argument — every one of those
  methods takes one — while the same table scopes M1, the order-bias
  diagnostic and the reliability row per mode and gates the caption on
  ``log.n("zero_to_one")``. Design demonstrated it (states.md §6.18) and this
  seat reproduced it before registering the row, **and the reproduction
  narrowed it**: with A≻B, B≻C, A≻C logged in 1→N the displayed ζ is 1.00, and
  ONE 0→1 comparison reversing the **A–C** pair drops the DISPLAYED row to
  ζ = 0.00 while ``kendall_zeta("one_to_n")`` is still 1.00 — but reversing the
  **A–B** pair instead leaves it at 1.00 (B≻A, B≻C, A≻C is still transitive).
  So the true condition is a cross-mode re-comparison that BOTH overwrites an
  edge AND closes a circular triad, not any cross-mode re-comparison at all;
  the wider sentence is the one a reader would quote and it does not
  reproduce. The mechanism is design's and it holds (``log.py:198-206``):
  edges are keyed by unordered idea name over the whole log,
  most-recent-write-wins, so the second comparison replaces the first instead
  of being a different question. The sharpest case is ``Brier (vs. labeled outcomes)``,
  which can absorb 0→1 outcome labels and render as a number one line above a
  caption that says no such data exists.

T-NEG-09b does NOT assert that the pooling is correct, and it does NOT freeze
it: it is a CENSUS with an explicit classification, so the open row's
population is derived from ``app.py`` rather than kept as a hand list in
prose. Scoping a statistic per mode — the fix, owner engineering, deferred
past the M-UX-02a sitting because nobody should be moving code this week —
leaves this clause green. Adding a FIFTH undisclosed pooled statistic to the
honesty table reds it, in the change that does it. When the F-35 entries are
gone from the classification below, the row closes and this half of the file
has no work left to do.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import pairwisepm

REPO = Path(pairwisepm.__file__).resolve().parent.parent
APP = REPO / "app.py"

# Every ``log.<stat>()`` call in ``render_audit`` that passes NO mode
# argument, classified. A statistic reaching this table without an entry here
# is an unclassified claim about the user's judgment on the surface whose
# whole job is honesty — T-NEG-09b reds on it.
#
# POOLED-DISCLOSED  = pooled deliberately AND the pooling is visible on screen.
# POOLED-F-35       = pooled with the split invisible; compliance row F-35,
#                     owner engineering, fix = pass the mode through.
_AUDIT_POOLED_STATS = {
    "n": (
        "POOLED-DISCLOSED — the count row prints the per-mode split beside "
        "the total ('Decisions logged 5 (1→N: 3, 0→1: 2)'), so the reader can "
        "see what the number is over. This is the shape the four below need."
    ),
    "kendall_zeta": (
        "POOLED-F-35 — ζ over the whole log. Edges are keyed by unordered idea "
        "name with most-recent-write-wins, so the same pair compared in both "
        "modes overwrites rather than adding a question; where that overwrite "
        "also closes a circular triad the displayed row goes 1.00 → 0.00 with "
        "per-mode 1→N still 1.00 (reproduced from this seat, round 19; a "
        "reversal that leaves the graph transitive does NOT move it, which "
        "bounds the finding and is stated in this file's header)."
    ),
    "brier": (
        "POOLED-F-35 — model-vs-your-picks calibration over both modes at "
        "once, under a caption that scopes itself to 0→1."
    ),
    "outcome_brier": (
        "POOLED-F-35 — the Spine-sharpest one: an accuracy number that can "
        "absorb 0→1 outcome labels renders one line above 'No outcome data "
        "about ideas like yours exists' (Spine, Out: accuracy claims in 0→1 "
        "mode)."
    ),
    "override_rate": (
        "POOLED-F-35 — how often you overrode the model, over both modes."
    ),
}


def _app_module():
    """The live app module. Its own subject is gradio, which it imports.

    Gated the way ``test_packaging.py::_load_app`` is gated and for the same
    reason: the engine has no gradio dependency (T-PKG-02's UI-only rule), so
    a tree without it cannot render anything and a skip here is the truth
    about THIS clause's subject, not a hole in the census — T-NEG-09b below
    reads the source and never skips, so this file cannot return an
    all-skipped green (T-VEND-07's finding, applied prospectively).
    """
    pytest.importorskip("gradio")
    import importlib.util

    spec = importlib.util.spec_from_file_location("pairwisepm_app_audit", APP)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _record(mode: str, a: str, b: str, pick: str) -> dict:
    """A minimal log record: enough for the audit view's own gates.

    Deliberately carries empty factor vectors — ``training_data`` skips
    records missing current factor keys (schema-drift tolerance), so the M1
    rows read 'locked' and this fixture cannot accidentally assert anything
    about the ladder. It exercises the count row, the caption gate and the
    pooled statistics, which is exactly this file's subject.
    """
    return {
        "timestamp": "2026-08-31T00:00:00Z",
        "mode": mode,
        "idea_a": {"name": a, "raw": {}, "z": {}},
        "idea_b": {"name": b, "raw": {}, "z": {}},
        "pick": pick,
    }


def test_audit_0to1_caption_renders_only_when_the_log_carries_0to1():
    """T-NEG-09 — the audit view's no-prediction refusal reaches the screen.

    Spine, Scope Boundaries (Out): *accuracy claims in 0→1 mode*. In the
    verdict card that refusal is carried by the permanent banner, which is
    guarded three ways (config value, catalogue byte-identity, and an import
    assert in ``app.py`` that stops the process before first paint). In the
    AUDIT view it is carried by ``str.audit.01_caption``, and the catalogue
    guards are all guards on the STRING: they prove the sentence exists and
    says what design minted, and say nothing about whether a user ever sees
    it. Deleting the ``if log.n("zero_to_one")`` gate leaves 78/78 green.

    Both directions are asserted, because a caption pasted unconditionally is
    a different defect and passes a one-way check: the sentence is scoped to
    0→1 (``ZERO_TO_ONE_SCOPED_IDS``), and rendering "No outcome data about
    ideas like yours exists" under a pure 1→N table would be the honesty copy
    itself making a claim about the wrong mode.
    """
    from pairwisepm.log import DecisionLog
    from pairwisepm.strings import STRINGS

    mod = _app_module()
    caption = STRINGS["str.audit.01_caption"]

    only_1n = DecisionLog(records=[
        _record("one_to_n", "A", "B", "A"),
        _record("one_to_n", "B", "C", "A"),
    ])
    html_1n = mod.render_audit(only_1n, 0)
    assert caption not in html_1n, (
        "the 0→1 no-prediction caption renders on a log with no 0→1 "
        "decisions. str.audit.01_caption is a 0→1-SCOPED string (design's "
        "ZERO_TO_ONE_SCOPED_IDS); pasted unconditionally it stops being a "
        "mode promise and becomes a disclaimer the reader learns to skip."
    )

    with_01 = DecisionLog(records=only_1n.records + [
        _record("zero_to_one", "D", "E", "B"),
    ])
    html_01 = mod.render_audit(with_01, 0)
    assert caption in html_01, (
        "the audit view renders consistency and calibration numbers over a "
        "log containing 0→1 decisions WITHOUT str.audit.01_caption. That "
        "caption is the only place the audit surface states the Spine's "
        "refusal — 'they do not predict outcomes. No outcome data about "
        "ideas like yours exists.' Three instruments guard the sentence's "
        "bytes (T-VEND-01/02/05) and none of them guards its arrival on a "
        "screen; without this clause the refusal can be deleted from the "
        "surface it was minted for with the whole suite green."
    )


def test_audit_view_pooled_statistics_are_censused_and_classified():
    """T-NEG-09b — every pooled number in the honesty table is classified.

    A CENSUS, not a requirement, and the distinction is the point. Design's
    §6.18 finding is that four of the audit table's statistics are computed
    over the whole log while everything around them is per-mode. That is a
    defect with a named owner (engineering, ``render_audit``) and a fix that
    is deliberately deferred past the M-UX-02a sitting — so what this seat can
    honestly instrument tonight is not "the numbers are right" but **"the
    population of pooled numbers is the population the open row describes"**.

    Read off ``app.py``'s AST rather than by grep, so a reflowed call cannot
    empty it. It is silent in both directions that matter:

    * Passing a mode through (THE FIX) removes a call from the census and
      leaves this clause green — a guard that reds when someone repairs the
      thing it is about is a guard that gets deleted rather than heeded.
    * Adding a fifth undisclosed pooled statistic to this table reds HERE, in
      the change that adds it, because the classification below is the row's
      population and an unclassified claim about the user's judgment is
      exactly what F-35 exists to keep countable.

    When every ``POOLED-F-35`` entry is gone, F-35 closes and this clause is
    a two-line delete. It is deliberately NOT in ``test_copy_surfaces.py``'s
    ``_REQUIRED_CLAUSES``: freezing a witness in place is how an open row
    becomes permanent furniture.
    """
    assert APP.exists(), (
        "app.py is missing from a tree that ships pairwisepm — the audit "
        "surface cannot be censused, and this clause never skips because its "
        "subject is the shipped app itself."
    )
    tree = ast.parse(APP.read_text(encoding="utf-8"))

    audits = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "render_audit"
    ]
    assert len(audits) == 1, (
        f"expected exactly one module-level render_audit in app.py; found "
        f"{len(audits)}. The audit view is where the Spine's 0→1 refusal is "
        "rendered as a number; it is not a function to have two of."
    )

    pooled = set()
    scoped = set()
    for sub in ast.walk(audits[0]):
        if not isinstance(sub, ast.Call):
            continue
        func = sub.func
        if not (isinstance(func, ast.Attribute)
                and isinstance(func.value, ast.Name)
                and func.value.id == "log"):
            continue
        (pooled if not sub.args and not sub.keywords else scoped).add(func.attr)

    unclassified = sorted(pooled - set(_AUDIT_POOLED_STATS))
    assert not unclassified, (
        "render_audit computes statistics over the WHOLE LOG that this "
        f"census does not classify: {unclassified}. Every number in the audit "
        "table is a claim about the user's own judgment, and the table is "
        "captioned with the Spine's 0→1 no-prediction refusal. Either pass "
        "the mode through (the F-35 fix — this clause stays green), or add "
        "an entry to _AUDIT_POOLED_STATS saying, in writing, why pooling is "
        "right here and where the reader can see what the number is over."
    )

    # A statistic cannot be BOTH pooled and per-mode in one render without
    # somebody having decided which the reader is looking at.
    ambiguous = sorted(pooled & scoped - {"n"})
    assert not ambiguous, (
        f"render_audit calls {ambiguous} both pooled and mode-scoped in the "
        "same table. ``n`` is the sanctioned case: it prints the total AND "
        "the split, which is what makes it honest. Any other statistic "
        "rendered twice under different scopes gives the reader two numbers "
        "for one question with no way to tell them apart."
    )
