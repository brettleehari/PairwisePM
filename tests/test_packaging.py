"""T-PKG + T-NEG-06 — packaging contract and server-side-storage static audit.

These are the in-suite halves of compliance rows F-16, F-18, F-24 and N-06.
The remaining release-gate steps need network or a browser and stay manual:
clean-venv ``pip install .`` (T-PKG-01), HF Space README sdk_version validation
against the live Space image, and the M-UX behavioral checks.

Only ``test_app_module_level_demo`` needs gradio; it skips cleanly where gradio
is not installed and MUST pass in the Space image (checklist P-8).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

import pairwisepm

REPO = Path(pairwisepm.__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# T-PKG — pip-installable package + HF Space files (SC-14)
# ---------------------------------------------------------------------------

def test_package_version_matches_pyproject():
    assert pairwisepm.__version__ == "0.1.0"
    py = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r'^name\s*=\s*"pairwisepm"', py, re.M)
    assert re.search(r'^version\s*=\s*"0\.1\.0"', py, re.M)
    # Engine deps only; gradio is confined to the [app] extra (UI-only rule).
    deps = re.search(r"^dependencies\s*=\s*\[(.*?)\]", py, re.M | re.S).group(1)
    assert "numpy" in deps and "PyYAML" in deps and "gradio" not in deps


def test_space_files_ship():
    for f in ("README.md", "requirements.txt", "app.py",
              "configs/one_to_n.yaml", "configs/zero_to_one.yaml",
              "decisions.sample.jsonl"):
        assert (REPO / f).is_file(), f


def test_readme_hf_yaml_header():
    text = (REPO / "README.md").read_text(encoding="utf-8")
    assert text.startswith("---\n")
    header = text.split("---", 2)[1]
    assert re.search(r"^sdk:\s*gradio\s*$", header, re.M)
    assert re.search(r"^app_file:\s*app\.py\s*$", header, re.M)
    # sdk_version must be an exact pin (validated against the live Space at
    # push time — sequencing node hf-space-setup / space-smoke-test).
    assert re.search(r"^sdk_version:\s*\d+\.\d+\.\d+\s*$", header, re.M)


def test_readme_epistemics_substrings():
    """T-PKG-02c: the three §7 epistemics statements (F-18)."""
    text = " ".join((REPO / "README.md").read_text(encoding="utf-8").split())
    for phrase in (
        "a stated, editable policy, not fitted",
        "0→1 mode makes no accuracy claim",
        "The LLM's job was at build time",
        "the runtime is weights and a bias term",
    ):
        assert phrase in text.replace("**", ""), phrase


def test_app_module_level_demo():
    """HF Spaces contract: app.py exposes a module-level ``demo`` gr.Blocks."""
    gr = pytest.importorskip("gradio")
    import importlib.util
    spec = importlib.util.spec_from_file_location("pairwisepm_app",
                                                  REPO / "app.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert isinstance(mod.demo, gr.Blocks)


# ---------------------------------------------------------------------------
# T-NEG-06 — no server-side storage of user data (R-06, SC-07): static audit
# ---------------------------------------------------------------------------

def test_no_server_side_persistence_static():
    src = (REPO / "app.py").read_text(encoding="utf-8")
    # No DB clients, no HF persistence, no cloud SDKs anywhere in the app.
    forbidden = ("sqlite3", "sqlalchemy", "psycopg", "pymongo", "redis",
                 "boto3", "google.cloud", "firebase", "supabase",
                 "huggingface_hub", "datasets")
    pat = re.compile(r"^\s*(import|from)\s+(" + "|".join(
        re.escape(f) for f in forbidden) + r")\b", re.M)
    assert not pat.search(src)
    # Log custody lives in per-session gr.State, and the only file writes are
    # user-initiated downloads through tempfile.
    assert "gr.State(DecisionLog())" in src
    assert "tempfile.mkdtemp()" in src
    writes = re.findall(r"\.write_text\(", src)
    assert len(writes) == 1  # exactly the export path
    # The engine package itself performs no file writes at all (the UI owns
    # file I/O; the log module has no paths and no clock).
    write_pat = re.compile(r"write_text|write_bytes|open\([^)]*[\"'][wa]")
    for p in (REPO / "pairwisepm").glob("*.py"):
        assert not write_pat.search(p.read_text(encoding="utf-8")), p


# ---------------------------------------------------------------------------
# T-CUST-01 — custody nudge counts session appends only (matrix F-26, S10b)
# ---------------------------------------------------------------------------

def _load_app():
    pytest.importorskip("gradio")
    import importlib.util
    spec = importlib.util.spec_from_file_location("pairwisepm_app_cust",
                                                  REPO / "app.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_custody_nudge_counts_session_appends_only(tmp_path):
    """T-CUST-01: `str.log.unsaved_nudge`'s ``{n_session}`` slot receives the
    count of records APPENDED THIS SESSION only — never the total log size —
    and the nudge is suppressed at 0 (design S10b, binding semantics).

    Guards the round-2 honesty defect (states.md §6.4 R-1): uploaded records
    already live in the user's own file; a nudge that counts them makes a
    false custody claim, and the Spine's log-in-the-user's-hands commitment
    (SC-07) is made visible through exactly this copy.
    """
    from pairwisepm.log import DecisionLog
    from pairwisepm.strings import STRINGS

    mod = _load_app()
    marker = "decisions from this sitting exist only in this browser"
    assert marker in STRINGS["str.log.unsaved_nudge"]  # stable anchor

    sample = (REPO / "decisions.sample.jsonl").read_text(encoding="utf-8")
    log = DecisionLog.from_jsonl(sample)
    assert log.n() >= 2 and log.n() != 1  # scenario needs uploads ≠ session count

    # (a) All records uploaded, none appended this sitting ⇒ no nudge at all.
    assert marker not in mod.render_audit(log, n_session=0)

    # (b) One session append ⇒ the nudge says 1, never the log total — via
    # the SINGULAR variant (R-10(i), §6.8 rule: count == 1 selects the
    # ``_one`` ID; "1 decisions" is the session-2 defect class it kills).
    html = mod.render_audit(log, n_session=1)
    assert STRINGS["str.log.unsaved_nudge_one"] in html
    assert STRINGS["str.log.unsaved_nudge"].format(n_session=log.n()) not in html
    assert "1 decisions" not in html

    # (c) The original defect scenario end-to-end: a fresh session that only
    # uploads a log must show no "exists only in this tab" claim afterwards.
    up = tmp_path / "uploaded.jsonl"
    up.write_text(sample, encoding="utf-8")
    merged, audit_html, _msg = mod.do_upload(str(up), DecisionLog(), 0)
    assert merged.n() == log.n()
    assert marker not in audit_html


# ---------------------------------------------------------------------------
# T-CEIL-03 — S5 routing strip renders in the UI (matrix F-27; SC-09, SC-13,
# R-03 legibility half; design states.md §6.4 R-3, landed round 2)
# ---------------------------------------------------------------------------

def test_ceiling_routing_strip_renders():
    """T-CEIL-03: the verdict card renders the full S5 routing strip — the
    design explanation that makes the score-exclusion legible — alongside the
    engine's pinned note, per flag state:

    - one idea flagged  ⇒ ``str.ceiling.strip`` formatted with THAT idea's
      name, plus the engine note + ``str.ceiling.mech_label``;
    - both flagged      ⇒ ``str.ceiling.both`` (and two engine notes);
    - no flag           ⇒ neither strip string appears.

    T-CEIL-01 proves the flag never moves the number (engine half); this pins
    the UI half: the user must SEE the exclusion asserted AND explained. A
    refusal whose explanation silently vanishes from the card would pass every
    engine test — that is exactly the honor-system gap this closes.
    """
    from pairwisepm.config import load_mode_config
    from pairwisepm.engine import compare
    from pairwisepm.strings import STRINGS

    mod = _load_app()
    z2o = load_mode_config(REPO / "configs" / "zero_to_one.yaml")
    raw_a = {"problem_severity_frequency": 3.0,
             "capability_trajectory_exposure": 1.0, "evidence_of_pull": 2.0,
             "genai_necessity": 3.0, "data_distribution_advantage": 2.0,
             "cost_to_test": 3.0}
    raw_b = {"problem_severity_frequency": 2.0,
             "capability_trajectory_exposure": -1.0, "evidence_of_pull": 1.0,
             "genai_necessity": 3.0, "data_distribution_advantage": 1.0,
             "cost_to_test": 2.0}
    name_a, name_b = "Meeting Copilot", "Spec Drafter"
    strip_a = STRINGS["str.ceiling.strip"].format(idea_name=name_a)
    strip_b = STRINGS["str.ceiling.strip"].format(idea_name=name_b)
    both = STRINGS["str.ceiling.both"]
    mech = STRINGS["str.ceiling.mech_label"]

    def card(ca, cb):
        res = compare(z2o, raw_a, raw_b, seed=11, n_boot=200,
                      ceiling_a=ca, ceiling_b=cb)
        return mod.render_verdict(res, name_a, name_b, ceiling=(ca, cb))

    # (a) No flag ⇒ no routing strip, no engine note.
    html = card(False, False)
    for s in (strip_a, strip_b, both, mech):
        assert s not in html

    # (b) A flagged ⇒ A's strip (never B's), engine note + mech label present.
    html = card(True, False)
    assert strip_a in html and strip_b not in html and both not in html
    assert mech in html

    # (c) B flagged ⇒ B's strip — the name tracks the flagged idea.
    html = card(False, True)
    assert strip_b in html and strip_a not in html

    # (d) Both flagged ⇒ the portfolio-conversation copy.
    html = card(True, True)
    assert both in html and strip_a not in html and strip_b not in html
    assert mech in html


# ---------------------------------------------------------------------------
# T-SER-01 — untouched factors never reach the handlers as values
# (design states.md §6.4 R-8; Spine metric #4 "honest by construction")
# ---------------------------------------------------------------------------

def _compare_vals(mod, n2n_a=None, n2n_b=None):
    """Build the flat *vals list do_compare receives, with the exact payloads
    the frontend submits: strings for factor Textboxes ('' when untouched)."""
    kn, kz = mod.N2N.factor_keys, mod.Z2O.factor_keys
    a = dict.fromkeys(kn, "") if n2n_a is None else n2n_a
    b = dict.fromkeys(kn, "") if n2n_b is None else n2n_b
    return ([a[k] for k in kn] + [b[k] for k in kn]
            + [""] * (2 * len(kz)) + [False, False] + [""] * 4)


def test_untouched_factor_never_scores():
    """T-SER-01 (test_engine_spec.md §20; matrix F-28, gate P-10): the
    round-1 blocking commitment (§6.4 delta (d)), guarded
    at the serialization boundary the suite was previously blind to.

    gradio 6 renders ``gr.Number(value=None)`` as a literal 0 and submits it,
    so a form of untouched Number fields reached do_compare as 12 real scores
    and _missing_factors never fired — a full verdict computed from silently
    imputed averages (states.md §6.4 R-8, browser-verified). The shipped
    mechanism is Textbox factor inputs, whose untouched payload is the empty
    string; this test drives the handlers with exactly those frontend
    payloads, and pins that 0 stays a legitimate SCORE, never "unfilled"."""
    gr = pytest.importorskip("gradio")  # clean skip in non-UI envs (P-8)
    from pairwisepm.log import DecisionLog
    from pairwisepm.strings import STRINGS

    mod = _load_app()

    # (a) No factor input is a gr.Number — the component class whose empty
    # state serializes as 0. Untouched Textboxes serialize as "".
    for f in mod.N2N.factors + mod.Z2O.factors:
        comp = mod._factor_input(f, "a")
        assert not isinstance(comp, gr.Number), f.key
        assert isinstance(comp, gr.Textbox) and comp.value in ("", None), f.key

    # (b) A completely untouched form must render the S2 partial placeholder —
    # never a verdict, never a 50/50 computed from defaulted scores.
    verdict, lev, ladder, ctx = mod.do_compare(
        mod.N2N.label, "A1", "B1", DecisionLog(), *_compare_vals(mod))
    assert ctx is None and lev == "" and ladder == ""
    assert "factor scores to go before the verdict" in verdict
    assert verdict.count("(both ideas)") == len(mod.N2N.factor_keys)
    assert "wins this comparison" not in verdict

    # (c) One field left untouched ⇒ placeholder naming that factor/side —
    # via the SINGULAR variant (R-10(i), §6.8 rule: count == 1 selects the
    # ``_one`` ID; "1 factor scores" is the defect class the mint kills).
    ra = {k: f"{v:g}" for k, v in mod._seed_raw("A").items()}
    rb = {k: f"{v:g}" for k, v in mod._seed_raw("B").items()}
    hole = dict(rb, reach="")
    verdict, _, _, ctx = mod.do_compare(
        mod.N2N.label, "A1", "B1", DecisionLog(), *_compare_vals(mod, ra, hole))
    assert ctx is None
    assert STRINGS["str.partial.verdict_placeholder_one"].format(
        missing_list="Reach (Idea B)") in verdict
    assert "1 factor scores" not in verdict

    # (d) Non-numeric and out-of-plausible-range entries also block, through
    # the same S2 list (no raw Gradio error toasts in the mechanism at all).
    bad = dict(rb, reach="lots", effort="0")  # effort plausible range is 0.5–52
    verdict, _, _, ctx = mod.do_compare(
        mod.N2N.label, "A1", "B1", DecisionLog(), *_compare_vals(mod, ra, bad))
    assert ctx is None
    assert "Reach (Idea B — not a number)" in verdict
    assert "outside 0.5" in verdict and "wins this comparison" not in verdict

    # (e) An explicit 0 is a score, not "unfilled": reach 0 is in range and
    # the verdict must compute — the exact distinction Number's None-as-0
    # serialization destroyed.
    zero = dict(ra, reach="0")
    verdict, _, _, ctx = mod.do_compare(
        mod.N2N.label, "A1", "B1", DecisionLog(), *_compare_vals(mod, zero, rb))
    assert ctx is not None
    assert "factor scores to go" not in verdict
    assert ctx["raw_a"]["reach"] == 0.0


# ---------------------------------------------------------------------------
# T-THEME-01 — forced light backgrounds force their text color
# (design states.md §6.4 R-9: MP-1 must survive Gradio's dark theme)
# ---------------------------------------------------------------------------

def test_forced_light_backgrounds_force_text_color():
    """T-THEME-01: any HTML block that forces a light background must force
    its text color in the same style attribute, or Gradio's dark theme paints
    near-white inherited text on the light block — the MP-1 probability
    headline rendered invisible (§6.4 R-9, verified by live screenshot).

    Source-level so it also covers blocks that are hard to render
    deterministically (e.g. the fragility strip): every occurrence of a
    forced background in app.py must be immediately followed by a forced
    color in the same string literal.

    Broadened round 5 (compliance) to the full spec §21 contract: ANY
    forced hex background — `background:` or `background-color:`, any
    color, not just the two hexes shipped today — requires an adjacent
    forced text color. A dark forced background with inherited light-theme
    text is the same defect class mirrored; a future block added with
    `background:#ffffff` must red this pin, not evade it. Text-free
    blocks with dynamic backgrounds (the leverage bar's `background:{col}`)
    carry no hex literal and are out of scope per §21's text-bearing
    clause."""
    src = (REPO / "app.py").read_text(encoding="utf-8")
    hits = list(re.finditer(r"background(?:-color)?:#[0-9a-fA-F]{3,8};", src))
    assert len(hits) >= 2, "expected forced-background blocks in app.py"
    for m in hits:
        assert src[m.end():].startswith("color:#"), (
            f"forced background without forced text color at "
            f"offset {m.start()}: {src[m.start():m.end() + 20]!r}")


# -- T-THEME-01b: the R-9b strengthening (render-level) ----------------------

class _NestedColorAudit:
    """Walk rendered HTML; inside any element that forces a background, every
    element that DIRECTLY bears text must carry its own inline ``color:``.

    Why element-level, not wrapper-level: gradio 6 ships
    ``.gradio-container-* .prose * { color: var(--body-text-color) }``, which
    outranks CSS inheritance — a wrapper's forced color never reaches nested
    elements, so the wrapper-only discipline the source-level pin enforces
    left the S3/S4 headlines, the MP-1 token's <b>, the runner-up chip span,
    and the S1/S2 placeholder inner divs near-invisible in the served dark
    theme while this test's source half stayed green (design §6.7, R-9b —
    the same guard-blindness class T-SER-01 closed at the serialization
    boundary, one layer further down)."""

    _FORCED_BG = re.compile(r"background(?:-color)?\s*:\s*#")
    _OWN_COLOR = re.compile(r"(?<![-\w])color\s*:")

    def __init__(self) -> None:
        self.violations: list = []

    def audit(self, html_text: str) -> "_NestedColorAudit":
        from html.parser import HTMLParser

        outer = self

        class P(HTMLParser):
            def __init__(self) -> None:
                super().__init__()
                self.stack: list = []  # (tag, style, inside_forced_bg)

            def handle_starttag(self, tag, attrs):
                style = dict(attrs).get("style") or ""
                forced = ((self.stack[-1][2] if self.stack else False)
                          or bool(outer._FORCED_BG.search(style)))
                self.stack.append((tag, style, forced))

            def handle_endtag(self, tag):
                while self.stack:
                    t = self.stack.pop()[0]
                    if t == tag:
                        break

            def handle_data(self, data):
                if not data.strip() or not self.stack:
                    return
                tag, style, forced = self.stack[-1]
                if forced and not outer._OWN_COLOR.search(style):
                    outer.violations.append((tag, data.strip()[:60]))

        P().feed(html_text)
        return self


def test_forced_light_blocks_color_every_nested_element():
    """T-THEME-01b (design §6.7 R-9b; strengthens T-THEME-01 to the
    every-nested-element contract): render the real S1/S2/S3/S4 surfaces and
    assert no text-bearing element inside a forced-background block relies on
    inherited color."""
    pytest.importorskip("gradio")
    from pairwisepm.config import load_mode_config
    from pairwisepm.engine import compare

    mod = _load_app()

    # Sensitivity self-test: the pre-R-9b headline shape (nested <b> with no
    # own color inside a forced-light wrapper) MUST be flagged — this is the
    # exact rendered shape browser session 2 caught, i.e. red-by-construction
    # against the pre-fix build.
    bad = ("<div style='background:#fafaf9;color:#1c1917'>"
           "<b>Reply Drafts wins</b></div>")
    assert _NestedColorAudit().audit(bad).violations, \
        "audit failed to flag an uncolored nested element"
    # ...and inline color on the nested element satisfies it (inline styles
    # outrank the `.prose *` stylesheet rule).
    good = ("<div style='background:#fafaf9;color:#1c1917'>"
            "<b style='color:#1c1917'>Reply Drafts wins</b></div>")
    assert not _NestedColorAudit().audit(good).violations

    z2o = load_mode_config(REPO / "configs" / "zero_to_one.yaml")
    raw_a = {"problem_severity_frequency": 3.0,
             "capability_trajectory_exposure": 1.0, "evidence_of_pull": 2.0,
             "genai_necessity": 3.0, "data_distribution_advantage": 2.0,
             "cost_to_test": 3.0}
    raw_b = {"problem_severity_frequency": 2.0,
             "capability_trajectory_exposure": -1.0, "evidence_of_pull": 1.0,
             "genai_necessity": 3.0, "data_distribution_advantage": 1.0,
             "cost_to_test": 2.0}

    # S3 decisive card, with ceiling strip + fragility surface + eval annex.
    res = compare(z2o, raw_a, raw_b, seed=11, n_boot=200, ceiling_a=True)
    assert res.active.verdict in ("A", "B")  # fixture must exercise S3
    s3 = mod.render_verdict(res, "Meeting Copilot", "Spec Drafter",
                            eval_notes='A · Strategic fit — "core"',
                            ceiling=(True, False))
    # S4 too-close card: identical vectors ⇒ p = 0.5, interval straddles.
    tie = compare(z2o, raw_a, raw_a, seed=11, n_boot=200)
    assert tie.active.verdict == "too_close"
    s4 = mod.render_verdict(tie, "Meeting Copilot", "Spec Drafter")

    surfaces = {
        "S1 empty placeholder": mod.render_placeholder(),
        "S2 partial placeholder": mod.render_placeholder(["Reach (Idea B)"]),
        "stale card": mod.render_stale(),
        "S3 verdict card": s3,
        "S4 too-close card": s4,
        "banner": mod.BANNER_HTML,
    }
    for name, html_text in surfaces.items():
        v = _NestedColorAudit().audit(html_text).violations
        assert not v, f"{name}: uncolored text inside forced-bg block: {v}"


# ---------------------------------------------------------------------------
# T-BANNER-01 — str.banner.01 is scroll-persistent (M-UX-03 static pin, §22b)
# ---------------------------------------------------------------------------

def test_banner_scroll_persistent_static():
    """M-UX-03 static half: the 0→1 banner wrapper is pinned position:fixed.

    Lesson this pin carries (design states.md §6.9, render session 3 — the
    fourth green-guard/browser-false instance): the previous sticky pin
    verified the rule was APPLIED — the browser itself computed
    position:sticky/top:0px/z-index:100 on this very wrapper — yet the rule
    was not EFFECTIVE, because gradio's own container
    (.gradio-container-6-26-0) computes overflow:hidden while the DOCUMENT is
    the scroller, so sticky's nearest scrollport never scrolls and the banner
    left the viewport (rect top -1255 at scrollY 1500). A static pin verifies
    rule-applied; rule-EFFECTIVE belongs to the browser. F-19 flips off
    manual-FAILED, and P-5 clears, ONLY on render session 4's behavioral
    check — banner rect within the viewport at scrollY 1500 — never on this
    pin's green.

    Mechanism pinned (spec §22b, red-first by construction against the
    sticky build): position:fixed on the component wrapper —
    viewport-anchored regardless of ancestor overflow, §6.9 verified zero
    fixed-position breakers between banner and root; left/right anchoring so
    the fixed box doesn't shrink-to-fit; in-flow height reservation via a
    hidden content-exact duplicate spacer FIRST in the layout (a top:0 fixed
    box covers the top of the viewport, so the reservation must sit at the
    top of the page — and a duplicate, not a magic pixel height, tracks the
    real copy through edits and wrapping) toggled together with the banner;
    and the css actually wired into the served Blocks."""
    src = (REPO / "app.py").read_text(encoding="utf-8")
    assert 'elem_id="pwpm-banner"' in src  # the banner carries the id
    m = re.search(r"#pwpm-banner\s*\{([^}]*)\}", src)
    assert m, "no #pwpm-banner CSS rule in app.py"
    rule = m.group(1)
    assert "position: fixed" in rule and "top: 0" in rule
    assert "left: 0" in rule and "right: 0" in rule  # no shrink-to-fit width
    assert "z-index" in rule  # must layer above the cards it scrolls over
    # Fixed removes the wrapper from flow: height must be reserved in-flow.
    assert 'elem_id="pwpm-banner-spacer"' in src
    assert re.search(r"BANNER_SPACER_HTML\s*=\s*\(\"<div style="
                     r"'visibility:hidden' aria-hidden='true'>\"", src), \
        "spacer must be an invisible in-flow duplicate of the banner"
    assert "f\"{BANNER_HTML}</div>\"" in src  # content-exact, no magic height
    # ...spacer visibility travels WITH the banner on every mode change.
    assert re.search(r"outputs=\[grp_n2n, grp_z2o, banner, banner_spacer",
                     src), "spacer must toggle with the banner"
    # ...and the rule is actually wired into the Blocks the Space serves.
    assert re.search(r"gr\.Blocks\([^)]*css=_CSS", src, re.S)


# ---------------------------------------------------------------------------
# T-STR-01 — count-template singular selection (design §6.8 R-10(i) wiring)
# ---------------------------------------------------------------------------

def test_count_templates_select_singular_variant():
    """R-10(i) wiring pin: a count of exactly 1 renders the ``_one`` catalogue
    ID, never the plural template with 1 interpolated ("1 decisions", the
    session-2 defect class). Also pins R-10(ii): the stale card must state the
    as-built manual-Compare flow, never claim a recompute that never happens —
    copy and behavior state the same thing."""
    pytest.importorskip("gradio")
    from pairwisepm.strings import STRINGS

    mod = _load_app()

    # Catalogue shape: every _one ID is the singular of an existing plural.
    one_ids = [k for k in STRINGS if k.endswith("_one")]
    assert one_ids, "R-10(i) singular variants missing from the catalogue"
    for k in one_ids:
        assert k[:-len("_one")] in STRINGS, f"{k} has no plural counterpart"

    # Selection rule, at the helper every wired call site routes through.
    for base in ("str.partial.verdict_placeholder", "str.m1.progress",
                 "str.log.unsaved_nudge", "str.log.uploaded_ok"):
        assert mod._S_n(base, 1) == STRINGS[base + "_one"]
        assert mod._S_n(base, 2) == STRINGS[base]

    # Render-level: the S2 placeholder pluralizes by count.
    s2_one = mod.render_placeholder(["Reach (Idea B)"])
    assert "1 factor score to go" in s2_one and "scores" not in s2_one
    s2_two = mod.render_placeholder(["Reach (Idea B)", "Effort (Idea A)"])
    assert "2 factor scores to go" in s2_two

    # R-10(ii): stale card states the manual flow, no phantom auto-recompute.
    stale = mod.render_stale()
    assert "Press Compare" in stale and "Recomputing" not in stale


# ---------------------------------------------------------------------------
# T-NEG-07 — no unearned measured-speed claim in shipped copy
# (Spine Success Metrics SC-06; matrix rows F-17 / "under 5 minutes framed as a
#  design target only"). Compliance round 13.
# ---------------------------------------------------------------------------
#
# SC-06 ("a PM completes a full A-vs-B comparison ... in under 5 minutes") is
# the ONLY Spine success metric whose evidence is a human-witnessed timed run
# (M-UX-02). Until that record exists, shipped user-facing copy may state the
# five minutes as a DESIGN TARGET and may not state it as a MEASURED result.
# The Spine's governing refusal is explicit: "A judge that overstates its
# confidence is worse than no judge" — an unearned speed claim is that
# overstatement pointed at the tool's own performance.
#
# This is a TRIPWIRE, and honestly labelled as one: today it passes because
# neither shipped artifact mentions five minutes at all, so the assertion body
# is vacuous. Its whole value is on introduction — the moment anyone writes the
# number into README.md or app.py, the claim must carry target framing or this
# test goes red. Red-first was demonstrated at the predicate level rather than
# by mutating a shipped file (compliance does not edit artifacts it does not
# own): the discriminator was exercised over seven synthetic lines and split
# them correctly — "PairwisePM takes under 5 minutes" RED (bare duration),
# "Users complete a comparison in under five minutes" / "Measured: blank to
# verdict in under 5 minutes" / "Elapsed vs bound 5:00 — verified" RED
# (measured-claim framing), "The design target is ... under 5 minutes" and
# "Under 5 minutes is the design goal, not yet timed" GREEN, and unrelated
# prose not matched at all. That is the honest scope of the demonstration:
# the predicate is shown to discriminate; the file-level assertion is vacuous
# until someone writes the number.

_FIVE_MIN = re.compile(
    r"(under|less than|in)\s+(5|five)\s*(-|\s)?\s*(min|minute|minutes)\b"
    r"|\b5:00\b",
    re.I,
)

# Words that mark the number as a stated goal rather than a measurement.
_TARGET_FRAMING = ("target", "designed", "design goal", "goal", "aim",
                   "intended", "not yet timed")

# Words that would make it an assertion of measured fact.
_CLAIM_FRAMING = ("measured", "verified", "proven", "benchmarked",
                  "on average", "typically takes", "users complete")


def test_no_unearned_five_minute_claim_in_shipped_copy():
    """T-NEG-07: five-minute copy ships as a target, never as a measurement.

    Scope note for future readers: this guards SHIPPED artifacts only
    (README.md, app.py). Leaf working documents are allowed — and required —
    to discuss the pending measurement in full.
    """
    for name in ("README.md", "app.py"):
        text = (REPO / name).read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if not _FIVE_MIN.search(line):
                continue
            low = line.lower()
            assert not any(c in low for c in _CLAIM_FRAMING), (
                f"{name}:{line_no} states the five-minute figure as a measured "
                f"result; SC-06 has no witnessed timed record (M-UX-02 is the "
                f"matrix's last manual-pending row). Reframe as a target or "
                f"land the record first.\n  {line.strip()}"
            )
            assert any(t in low for t in _TARGET_FRAMING), (
                f"{name}:{line_no} states five minutes with no target framing; "
                f"bare duration copy reads as a measurement. Say it is the "
                f"design target, or land M-UX-02 first.\n  {line.strip()}"
            )


# ---------------------------------------------------------------------------
# T-DELIV-01 — the M-UX-03 banner rule is DELIVERED, not merely written
# (spec §25; registered round 14 on engineering's demand)
#
# Every other M-UX-03 instrument on the board is a static assertion over
# app.py's source: T-BANNER-01 pins that `#pwpm-banner { position:fixed ... }`
# is WRITTEN. That is rule-APPLIED. Rule-EFFECTIVE is a separate claim with a
# separate failure mode, and round 14 established that the delivery path is
# thinner than the source pin suggests:
#
#   app.py passes the rule via `gr.Blocks(css=...)`, which gradio 6 DEPRECATED.
#   On the constructed object `demo.css` is None; the rule survives only in the
#   private `demo._deprecated_css`, which `Blocks.launch()` reads at
#   gradio/blocks.py:2785 (`css = css if css is not None else
#   self._deprecated_css`). A gradio major that drops that fallback serves the
#   banner UNSTYLED, with no exception, no warning at the failing site, and
#   every static pin still green — the §22b banner scroll-persistence
#   acceptance silently voided.
#
# Hence the major bound `gradio>=6.0,<7` (requirements.txt, pyproject [app]),
# keyed to README's pinned Space sdk_version. This test is that bound's
# instrument: widening it, or losing the fallback, reads as EVIDENCE LOSS here
# rather than passing as housekeeping.
# ---------------------------------------------------------------------------

_GRADIO_REQ = re.compile(r"^\s*gradio\s*([<>=!,\.\d\s]+)$", re.M)


def _gradio_requirement(text: str) -> str:
    """The version specifier on requirements.txt's bare `gradio` line."""
    m = _GRADIO_REQ.search(text)
    assert m, "no gradio requirement line found in requirements.txt"
    return m.group(1).strip()


