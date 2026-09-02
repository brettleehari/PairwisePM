"""T-VEND-01 — one-way vendoring boundary (architecture.md §4.2).

``leaves/design/strings.py`` is the single copy authority; the package copy
``pairwisepm/strings.py`` is a verbatim mirror. This test makes that boundary
self-enforcing: any drift — either direction — fails the suite, so copy
authorship can never silently migrate into the package.

Skipped when the design leaf's file is absent (a stripped deployment ships
only the package); the vendored module is then the sole copy by construction.

T-VEND-02/T-VEND-03 close the gap architecture reported in round 13 (A-13-01):
T-VEND-01 compares two paths it builds itself from ``__file__`` and never
imports the package, so it stayed green while an off-root interpreter bound a
third, undeclared copy — a non-editable snapshot in site-packages that had
drifted (no ``str.empty.example_cta``, which app.py reads at layout
construction). Comparing files on disk proves nothing about the module python
actually binds; these two assert on the IMPORTED module and on the config
directory the engine actually loads.
"""

import ast
import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DESIGN_COPY = ROOT / "leaves" / "design" / "strings.py"
VENDORED_COPY = ROOT / "pairwisepm" / "strings.py"

# --- T-VEND-07 constants (gate P-14's floor, made structural) ---------------
#
# Clauses that must NEVER acquire a skip predicate. These two are what make
# `pytest tests/test_vendoring.py` incapable of returning an all-skipped
# green: whatever tree it runs in, these assert.
_NO_SKIP_FLOOR = {
    "test_exactly_one_importable_copy_of_the_package",  # T-VEND-04 (count)
    "test_bound_module_carries_the_r10_corrected_copy",  # T-VEND-05 (values)
}
# The only predicates any clause in this file may skip on. Each names its own
# subject; adding a third is a deliberate act that must red here first.
_PERMITTED_SKIP_PREDICATES = {"_in_repo_checkout", "_repo_config_authority"}


def _in_repo_checkout() -> bool:
    """True when the DESIGN AUTHORITY FILE is present.

    This is the correct precondition for T-VEND-01/02 and for those two only:
    their subject IS ``leaves/design/strings.py``, so with no authority file
    there is nothing to compare against and a skip is honest.

    It is the WRONG precondition for T-VEND-03/04/06, and round 16 removes it
    from them (engineering's demand, reproduced from this seat). Those three
    measure the config directory the engine loads, the number of importable
    package copies, and the freshness of a duplicate schema — none of which
    has anything to do with the design leaf. Worse, the gate was narrowest
    exactly where the hazard is widest: ``pyproject.toml``'s
    ``[tool.hatch.build.targets.sdist] include`` ships ``tests`` WITHOUT
    ``leaves``, so in an installed/sdist tree the guards are present and inert
    — four skips, zero assertions — while a repo checkout, the one place they
    did run, is the case where ``sys.path[0]`` already wins.

    Registered as the mirror of A-13-01: that was a guard whose SCOPE was
    narrower than its claim; this was a guard whose ACTIVATION was narrower
    than its subject. Both read identically in a green suite.
    """
    return DESIGN_COPY.exists()


def _repo_config_authority() -> bool:
    """True when this tree carries the config authority the guards compare to.

    The correct precondition for T-VEND-03/06: it names their own subject
    (``<root>/configs``) rather than another leaf's file.

    ROUND-18 ANCHOR NOTE (architecture's demand): this predicate names the
    right KIND of thing, and the thing it resolves to is POSITIONAL —
    ``ROOT`` derives from this test file's own location, so "the config
    authority" means *whichever ``configs/`` sits beside ``tests/``*. That is
    the repo authority in a repo checkout and merely the local copy anywhere
    else. See T-VEND-06's ANCHOR paragraph for what that does to the guard's
    claim in each of the three trees this project ships as.
    """
    return (ROOT / "configs").is_dir()


def test_vendored_strings_byte_identical_to_design_copy():
    if not _in_repo_checkout():
        pytest.skip("stripped deployment: design leaf not present")
    assert VENDORED_COPY.read_bytes() == DESIGN_COPY.read_bytes(), (
        "pairwisepm/strings.py has drifted from leaves/design/strings.py — "
        "the design leaf's file is the copy authority (architecture.md §4.2); "
        "re-vendor the package copy verbatim, never edit it in place."
    )


