"""Rendered text that reaches the user from OUTSIDE the string catalogue.

Registered round 16 on design's §6.15 census (CX-15-01 / CX-15-02), which
found the copy chain certifying one population of three. Every copy-integrity
instrument on this board — T-VEND-01 (files on disk), T-VEND-02 (the bound
module's bytes), T-VEND-05 (the bound module's values), and design's own
mirror checks — is scope-limited to ``leaves/design/strings.py``. Two other
populations render to the browser and no instrument watched either:

* **CX-15-01** — ``configs/*.yaml`` rendered text: ``label``,
  ``factors[].name``/``.scale``/``.rationale``, ``flags[].name``/
  ``.description``, ``evaluative_inputs[].name``/``.note``. The only coverage
  anywhere was ``test_engine.py::test_config_shapes``, which asserts
  ``rationale.strip()`` and ``scale.strip()`` — non-empty, not correct. A
  rationale replaced with "TBD" passed every test in this repository.
  The hazard has a date: the D1-D6 resolution round edits these files, and in
  ``configs/*.yaml`` a policy value and a rendered string are neighbouring
  lines of the same block, so "YAML only, no new surface" and "no rendered
  surface" are different statements.

* **CX-15-02** — literals in ``app.py``, of which four carry a SPINE REFUSAL:
  the evaluative-input labels' ``(not scored)`` marker. The Spine's scope
  boundary reads *"evaluative factors (brand, strategic fit) inside the
  mechanical score — they are captured and displayed as labeled override
  inputs only"*. That refusal is made visible to the user by four
  parentheticals that, until this file, nothing asserted.

These are NEGATIVE tests in the strict sense: each one reds when a refusal
the Spine makes stops being visible, or when text ships in a state that says
nothing. They do not invent a copy authority for either population — that is
design's call, not this seat's — they pin the properties that are checkable
without one, so the open rows (F-32, F-33) rest on an instrument rather than
on prose while their authority question is settled.
"""

import ast
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app.py"
CONFIG_DIR = ROOT / "configs"
# Design's ratified expected-values fixture (round 17, leaves/design/states.md
# §6.17). Created by design as the answer to F-32/F-33's authority question:
# generated from live bytes, ratified by the seat that owns the copy, carrying
# NO policy/numeric field so the D1/D2 resolution round cannot red it.
FIXTURE = ROOT / "leaves" / "design" / "copy-authority.yaml"

# --- T-COPY-03 constants (gate P-15's shape, made structural) ---------------
#
# The clauses this file must contain. Renaming or deleting one is a change to
# an instrument two other seats have retired a check on the strength of; it
# reds here first, in the same change, rather than silently.
_REQUIRED_CLAUSES = {
    "test_config_rendered_text_is_written_not_stubbed",            # T-COPY-01
    "test_config_rendered_text_is_not_a_bare_key_echo",            # T-COPY-01b
    "test_config_rendered_text_matches_design_ratified_fixture",   # T-COPY-02
    "test_app_evaluative_labels_match_design_ratified_fixture",    # T-COPY-02b
    "test_exempted_rendered_text_names_a_live_instrument",         # T-COPY-02c
    "test_every_rendered_config_text_field_has_a_named_authority",  # T-COPY-02d
    "test_banner_exemption_rests_on_an_import_time_assert",        # T-COPY-02e
    "test_evaluative_inputs_are_labelled_not_scored_on_screen",    # T-NEG-08
    "test_evaluative_note_states_the_refusal_in_every_schema",     # T-NEG-08a
    "test_evaluative_inputs_carry_no_weight_by_construction",      # T-NEG-08b
    "test_the_pick_question_asks_for_the_users_own_pick",          # T-NEG-08c
}
# Clauses that must never acquire a skip: their subjects exist in every tree.
_NO_SKIP_FLOOR = {
    "test_every_rendered_config_text_field_has_a_named_authority",
    "test_the_copy_guards_cannot_be_quietly_weakened",
    "test_banner_exemption_rests_on_an_import_time_assert",
}
# The only helpers in this file that may call ``pytest.skip``, each mapped to
# the SUBJECT CONSTANT it must name. A skip is honest only when the thing it
# gates on is the clause's own subject (the round-16 activation defect, spec
# §27a); a fourth entry is a deliberate act that reds here first.
_PERMITTED_SKIP_HELPERS = {
    "_mode_configs": "CONFIG_DIR",
    "_app_evaluative_labels": "APP",
    "_app_widget_labels": "APP",
    "_design_ratified_copy": "FIXTURE",
}

# The literal that makes the log a record of the USER's pick rather than the
# model's — MP-2's separation, rendered. Byte-exact on purpose: "Which do you
# pick?" and "Your pick" both read fine and both drop the word doing the work.
_PICK_QUESTION = "Which do you actually pick?"

# Rendered config text that the design fixture deliberately does NOT ratify,
# mapped to the authority that DOES own it AND to the live clauses that assert
# it. An exemption is only honest if the citation is real, so T-COPY-02c
# CHECKS these citations rather than displaying them: file present, clauses
# present by name, each referencing the named authority key. A key added here
# without a live instrument behind it is the hole this file exists to refuse.
_RATIFIED_ELSEWHERE = {
    "banner": (
        "str.banner.01",
        "tests/test_engine.py",
        (
            "test_zero_to_one_banner_mandatory",   # schema == catalogue string
            "test_banner_attached_and_wording",    # served verdict carries it
        ),
    ),
}

# Dataclass string fields that are MACHINE identifiers, not rendered copy.
# Everything else typed ``str``/``Optional[str]`` on a config dataclass is copy
# a user can read, and T-COPY-02d makes that census self-updating: add a text
# field to a schema type and it must acquire an authority in the same change.
_NON_COPY_STR_FIELDS = {
    # `mode` is the machine key ("one_to_n"); `fingerprint` is F-21's sha256
    # over the parsed YAML — a policy version, computed, never authored, never
    # read by a user. Both are identifiers, which is the only honest ground
    # for an entry here.
    "ModeConfig": {"mode", "fingerprint"},
    "Factor": {"key", "tag", "transform"},
    "Flag": {"key"},
    "EvaluativeInput": {"key"},
}