def _pyproject_app_gradio(text: str) -> str:
    """The version specifier on pyproject's `app = [... "gradio..." ]` extra."""
    m = re.search(r"""app\s*=\s*\[[^\]]*["']gradio([^"']*)["']""", text, re.S)
    assert m, "no gradio entry found in pyproject.toml's [app] extra"
    return m.group(1).strip()


def _has_major_upper_bound(spec: str) -> bool:
    """True when the specifier caps the major version (e.g. `>=6.0,<7`).

    A bare `>=X` is not a bound. `!=` exclusions are not a bound either: they
    exclude a known-bad release, not the unknown future major that is the
    actual risk here.
    """
    return bool(re.search(r"<=?\s*\d", spec))


def test_gradio_major_is_upper_bounded_in_both_declarations():
    """T-DELIV-01a (static, never skips): the bound exists in both files.

    An open-ended `gradio>=4.0` was the shipped state until round 14. It is not
    a style preference: it is the difference between the banner rule being
    guaranteed to reach the browser and merely happening to.
    """
    declarations = {
        "requirements.txt": _gradio_requirement(
            (REPO / "requirements.txt").read_text(encoding="utf-8")
        ),
        "pyproject.toml [app]": _pyproject_app_gradio(
            (REPO / "pyproject.toml").read_text(encoding="utf-8")
        ),
    }

    for where, spec in declarations.items():
        assert _has_major_upper_bound(spec), (
            f"{where} declares gradio without a major upper bound. The "
            f"M-UX-03 banner rule reaches the browser only through "
            f"gr.Blocks(css=...), which gradio 6 honors via a DEPRECATED "
            f"fallback; an unbounded major may drop it and serve the banner "
            f"unstyled with every static pin green (F-19 / spec §22b). "
            f"Re-bound it, or land a new render session proving delivery on "
            f"the wider range."
        )

    # The declared floor must match the Space image the README pins, or the
    # bound is guarding a runtime the Space does not actually run.
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    sdk = re.search(r"^sdk_version:\s*([\d.]+)", readme, re.M)
    assert sdk, "README has no sdk_version pin"
    assert sdk.group(1).split(".")[0] == "6", (
        f"README pins Space sdk_version {sdk.group(1)}, whose major differs "
        f"from the declared gradio bound (>=6.0,<7)."
    )