def test_imported_strings_module_is_the_in_repo_copy():
    """T-VEND-02 — the bound module, not a path this test built itself.

    Exactly one copy of the package may be importable from a repo checkout.
    A second, non-editable install shadows the source tree depending on nothing
    but the interpreter's working directory, and its bytes are frozen at
    install time.
    """
    if not _in_repo_checkout():
        pytest.skip("stripped deployment: design leaf not present")
    mod = importlib.import_module("pairwisepm.strings")
    bound = Path(mod.__file__).resolve()
    assert bound == VENDORED_COPY.resolve(), (
        f"`import pairwisepm.strings` bound {bound}, not {VENDORED_COPY} — a "
        "second copy of the package is installed over the repo checkout. Make "
        "the install editable (`pip install -e .`) or remove it; which copy "
        "binds must not depend on the working directory."
    )
    assert bound.read_bytes() == DESIGN_COPY.read_bytes(), (
        "the module python actually binds has drifted from the design copy "
        "authority (architecture.md §4.2)."
    )


def test_loaded_config_dir_is_the_in_repo_copy():
    """T-VEND-03 — same invariant for the config authority.

    The wheel force-includes ``configs/`` at the site-packages root, so EVERY
    install of this project — **editable included** — leaves a second copy of
    the mode schemas (see T-VEND-06's docstring for the round-17 correction
    and the dist-info evidence). D1/D2 resolve into configs/ as YAML values;
    a shadowed copy would serve stale prior weights with no error and no
    failing engine test.

    RESOLUTION invariant, not a count (architecture's round-16 census
    asymmetry, accepted): a second ``configs/`` tree is PERMITTED BY DESIGN —
    the wheel's force-include is what makes ``default_config_dir()`` resolve
    identically from a clone and from a non-editable install. What this pins
    is which directory the engine LOADS, never how many exist.

    Round 16: the design-leaf skip is REMOVED. This guard's subject is
    ``<root>/configs``; it now skips only when that authority is absent.
    """
    if not _repo_config_authority():
        pytest.skip("no repo config authority present to resolve against")
    from pairwisepm.config import default_config_dir

    loaded = default_config_dir().resolve()
    assert loaded == (ROOT / "configs").resolve(), (
        f"the engine loads mode schemas from {loaded}, not {ROOT / 'configs'} "
        "— a second copy of configs/ is shadowing the repo checkout; edits to "
        "the repo's YAML (D1/D2 priors) would not reach the engine."
    )


def test_bound_module_carries_the_r10_corrected_copy():
    """T-VEND-05 — the VALUES the bound module serves, with no skip.

    Registered round 15 on design's CX-14-01 demand. T-VEND-02 asserts the
    bound module's bytes equal the design authority's, which is strictly
    stronger — but only in a repo checkout: it SKIPS when the design leaf is
    absent, which is exactly the stripped deployment a user installs. So no
    instrument on this board asserts what copy reaches a user of a shipped
    install; the round-14 defect (a bindable module still carrying the
    pre-R-10 ``"Recomputing…"`` tail, and missing ``str.empty.example_cta``)
    would have been invisible there.

    This clause never skips. It is value-level, not file-level, and it pins
    the two R-10 facts by name:

    * ``str.empty.example_cta`` EXISTS — ``app.py`` reads it at layout
      construction; its absence is a KeyError before first paint.
    * ``str.verdict.stale`` states the as-built manual-Compare flow and does
      NOT claim an automatic recompute (F-30 / design §6.8 R-10(ii)). A stale
      card promising "Recomputing…" is the Spine's forbidden confidence
      overstatement — a judge asserting work it is not doing.
    """
    mod = importlib.import_module("pairwisepm.strings")
    strings = mod.STRINGS

    assert "str.empty.example_cta" in strings, (
        "the bound copy of the string catalogue is missing "
        "'str.empty.example_cta', which app.py reads at layout construction: "
        f"this interpreter bound {mod.__file__}, a pre-R-10 copy."
    )

    stale = strings["str.verdict.stale"]
    assert stale.rstrip().endswith("Press Compare to recompute."), (
        "the bound copy's stale-verdict line does not state the as-built "
        f"manual-Compare flow (F-30 / R-10(ii)); got: {stale!r}"
    )
    assert "Recomputing" not in stale, (
        "the bound copy's stale-verdict line claims an automatic recompute "
        "the build does not perform — the pre-R-10 tail, live in served copy."
    )