# Placeholder shapes that mean "nobody has written this yet" but pass every
# non-empty assertion in the suite.
_PLACEHOLDER = re.compile(
    r"(?<![A-Za-z])(TBD|TODO|FIXME|XXX|WIP|lorem ipsum|placeholder|\?\?\?)"
    r"(?![A-Za-z])",
    re.IGNORECASE,
)

# The rendered text fields of a mode schema, by path. Kept explicit rather
# than derived so that ADDING a rendered field to the schema is a deliberate
# act that shows up as a diff here.
_MODE_TEXT_FIELDS = ("label", "banner")
_FACTOR_TEXT_FIELDS = ("name", "scale", "rationale")
_FLAG_TEXT_FIELDS = ("name", "description")
_EVAL_TEXT_FIELDS = ("name", "note")


def _mode_configs():
    from pairwisepm.config import load_mode_config

    if not CONFIG_DIR.is_dir():
        pytest.skip("no repo config authority present")
    paths = sorted(CONFIG_DIR.glob("*.yaml"))
    assert paths, "no mode schemas found in configs/"
    return [(p.name, load_mode_config(p)) for p in paths]


def _rendered_config_text():
    """(schema, dotted-field, value) for every config string that renders."""
    out = []
    for name, cfg in _mode_configs():
        for field in _MODE_TEXT_FIELDS:
            value = getattr(cfg, field)
            # ``banner`` is mandatory in 0→1 and FORBIDDEN in 1→N (T-NEG-04 /
            # T-CFG-01b own that rule). Absent-by-design is not stub copy.
            if field == "banner" and value is None:
                continue
            out.append((name, field, value))
        for f in cfg.factors:
            for field in _FACTOR_TEXT_FIELDS:
                out.append((name, f"factors[{f.key}].{field}", getattr(f, field)))
        for g in cfg.flags:
            for field in _FLAG_TEXT_FIELDS:
                out.append((name, f"flags[{g.key}].{field}", getattr(g, field)))
        for e in cfg.evaluative_inputs:
            for field in _EVAL_TEXT_FIELDS:
                out.append(
                    (name, f"evaluative_inputs[{e.key}].{field}", getattr(e, field))
                )
    return out


# --------------------------------------------------------------------------
# CX-15-01 — configs/*.yaml rendered text
# --------------------------------------------------------------------------


def test_config_rendered_text_is_written_not_stubbed():
    """T-COPY-01 — no rendered config string is a placeholder.

    ``test_config_shapes`` asserts ``.strip()``. This asserts the field says
    something: a factor whose rationale reads "TBD" renders "TBD" into the
    help text a PM uses to decide what a 0-4 means, and shipped green.
    """
    offenders = [
        (schema, field, value)
        for schema, field, value in _rendered_config_text()
        if not str(value).strip() or _PLACEHOLDER.search(str(value))
    ]
    assert not offenders, (
        "rendered text in the mode schemas is empty or still a placeholder — "
        "these strings reach the browser as factor names, scales, help text "
        "and flag descriptions:\n"
        + "\n".join(f"  {s}: {f} = {v!r}" for s, f, v in offenders)
    )


def test_config_rendered_text_is_not_a_bare_key_echo():
    """T-COPY-01b — a rendered name is prose, not the machine key.

    The failure shape this catches is a schema edit that fills a text field
    from the key ("impact_primary_metric") rather than writing the label
    ("Impact on primary metric"). It renders, it is non-empty, and it reads
    to a user as a leaked internal identifier.
    """
    bad = []
    for schema, cfg in _mode_configs():
        for f in cfg.factors:
            if f.name.strip() == f.key or "_" in f.name.strip():
                bad.append((schema, f"factors[{f.key}].name", f.name))
        for e in cfg.evaluative_inputs:
            if e.name.strip() == e.key:
                bad.append((schema, f"evaluative_inputs[{e.key}].name", e.name))
        for g in cfg.flags:
            if g.name.strip() == g.key:
                bad.append((schema, f"flags[{g.key}].name", g.name))
    assert not bad, (
        "a rendered label is the machine key rather than written copy:\n"
        + "\n".join(f"  {s}: {f} = {v!r}" for s, f, v in bad)
    )


# --------------------------------------------------------------------------
# CX-15-01 — the AUTHORITY half, closed round 18 on design's ratified fixture
# --------------------------------------------------------------------------