def test_banner_css_is_actually_carried_by_the_served_blocks():
    """T-DELIV-01b: the rule is on the object gradio will serve, and the
    fallback that delivers it still exists in the INSTALLED gradio.

    This is the rule-EFFECTIVE half that no source grep can reach. It is the
    automatable analogue of the browser row: not "the CSS is in app.py" but
    "the CSS is in the attribute launch() reads, and launch() still reads it".
    """
    pytest.importorskip("gradio")
    import app

    demo = app.demo
    delivered = getattr(demo, "css", None) or getattr(demo, "_deprecated_css", None)
    assert delivered, (
        "the constructed Blocks carries no CSS at all — neither `css` nor "
        "`_deprecated_css`. The banner rule is written in app.py but is not "
        "on the object that gets served."
    )
    flat = delivered.replace(" ", "")
    assert "#pwpm-banner" in flat and "position:fixed" in flat, (
        "the served Blocks' CSS does not carry the #pwpm-banner position:fixed "
        "rule (F-19 / spec §22b acceptance, browser-confirmed states.md §6.11)."
    )

    # If app.py still uses the deprecated constructor path, the delivery
    # mechanism itself must exist in the installed gradio. When gradio drops
    # `_deprecated_css`, THIS is the line that reds — before a silent unstyled
    # banner reaches a user.
    if getattr(demo, "css", None) is None:
        import gradio

        assert hasattr(demo, "_deprecated_css"), (
            "app.py delivers the banner rule through gr.Blocks(css=...), but "
            "the installed gradio "
            f"{getattr(gradio, '__version__', '?')} has no `_deprecated_css` "
            "fallback. The rule is written and will NOT be served. Move the "
            "CSS to a supported channel and re-run a render session before "
            "shipping."
        )