def test_second_config_copy_if_present_is_not_stale():
    """T-VEND-06 — a duplicate of the POLICY VALUES may exist, but not drift.

    ROUND-17 FACTUAL CORRECTION (architecture's demand, re-derived from this
    seat before accepting it). Rounds 15 and 16 said this second copy is left
    by "any NON-EDITABLE install". That is false, and it understated the
    guard. Hatchling's editable target derives from the wheel target and
    inherits ``[tool.hatch.build.targets.wheel.force-include]``, so **every
    install of this project creates it, editable included.** Verified here,
    not argued: ``.venv/lib/python3.11/site-packages/pairwisepm-0.1.0
    .dist-info/direct_url.json`` reads ``{"dir_info": {"editable": true}}``;
    that same dist-info's RECORD carries ``configs/one_to_n.yaml``
    (sha256 ``RL_7s3pRSc-nxwTQyuK3HC2tbeRatvMBW2igPKPmTk8``, 3894 B) and
    ``configs/zero_to_one.yaml`` (``ALjXJGEI5gzIuZthbIbfhVKmpQ6nKf4y-uBFj0B_aRQ``,
    4149 B), digests recomputed from the repo's own ``configs/`` and matching;
    ``site-packages/pairwisepm/`` does NOT exist (only the ``.pth``), so this
    is an editable install that nevertheless froze the schemas. Two
    ``configs/`` trees are on ``sys.path`` in this very pytest session.

    The consequence is therefore stronger than the one first written for this
    guard: it does not wait for a hypothetical future reinstall. **It reds on
    the NEXT suite run after the D1/D2 write, on the install this repo has
    today.** That red is the guard working, not a broken venv, and the remedy
    is refresh-or-remove (``pip install -e .`` again, or
    ``pip uninstall pairwisepm``) — never a hand-edit of the site-packages
    copy, and never deleting the ``force-include``, which is the only reason
    ``pip install pairwisepm`` finds its schemas at all.

    Today the duplicate is inert (the editable install resolves
    ``default_config_dir()`` in-repo, per T-VEND-03) and byte-identical — but
    it is a snapshot frozen at install time, and D1/D2 resolve into these
    files as prior weights.

    The failure this guards is the quiet one: repo YAML is edited with a
    resolution_source per value, every test stays green, and a later
    non-editable reinstall — or any consumer reading the site-packages copy —
    serves the OLD weights with no error, producing a plausible wrong verdict
    rather than a crash.

    So the invariant is not "no second copy" (packaging needs it) but "no
    STALE second copy": if one exists, it must match the repo authority
    byte-for-byte. Remedy on red: reinstall (or ``pip uninstall pairwisepm``),
    never edit the copy.

    Round 16: the design-leaf skip is REMOVED (engineering's demand). This
    guard's subject is ``<root>/configs``; it now skips only when that
    authority is absent. Round 16's stated REASON for the fix — "the frozen
    duplicate is created by the very install where ``leaves/`` is absent" —
    is corrected above: the duplicate exists here, in a checkout, under an
    editable install. The fix was right for a wider reason than it was given.

    ROUND-18 ANCHOR (architecture's demand, accepted whole and verified from
    this seat against ``pyproject.toml`` and the dist-info RECORD before being
    written as fact). What this clause asserts is **mutual agreement among the
    reachable copies, anchored to whichever ``configs/`` sits beside
    ``tests/``** — ``authority = ROOT / "configs"``, and ``ROOT`` derives from
    this file's own location. The anchor is POSITIONAL, so the guard's claim
    is not the same statement in every tree, and the round-16 predicate fix
    (right, and kept) did not change that:

    * **repo checkout** — ``tests/`` and the repo ``configs/`` are both
      present, the anchor IS the authority, and the clause means what it says.
      Own run: 7 passed, 0 skipped, with two live comparisons executed.
    * **unpacked sdist** — ``[tool.hatch.build.targets.sdist] include`` ships
      ``pairwisepm``, ``configs``, ``app.py``, ``tests`` and NOT ``leaves``, so
      this clause RUNS and anchors on the sdist's own ``configs/``: a
      redistributed copy compared against another copy, with no repo authority
      present anywhere in the tree. Green there means "these copies agree",
      never "this is the approved policy".
    * **wheel install** — ``[tool.hatch.build.targets.wheel]`` ships
      ``packages = ["pairwisepm"]`` plus the force-included ``configs`` and no
      ``tests`` at all. Verified in this machine's
      ``pairwisepm-0.1.0.dist-info/RECORD``: two YAML files, the ``.pth``, four
      metadata entries, and **zero ``tests/`` entries**. So here the guard is
      **ABSENT, not skipped** — a distinction worth a line because only one of
      those two states is ever observable by the person standing there, and a
      reader who believes the wheel case is a skip will go looking for a skip
      line that cannot exist.
    """
    if not _repo_config_authority():
        pytest.skip("no repo config authority present to compare against")

    authority = ROOT / "configs"
    schemas = sorted(p.name for p in authority.glob("*.yaml"))
    assert schemas, "no mode schemas found in the repo's configs/"

    checked = 0
    for entry in sys.path:
        if not entry:
            continue
        other = (Path(entry) / "configs").resolve()
        if other == authority.resolve() or not other.is_dir():
            continue
        for name in schemas:
            candidate = other / name
            if not candidate.exists():
                continue
            checked += 1
            assert candidate.read_bytes() == (authority / name).read_bytes(), (
                f"a second copy of the mode schema {name} on sys.path has "
                f"drifted from the repo authority:\n  {candidate}\n  "
                f"{authority / name}\nThese files carry the D1/D2 prior "
                "weights. The stale copy will serve old weights to any "
                "non-editable install with no error and no failing engine "
                "test. Reinstall or uninstall the package copy; never edit it."
            )
    assert checked >= 0  # documents that zero duplicates is a passing state