def _design_ratified_copy():
    """The design-owned expected-values fixture, or an honest skip.

    Subject-named predicate (spec §27a): this pair's subject IS
    ``leaves/design/copy-authority.yaml``, so with no fixture there is nothing
    to diff against and a skip is the truth. It is the WRONG predicate for any
    other clause in this file, and T-COPY-03 asserts none acquires it.

    ANCHOR, stated because a skip and an absence are different observable
    states and only one is ever seen by whoever is standing there: ``FIXTURE``
    is positional — ``ROOT`` derives from this test file's own location. In a
    repo checkout it resolves to the design leaf's ratified bytes. In an
    unpacked sdist it is ABSENT (``[tool.hatch.build.targets.sdist] include``
    ships ``configs`` and ``tests``, not ``leaves``) and this pair SKIPS. In a
    wheel install the whole file is ABSENT, not skipped — the wheel ships
    ``pairwisepm`` plus a force-included ``configs`` and no ``tests`` at all,
    so a reader looking for a skip line there will not find one.

    THE THIRD OBSERVABLE STATE (round 20, engineering's demand, accepted): the
    fixture can be PRESENT AND UNPARSEABLE, and that state stays a RED — it is
    not skippable, because "design's ratified text is unreadable" is not the
    same claim as "this tree has no design leaf". What changes is only the
    sentence the reader gets: pyyaml's bare ``ScannerError`` names a line in
    ``yaml/scanner.py`` and no owner, and gate P-15's own procedure tells
    whoever runs it that a red there means the values round moved rendered
    text — false for this one mode. Engineering OBSERVED it (round 19, mid-save
    of the fixture, their edits confined to two docstrings: 2 failed, green 40
    seconds later) and priced the class without mutating any repo file: of the
    8593 single-byte prefixes of the fixture, 855 fail to parse. So the
    re-raise below says whose file it is and that the first action is to
    re-run, at the point of failure rather than in another leaf's procedure.
    It catches ``UnicodeDecodeError`` alongside ``yaml.YAMLError`` for a reason
    found by demonstrating the red rather than by reasoning about it: a
    truncated save can cut a multi-byte character, and that state raises out of
    ``read_text`` BEFORE pyyaml is ever reached — the same class of accident,
    one exception earlier, and it would otherwise have kept the bare traceback
    this clause exists to replace.
    """
    import yaml

    if not FIXTURE.exists():
        pytest.skip("no design copy authority in this tree (stripped install)")
    try:
        data = yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))
    except (yaml.YAMLError, UnicodeDecodeError) as exc:
        raise AssertionError(
            f"{FIXTURE} is present but does not PARSE, so T-COPY-02/02b have "
            f"no ratified text to diff against.\n\n  {type(exc).__name__}: "
            f"{exc}\n\n"
            "READ THIS BEFORE YOU TOUCH ANYTHING. That file belongs to the "
            "DESIGN leaf (leaves/design/copy-authority.yaml). It is outside "
            "every tree the D1-D6 resolution round writes to, so if you are "
            "mid-write on configs/*.yaml this red is NOT yours and no edit of "
            "yours will clear it. FIRST ACTION: re-run the command. A "
            "half-written save is the observed cause — engineering hit exactly "
            "this in round 19 with their own edits confined to two docstrings, "
            "and the same command 40 seconds later was green.\n"
            "If it persists, it is a real defect in design's fixture and "
            "design owns the fix: tell them, and do not repair the YAML from "
            "this seat. Never delete or blank the file to get a skip — an "
            "absent fixture skips honestly on its own subject, so blanking it "
            "converts a loud red into a quiet green while the config copy "
            "stops being diffed against anything at all."
        ) from exc
    assert isinstance(data, dict) and data.get("configs"), (
        f"{FIXTURE} is present but carries no `configs:` block — an empty "
        "authority is worse than none: it diffs green against anything."
    )
    return data


def test_config_rendered_text_matches_design_ratified_fixture():
    """T-COPY-02 — the config text is the text DESIGN RATIFIED.

    Registered round 18 on design's demand, and it closes the one thing
    T-COPY-01/01b structurally could not assert: those two pin that the text
    exists, says something, and is not a leaked machine key — properties
    checkable WITHOUT an authority. Whether it is the approved text needed a
    ruling, and design ruled it (states.md §6.17, F-32 answer (a)) by creating
    ``leaves/design/copy-authority.yaml`` from live bytes.

    This clause diffs BOTH DIRECTIONS, because a one-way diff is how a copy
    guard goes quietly empty: a field deleted from the fixture would otherwise
    stop being watched, and a field deleted from the schema would otherwise
    pass as "nothing to compare". Every ratified key must exist in the live
    schema and every live value must equal the ratified one.

    It is deliberately POLICY-BLIND. The fixture carries no ``prior_weight``,
    ``sign``, ``seed_mean``, ``seed_std``, ``transform`` or
    ``plausible_range``, so the D1-D6 resolution round — which rewrites exactly
    those — cannot red it. It reds on one event only: a rendered string moving
    without design ratification, which is the per-line notification of design's
    §6.12(b6) converted from a promise five seats accepted into an instrument.
    """
    fixture = _design_ratified_copy()
    ratified = fixture["configs"]
    live = {name: cfg for name, cfg in _mode_configs()}
    live_by_path = {f"configs/{name}": cfg for name, cfg in live.items()}

    unknown = sorted(set(ratified) - set(live_by_path))
    unratified = sorted(set(live_by_path) - set(ratified))
    assert not unknown, (
        f"the ratified fixture names schemas this tree does not have: "
        f"{unknown}. Either a schema was deleted without a design ruling, or "
        "the fixture is stale — both are copy moving without its authority."
    )
    assert not unratified, (
        f"mode schemas render text under NO ratified authority: {unratified}. "
        "A new schema is new copy; it enters leaves/design/copy-authority.yaml "
        "in the same change, or F-32's authority hole reopens one file wider."
    )

    diffs = []
    for path, expected in ratified.items():
        cfg = live_by_path[path]
        if expected.get("label") != cfg.label:
            diffs.append((path, "label", cfg.label, expected.get("label")))
        for group, items, fields in (
            ("factors", cfg.factors, _FACTOR_TEXT_FIELDS),
            ("flags", cfg.flags, _FLAG_TEXT_FIELDS),
            ("evaluative_inputs", cfg.evaluative_inputs,
             ("name", "scale", "note")),
        ):
            exp_group = expected.get(group) or {}
            live_keys = {i.key for i in items}
            for key in sorted(set(exp_group) - live_keys):
                diffs.append((path, f"{group}[{key}]", "<absent>", "<ratified>"))
            for key in sorted(live_keys - set(exp_group)):
                diffs.append((path, f"{group}[{key}]", "<present>", "<unratified>"))
            for item in items:
                exp = exp_group.get(item.key)
                if exp is None:
                    continue
                for field in fields:
                    got = getattr(item, field, None)
                    want = exp.get(field)
                    if got != want:
                        diffs.append(
                            (path, f"{group}[{item.key}].{field}", got, want)
                        )

    assert not diffs, (
        "rendered config text has moved away from design's ratified copy "
        f"authority ({FIXTURE.name}, ratified {fixture.get('ratified')}):\n"
        + "\n".join(
            f"  {p}: {f}\n      live     = {g!r}\n      ratified = {w!r}"
            for p, f, g, w in diffs
        )
        + "\n\nThis is a COPY change, not a YAML-only edit (design's bright "
        "line, states.md §6.12(b6)): re-ratify in leaves/design/copy-authority"
        ".yaml in the same change, and notify design and gtm per line. Never "
        "edit the fixture to match a text edit nobody ratified — that is the "
        "authority following the copy instead of the other way round."
    )