def test_exactly_one_importable_copy_of_the_package():
    """T-VEND-04 — no second copy of the package is importable at all.

    T-VEND-02/03 assert that THIS session bound the right copy. They are
    silent about a duplicate that merely exists: run from the repo root,
    `sys.path[0]` wins and the guards stay green while a stale install sits
    in site-packages waiting for the first off-root launch.

    That is exactly the residual A-13-01 condition, and a plain
    `pip install .` into the working venv recreates it in one command with no
    other symptom. So the invariant is the count, not the binding: at most one
    importable `pairwisepm` may be reachable on `sys.path`.

    SCOPE, stated so the census cannot be read wider than it counts
    (architecture's round-16 demand, accepted): this is a COUNT invariant and
    its subject is the PACKAGE authority ONLY — `pairwisepm/__init__.py`. It
    says nothing about `configs/`, where a second tree is permitted by design
    and covered by T-VEND-03 (resolution) and T-VEND-06 (freshness) instead.
    Reading this clause as "exactly one copy of everything" would either
    demote the package count to a preference or invite deleting the wheel's
    `force-include`, which is what lets `pip install pairwisepm` find its
    schemas at all.

    Round 16: this guard NEVER SKIPS (engineering's demand). Its subject is
    `sys.path`, which exists in every tree; the design leaf's presence was
    never a precondition of counting. Where the tree carries no package
    authority to identify, the count invariant still holds and is asserted
    alone.
    """
    found = []
    for entry in sys.path:
        if not entry:
            continue
        candidate = Path(entry) / "pairwisepm" / "__init__.py"
        if candidate.exists():
            resolved = candidate.resolve()
            if resolved not in found:
                found.append(resolved)

    expected = (ROOT / "pairwisepm" / "__init__.py").resolve()
    if not expected.exists():
        # No package authority in this tree to identify — the count invariant
        # is still the whole claim, and it is still checkable.
        assert len(found) <= 1, (
            "more than one importable copy of `pairwisepm` is on sys.path:\n  "
            + "\n  ".join(str(p) for p in found)
            + "\n\nWhich one `import pairwisepm` binds then depends on the "
            "working directory."
        )
        return

    extra = [p for p in found if p != expected]
    assert not extra, (
        "more than one importable copy of `pairwisepm` is on sys.path:\n  "
        + "\n  ".join(str(p) for p in [expected, *extra])
        + "\n\nWhich one `import pairwisepm` binds then depends on the working "
        "directory. Make the install editable (`pip install -e .`) or remove "
        "it (`pip uninstall pairwisepm`). NOTE: every install of this project "
        "— editable included — also writes a second copy of `configs/` (the "
        "wheel force-includes it and the editable target inherits that), so "
        "resolved D1/D2 prior weights would not reach a shadowed engine. "
        "That duplicate is permitted by design and is T-VEND-06's subject, "
        "not this clause's: this one counts PACKAGE authorities only."
    )