def test_app_evaluative_labels_match_design_ratified_fixture():
    """T-COPY-02b — the four on-screen labels are the ratified four.

    T-NEG-08 censuses the ``(not scored)`` MARKER and pins the count at four.
    That is the Spine refusal's instrument and it is silent about the rest of
    the string: ``A · Strategic fit (not scored)`` could become
    ``A · Strat. fit (not scored)`` with T-NEG-08 green — while gtm's tour
    stop 483 narrates those exact words and design's §6.17 ruling names them
    as the sole on-screen carrier of the excluded-from-score refusal.

    So this clause pins the WORDS against design's ratified set, which also
    makes gtm's byte-identical-move demand on engineering machine-checkable:
    when ENG-COPY-EVALLABELS-01 fires and these four move into the catalogue,
    a move that also "tidies" the phrasing reds HERE, in the push that does it.
    """
    fixture = _design_ratified_copy()
    ratified = fixture.get("app_py_candidates")
    assert ratified, (
        f"{FIXTURE.name} carries no `app_py_candidates` list — the CANDIDATES "
        "half of F-33 has no diff target and this clause would assert nothing."
    )
    labels = _app_evaluative_labels()
    live = [
        lbl for lbl in labels
        if re.search(r"strategic fit|brand fit", lbl, re.IGNORECASE)
    ]
    assert sorted(live) == sorted(ratified), (
        "the evaluative labels rendered by app.py are not design's ratified "
        f"copy:\n  live     = {sorted(live)!r}\n  ratified = "
        f"{sorted(ratified)!r}\nThese four strings are the only place on this "
        "board where the Spine's excluded-from-score refusal reaches a screen "
        "(design §6.17: the schema `note` that reads like it does renders "
        "nowhere). Reword them and gtm's demo narration is false while every "
        "other test stays green."
    )


def test_exempted_rendered_text_names_a_live_instrument():
    """T-COPY-02c — an exemption must cite a guard that exists, not a memory.

    ROUND-18 FINDING, AND A CORRECTION TO THIS SEAT'S FIRST DRAFT OF IT.
    Writing T-COPY-02 exposed a field nobody's census carries: design's §6.15
    census (seven fields), design's round-17 correction (four render), this
    matrix's F-32 row and the ratified fixture's own ``render_map`` all
    enumerate the ``configs/*.yaml`` text population, and **none of them lists
    ``banner``** — the permanent 0→1 claim-limiting banner, which is the single
    most Spine-load-bearing string in either schema (Spine, Out: "no accuracy
    claims in 0→1 mode"). It renders on every 0→1 result and is not in the
    ratified fixture.

    This clause was first drafted to assert the banner against
    ``str.banner.01`` directly, on the premise — written into its docstring —
    that nothing asserted the quotation. **That premise was false, and it was
    false in the direction that flatters a new test.** Demonstrating the red
    before proposing it (engineering's admission standard, which this seat
    registered the same round and therefore owes first) showed the mutation
    reddening THREE clauses, two of them already shipped:
    ``test_zero_to_one_banner_mandatory`` asserts the schema's banner equals
    ``STRINGS["str.banner.01"]``, and ``test_banner_attached_and_wording``
    asserts the served verdict carries that same string. The field is covered;
    only the CENSUS was wrong.

    So the clause became the thing that was actually missing. An exemption from
    the fixture's authority is a claim that some other guard owns the field,
    and until now such claims lived in prose — where they age, and where a
    guard cited by a comment can be deleted in another file with this one
    green. Here the citation is CHECKED: the named file exists, the named
    clauses exist in it by AST, and each references the authority key it is
    cited for. Delete or rename one of the banner's two guards and this reds,
    naming the field that just lost its authority.
    """
    import ast as _ast

    for field, (key, rel, clause_names) in _RATIFIED_ELSEWHERE.items():
        path = ROOT / rel
        assert path.exists(), (
            f"rendered config field {field!r} is exempt from design's ratified "
            f"fixture on the citation {rel}, which is not in this tree. An "
            "exemption whose instrument cannot be found is an unwatched field "
            "with a footnote."
        )
        src = path.read_text(encoding="utf-8")
        found = {
            node.name
            for node in _ast.walk(_ast.parse(src))
            if isinstance(node, _ast.FunctionDef)
        }
        missing = [c for c in clause_names if c not in found]
        assert not missing, (
            f"the guards cited as the authority for rendered field {field!r} "
            f"are gone from {rel}: {missing}. Either restore them, or ratify "
            f"{field!r} in leaves/design/copy-authority.yaml and drop the "
            "exemption — a field may lose an instrument, but not silently."
        )
        for clause in clause_names:
            body = _ast.get_source_segment(
                src,
                next(
                    n for n in _ast.walk(_ast.parse(src))
                    if isinstance(n, _ast.FunctionDef) and n.name == clause
                ),
            ) or ""
            assert key in body, (
                f"{rel}::{clause} is cited as the authority guard for "
                f"{field!r} but no longer references {key!r} — the citation "
                "has drifted off the thing it was supposed to pin."
            )