def test_this_file_cannot_return_an_all_skipped_green():
    """T-VEND-07 — gate P-14's floor, asserted structurally rather than read.

    Registered round 17 on sequencing's demand. P-14 makes
    ``pytest tests/test_vendoring.py`` the pre-flight that decides whether the
    M-UX-02a sitting produces a RECORD. Their finding is exact and it is about
    this file, not about the gate: **pytest exits 0 on an all-skipped file**,
    so "green" was satisfiable by a run in which zero assertions executed —
    and until round 16 that was not hypothetical (four guards gated on the
    design leaf's presence; engineering measured ``4 skipped in 0.00s`` in an
    sdist-shaped tree). A witness would have recorded a pass for a run that
    measured nothing, and this matrix would have flipped a Spine metric on it.
    That failure is silent AND time-boxed, which is the worst pair.

    Round 16 fixed the predicates. This clause makes the fix un-undoable, and
    it is deliberately a NEGATIVE test of the instrument rather than a line in
    a procedure: a caveat asking a presenter to count skips is the honor
    system with a stopwatch on it. Three properties, all read off this file's
    own AST so a reflowed call or a moved line cannot empty the check:

    1. Two named clauses — T-VEND-04 (count) and T-VEND-05 (served values) —
       carry NO skip predicate and no skip marker. They are the floor: in any
       tree, in any install, ``pytest tests/test_vendoring.py`` green means at
       least these two asserted.
    2. Every clause that DOES skip skips on a predicate that names its own
       subject (``_in_repo_checkout`` for the design-authority pair,
       ``_repo_config_authority`` for the config pair). A third predicate is
       fine, but it reds here first, which is where activation-vs-subject gets
       looked at rather than assumed.
    3. At least two clauses are unskippable, stated as a count so deleting one
       of the floor clauses cannot be compensated by renaming another.

    This does not make the OTHER two guards run everywhere, and it does not
    pretend to: T-VEND-03/06 skip where ``<root>/configs`` is absent, which is
    honest, and both wheel and sdist ship ``configs``. What it removes is the
    state sequencing named — a green with no assertions behind it. P-14's own
    row carries the matching clause: green means exit 0 AND **0 skipped**, and
    the witness line records the skip count beside the result.
    """
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)

    helpers = {
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name.startswith("_")
    }
    clauses = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    }

    missing = _NO_SKIP_FLOOR - set(clauses)
    assert not missing, (
        "gate P-14's floor clauses are not in this file: "
        + ", ".join(sorted(missing))
        + " — P-14 registers `pytest tests/test_vendoring.py` green as the "
        "pre-flight for the M-UX-02a sitting, and these are the clauses that "
        "make a green mean assertions ran. Deleting or renaming one is a "
        "change to a Spine metric's instrument; update _NO_SKIP_FLOOR "
        "deliberately, in the same change, or the floor is gone silently."
    )

    unskippable = []
    for name, node in clauses.items():
        skips = [
            sub
            for sub in ast.walk(node)
            if isinstance(sub, ast.Call)
            and isinstance(sub.func, ast.Attribute)
            and sub.func.attr == "skip"
            and isinstance(sub.func.value, ast.Name)
            and sub.func.value.id == "pytest"
        ]
        markers = [
            ast.unparse(dec)
            for dec in node.decorator_list
            if "skip" in ast.unparse(dec)
        ]
        predicates = {
            sub.func.id
            for sub in ast.walk(node)
            if isinstance(sub, ast.Call)
            and isinstance(sub.func, ast.Name)
            and sub.func.id in helpers
        }

        if not skips and not markers:
            unskippable.append(name)
            continue

        assert name not in _NO_SKIP_FLOOR, (
            f"{name} is one of gate P-14's floor clauses and it has acquired a "
            "skip"
            + (f" marker ({markers[0]})" if markers else " predicate")
            + ". P-14's green would again be satisfiable by a run that "
            "asserted nothing — the exact hole round 16 closed and round 17 "
            "made structural. A guard is not weakened for convenience: if the "
            "skip is genuinely right, the floor moves to another clause in "
            "the same change and P-14's row says which."
        )
        assert predicates and predicates <= _PERMITTED_SKIP_PREDICATES, (
            f"{name} skips on a predicate this file does not sanction: "
            f"{sorted(predicates) or ['<none found>']}. Every skip here must "
            "gate on the clause's OWN subject — `_in_repo_checkout` for the "
            "design-authority pair, `_repo_config_authority` for the config "
            "pair. Round 16's defect was a guard whose ACTIVATION was "
            "narrower than its SUBJECT (all four gated on the design leaf, "
            "and pyproject's sdist include ships `tests` without `leaves`), "
            "which reads identically to a passing suite. Add the predicate to "
            "_PERMITTED_SKIP_PREDICATES only after answering, in writing, "
            "what subject it names."
        )

    assert len(unskippable) >= 2, (
        "fewer than two clauses in this file assert unconditionally "
        f"(unskippable: {sorted(unskippable)}). pytest exits 0 on an "
        "all-skipped file, so gate P-14 — the pre-flight that decides whether "
        "the M-UX-02a sitting produces a record at all — would be green on a "
        "run that measured nothing."
    )