def test_every_rendered_config_text_field_has_a_named_authority():
    """T-COPY-02d — the census cannot go stale by someone adding a field.

    Every copy census on this board has been a HAND-WRITTEN LIST, and every
    one of them has been wrong at least once inside three rounds (design's
    seven "rendered" fields were four; this file's own list omitted ``banner``
    until round 18). A list that must be maintained by memory is the honor
    system with a table in it.

    So this clause derives the population from the dataclasses instead: every
    ``str``/``Optional[str]`` field on ``ModeConfig``/``Factor``/``Flag``/
    ``EvaluativeInput`` that is not a declared machine identifier is rendered
    copy, and must be covered by either the fixture diff (T-COPY-02, via the
    ``_*_TEXT_FIELDS`` constants) or a NAMED alternative authority
    (``_RATIFIED_ELSEWHERE``, asserted by T-COPY-02c). Add a text field to a
    schema type and this reds in the same change, naming the field.

    Never skips: its subject is the type declarations, which exist wherever
    the package is importable.
    """
    from pairwisepm.config import EvaluativeInput, Factor, Flag, ModeConfig

    covered = {
        "ModeConfig": set(_MODE_TEXT_FIELDS),
        "Factor": set(_FACTOR_TEXT_FIELDS),
        "Flag": set(_FLAG_TEXT_FIELDS),
        "EvaluativeInput": set(_EVAL_TEXT_FIELDS) | {"scale"},
    }
    unowned = []
    for cls in (ModeConfig, Factor, Flag, EvaluativeInput):
        name = cls.__name__
        for field, spec in cls.__dataclass_fields__.items():
            if str(spec.type) not in ("str", "Optional[str]"):
                continue
            if field in _NON_COPY_STR_FIELDS.get(name, set()):
                continue
            if field in covered[name] or field in _RATIFIED_ELSEWHERE:
                continue
            unowned.append(f"{name}.{field}")

    assert not unowned, (
        "a rendered text field on a config schema type has NO copy authority: "
        f"{sorted(unowned)}. Every string a user can read is either ratified "
        "in leaves/design/copy-authority.yaml (add it to the fixture and to "
        "this file's _*_TEXT_FIELDS census, same change) or owned by a named "
        "alternative authority with its own instrument (_RATIFIED_ELSEWHERE, "
        "e.g. the banner's str.banner.01, asserted by T-COPY-02c). Adding the "
        "field to _NON_COPY_STR_FIELDS is only honest if it is a machine "
        "identifier no user reads."
    )


def test_banner_exemption_rests_on_an_import_time_assert():
    """T-COPY-02e — the banner's strongest guard, pinned where it lives.

    ROUND 19, closing the loop this seat opened in round 18 and design ruled on
    in §6.19. The census gap is now answered from both ends: design added a
    ``banner`` row to ``render_map`` and ruled it **exempt from the fixture by
    authority, not by omission** — the catalogue's ``str.banner.01`` owns those
    bytes, ``configs/zero_to_one.yaml`` carries a replica, and the two are
    asserted equal **at import** by ``app.py``::

        assert Z2O.banner == S["str.banner.01"], "0→1 banner drifted from design copy"

    Architecture's demand this round is that the banner's row NAME that assert
    as its actual instrument, on the ground that it is stronger than any diff
    written here: it runs at import rather than under pytest, so it cannot
    acquire a skip, cannot be deselected by ``-k``, and reds as *the app does
    not start* rather than as a line in a report. That is right, and it is
    exactly why it needed a guard of its own. **An instrument nothing watches is
    one keystroke from being an instrument nothing has** — and this one is a
    bare ``assert`` in a UI file, the single easiest line in this repository to
    delete while chasing an unrelated import error, with every test in the suite
    green afterwards (demonstrated: removing it reds only this clause).

    So the doctrine of T-COPY-02c — *an exemption must cite a guard that still
    exists* — is extended one rung, to the guard that is not a test. The check
    is structural: a MODULE-LEVEL assert (not one nested in a function, where it
    would fire on nobody's launch) comparing the served banner against the
    catalogue key. Never skips: its subject is ``app.py``, which ships wherever
    this file does.

    What this clause does NOT claim, said plainly because the banner has cost
    this seat one false premise already: it does not assert the banner's WORDS
    (``test_zero_to_one_banner_mandatory`` and ``test_banner_attached_and_
    wording`` do, and T-COPY-02c checks that those two still exist), and it does
    not assert the banner reaches the screen (F-19/P-5's browser record and
    T-BANNER-01 own that). It asserts that the cross-reference which makes the
    config replica safe is still in the file design's fixture says it is in.
    """
    assert APP.exists(), (
        "app.py is absent from a tree carrying this file — the banner's "
        "import-time cross-reference cannot be checked. This clause never "
        "skips: its subject is the shipped app."
    )
    tree = ast.parse(APP.read_text(encoding="utf-8"))
    module_level = [n for n in tree.body if isinstance(n, ast.Assert)]
    cross_refs = [
        n for n in module_level
        if "banner" in ast.unparse(n.test)
        and "str.banner.01" in ast.unparse(n.test)
    ]
    assert cross_refs, (
        "app.py no longer asserts, AT IMPORT, that the 0→1 config banner "
        "equals the catalogue's 'str.banner.01'. That assert is the banner's "
        "primary authority: design's leaves/design/copy-authority.yaml "
        "deliberately does NOT ratify the banner's bytes (§6.19) and names "
        "this line as the guard that makes the exemption honest, so deleting "
        "it leaves the most Spine-load-bearing string in either schema — the "
        "permanent 0→1 'It does not predict product-market fit' box, the "
        "on-screen carrier of the Spine's 'no accuracy claims in 0→1 mode' — "
        "governed by a fixture row pointing at nothing. If the assert must "
        "move, ratify the banner in the fixture in the SAME change and drop "
        "the exemption; never one without the other."
    )
    nested = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Assert)
        and n not in module_level
        and "str.banner.01" in ast.unparse(n.test)
    ]
    assert not nested or cross_refs, (
        "the banner cross-reference has moved inside a function or handler. "
        "Its whole strength is that it fires at IMPORT, before first paint, on "
        "every launch — a copy of it behind a call site is a check that runs "
        "when someone happens to reach that code path."
    )


# --------------------------------------------------------------------------
# CX-15-02 — the Spine refusal that renders from app.py, not the catalogue
# --------------------------------------------------------------------------


def _app_evaluative_labels():
    """Every ``gr.Textbox(label=<literal>)`` in the evaluative panel.

    Read by AST rather than by regex so a moved line, a reflowed call or a
    changed line number cannot silently empty the census.
    """
    if not APP.exists():
        pytest.skip("app.py not present in this tree")
    tree = ast.parse(APP.read_text(encoding="utf-8"))
    labels = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "Textbox"):
            continue
        for kw in node.keywords:
            if kw.arg == "label" and isinstance(kw.value, ast.Constant):
                if isinstance(kw.value.value, str):
                    labels.append(kw.value.value)
    return labels


def test_evaluative_inputs_are_labelled_not_scored_on_screen():
    """T-NEG-08 — the Spine's excluded-from-score refusal is VISIBLE.

    Spine, Scope Boundaries (Out): evaluative factors are "captured and
    displayed as labeled override inputs only". The engine honors that
    structurally (T-NEG-08b below), but a user cannot read a dataclass. What
    tells them is the ``(not scored)`` marker on each of the four evaluative
    text boxes — the exact beat a presenter points at when they say the model
    refuses to score strategic fit.

    Delete the parenthetical and every other test in this repository stays
    green while the screen now offers two unmarked judgment fields beside the
    scored ones — the tool implying it weighed something it refused to weigh,
    which is the Spine's forbidden overstatement arriving as an omission.

    **THIS CLAUSE HAS A NAMED DEPENDENT — READ BEFORE WEAKENING IT** (round 19,
    gtm's demand, accepted whole and written here at the point of use rather
    than promised in a packet, because a per-line notification is honored by
    whoever remembers and a docstring is read by whoever has the file open):
    **gtm DELETED its eyes-on pre-flight check on these four labels in round 17
    on the strength of this AST census** (``leaves/gtm/launch-copy.md`` item
    11). Weakening this clause to a regex, making it skippable, or removing it
    silently returns the on-screen proof of the Spine's excluded-from-score
    refusal to ZERO instruments — no test, and no presenter looking either.
    That trade was correct: an executed census beats a human glance. It is also
    a dependency, and the seat that took the benefit is not the seat that would
    notice the loss. T-COPY-03 enforces the same four properties structurally;
    this paragraph is here for the reader who is about to edit the clause
    rather than the report of the test that stopped them.
    """
    labels = _app_evaluative_labels()
    evaluative = [
        lbl for lbl in labels
        if re.search(r"strategic fit|brand fit", lbl, re.IGNORECASE)
    ]
    assert len(evaluative) == 4, (
        "expected four evaluative input labels (A/B x strategic/brand fit) in "
        f"app.py; found {len(evaluative)}: {evaluative!r}. If the panel was "
        "restructured, this census must be updated deliberately — it carries "
        "a Spine refusal."
    )
    unmarked = [lbl for lbl in evaluative if "(not scored)" not in lbl]
    assert not unmarked, (
        "an evaluative input renders WITHOUT the '(not scored)' marker: "
        f"{unmarked!r}. The Spine captures brand and strategic fit as labeled "
        "override inputs only; the label is where that refusal reaches the "
        "user, and it is not in the string catalogue, so nothing else guards "
        "it."
    )


def test_evaluative_note_states_the_refusal_in_every_schema():
    """T-NEG-08a — the same refusal, IN THE SCHEMA. Not on the screen.

    SCOPE WORD, round 18 (design's demand, accepted — and it is a correction to
    what this clause's own docstring implied). This asserts the refusal in a
    config field with **no call site**: design went looking round 17 and found
    that ``evaluative_inputs[].name``/``.note`` render nowhere — the checkbox
    label is ``S['str.factor.ceiling_label']``, the ceiling routing copy is the
    engine's pinned ``PINNED_CEILING``, and the four ``(not scored)``
    parentheticals in ``app.py`` are the sole ON-SCREEN carrier of this
    refusal. So the division is:

    * **T-NEG-08 speaks about the SCREEN** — four AST-censused ``app.py``
      labels; that is the clause a reader may cite for "the user is told".
    * **T-NEG-08a speaks about the SCHEMA** — the authoritative record of what
      an evaluative input IS, read by the log record and any downstream
      consumer of the config, and the text that would carry the refusal the
      day someone wires a call site. It is a true assertion about a field a
      user cannot currently see, and citing it for on-screen visibility is
      exactly the scope-wider-than-claim error this file was written against.

    Both must say it, in both modes; neither substitutes for the other.
    """
    missing = []
    for schema, cfg in _mode_configs():
        assert cfg.evaluative_inputs, f"{schema}: no evaluative_inputs declared"
        for e in cfg.evaluative_inputs:
            if "not scored" not in e.note.lower():
                missing.append((schema, e.key, e.note))
    assert not missing, (
        "an evaluative input's note no longer states that it is excluded from "
        "the mechanical score:\n"
        + "\n".join(f"  {s}: {k} note = {n!r}" for s, k, n in missing)
    )


def test_evaluative_inputs_carry_no_weight_by_construction():
    """T-NEG-08b — the refusal is structural, not merely stated.

    ``EvaluativeInput`` has no ``prior_weight``, ``sign`` or ``tag`` field, so
    there is no way to give one a weight without changing the dataclass. This
    pins that absence: a schema edit that adds ``prior_weight: 0.1`` under
    ``evaluative_inputs`` must not quietly become scored weight.
    """
    from pairwisepm.config import EvaluativeInput

    for forbidden in ("prior_weight", "sign", "tag", "seed_mean", "seed_std"):
        assert forbidden not in EvaluativeInput.__dataclass_fields__, (
            f"EvaluativeInput gained a {forbidden!r} field — evaluative "
            "inputs are captured and displayed only (Spine scope boundary); "
            "a weight field is the door through which they enter the score."
        )

    for schema, cfg in _mode_configs():
        keys = {e.key for e in cfg.evaluative_inputs}
        overlap = keys & set(cfg.factor_keys)
        assert not overlap, (
            f"{schema}: {sorted(overlap)} appears BOTH as a scored factor and "
            "as an evaluative input — the same judgment would be both refused "
            "and weighed."
        )


def _app_widget_labels():
    """Every ``gr.<Widget>(label=<literal>)`` on app.py's construction surface.

    Deliberately WIDER than ``_app_evaluative_labels`` (which reads Textbox
    labels only) and deliberately a separate helper: T-NEG-08's census is
    pinned at four by T-COPY-03, and widening it in place would also widen
    engineering's ENG-COPY-EVALLABELS-01 trigger, which they accepted on the
    strength of its boundedness. Same subject-named skip predicate (``APP``),
    same AST read, so a reflowed call cannot empty it.
    """
    if not APP.exists():
        pytest.skip("app.py not present in this tree")
    tree = ast.parse(APP.read_text(encoding="utf-8"))
    labels = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute)
                and isinstance(func.value, ast.Name)
                and func.value.id == "gr"):
            continue
        for kw in node.keywords:
            if kw.arg == "label" and isinstance(kw.value, ast.Constant):
                if isinstance(kw.value.value, str):
                    labels.append((func.attr, kw.value.value))
    return labels


def test_the_pick_question_asks_for_the_users_own_pick():
    """T-NEG-08c — the log records the USER's pick, and the screen says so.

    Registered round 20 on design's demand (states.md §6.19(iii)), as its OWN
    clause rather than as a fifth member of T-NEG-08's set — design's condition
    and this seat's agreement: T-NEG-08's ``== 4`` count pin is what makes a
    restructured panel rendering ZERO evaluative labels fail, and widening that
    census to five would silently widen engineering's bounded
    ENG-COPY-EVALLABELS-01 trigger, which §6.18 refused to grow for thirteen
    strings.

    The subject is one literal on the decision panel's radio:
    ``"Which do you actually pick?"`` (app.py, currently line 947 — read by
    AST, so the number is a courtesy, not the anchor). It carries MP-2's
    separation on screen: the verdict card states what the MODEL computes, and
    this question asks what the PERSON does, which is what makes the logged
    ``pick`` a record of a human judgment rather than an acceptance of the
    machine's. Drop the word ``actually`` — "Which do you pick?", "Your pick" —
    and the screen stops distinguishing the two, while every other test in this
    repository stays green.

    WHY IT NEEDED A CLAUSE AT ALL, in the honest order: design's §6.17(ii)
    recorded it as "covered in the interim by the eyes-on five", gtm correctly
    RETIRED that pre-flight ritual in round 17 on the strength of executed
    censuses, and design struck their own cover sentence in place when they
    found it named nothing that runs. Between those two rounds the literal had
    ZERO instruments. Design declined gtm's offer to reinstate one eyes-on line
    to cover it — trading an instrument for a ritual — and filed here instead.
    Byte-exact and count-pinned, for the reason a marker census is: a clause
    that merely asserts "some radio has a label" is green on the rewording it
    exists to catch.
    """
    labels = _app_widget_labels()
    matches = [(widget, lbl) for widget, lbl in labels if lbl == _PICK_QUESTION]
    assert len(matches) == 1, (
        f"expected exactly one gr.* widget on app.py's construction surface "
        f"labelled {_PICK_QUESTION!r}; found {len(matches)}: {matches!r}.\n"
        "Near misses present on the surface, for whoever is reading this at "
        "the wrong hour: "
        + repr(sorted(
            lbl for _, lbl in labels
            if lbl != _PICK_QUESTION and "pick" in lbl.lower()
        ))
        + ".\nThis is the wording that makes the decision log a record of the "
        "USER's pick rather than an acceptance of the model's (MP-2's "
        "separation, design §6.19(iii)). A reword is a COPY change: it needs "
        "design's mint and the per-line notification, not a tidy-up in a "
        "layout push. If the panel was genuinely restructured, update this "
        "clause deliberately, in the same change, and say so in the matrix."
    )
    widget, _ = matches[0]
    assert widget == "Radio", (
        f"the pick question is now rendered by gr.{widget} rather than a "
        "Radio. The two-choice radio is what makes the recorded pick one of "
        "exactly the two ideas compared (Spine: v1 is strictly A-vs-B); a "
        "free-text or dropdown carrier is a product change, not a layout one."
    )


# --------------------------------------------------------------------------
# The guards' own shape — gate P-15's floor, and gtm's deletion trigger
# --------------------------------------------------------------------------


def test_the_copy_guards_cannot_be_quietly_weakened():
    """T-COPY-03 — this file cannot be softened without reddening first.

    Registered round 18 on gtm's demand, and executed as an instrument rather
    than as the per-line notification they asked for, for the reason their own
    packet gives: on the strength of T-NEG-08 gtm DELETED an eyes-on check from
    the witness pre-flight, and design's §6.17 ruling records those four
    labels as the sole on-screen carrier of a Spine refusal. A promise to
    notify is honored by whoever remembers; a promise ABOUT AN INSTRUMENT that
    two other seats have retired checks against should not rest on memory.
    (The notification is still owed and is registered in the matrix — this
    clause is what makes it impossible to owe it silently.)

    Four properties, all read off this file's own AST so a moved line, a
    reflowed call or a rename cannot empty the check:

    1. Every required clause is present by NAME. Deleting or renaming
       T-NEG-08 — or T-COPY-02, which pins the ratified wording — reds here in
       the same change, naming what went missing.
    2. T-NEG-08 still censuses by AST and still pins the count at four. The
       specific weakenings gtm named are a regex form (which a reflowed call
       empties silently) and dropping the count pin (which turns "four labels
       carry the marker" into "the labels that exist carry it" — vacuously
       true of zero labels).
    3. No clause carries a skip marker, and every ``pytest.skip`` in this file
       lives in a sanctioned helper that NAMES ITS OWN SUBJECT — the round-16
       activation defect (spec §27a) applied prospectively to the newer file
       rather than only retrospectively to the older one.
    4. A counted floor of clauses that never skip, so gate P-15 cannot go
       green on a run in which nothing asserted (T-VEND-07's finding,
       generalized: pytest exits 0 on an all-skipped file).

    A guard is not weakened for convenience. If a weakening is genuinely
    right, it is made here first, in the same change, in writing.
    """
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)

    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    clauses = {n: f for n, f in functions.items() if n.startswith("test_")}
    helpers = {n for n in functions if n.startswith("_")}

    missing = sorted(_REQUIRED_CLAUSES - set(clauses))
    assert not missing, (
        "copy-surface clauses have gone missing from this file: "
        + ", ".join(missing)
        + " — gate P-15 cites this file by name, gtm deleted a presenter "
        "eyes-on check on the strength of T-NEG-08, and design's F-32/F-33 "
        "ruling rests on T-COPY-02's diff against their ratified fixture. A "
        "clause here is removed or renamed only deliberately: update "
        "_REQUIRED_CLAUSES in the same change and say so in the matrix row."
    )

    # (2) T-NEG-08's census must stay an AST census pinned at four.
    census = functions["_app_evaluative_labels"]
    parses = [
        sub for sub in ast.walk(census)
        if isinstance(sub, ast.Call)
        and isinstance(sub.func, ast.Attribute)
        and sub.func.attr == "parse"
        and isinstance(sub.func.value, ast.Name)
        and sub.func.value.id == "ast"
    ]
    assert parses, (
        "_app_evaluative_labels no longer parses app.py's AST. A regex over "
        "the source reads identically in a green suite and empties silently "
        "the first time the call is reflowed across lines — which app.py's "
        "evaluative panel has done three times in three rounds."
    )
    neg08 = clauses["test_evaluative_inputs_are_labelled_not_scored_on_screen"]
    assert any(
        isinstance(sub, ast.Constant) and sub.value == 4
        for sub in ast.walk(neg08)
    ), (
        "T-NEG-08 no longer pins the label count at four. Without the count "
        "pin, a restructured panel that renders ZERO evaluative labels passes "
        "vacuously, and the Spine's excluded-from-score refusal is unwatched "
        "on screen with the suite green."
    )
    assert any(
        isinstance(sub, ast.Call)
        and isinstance(sub.func, ast.Name)
        and sub.func.id == "_app_evaluative_labels"
        for sub in ast.walk(neg08)
    ), "T-NEG-08 no longer reads the labels through the AST census helper."

    # (3) Skips: markers forbidden; pytest.skip only in subject-named helpers.
    for name, node in clauses.items():
        markers = [
            ast.unparse(dec) for dec in node.decorator_list
            if "skip" in ast.unparse(dec)
        ]
        assert not markers, (
            f"{name} carries a skip marker ({markers[0]}). A clause in this "
            "file is skipped only through a helper that gates on the clause's "
            "own subject; a decorator hides the reason from the report."
        )

    for name in sorted(helpers):
        node = functions[name]
        skips = [
            sub for sub in ast.walk(node)
            if isinstance(sub, ast.Call)
            and isinstance(sub.func, ast.Attribute)
            and sub.func.attr == "skip"
            and isinstance(sub.func.value, ast.Name)
            and sub.func.value.id == "pytest"
        ]
        if not skips:
            continue
        assert name in _PERMITTED_SKIP_HELPERS, (
            f"helper {name} skips on a predicate this file does not sanction. "
            "Every skip here must gate on the SUBJECT of the clauses it "
            "serves — CONFIG_DIR, app.py, or the design fixture. Round 16's "
            "defect was a guard whose ACTIVATION was narrower than its "
            "SUBJECT, and it reads identically to a passing suite. Add the "
            "helper to _PERMITTED_SKIP_HELPERS only after answering, in "
            "writing, what subject it names."
        )
        subject = _PERMITTED_SKIP_HELPERS[name]
        referenced = {
            sub.id for sub in ast.walk(node) if isinstance(sub, ast.Name)
        }
        assert subject in referenced, (
            f"helper {name} skips without referencing {subject}, the subject "
            "this file sanctions it to gate on. A skip predicate that has "
            "drifted off its own subject is the round-16 defect returning."
        )

    # (4) The counted floor.
    unskippable = []
    for name, node in clauses.items():
        called = {
            sub.func.id for sub in ast.walk(node)
            if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name)
        }
        if not (called & set(_PERMITTED_SKIP_HELPERS)):
            unskippable.append(name)
    floor_missing = sorted(_NO_SKIP_FLOOR - set(unskippable))
    assert not floor_missing, (
        "clauses that must assert in EVERY tree have acquired a skip path: "
        + ", ".join(floor_missing)
        + ". Gate P-15 runs in the D1-D6 resolution round, and a green there "
        "must mean assertions executed."
    )
    assert len(unskippable) >= 2, (
        f"fewer than two clauses in this file assert unconditionally "
        f"(unskippable: {sorted(unskippable)}). pytest exits 0 on an "
        "all-skipped file, so gate P-15 would be green on a run that "
        "measured nothing."
    )
