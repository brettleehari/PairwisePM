# PairwisePM — Compliance Leaf: Traceability Matrix

leaf: compliance
derives_from: /spine/SPINE.md (spine_version 0.1) and /docs/technical-spec.md
status: INTEGRATED — suite implemented at `/tests/test_engine.py` (engine, 45
  tests), `/tests/test_packaging.py` (T-PKG + T-NEG-06 static audit + T-CUST-01
  + T-CEIL-03 + T-SER-01 serialization guard + T-THEME-01 theme pin +
  T-THEME-01b nested-element render audit + T-BANNER-01 fixed-banner static
  pin (rewritten per §22b) + T-STR-01 singular-selection pin + T-NEG-07
  unearned-five-minute-claim tripwire (round 13) + T-DELIV-01a/b banner
  delivery-layer guard (round 14, spec §25), 16 tests), and
  `/tests/test_vendoring.py` (T-VEND-01 byte-identity guard + T-VEND-02
  bound-module identity + T-VEND-03 loaded-config-dir identity + T-VEND-04
  single-importable-copy count, round 14, spec §24; + T-VEND-05 bound-module
  R-10 value pin, never skips, and T-VEND-06 no-stale-second-copy of the
  policy values, round 15, spec §26, 6 — **skip predicates corrected round 16,
  spec §27a: T-VEND-03/06 now gate on the CONFIG authority and T-VEND-04 does
  not skip at all; the design-leaf gate made them inert in every installed
  tree, which is the only tree where the frozen second copy can exist**), and
  **`/tests/test_copy_surfaces.py` (round 16, spec §27b, 5 tests): T-COPY-01 /
  01b on `configs/*.yaml` rendered text and T-NEG-08 / 08a / 08b on the Spine's
  excluded-from-score refusal — the two rendered populations that sit OUTSIDE
  the string catalogue and outside every copy-integrity instrument on this
  board (design's §6.15 census; rows F-32/F-33)**, and **T-VEND-07 (round 17,
  spec §27c): `pytest tests/test_vendoring.py` cannot return an all-skipped
  green — the floor under gate P-14, asserted from this file's own AST rather
  than left as a caveat a presenter is asked to honor**, and **round 18, spec
  §27e/f, 5 more in `test_copy_surfaces.py` (10 total): T-COPY-02 / 02b (the
  config text and the four evaluative labels diffed against design's ratified
  `leaves/design/copy-authority.yaml` — the AUTHORITY half F-32/F-33 could not
  have without a design ruling, delivered round 17), T-COPY-02c (an exemption
  must cite a guard that still exists), T-COPY-02d (the rendered-text census
  derived from the dataclasses, not from a hand-written list that has been
  wrong four times), T-COPY-03 (T-NEG-08 and its siblings cannot be weakened,
  renamed or made skippable without reddening in the same change — gtm's
  deletion trigger, executed as an instrument because two seats have retired
  checks on the strength of that test)**; 78/78 green against the real
  `pairwisepm` package on
  2026-08-31 (compliance's own re-run, round 16, from the repo root AND from an
  off-root working directory) in the project venv
  WITH gradio 6.26.0 installed (the Space-contract test passes, no skips).
  **Round-14 qualification on every suite pin above:** counts from rounds
  9–13 were cwd-conditional — nothing in the suite established WHICH copy of
  the package produced them (see the round-14 entry and spec §24). From this
  round the run is anchored: T-VEND-02 asserts the bound module, and the
  67/67 above was re-confirmed from an off-root working directory against
  the in-repo module. **Round-15 extension of that same correction:** the
  anchoring instruments SKIP in a stripped deployment, so they anchored the
  checkout and not the install; T-VEND-05 never skips. **Round-16 completion of
  that same correction:** T-VEND-03/04/06 skipped there too, for a reason that
  was not even theirs (the design leaf's absence), so on an sdist or installed
  tree the count, the resolution and the freshness of the POLICY VALUES were
  all unasserted. Fixed at the predicate; measured before and after (spec §27a).
  **Round-17 closure of that class:** the predicate fix was correct but
  reversible by one line, and the gate standing on top of it (P-14) reads
  pytest's exit code, which is 0 for a file in which nothing ran. T-VEND-07
  makes the floor structural — two named clauses may never acquire a skip, and
  no clause may skip on a predicate that does not name its own subject — so
  "green" in that file now entails that assertions executed. Suite 73/73 from
  the repo root AND off-root, own run 2026-08-31.
  ROUND-4 CAVEAT RESOLVED ROUND 5: the round-3 browser render proved the suite
  structurally blind to Gradio's serialization layer (F-28 / states.md §6.4
  R-8); the R-8 fix landed round 4 WITH T-SER-01 in the same change, red-first
  demonstrated AND verifiable by construction (spec §20 status block), so the
  suite now guards that layer with real frontend payloads. T-THEME-01 landed
  the same way for R-9 and was broadened round 5 to the full §21 contract.
  Manual-side results are CITABLE: states.md §6.5 (browser render session
  1, 2026-08-30) — M-UX-01 PASS, M-UX-03 FAIL, M-DOC-01 PASS, M-UX-02 pending
  — AND states.md §6.7 (browser render session 2, 2026-08-31, append-only):
  R-8 acceptance PASS on all four behaviors (F-28 browser-confirmed), R-9
  acceptance FAIL at the descendant level (residual R-9b — F-29 DEMOTED
  round 6 to partial; T-THEME-01 green while the MP-1 token is illegible in
  served dark theme; strengthened contract T-THEME-01b specified spec §21b;
  new pre-push gate P-11 blocks), M-UX-03 FAIL stands as of §6.7,
  M-UX-02 now schedulable.
  ROUND 7 (2026-08-31): BOTH residual fixes verified LANDED in app.py by
  compliance's own audit — R-9b (inline color on every text-bearing element
  inside forced-light blocks, app.py render functions) paired SAME-CHANGE
  with T-THEME-01b (§21b honored: render-level audit + red-by-construction
  sensitivity self-test), and the M-UX-03 sticky banner (`#pwpm-banner
  { position: sticky; top: 0; z-index: 100 }` via elem_id + Blocks css)
  paired with static pin T-BANNER-01.
  ROUND 8 (2026-08-31): render session 3 RAN (states.md §6.9, dated
  per-check-ID append-only — verified from this seat, suite re-run 58/58
  own run). **F-29 FLIPPED VERIFIED — browser-confirmed** on §6.9 rows
  (a)–(e) + overall PASS (every §6.7-failing surface computes legible ink
  in served dark theme, computed-style evidence); **P-11 CLEARS** — all
  three clauses met (fix + strengthened guard same-change + session-3
  PASS). **F-19 stays manual-FAILED on a THIRD §6.9 FAIL row**, and the
  FOURTH green-guard/browser-false instance is REGISTERED: T-BANNER-01
  green and the browser itself confirms computed `position: sticky` —
  yet the banner scrolls away, because `.gradio-container-6-26-0`
  computes `overflow: hidden` while the DOCUMENT is the scroller, so
  sticky is structurally inert. The blindness ladder now reads:
  serialization (T-SER-01) → specificity (T-THEME-01b) → structural
  context (T-BANNER-01): a static pin can verify a rule is APPLIED;
  only the browser can verify it takes EFFECT. Strengthened contract
  §22b written BEFORE the fallback lands (position:fixed + height
  reservation + same-change T-BANNER-01 update, red-first against the
  current sticky build); P-5 clears only on session 4's single
  banner-in-viewport check. M-UX-02's light-theme rider is LIFTED
  per §6.9 conclusion (4).
  ROUND 9 (2026-08-31): the §22b fallback is LANDED and verified from this
  seat — `#pwpm-banner { position: fixed; top: 0; left: 0; right: 0;
  z-index: 100 }` in app.py `_CSS`, height reserved by an in-flow hidden
  content-exact duplicate spacer FIRST in the layout toggling with the
  banner on mode change, **T-BANNER-01 rewritten IN THE SAME CHANGE** per
  every §22b clause, red-first by construction (a position:fixed assertion
  cannot pass on the prior sticky build), docstring naming session 4's
  browser check as the acceptance owner — the SEVENTH same-change fix+guard
  pairing. **F-19 stays manual-FAILED and P-5 stays blocking**: clause (1)
  of §22b is satisfied, but the row flips ONLY on render session 4's single
  behavioral check (banner rect in viewport at scrollY 1500), recorded
  per-check-ID in states.md's next append-only section (§6.10 is now the
  R-10 mint record, so the session-4 row lands as §6.11 or later — the
  citation is the row-set, never the section number). ALSO round 9:
  **T-VEND-01's FIRST LIVE CATCH registered** (design's canonical R-10 mint
  turned the guard red mid-flow; engineering's byte-identical re-vendor
  closed it in the same change — the documented direction, verified
  byte-identical again from this seat via cmp), and **T-STR-01 registered**
  (new row F-30, spec §23): R-10(i) singular selection wired through one
  `_S_n` selector, R-10(ii) stale-card honesty (the false "Recomputing…"
  claim is DEAD in served copy — "Press Compare to recompute." verified in
  both canonical and vendored strings and negatively pinned), with
  T-CUST-01(b)/T-SER-01(c) strengthened same-change because both previously
  pinned the plural-with-1 defect shape as expected output.
  ROUND 10 (2026-08-31): **F-19 FLIPPED VERIFIED — browser-confirmed — and
  P-5 CLEARED**, on states.md §6.11 (browser render session 4, dated
  per-check-ID append-only, verified from this seat: suite re-run 59/59 own
  run 1.21s, cmp byte-identical, §6.11 row-set read in full). The single
  §22b acceptance check PASSED: banner rect top 0 / bottom 77.2, fully
  within the 792px viewport at scrollY 1500 (and at max scroll 1824.5),
  computed `position: fixed`, served 0→1 dark theme — the row flipped on
  exactly the one check §22b pre-stated, and nothing else. Height
  reservation verified live (spacer height 77.2 = banner height, no magic
  pixels); opaque background verified (no ghosting). **The matrix carries
  ZERO open browser-refutations for the first time.** The guard-doctrine
  arc closes its fifth chapter: applied verified by the static pin,
  effective verified by the browser — each half by the instrument that
  owns it. ALSO round 10: §6.11's two bonus rows registered on F-30 — the
  copy chain (states.md → strings.py → vendored copy → browser) is
  browser-confirmed END-TO-END (singular '1 factor score to go' and the
  corrected 'Press Compare to recompute.' tail both ON SCREEN); R-12
  classification sign-off RECEIVED explicit (states.md §6.4 catalogue
  entry + §6.11 conclusion 5) — design-catalogued, post-pilot, no matrix
  row, on the designer's own stated rationale, closing the carried round-8
  question. F-25's arc is registered with direction: drift-episode (round
  2) → test-enforced (round 3) → first live exercise clean (round 9).
  REMAINING on the release path: M-UX-02 (F-17, sole manual-pending row,
  gtm witness slot named for today) and D1-D6 resolution (SLA executes
  2026-09-01; regeneration duty ARMED — T-M0-01/T-PAR pinned constants and
  every T-FRAG fixture regenerate in the resolution round with a
  provenance line per constant citing the per-entry resolution_source).
  ROUND 11 (2026-08-31): registration round on refreshed evidence (suite
  re-run 59/59 own run 1.23s; cmp byte-identical; decisions.yml re-grepped —
  D1-D6 all six pending on the final human-window day; states.md §6.11
  conclusions re-read in full). THREE registrations: (1) **the
  pin-before-implementation doctrine is registered as STANDING METHOD**
  (§6, "Standing method" block) — four consecutive cycles, zero
  renegotiation, closing with the full applied-vs-effective division of
  labor; any future defect crossing the repo/browser seam runs the same
  sequence, no longer episode history. (2) **gtm's gate-protocol close
  registered on F-17/F-19**: the banner-in-frame demo gate lifted round 10
  on §6.11's single PASS line per the pre-wired per-line protocol, after
  holding through THREE guard-green repo landings — the discipline held in
  both directions (no early lift on green guards, no late drift after
  PASS), and the demo surface carries zero gates and zero workarounds.
  F-17/SC-06 conversion stays EXACTLY as written: dated timed record with
  named witness, unsoftened if the sitting slips to the 2026-09-01
  backstop hour. (3) **Sequencing's flip demand confirmed already
  executed round 10** — F-19 verified/P-5 cleared on §6.11's row and the
  render-session ledger encoded CLOSED are both in this file's round-10
  entry; matrix and graph price the same reality. ALSO round 11: my
  carried retrigger question to design is answered by the record itself —
  §6.11 conclusion (3) names "copy or layout changes" in its own text
  (re-read from this seat), so the ledger's reopen clause binds both
  directions in writing; design's one-sentence confirmation remains
  welcome but the written clause is the binding instrument.
  ROUND 12 (2026-08-31): evidence-vehicle pre-registration round, on refreshed
  evidence (suite re-run 59/59 own run 1.30s; cmp byte-identical; decisions.yml
  re-grepped — D1-D6 all six still pending; states.md read through §6.12; gtm's
  launch-copy.md 1c-i template read verbatim from this seat). THREE
  registrations: (1) **the pre-staged M-UX-02 witness-record format
  (launch-copy.md 1c-i, round 11) is REGISTERED as the agreed evidence vehicle
  for the F-17/SC-06 flip** — verified against the actual template, not gtm's
  description: dated, per-check-ID (M-UX-02), fresh-user identity + recruited-
  by-Hari + no-prior-exposure affirmation, mode 1→N, theme, start/end/elapsed
  vs the 5:00 bound → explicit PASS|FAIL, design's same-sitting timer reading
  (second instrument), named witness (gtm), and the coaching-given line
  (mode selection only; anything more VOIDS the record). The template meets
  this matrix's citable per-check-ID standard AS WRITTEN, so when the filled
  record lands the flip is a read, not a negotiation — the F-19 discipline
  applied forward: the acceptance clause exists before the evidence does.
  (2) **The recordless branch is PRE-REGISTERED, unsoftenable**: if the window
  closes (backstop first hour of 2026-09-01 passes) with no filled record,
  F-17 STAYS manual-pending, SC-06 stays "designed so" in every payload, and
  the miss is recorded as a DATED SCHEDULING FACT — never paraphrased into a
  soft claim, never flipped on a narrative. A voided record (coaching beyond
  mode selection, non-fresh user) counts as NO record. (3) **Design's §6.12
  registered, closing my retrigger question one notch past the round-11
  close**: the render-session ledger's retrigger clause is now EXPLICITLY
  bidirectional in design's own written text (copy direction AND layout/rule
  direction, binding even when every static pin stays green, with the
  rule-applied-vs-rule-effective lesson stated inside the clause) — verified
  from this seat, no inference left anywhere in the chain; AND §6.12
  pre-states the M-UX-02 protocol (clock from S1 first paint to first
  verdict-surface render, 1→N, fresh user, both seats' numbers) so the
  sitting's acceptance definition is fixed in the design instrument too.
  As of this round NO sitting record exists in either instrument (own check).
  T-minus-zero: tomorrow's D1-D6 regeneration duty stays ARMED unchanged.
  ROUND 13 (2026-08-31): SELF-CAUGHT SCOPE DEFECT + one new negative test, on
  refreshed evidence (suite 60/60 own run 1.41s in the project venv; zero
  gradio imports in `pairwisepm/`; decisions.yml re-grepped from this seat —
  six `status: pending` entries at lines 32/73/116/138/166/198, D7
  resolved_uncontested; gtm's 1c-i and design's §6.12 re-read verbatim).
  (1) **THE DEFECT, reported against myself.** Round 12 registered a flip
  instrument without checking it against the check it discharges. This matrix
  defines M-UX-02 as a timed walkthrough of BOTH modes (F-17 row; §6 manual-
  checks list). Both pre-registered instruments measure ONE: gtm's template
  fixes `mode: 1→N`, design's §6.12 fixes "one blank-to-verdict 1→N run" —
  and my own round-12 entry above records "mode 1→N" in the template
  description without noticing it contradicted the check. Had the sitting run
  tomorrow, a one-mode measurement would have flipped a two-mode row "as a
  read", which is the precise failure this matrix exists to prevent, pointed
  at the matrix itself. FIX (a correction, never a relaxation): M-UX-02
  splits into **M-UX-02a (1→N, instrumented, schedulable now)** and
  **M-UX-02b (0→1, no instrument, unscheduled)**. A filled 1→N record
  converts SC-06 for 1→N and SC-06's payload claim must name the measured
  mode; the unqualified both-modes claim, and 0→1, stay "designed so, not yet
  timed". Neither half's bar moves; the evidence simply stops covering more
  than it measured. The lesson generalises and is registered as standing
  method: **an evidence vehicle is not registered until it has been diffed
  against the acceptance clause it discharges, field by field** — round 12
  verified the template's INTERNAL quality (six fields, citable, per-check-ID)
  and never diffed its SCOPE. Internal quality is not coverage.
  (2) **T-NEG-07 landed** (`tests/test_packaging.py`), the automated half
  SC-06 never had: shipped user-facing copy (README.md, app.py) may state the
  five minutes as a design target and may NOT state it as a measured result,
  while F-17 is unconverted. Spine anchor: "A judge that overstates its
  confidence is worse than no judge" — an unearned speed claim is that
  overstatement aimed at the tool's own performance. Reported honestly as a
  TRIPWIRE: both artifacts currently contain no five-minute mention at all
  (own grep), so the file-level assertion is vacuous today and its value is
  entirely on introduction. Red-first was demonstrated at the PREDICATE level,
  not by mutating a file this leaf does not own — seven synthetic lines split
  correctly (bare duration RED, measured/verified framing RED, target-framed
  GREEN, unrelated prose unmatched). The vacuity is stated in the test's own
  docstring; a tripwire that hides its vacuity would be the same overstatement
  in miniature.
  (3) **gtm's round-12 demand accepted and executed**, with one correction to
  its premise. (a) The canonical non-conversion phrase is registered as
  exactly **"designed so, not yet timed"** — verified present verbatim in
  gtm's launch-copy.md (1c-i, lines 215 and 226) and design's states.md
  (§6.12, line 1468) on this seat's own grep. This matrix previously wrote the
  short form "designed so" in the F-17 row, the §6 gate block and the round-12
  entry; the long form is now the registered string and the short form is a
  reference to it, not a competing paraphrase. (b) The clock is registered as
  the measurement of record. gtm reported the two definitions as "verbatim"
  agreement; they are NOT character-identical — design §6.12 reads "clock
  starts at first paint of S1, stops at first render of S3/S4/S5", gtm's
  template reads "start = first paint of S1 (blank questionnaire), stop =
  first render of the verdict (S3/S4/S5)". They are something better than
  verbatim: they agree on identical STATE IDs (S1; S3/S4/S5), so the interval
  is fixed by reference to the state machine rather than by matching prose,
  and the two seats' numbers are comparable by construction. Registered on
  that stronger ground, with the wording difference recorded rather than
  smoothed over.
  Board state after this round: F-17 remains the last manual-pending row, now
  correctly split; nothing else on the release path is open; tomorrow's D1-D6
  regeneration duty (T-M0-01/T-PAR pinned constants + every T-FRAG fixture,
  one provenance line per constant, in the resolution round, before any push
  on new values) stays ARMED unchanged.
  ROUND 14 (2026-08-31): **THE MATRIX'S OWN EVIDENCE BASE AUDITED**, on
  architecture's A-13-01 — reproduced independently from this seat before
  acceptance, never registered on the report. Own runs: 65/65 (1.43s) from
  repo root AND from an off-root working directory; predicate-level red-first
  demonstrations for all five new clauses; decisions.yml unchanged (six
  pending); gtm's 1c-i, design's §6.13 and the dependency declarations all
  read verbatim from this seat.
  (1) **A-13-01 CONFIRMED, then verified CLOSED — both halves.** Before the
  fix: `.venv/.../site-packages/pairwisepm/` existed as a NON-editable install
  (`direct_url.json` = `{"dir_info": {}}`), drifted from the authority at line
  79 — no `str.empty.example_cta` (which `app.py:848` reads unconditionally at
  layout construction) and still carrying the pre-R-10 `"Recomputing…"` tail
  that F-30 exists to keep out of served copy. From `/tmp` the interpreter
  bound that stale module; **T-VEND-01 returned PASS anyway**, from either
  directory, because it compares two paths it builds from its own `__file__`
  and never imports the module it guards. Verified closed this round, again
  from this seat rather than on report: `direct_url.json` now reads
  `{"dir_info": {"editable": true}}`, `site-packages/pairwisepm/` is gone, an
  off-root interpreter binds the in-repo module, and the off-root suite is
  green against the RIGHT module.
  (2) **The guard half closed in this leaf's own files, same round.**
  **T-VEND-02** (bound module's identity AND bytes) and **T-VEND-03** (the
  config directory the engine actually loads — the wheel force-includes
  `configs/`, and D1/D2 resolve into those YAML files, so a shadowed copy
  would serve stale prior weights with no error and no failing engine test)
  are registered at spec §24 — plus **T-VEND-04**, which pins the COUNT rather
  than the binding: no second `pairwisepm/__init__.py` anywhere on `sys.path`.
  That closes the residual half T-VEND-02/03 are silent about — run from the
  repo root, `sys.path[0]` wins and the binding checks stay green while a
  stale install sits in site-packages waiting for the first off-root launch,
  which is precisely the A-13-01 condition. A plain `pip install .` into the
  working venv recreates it in one command with no other symptom, so the
  invariant had to be automated rather than left as a checklist habit; P-12 is
  now a green-or-red test, not an instruction to inspect `direct_url.json`.
  T-VEND-01 is RETAINED UNCHANGED, not superseded:
  it claims rule-APPLIED and is honest about that. Red-first demonstrated at
  the PREDICATE level per the T-NEG-07 method (a stale shadow copy on
  `sys.path` in scratchpad, mutating no file this leaf does not own): T-VEND-02
  (a) RED, (b) RED, T-VEND-03 RED — **and T-VEND-01 GREEN in the same run**.
  The blindness is now reproducible on demand rather than argued.
  (3) **THE COLLATERAL, PRICED AGAINST THIS LEAF'S OWN RECORD.** Every "own
  run, 59/59 / 60/60" certification in rounds 9–13 — mine included, and mine
  are the ones this matrix rests on — was **cwd-conditional evidence, not the
  unconditional evidence its wording implied**. The runs happened and the
  numbers were real; what was absent is that nothing in the suite established
  which module produced them. This is the round-13 lesson recurring one level
  down: round 13 found an instrument registered against a check broader than
  what it measured; round 14 finds instruments certifying a module they never
  identified. Both are the same error — **verifying an instrument's internal
  quality and never verifying what it is attached to** — and the standing
  method is extended accordingly (see §6). The header pin above now carries
  this qualification rather than quietly re-stating the old numbers.
  (4) **Engineering's delivery-side demand accepted and made TESTABLE rather
  than merely registered** (spec §25, **T-DELIV-01a/b**). Verified from this
  seat, and the mechanism is thinner than the demand stated: on the constructed
  Blocks **`demo.css` is `None`** — the banner rule survives only in the
  private `demo._deprecated_css`, read by `launch()` at
  `gradio/blocks.py:2785`. So `position:fixed live at app.py:769` evidences
  rule-WRITTEN; the bound `gradio>=6.0,<7` (verified present in BOTH
  `requirements.txt` and `pyproject.toml [app]`, matching README's pinned
  `sdk_version: 6.26.0`) evidences rule-DELIVERABLE; and T-DELIV-01 is the
  instrument that makes widening the bound read as **evidence loss** instead
  of housekeeping. Red-first at predicate level: `>=6.0,<7` GREEN, `>=4.0`
  (the pre-round-14 shipped state) RED, bare `gradio` RED, `>=6.0,!=6.1` RED;
  and a Blocks-alike with no `_deprecated_css` (the gradio-7 scenario) RED.
  A registered line would have satisfied the demand; a test satisfies the
  agenda — the claim is now falsifiable by machine, not by memory.
  (5) **gtm's and design's branch demands accepted in full** — see F-17. The
  M-UX-02 outcome space is now THREE dated branches, not two, and a missed
  window is an EXPIRED SLOT rather than a terminal FAIL.
  Board state: F-17 (split a/b) remains the last manual-pending row. F-25 is
  **restated, not flipped**: the boundary is verified at both the disk and
  bound-module levels, and its arc gains a fourth stage. Tomorrow's D1-D6
  regeneration duty stays ARMED unchanged — and T-VEND-03 now protects it,
  since regenerating fixtures against a shadowed `configs/` would have been
  undetectable.
  ROUND 15 (2026-08-31): **the copy chain's last untested link closed, and one
  demand refused on its premise while accepted on its substance.**
  (1) **design's CX-14-01 registered AND closed on a citable artifact rather
  than on memory** (see F-25). Verified from this seat first: the bindable
  module is now the in-repo copy from any working directory, its
  `str.verdict.stale` reads *"Inputs changed — the verdict above no longer
  applies. Press Compare to recompute."*, and `str.empty.example_cta` is
  present. But design's underlying point survived that verification: **the
  chain's terminal link had no instrument that runs where it matters.**
  T-VEND-02 proves bound-bytes == authority-bytes and is strictly stronger
  than any value check — and it SKIPS when the design leaf is absent, which is
  exactly the stripped install a user receives. So on a shipped install
  nothing on this board asserted anything about the copy that reaches the
  user. **T-VEND-05 (spec §26) never skips** and pins the two R-10 facts by
  value on the BOUND module: the CTA key exists, and the stale card states the
  manual-Compare flow with no "Recomputing…" claim. Design's scope word is
  adopted verbatim across the matrix: **file-identical is not copy-delivered**
  — and, one notch further than asked, copy-delivered-in-a-checkout is not
  copy-delivered-on-an-install.
  (2) **New row F-31 — the POLICY VALUES have their own copy authority**
  (engineering's demand (c), promoted out of F-25's prose where it did not
  belong: F-25's claim is about strings, and a row that carries a second
  invariant inside its narrative is the honor system with extra steps). Its
  instruments are T-VEND-03 (the config dir the engine loads), T-VEND-04 (the
  copy count) and new **T-VEND-06**: any `configs/*.yaml` under another
  `sys.path` entry MUST be byte-identical to the repo authority. The invariant
  is deliberately NOT "no second copy" — the wheel force-includes one and it is
  load-bearing on a non-editable install — but **"no STALE second copy"**.
  This is the more consequential half of the round-14 defect class, and the
  quieter one: a stale strings copy crashes loudly at `app.py:848`; a stale
  configs copy serves old prior weights with no error, no exception and no
  failing engine test — the confidence overstatement the Spine forbids,
  arriving as a number nobody would question. It is not a hypothetical guard:
  it compares two real duplicates on this machine right now
  (`site-packages/configs/{one_to_n,zero_to_one}.yaml`, byte-identical,
  install-time frozen), and it will red the instant tomorrow's resolution round
  edits the repo YAML while a snapshot survives.
  (3) **Red-first demonstrated, not asserted** (own run, synthetic shadow on
  `PYTHONPATH` built in scratchpad — no repo file mutated): T-VEND-02, 03, 04,
  **05 and 06 all FAIL while T-VEND-01 PASSES in the same run**. Clean: **67/67
  from the repo root and 67/67 from an off-root working directory**, both
  anchored to a verified module by T-VEND-02.
  (4) **gtm's F-17 voiding condition ACCEPTED on substance, REFUSED on its
  stated cause** (see F-17, and the open dispute). VOID-not-FAIL is correct and
  registered — recording a build accident as a FAIL of the 5:00 bound would
  tell a reader the claim was tested and lost when it was never tested, the
  mirror of the overstatement this matrix exists to stop — and the
  three-valued-ledger / cause-in-the-narrative reconciliation is registered so
  no fourth state is invented at the window's close. What is NOT registered is
  the mechanism gtm and architecture stated: *"launched outside the repository
  root ⇒ binds the stale copy ⇒ dies before first paint."* Sequencing
  disconfirmed it and this seat re-derived the same result rather than taking
  either side's word — `python /abs/path/app.py` puts the SCRIPT's directory on
  `sys.path[0]`, not the cwd, so the documented launch binds in-repo from any
  directory; and as of the editable install there is no stale copy to bind
  from any entry point at all. **A voiding condition written against a false
  mechanism is an untestable clause in a governing instrument** — it would
  void real records for the wrong reason and pass bad ones that arrive by
  another door. Registered instead in the form that is both true and
  checkable, which is design's: *a run whose bound module is not the design
  authority's copy produces NO RECORD*, plus a machine pre-flight (new gate
  **P-14**) so the witness records a test result rather than a guess about
  directories.
  (5) **decisions' D8 pointer accepted** — M-UX-02b's disposition now reads
  *"open — D8 (SLA 2026-09-02)"* in both F-17 and the SC-06 coverage row. The
  argument is this matrix's own standard turned on the one cell that failed it:
  every other state here rests on a citable artifact, and the b-half's rested
  on the absence of one. "No instrument, no sitting" is a true description and
  was becoming a decision by omission; it may still win as option 1, but it
  wins with an owner and a date.
  Board state: F-17 (split a/b) remains the last manual-pending row; F-31 is
  new and verified; F-25 gains the terminal-link scope word and CX-14-01,
  closed on T-VEND-05 rather than on this seat's re-run. Suite: 67/67.
  ROUND 16 — **TWO CORRECTIONS TO INSTRUMENTS THIS SEAT OWNS, BOTH REPORTED BY
  OTHER LEAVES, BOTH REPRODUCED HERE BEFORE BEING ACTED ON** (spec §27):
  (1) **THE SKIP PREDICATE — a guard whose ACTIVATION was narrower than its
  subject** (engineering's demand, accepted whole). All four round-14/15
  vendoring guards gated on `_in_repo_checkout()` — the presence of
  `leaves/design/strings.py`. Correct for T-VEND-01/02, whose subject IS that
  file; wrong for T-VEND-03 (which config dir the engine loads), T-VEND-04
  (how many importable package copies exist) and T-VEND-06 (whether a
  duplicate schema is stale), none of which has anything to do with the design
  leaf. And the gate was narrowest exactly where the hazard is widest:
  `pyproject.toml`'s `[tool.hatch.build.targets.sdist] include` ships `tests`
  WITHOUT `leaves`, so in an installed or sdist tree the guards were present
  and inert, while a repo checkout — the only tree they ran in — is the case
  where `sys.path[0]` already wins. **Measured from this seat in an
  sdist-shaped tree built in scratchpad (no repo file mutated): round-15
  predicate `1 passed, 5 skipped`; round-16 predicate `1 failed, 3 passed, 2
  skipped`** — the two remaining skips are T-VEND-01/02 and are honest, and
  the RED is a TRUE POSITIVE (that tree genuinely exposed two importable
  `pairwisepm` copies, the exact condition T-VEND-04 exists to name and the
  old predicate hid). Fixed: T-VEND-03/06 gate on `_repo_config_authority()`
  (their own subject); **T-VEND-04 no longer skips at all** — its subject is
  `sys.path`, and where a tree carries no package authority to identify, the
  COUNT invariant is still the whole claim and is asserted alone.
  **Stated as the mirror of A-13-01, because that is what it is:** A-13-01 was
  a guard whose SCOPE was narrower than its claim; this was a guard whose
  ACTIVATION was narrower than its subject. Both read identically in a green
  suite — `65 passed`, `67 passed`, and four of them never ran. This seat found
  the first species twice and did not look for the second in its own file.
  (2) **THE CATALOGUE IS ONE POPULATION OF THREE — new rows F-32/F-33 with
  instruments, not prose** (design's §6.15 census, accepted; and design's
  scope word applied to every copy-integrity row on this board, including the
  ones this seat wrote). New file `tests/test_copy_surfaces.py`, spec §27b:
  **T-COPY-01** (no rendered config string is empty or a placeholder),
  **T-COPY-01b** (a rendered label is prose, not the machine key),
  **T-NEG-08** (the four `(not scored)` evaluative labels in `app.py`,
  censused by AST — the Spine's excluded-from-score refusal as the USER reads
  it), **T-NEG-08a** (the same refusal at the config authority, both modes),
  **T-NEG-08b** (the refusal is structural: `EvaluativeInput` may never gain a
  weight field, and no key may be both scored and evaluative). **Red-first,
  demonstrated not asserted** (own run, mutated copies in scratchpad): a
  rationale replaced with `TBD`, one `(not scored)` deleted, one schema note
  reduced to `"captured"` ⇒ **3 failed, 2 passed here, and `tests/test_engine.py`
  entirely green on the same three mutations**. That is design's finding
  measured rather than restated: until this round the Spine's most quotable
  refusal could be deleted from the screen with the suite green.
  (3) **CENSUS ASYMMETRY carried into the guards and the rows** (architecture's
  demand, accepted): T-VEND-04 is a **count invariant — PACKAGE ONLY**;
  T-VEND-03 is a **resolution invariant — a second `configs/` tree is
  PERMITTED BY DESIGN**, because the wheel's `force-include` is what makes
  `default_config_dir()` resolve identically from a clone and a non-editable
  install. Both docstrings and both rows (F-25, F-31) now say so, so the pair
  cannot be compressed into "exactly one copy of everything" — a reading that
  would demote the package count to a preference or invite deleting the
  force-include, breaking `pip install pairwisepm`'s ability to find its
  schemas at all. This is the same correction this seat applied to itself in
  round 13, running the other direction: an instrument read WIDER than what it
  measures.
  (4) **DISPUTE B5 RESOLVED — by gtm's own retraction, on evidence, against
  their own finding.** The mechanism this seat refused to register in round 15
  ("launched outside the repo root ⇒ binds the stale copy ⇒ dies before first
  paint") has been retracted by the seat that authored it, after they
  reproduced sequencing's disconfirmation themselves. F-17 keeps the form
  registered in round 15 — design's bound-module condition plus gate P-14 —
  and now records that it was reached by three seats independently rather than
  chosen by this one. **Consequence for decisions' D9** (their demand,
  honored): this matrix did NOT register gtm's predicate as settled, and the
  three-way disagreement D9 was queued against has narrowed by retraction, not
  by the matrix picking a side. D9's remaining question — is design's clause
  CHECKED or a statement of principle — is answered from this file's side and
  only from this side: **it is checked**, by P-14 / `pytest tests/test_vendoring.py`.
  (5) **CITATION STRUCK** (sequencing's demand, accepted without argument): this
  seat's round-15 demand located an unencoded M-UX-02 split at
  `work-items.yaml:803`. That line does not contain it and the split had landed
  at round 14. The line reference is **WITHDRAWN**; the substance was already
  executed by sequencing and is not reopened. A line number cited for something
  it does not contain is a claim about a file that was not re-read at the moment
  it was made — the same species as this round's other two findings, one notch
  smaller, and it was in this seat's own packet.
  Board state after round 16: F-17 (split a/b) still the last manual-pending
  row; F-32/F-33 new and **OPEN** (partial instruments registered, authority
  question is design's to rule); dispute B5 closed. **Suite: 72/72 from the
  repo root AND 72/72 off-root**, own run (67 + 5).
  ROUND 17 (2026-08-31): **THE GATE ON TOP OF THE FIXED GUARDS COULD STILL BE
  GREEN WITH NOTHING BEHIND IT — closed as an instrument, plus one factual
  premise corrected against this seat's own text.**
  (1) **NEW GUARD T-VEND-07 — gate P-14's floor is now structural** (spec §27c;
  sequencing's demand, accepted whole and executed as a test rather than as the
  clause they asked for). Their finding is exact: **pytest exits 0 on an
  all-skipped file**, so P-14 — the pre-flight that decides whether the
  M-UX-02a sitting produces a RECORD — was green-satisfiable by a run in which
  zero assertions executed. That was not hypothetical last round (engineering
  measured `4 skipped in 0.00s` in an sdist-shaped tree). Round 16 fixed the
  predicates; round 17 makes the fix un-undoable: T-VEND-07 parses
  `tests/test_vendoring.py`'s own AST and asserts (a) T-VEND-04 and T-VEND-05
  carry no skip predicate and no skip marker — the floor, so a green in ANY
  tree means at least the count and the served values were asserted; (b) every
  clause that does skip skips on a predicate naming its OWN subject
  (`_in_repo_checkout` for the design-authority pair, `_repo_config_authority`
  for the config pair) — a third predicate reds here before it can be
  introduced quietly; (c) at least two clauses are unskippable, counted, so
  deleting one floor clause cannot be masked by renaming another. **Red-first
  demonstrated on scratch copies, no repo file mutated:** adding
  `pytest.skip` to T-VEND-05 reds with "one of gate P-14's floor clauses and
  it has acquired a skip predicate"; swapping T-VEND-06's predicate for an
  unsanctioned `_some_new_gate` reds with the activation-vs-subject message.
  **Why a test and not the clause as asked:** a caveat instructing a presenter
  to count skips is the honor system with a stopwatch on it, and this is the
  one gate whose failure mode is silent AND time-boxed. P-14's row carries the
  matching operative form — green means exit 0 **AND 0 skipped**, with the
  skip count recorded beside the result — and that clause is now backed by a
  guard rather than by the witness's attention.
  (2) **FACTUAL PREMISE CORRECTED IN F-31 AND IN THREE DOCSTRINGS**
  (architecture's demand, accepted after re-deriving it from this seat rather
  than on their report). Rounds 15–16 wrote, in this matrix and in the guards,
  that the second `configs/` tree is left by "any NON-EDITABLE install" and
  that the frozen duplicate "is created by the very install where `leaves/` is
  absent". **Both are false, and both understated the guard.** Verified here:
  `.venv/lib/python3.11/site-packages/pairwisepm-0.1.0.dist-info/direct_url.json`
  reads `{"dir_info": {"editable": true}}`; that dist-info's RECORD carries
  `configs/one_to_n.yaml` (sha256 `RL_7s3pRSc-…PKPmTk8`, 3894 B) and
  `configs/zero_to_one.yaml` (`ALjXJGEI5gz…j0B_aRQ`, 4149 B), digests
  recomputed here from the repo's own `configs/` and matching byte-for-byte;
  `site-packages/pairwisepm/` does not exist (only `_editable_impl_pairwisepm
  .pth`). Hatchling's editable target inherits the wheel's `force-include`, so
  **every install of this project creates the duplicate, editable included** —
  and this pytest session sees **two `configs/` trees on `sys.path`** with
  exactly one importable package. **The consequence is stronger than the one
  this seat wrote for its own guard:** T-VEND-06 does not wait for a
  hypothetical reinstall; it reds on the NEXT suite run after the D1/D2 write,
  on the install this repo has today. Demonstrated rather than predicted: a
  divergent `configs/one_to_n.yaml` placed on `sys.path` in scratch reds
  T-VEND-06 with the stale-weights message (`1 failed, 5 passed`), no repo
  file touched. The remedy line is unchanged and now matters more —
  refresh-or-remove, never a hand-edit of the site-packages copy and never
  deleting the `force-include`, which is the only reason
  `pip install pairwisepm` finds its schemas at all.
  (3) **TWO DEMANDS ARRIVED ALREADY EXECUTED — reported as such rather than
  re-executed.** Engineering's skip-predicate demand ("second time, unchanged
  and unanswered") and design's CX-15-01/02 registration demand were both
  filed against this file's round-15 state; both landed in round 16 in the
  packets that crossed. Verified in the current files before answering:
  `tests/test_vendoring.py` gates T-VEND-03/06 on `_repo_config_authority()`
  (`<root>/configs`) and T-VEND-04 skips on nothing; F-32/F-33 are OPEN rows
  with `tests/test_copy_surfaces.py` as their partial instrument and the scope
  word applied to F-25, F-30 and F-31. Saying "already done" is only worth
  anything with the citation attached, so both are answered with the file
  state rather than with a claim about a previous round.
  Board state after round 17: F-17 (split a/b) still the last manual-pending
  row; F-32/F-33 still OPEN awaiting design's authority ruling (my round-16
  demand, unanswered — re-pressed, and it is the only thing this seat is still
  waiting on); no open disputes. **Suite: 73/73 from the repo root AND 73/73
  off-root**, own run.
  ROUND 18 (2026-08-31): **THE TWO OPEN ROWS CLOSE ON AN INSTRUMENT RATHER
  THAN ON A SENTENCE — and the census that told me which fields to diff was
  wrong about one of them, in my favour, which is the round's real find.**
  (1) **F-32/F-33's AUTHORITY HALF IS INSTRUMENTED (spec §27e; design's demand,
  which is the other half of the demand this seat pressed twice).** Design
  ruled round 17 and created `leaves/design/copy-authority.yaml` — generated
  from live bytes, ratified by the seat that owns the copy, deliberately
  policy-free so the D1/D2 round cannot red it. Four new clauses:
  **T-COPY-02** diffs every ratified config text field against it in BOTH
  directions (ratified-but-absent, present-but-unratified, value mismatch — a
  one-way diff is how a copy guard goes quietly empty); **T-COPY-02b** pins the
  four `app.py` evaluative labels' WORDS against the ratified set, which
  T-NEG-08 never did (it watches the marker and the count: `Strategic fit` →
  `Strategic Fit` passed it, demonstrated); **T-COPY-02c** checks that a field
  EXEMPTED from the fixture cites a guard that still exists and still
  references its authority key; **T-COPY-02d** derives the rendered-text
  population from the dataclass annotations rather than a hand-written list.
  Design's §6.12(b6) per-line notification is now an instrument rather than a
  promise five seats accepted.
  (2) **THE CENSUS DEFECT: `banner` is in nobody's list.** Writing T-COPY-02
  exposed a rendered `configs/*.yaml` field that appears in NONE of the four
  independent enumerations of that population — design's §6.15 seven-field
  census, design's round-17 four-field correction, F-32's own header sentence,
  and the ratified fixture's `render_map` — and it is the permanent 0→1
  claim-limiting banner, the most Spine-load-bearing string in either schema.
  **My first draft of T-COPY-02c asserted it against `str.banner.01` on the
  premise that nothing asserted the quotation. The premise was false.**
  Demonstrating the red before proposing the clause (engineering's admission
  standard, which I registered the same round and therefore owed first)
  reddened three clauses, two of them shipped years of rounds ago in this
  board's terms: `test_zero_to_one_banner_mandatory` and
  `test_banner_attached_and_wording` both pin the banner byte-equal to
  `STRINGS["str.banner.01"]`. **The field was covered; the census was wrong** —
  which is the more interesting defect, because four enumerations by three
  seats all missed the same field and each was read by the others as complete.
  So the clause became what was actually missing (an exemption must cite a
  guard that EXISTS, checked by AST, not displayed in a comment), and the
  ratification question for `banner` is filed to design as this round's one
  demand. A duplicate assertion would have been cheap and dishonest; the
  retraction is written into the clause's own docstring where the false premise
  was going to live.
  (3) **T-COPY-03 — gtm's deletion trigger, executed as an instrument.** gtm
  deleted a presenter eyes-on check from the witness pre-flight on the strength
  of T-NEG-08 and asked for a per-line notification if that test is ever
  weakened, renamed, made skippable or removed. The duty is registered and
  owed; the guard is what makes it impossible to owe silently. T-COPY-03 reads
  this file's own AST: required clauses present by name, T-NEG-08 still an
  `ast.parse` census, the count still pinned at four, no skip marker on any
  clause, every `pytest.skip` in a helper naming its own subject (spec §27a
  applied PROSPECTIVELY to the newer file, not only retrospectively to the
  older one), and a counted floor of clauses that never skip.
  (4) **THE ADMISSION STANDARD IS REGISTERED AGAINST THE RESOLUTION-ROUND
  PROCEDURE (engineering's demand, accepted whole, P-15's row):** no further
  gate, command or check enters that procedure without a demonstrated red from
  the proposing seat. Paid on entry — eight mutations, scratch tree, no repo
  file mutated, tabulated in spec §27f, including the one that cost this seat
  a claim it had already drafted.
  (5) **T-VEND-06's ANCHOR (architecture's demand, verified here against
  `pyproject.toml` and this machine's dist-info RECORD before being written as
  fact):** the guard's authority is `ROOT / "configs"` with `ROOT` derived from
  the test file's own location, so it asserts mutual agreement among reachable
  copies anchored to whichever `configs/` sits beside `tests/` — the repo
  authority only in a checkout. Repo checkout: anchor is the authority.
  Unpacked sdist: RUNS, anchored on the sdist's own copy, no authority in the
  tree at all. Wheel install: **ABSENT, not skipped** — RECORD carries two YAML
  files, the `.pth`, four metadata entries, zero `tests/` entries. Written into
  the docstring and F-31, because only one of skip-versus-absence is ever
  observable by the person standing there.
  (6) **P-14 takes two clauses and neither weakens it** — sequencing's
  re-opened-sitting path is written as a PRECONDITION STEP (refresh the
  install, or confirm zero duplicate `configs` trees, THEN run the pre-flight)
  rather than as an exemption a presenter reads off a red at the hour; and
  decisions' D9 narrowing is registered with the two states distinguished:
  pre-flight, ANY red or skip means the sitting does not start; post-hoc, only
  the bound-copy clauses T-VEND-01/02/05 void a completed record, because D9's
  predicate is which copy was SERVED.
  Board state after round 18: F-17 (split a/b) is the last manual-pending row;
  **F-32 and F-33 move OPEN → PARTIAL with their authority question CLOSED**
  (F-33's STRUCTURAL 16 registered as permanently partial BY DECISION, design's
  ruling, with two named revisit events — a decision not to instrument is a
  decision, and it is not the same thing as a row waiting on nobody); one new
  demand (design: ratify `banner` or confirm the exemption); no open disputes.
  **Suite: 78/78 from the repo root AND 78/78 off-root**, own run (73 + 5).
  ROUND 19 (2026-09-01): **THE SUITE WAS RED WHEN I OPENED IT, AND THE RED WAS
  ON THE SPINE'S FIRST REFUSAL.** `pytest tests/` reported
  `1 failed, 79 passed` — `test_no_llm_or_network_imports`, N-01, gate P-1 —
  and it passed when run alone. That is the whole finding: the clause asserted
  `sys.modules` **of the pytest process**, which is not the product but
  whatever every previously-collected file happened to import, so its green was
  an artifact of collection order and its red was reachable on the unmutated
  repo by `pytest tests/test_packaging.py tests/test_engine.py` (run before any
  edit: FAILED, `httpx`). Two disclosures, in the order that matters. **First,
  the trigger was mine**: this seat's new `tests/test_audit_honesty.py` execs
  `app.py` to render the audit view for real, sorts before `test_engine`, and
  therefore imported gradio — which imports `httpx` — one file earlier than
  before. **Second, the defect was not mine and predates the file that exposed
  it**: the ordering red reproduces with my file deleted, because
  `test_packaging.py` has always loaded the app. A guard that reds on the order
  its own suite is invoked in is worse than a missing guard at the hour someone
  meets it — the honest reading of that red is "some other test imported
  gradio", and the fix a hurried reader reaches for is to delete the line.
  Corrected in the strengthening direction (spec §27i): the claim is asserted
  in a CHILD PROCESS — importing the engine in a fresh interpreter pulls in no
  LLM and no network client — which is order-independent, is the property a
  `pip install` can break, and catches a lazy `import_module("httpx")` that the
  regex source scan cannot see. Both reds demonstrated, control run beside the
  mutant. The gradio/UI half stays where it belongs (T-PKG-02 keeps gradio out
  of the engine; `test_no_network_calls_at_runtime` kills the socket), so
  nothing was narrowed away to make a red go away — the one move this
  correction could have been mistaken for.
  (2) **F-34 and F-35 REGISTERED on design's two demands** — the runtime-HTML
  rendering surface (`render_*` builders → `gr.HTML`), which every copy census
  on this board including this matrix's own rows has silently excluded; and the
  audit view's four POOLED-ACROSS-MODES statistics rendering one line above the
  caption that scopes itself to 0→1. F-34 is filed as design asked, as a SCOPE
  CLAUSE on the ruling they gave this matrix one round ago and this seat
  registered verbatim on their word — a seat narrowing its own ruling, in its
  own file, gaining nothing by it.
  (3) **THE OPEN ROWS GOT INSTRUMENTS THE SAME ROUND THEY OPENED**, which is
  this seat's agenda rather than a courtesy: T-NEG-09 asserts the 0→1
  no-prediction caption's ARRIVAL on the audit surface, both directions
  (deleting the `if log.n("zero_to_one")` gate left 78/78 green — the F-33
  defect one view over), and T-NEG-09b censuses the pooled statistics with an
  explicit classification, built to stay GREEN when engineering passes the mode
  through and to red when a FIFTH undisclosed pooled number joins the table. A
  guard that reds when someone repairs the thing it is about is a guard that
  gets deleted rather than heeded.
  (4) **DEMONSTRATION A RE-RUN, AND NARROWED AGAINST MY OWN NEW ROW.** Design's
  ζ finding reproduces exactly — displayed 1.00 → 0.00 with per-mode 1→N still
  1.00 — but only when the cross-mode re-comparison BOTH overwrites an edge AND
  closes a circular triad; this seat's first probe reversed a different pair and
  ζ did not move. The mechanism is design's and it holds; the wide sentence a
  later reader would quote does not reproduce, and it is corrected in the row
  and in the test file rather than left to be found. Demonstration B is cited as
  DESIGN'S and was not re-run here — what this seat verified is the structural
  half the row actually rests on.
  (5) **T-COPY-02e (spec §27h) — the banner's exemption now has a guard on its
  guard.** Design ruled `banner` in §6.19 by option (b): exempt from their
  fixture by AUTHORITY, with `app.py`'s import-time
  `assert Z2O.banner == S["str.banner.01"]` named as the instrument.
  Architecture is right that it is stronger than any diff written here — it
  fires before first paint, cannot acquire a skip, cannot be deselected — and
  that is exactly why it needed watching: it is a bare `assert` in a UI file,
  and deleting it left the entire suite green before this round (demonstrated;
  afterwards it reds exactly one clause and nothing else). T-COPY-02c's
  doctrine — an exemption must cite a guard that still exists — extended one
  rung, to the guard that is not a test.
  (6) **Both marks other seats asked for are on their cells and neither changed
  a position:** P-14's stripped-tree consequence is marked CONTESTED (D10, SLA
  2026-09-02) with this seat's reading kept at full strength beside it AND its
  cost written down for the first time (it makes tree SHAPE a de facto
  precondition of the gate); P-15 carries engineering's boundary on the
  red-first standard — it binds proposals that ADD A STEP, not proposals that
  FIX A SENTENCE, tested by whether the procedure's step count moves, because a
  correction taxed like a feature buys length while pretending to sell brevity.
  Sequencing's re-press is answered where they looked: clause (a) landed in the
  round their grep was run against, and the narrowing stays open to dispute
  rather than assumed agreed.
  Board state after round 19: F-17 (split a/b) is the last manual-pending row;
  F-32/F-33 partial; **F-34 and F-35 OPEN, each with a named owner, a closing
  condition and an instrument on the day it opened**; no open disputes; no
  demand outstanding on this seat. **Suite: 81/81 from the repo root AND 81/81
  off-root**, own run (78 + 3), and 61/61 on the two-file ordering that was red
  when this round began.
  ROUND 20 (2026-09-01, final round): **THE ROUND'S WORK IS THE RESIDUE OF LAST
  ROUND'S REPAIR, AND THE FIRST ITEM IS A FLOOR UNDER MY OWN FIX.** §27i
  strengthened N-01's guard and created, in the same edit, a one-token exit that
  did not exist before it: the clause's red now reads
  `importing the engine pulls in ['httpx']`, and the fastest way to clear it is
  to delete `"httpx"` from `FORBIDDEN_IMPORTS` — no test removed, no docstring
  touched, whole suite green, the Spine's offline promise unwatched from that
  minute. Design demanded the floor and set the constraint (may not shorten the
  tuple, may not add a skip); this seat wrote **T-NEG-01d** in the
  T-COPY-03 / T-VEND-07 pattern and paid the entry price first: four mutants —
  drop `"httpx"`, add `@pytest.mark.skip`, delete the source-scan half, delete
  the child-process half — **each reds T-NEG-01d ALONE, and in all four
  T-NEG-01a itself stayed GREEN.** That last column is the finding, not the
  test: the four cheapest ways to retire this board's loudest refusal were all
  invisible to the instrument that carries it.
  (2) **A SCOPE WORD ON A SENTENCE I WROTE ONE ROUND AGO** (decisions' demand,
  accepted whole). T-NEG-01a's docstring ended *"the source scan is unchanged
  and still covers `app.py`"* — true of the TEXT, false of the GRAPH, because
  the scan is a regex over DIRECT import lines while the probe's subject is the
  engine only. `app.py`'s transitive graph is asserted by nothing there, and
  that is correct rather than a hole (app.py → gradio → `httpx` is a legitimate
  UI dependency; T-NEG-01b's socket kill-switch holds the runtime claim on that
  surface). The false sentence is struck in place with its text legible. This is
  the sixth instrument-scope correction of the cycle and the second one where
  the over-wide sentence was this seat's own.
  (3) **T-NEG-08c — the residue design DECLARED rather than papered over.**
  `"Which do you actually pick?"` had zero instruments between gtm's correct
  retirement of the eyes-on pre-flight (round 17) and this round; design struck
  their own "covered in the interim" sentence in place and refused gtm's offer
  to reinstate a ritual to cover a gap the retirement revealed. It lands as its
  OWN clause — byte-exact, count-pinned at one, carrier pinned to `gr.Radio` —
  never as a fifth member of T-NEG-08's set, because that set's `== 4` pin is
  load-bearing and because widening it would silently widen engineering's
  bounded ENG-COPY-EVALLABELS-01 trigger. Two mutants, each reddening it alone.
  (4) **ENGINEERING'S DEMAND TAKEN AS FILED, AND IT IS AN ERROR MESSAGE RATHER
  THAN A GATE** — which is the boundary this seat registered on their behalf
  last round, applied to a proposal aimed at this seat. The design fixture's
  third observable state (present but unreadable) stays a RED and now names its
  owner at the point of failure: whose file it is, that the first action is to
  re-run, and that blanking it to obtain a skip trades a loud red for a quiet
  green. Engineering OBSERVED the state and priced the class without mutating a
  repo file (855 of 8593 prefixes fail to parse); demonstrating the red found
  what the demand had not — a truncated save can cut a multi-byte character and
  raise out of `read_text` before pyyaml is reached, so `UnicodeDecodeError` is
  caught beside `yaml.YAMLError`.
  (5) **ARCHITECTURE'S CITATION ALIGNMENT ON F-32, no test touched**, and it
  cuts both ways at once: T-COPY-02's population is WIDER than this row's
  sentence (all NINE declared config text names are diffed, rendering or not —
  four are declared-and-dead today and are diffed anyway) and NARROWER by one
  rendering field (`banner`, which routes to Authority A by design's §6.19
  option (b)). The row's "seven fields" numeral is struck with the false figure
  legible. The activation asymmetry is recorded as measured: in an sdist-shaped
  tree the fixture-governed pair SKIPS while the cross-referenced clauses and
  the banner's engine clauses run — **the one field that delegates to the
  catalogue is the one whose authority survives off a checkout.**
  Board state after round 20: F-17 (split a/b) is the last manual-pending row;
  F-32/F-33 partial with their citations now scoped in both directions;
  F-34/F-35 open with instruments and named owners; no open disputes; the three
  demands filed on this seat this round (architecture, engineering, decisions)
  are executed as filed, and design's two are executed with the floor clause
  written to their constraint. **Suite: 83/83 from the repo root AND 83/83
  off-root**, own run (81 + 2); gate P-1's `-k` form 3 passed / 80 deselected
  (T-NEG-01d is inside the selection — verified, not assumed); gate P-15's file
  12 passed / 0 skipped in a checkout and 10 passed / 2 skipped in an
  sdist-shaped tree; `pytest tests/test_audit_honesty.py tests/test_engine.py`
  48/48, the ordering pair that was red two rounds ago. Those are this minute's
  readings, not a stability claim — the lesson this seat has now been taught
  twice by its own file.
  Artifact and test columns cite the real shipped files and as-built test names.
  Updates required on any Spine version bump.
maintainer: Compliance Leaf (this file); verification owners named per row

Per the Spine's Traceability Anchor: **every element of every Leaf maps back to a
commitment on the Spine page. Anything in a Leaf that does not map back is scope creep
or a missing Spine update.** This matrix is the enforcement instrument. It covers both
directions:

1. **Positive traceability** — every In-scope feature and Success Metric maps to a
   Spine commitment, a concrete artifact, and one or more test cases with a named
   verification owner.
2. **Negative traceability** — every deliberate refusal ("Out — refused") maps to a
   **negative test**: a test that fails if the refused capability ever appears.
   A refusal without a negative test is a refusal on the honor system.

Test IDs are defined in `/tests/test_engine_spec.md` (normative spec, incl. the
§0.1 deviation register) and implemented in `/tests/test_engine.py` (pytest;
no mocks of the engine). Owner keys are Leaf keys: `engineering | design | gtm |
architecture | sequencing | decisions | compliance`. "Owner" means: the leaf that
must demonstrate the row is verified before release; compliance audits, it does
not substitute.

Status vocabulary: `verified` = automated test implemented and green;
`partial` = implemented with a stated remainder; `manual-pending` = release-gated
manual check not yet executed; `manual-FAILED` = release-gated manual check
executed and failed (release-blocking until the fix lands AND the check re-runs
— a failed check never flips to verified on the fix alone); `pending` = blocked
on a decision; `GAP` = a committed mechanism not present (or proven void) in
the shipped build (integrator action needed).

Manual results source of record: a manual check flips a row ONLY against a
citable per-check-ID result. Current citations: **states.md §6.5, browser
render session 1, 2026-08-30** (M-UX-01 PASS · M-UX-02 PENDING · M-UX-03 FAIL
· M-DOC-01 PASS) and **states.md §6.7, browser render session 2, 2026-08-31**
(R-8 acceptance PASS ×4 · M-UX-01 re-check PASS · R-9 nested-element FAIL
= R-9b · amber strips PASS · M-UX-03 FAIL stands · M-UX-02 schedulable)
AND **states.md §6.9, browser render session 3, 2026-08-31** (R-9b rows
(a)–(e) + overall PASS · S5 whole-screen parity PASS · M-UX-03 FAIL stands,
third row, with clipping-ancestor mechanism evidence + fixed-fallback
viability · M-UX-02 light-theme rider lifted)
AND **states.md §6.11, browser render session 4, 2026-08-31** (M-UX-03
single-check PASS — banner rect in viewport at scrollY 1500, computed
position:fixed · height-reservation rider PASS · opaque-background rider
PASS · R-10(i) singular live PASS · corrected stale tail live PASS ·
R-12 classification sign-off explicit).
A narrative summary never flips a row — and a browser FAIL outranks a green
static pin over the same surface, in both directions and every round.

---

## 1. Commitment register (Spine anchors)

Every matrix row cites one of these IDs. Quotes are verbatim from `/spine/SPINE.md`.

| ID | Spine section | Commitment (verbatim anchor) |
|---|---|---|
| SC-01 | The Problem | Remove judgment noise: "the same PM disagrees with themselves across occasions" — the tool must judge more consistently than the PM. |
| SC-02 | The User | "Is not a statistician and should never need to be." |
| SC-03 | Solution Direction | "Two ideas enter on one standard questionnaire, on one screen, in one sitting." |
| SC-04 | Solution Direction | "Out comes the winner, a win probability with an interval, and the specific levers that would flip the verdict." |
| SC-05 | Solution Direction | "The runtime model is a traditional offline model — weights and a bias term, no LLM, no API key." |
| SC-06 | Success Metrics | "A PM completes a full A-vs-B comparison, from blank questionnaire to verdict card, in under 5 minutes." |
| SC-07 | Success Metrics | "Runs entirely offline after download: no API key, no server-side storage, log fully in the user's hands." |
| SC-08 | Success Metrics | "Model-of-the-judge activates from the user's own log by roughly decision 10; ζ and Brier accumulate from decision 1." |
| SC-09 | Success Metrics | "The verdict is honest by construction: intervals shown always, 'too close to call' when the interval straddles 50%, and 0→1 mode never claims predictive accuracy." |
| SC-10 | Scope Boundaries (In) | "Pairwise valuation of exactly two ideas." |
| SC-11 | Scope Boundaries (In) | "Two modes (0→1 search, 1→N allocation) with GenAI-specific factor sets." |
| SC-12 | Scope Boundaries (In) | "Decision log (JSONL, downloadable)." |
| SC-13 | Scope Boundaries (In) | "Leverage panel ('path to parity', lever-vs-fact filter, fragility flag)." |
| SC-14 | Scope Boundaries (In) | "Hugging Face Gradio Space plus pip-installable repo." |
| SC-15 | Scope Boundaries (Out) | Refusals block, plus: "A judge that overstates its confidence is worse than no judge... Every Leaf must preserve that refusal." |

Refusal sub-IDs under SC-15:

| ID | Refusal (verbatim) |
|---|---|
| R-01 | "any LLM in the runtime loop" |
| R-02 | "ranking more than two ideas at once (v1 is strictly A-vs-B)" |
| R-03 | "portfolio/knapsack automation (flagged, not decided)" |
| R-04 | "accuracy claims in 0→1 mode" |
| R-05 | "evaluative factors (brand, strategic fit) inside the mechanical score — they are captured and displayed as labeled override inputs only" |
| R-06 | "server-side storage of any user data" |

---

## 2. Positive traceability — In-scope features

| Row | Feature (committed) | Spine anchor | Spec anchor | Artifact (real path) | Test case(s) | Verification owner | Status |
|---|---|---|---|---|---|---|---|
| F-01 | Single-screen pairwise questionnaire: both ideas scored together, one sitting (occasion-noise cancellation) | SC-01, SC-03, SC-10 | §1 | `app.py`; `leaves/design/states.md` | T-NEG-02 (exactly-two-ideas surface, `test_strictly_two_ideas`); manual M-UX-01 | engineering (T), design (M) | verified — T green; M-UX-01 PASS (states.md §6.5, 2026-08-30). Input-blocking on the same screen is NOT covered by this row: see F-28 (verified round 5 via T-SER-01) |
| F-02 | Mode toggle: 0→1 vs 1→N, each with its own GenAI factor schema loaded from editable config | SC-11 | §1, §2 | `configs/one_to_n.yaml`, `configs/zero_to_one.yaml`, `pairwisepm/config.py` | T-CFG-01 (`test_config_shapes`, `test_zero_to_one_banner_mandatory`); T-CFG-02 (`test_weights_are_config`) | engineering | verified |
| F-03 | M0 mechanical score: p = σ(wᵀd), d = z_A − z_B, zero intercept for scoring | SC-01, SC-04, SC-05 | §3 | `pairwisepm/engine.py` (`compare`, `_score`) | T-M0-01; T-SYM-01 (fixture + 0→1 + 50-vector property); T-EQ-01 | engineering | verified |
| F-04 | M1 ridge logistic Bradley-Terry, shrinkage centered on M0 prior weights, activates at exactly 10 decisions | SC-08 | §3 | `pairwisepm/engine.py` (`fit_m1`, `M1_ACTIVATION_N = 10`) | T-MAP-01..04b; T-SHRINK-01/02; T-ACT-01 | engineering | verified |
| F-05 | Zero-intercept scoring constraint + free-intercept diagnostic (presentation-order bias, Wald z, surfaced in audit) | SC-01, SC-09 | §3 | `pairwisepm/engine.py` (`M1Fit.free_intercept`, `order_bias_flagged`) | T-SYM-01/-m1; T-BIAS-01/02 | engineering | verified |
| F-06 | Bootstrap interval on win probability; straddling 50% ⇒ "too close to call", never a forced winner | SC-09 | §4 | `pairwisepm/engine.py` (`_bootstrap_interval`, verdict rule); copy in `app.py` / `leaves/design/states.md` | T-VERDICT-01 (rule consistency property), -02 (near-tie & clear-winner end-to-end), -03 (interval always present) | engineering (T), design (copy) | verified — see DV-1 (§0.1 of spec): exact-boundary behavior flagged |
| F-07 | ζ (Kendall coefficient of consistency) from circular triads, live per-judge noise meter | SC-08 | §4 | `pairwisepm/log.py` (`DecisionLog.kendall_zeta`) | T-ZETA-01 (intransitive ⇒ 0), -02 (transitive 3- and 4-sets ⇒ 1), -03 (small-n ⇒ None, never fabricated) | engineering | verified — DV-2: majority-direction edge policy ratified |
| F-08 | Brier vs pick from decision 1; outcome-Brier separate and null-gated | SC-08 | §4 | `pairwisepm/log.py` (`brier`, `outcome_brier`) | T-BRIER-01 (hand case 0.21666…), -02 (n=1 and empty), outcome-separation test | engineering | verified |
| F-09 | Leverage panel: per-factor signed contribution bars w_j·d_j | SC-04, SC-13 | §5.1 | `pairwisepm/engine.py` (`leverage_panel`); `app.py` render_leverage | T-PAR-01 (contributions sum to logit) | engineering | verified |
| F-10 | Path to parity: smallest single-factor change to 50/50 (and 60/40), RAW units, levers only, plausible range only; all-facts ⇒ loses-on-fundamentals | SC-04, SC-13 | §5.2–5.3 | `pairwisepm/engine.py` (`_parity_target`, `ParityPath`) | T-PAR-01 (1.04σ / 1.248 raw arithmetic), -02 (facts never proposed), -03 (out-of-range ⇒ feasible:False, target None — DV-6 ratified), -04 (fundamentals fixture) | engineering | verified |
| F-11 | Fragility flag: margin flips on small plausible single-factor move ⇒ re-estimate warning | SC-09, SC-13 | §5.4 | `pairwisepm/engine.py` (`FRAGILITY_Z = 0.75`) | T-FRAG-01 (fragile at 0.4σ, names factor, message), -02 (robust at 1.04σ) | engineering | verified — 0.75 is the build-meanwhile default; threshold is live decision **D6** (pending); T-FRAG fixtures regenerate on resolution |
| F-12 | Ceiling flag (0→1): unweighted, routes to human portfolio judgment, NEVER enters the score | SC-11, SC-15/R-03 | §2 | `configs/zero_to_one.yaml` flags; `pairwisepm/engine.py` ceiling_notes | T-CEIL-01 (bitwise score invariance), -02 (routing note text) | engineering | verified |
| F-13 | Decision log: local JSONL, download/upload, full §6 record schema incl. raw+z, evaluative, both model outputs, override rationale, null outcome slot | SC-07, SC-12 | §6 | `pairwisepm/log.py` (`make_record`, `DecisionLog`) | T-LOG-01 (full-precision unicode round-trip + bad-file rejection), -02 (schema completeness, override recorded), -03 (re-read log alone reconstructs M1/ζ/Brier) | engineering | verified |
| F-14 | Equal-weight ablation toggle (all \|w\| equal, signs kept) as scientific control | SC-01 | §3 | `pairwisepm/engine.py` (`effective_weights(equal=True)`, `m0_equal`) | T-SYM-02/T-ABL-01 | engineering | verified |
| F-15 | M1-vs-M0 divergence display: revealed vs stated policy | SC-01, SC-08 | §3 | `pairwisepm/engine.py` weights; `app.py` render_ladder | T-ACT-01 (per-factor divergence computable at activation); render is UI-layer (engineering smoke suite) | engineering | verified (engine) / partial (UI render manual) |
| F-16 | Pip-installable package + HF Space files | SC-14 | §7 | `pyproject.toml`, `requirements.txt`, `app.py` (module-level `demo`), `configs/` | T-PKG in `tests/test_packaging.py` (`test_package_version_matches_pyproject`, `test_space_files_ship`, `test_readme_hf_yaml_header`, `test_app_module_level_demo` — PASSES under gradio 6.26.0, importorskips elsewhere); clean-venv `pip install .` stays a release-gate step (needs network) | engineering (build), sequencing (release gate) | verified (suite) — pip-install + live-Space sdk_version check remain at push |
| F-17 | Under-5-minute blank-to-verdict completion | SC-06 | §1 | `app.py`; `leaves/design/states.md`; `tests/test_packaging.py::test_no_unearned_five_minute_claim_in_shipped_copy` | M-UX-02a (1→N timed walkthrough) + M-UX-02b (0→1 timed walkthrough); T-NEG-07 (shipped-copy claim tripwire) | design (run), gtm (witness) | manual-pending — **the LAST manual-pending row in the matrix** (round 10). **ROUND-13 SCOPE CORRECTION (compliance's own read, self-reported):** this row defined M-UX-02 as "both modes", but BOTH pre-registered instruments measure ONE mode — gtm's 1c-i template fixes `mode: 1→N` and design's §6.12 protocol fixes "one blank-to-verdict 1→N run". The round-12 registration therefore priced a one-mode measurement as discharging a two-mode check. Corrected, not softened: the check SPLITS into **M-UX-02a (1→N)** — the mode both instruments already cover — and **M-UX-02b (0→1)**, which has no instrument and no scheduled sitting. A filled 1→N record flips F-17 to **verified (1→N measured)** and nothing wider; SC-06's payload claim must then NAME the measured mode. The unqualified both-modes claim stays unconverted until an 0→1 record exists, and 0→1 keeps the canonical phrase "designed so, not yet timed". Splitting the check does not lower the bar on either half — it stops one measurement from paying for two claims. Fully unblocked; witness slot NAMED (gtm: today 2026-08-31, first design sitting, backstop first hour of 2026-09-01 — inside sequencing's window). SC-06 converts to verified ONLY on a dated timed record with the named witness; needs a fresh human user, not agent-self-runnable. **Evidence vehicle REGISTERED round 12**: the pre-staged witness-record template (gtm launch-copy.md 1c-i — six fields, both seats' timer numbers, coaching-given line, PASS/FAIL vs 5:00) is the agreed flip instrument, mirrored by design's §6.12 protocol; a filled record flips this row as a read. **Recordless branch pre-registered**: window closes unfilled ⇒ row stays manual-pending, SC-06 stays "designed so", miss recorded as a dated scheduling fact — no softening; a voided record (coaching beyond mode selection, non-fresh user) counts as no record. **ROUND-14: THE OUTCOME SPACE IS THREE DATED BRANCHES, NOT TWO** (design's §6.13 demand + gtm's row-4 branch block, both read verbatim from this seat and both accepted in full): **(A) PASS** — filled six-field record, elapsed ≤ 5:00 ⇒ F-17 flips to *verified (1→N measured)*, SC-06 reads the measured number NAMING the mode. **(B) MEASURED, TARGET MISSED** — filled record, elapsed > 5:00 ⇒ F-17 flips to **`measured-FAILED (1→N)`**, a first-class registered state, NOT a fallback to manual-pending and NOT "designed so": SC-06 then reads *"measured at &lt;m:ss&gt; in 1→N, over the 5:00 target"*. **The metric is never re-defined to fit the number** — a build that measured and missed has told the user more than one that never measured, and collapsing (B) into (C) would destroy exactly that information. The 5:00 bound, the clock definition and the voiding rule are all fixed BEFORE the number is known, which is what makes (B) trustworthy. **(C) WINDOW CLOSED** — backstop passes unconvened ⇒ F-17 stays manual-pending, SC-06 keeps the canonical string *"designed so, not yet timed"*, and the miss lands as gtm's registered verbatim line: *"M-UX-02 window closed unconvened, [date/time] — no sitting convened, no record exists; designed so, not yet timed."* **(C) is an EXPIRED SLOT, not a terminal FAIL** (gtm's demand, accepted): it records that this slot expired, never that the five-minute claim was tested and lost — that would be the opposite overstatement, and the distinction between (B) and (C) is precisely what keeps it honest. M-UX-02 stays **convertible** by any later newly-scheduled witnessed run under the identical protocol (same six fields, same clock definition, same voiding rule). Registered as the presenter-facing half: gtm's row-4 branch block (launch-copy.md §0) pre-writes the exact claim-ledger Basis text for all three branches, so the ledger flips by swap and no fourth wording can be improvised — a truthful matrix behind a stale "pending" ledger row would be a truthful matrix behind an untruthful pitch. gtm's 1c-i also now states the mode scoping this leaf demanded in round 13 (verified verbatim: "A filled record converts SC-06 FOR 1→N ONLY"; 0→1 stays "designed so, not yet timed" on every branch). **ROUND-15 — VOIDING CONDITIONS REGISTERED, WITH ONE CAUSE CORRECTED (gtm's demand: accepted on substance, refused on its stated mechanism).** (i) **A VOID IS NOT A FAIL, and it is registered inside this row rather than as a fourth state:** a sitting that never produced a measured blank-to-verdict run — the app failed to reach S1, the record is partially filled, coaching went beyond mode selection, the user was not fresh — yields **NO RECORD**. It routes to branch (C)'s dated miss line **with its cause named in the narrative**, and it is explicitly **NOT branch (B)**. Recording a build or logistics accident as `measured-FAILED (1→N)` would tell a reader the five-minute claim was tested and lost when it was never tested — the exact mirror of the overstatement this row's three branches exist to prevent. (ii) **Reconciliation registered so no fourth state is invented at the window's close** (architecture's "dated void with the cause named" + design's §6.13 "no third branch", both satisfiable at once): **cause-in-the-narrative, three-valued-in-the-ledger.** The ledger has exactly three Basis texts (A/B/C) and gains no fourth; a void lands on (C)'s row and carries its cause as a note. (iii) **The mechanism gtm stated is NOT registered, because this seat could not reproduce it and re-derived the opposite:** "launched outside the repository root ⇒ binds the stale copy ⇒ dies before first paint" is false for the documented launch — `python /abs/path/app.py` puts the SCRIPT's directory on `sys.path[0]`, not the working directory (sequencing's disconfirmation, independently re-derived here), and as of the round-14 editable install there is no stale copy to bind from any entry point. A voiding condition written against a false mechanism is an **untestable clause inside the instrument that decides a Spine metric**: it would void good records for the wrong reason and wave through a bad one arriving by another door. (iv) **Registered instead in the form that is true AND machine-checkable** — design's formulation, which names the condition rather than a symptom: *a run whose bound module is not the design authority's copy produces NO RECORD.* That is no longer a judgement call at the hour: **new gate P-14** makes `pytest tests/test_vendoring.py` a pre-flight for the sitting, and the witness record carries its result. The witness records **a test outcome, not a guess about directories**; gtm's working-directory field stays as a free disambiguation datum, which is what sequencing already encoded. **ROUND-15 — M-UX-02b's DISPOSITION NOW CITES A DECISION, NOT AN ABSENCE** (decisions' demand, accepted): the b-half reads **"open — D8 (SLA 2026-09-02)"**, not "no instrument, no scheduled sitting" full stop. Both descriptions are true; only one has an owner. This matrix's standard is that a row's state rests on a citable artifact, and the b-half was the single cell where the state rested on nobody having asked — a permanent deliberate non-measurement recorded before any ruling existed to cite. Option 1 (leave 0→1 unmeasured) may well win; it then wins as a decision somebody made. **D8 does not gate this row, does not defer the D1-D6 resolution round, and changes no branch text**. **ROUND-16 — THE CONTESTED MECHANISM IS RETRACTED BY THE SEAT THAT AUTHORED IT; DISPUTE B5 CLOSES WITHOUT THIS MATRIX PICKING A SIDE.** gtm re-reproduced the launch hazard from their own seat, found the defect fixed AND their round-14 mechanism overbroad, and withdrew the clause they had asked this row to carry — against their own finding, in their own file, rather than narrowing it quietly. Three seats independently reached the same measurement (`python /abs/path/app.py` sets `sys.path[0]` to the SCRIPT's directory, not the cwd): sequencing by disconfirmation, this seat by re-derivation, gtm by their own probe. **What this row registers is therefore unchanged from round 15 and is now reached by convergence rather than by refusal:** a run whose BOUND MODULE is not the design authority's copy produces NO RECORD — routed to branch (C)'s dated miss line with its cause named, never branch (B), never a FAIL — and the check is **gate P-14, `pytest tests/test_vendoring.py`**, run on the machine that will run the app and recorded in the witness template. **Answering decisions' D9 from this file's side, and only from this side** (their demand, honored — this matrix did NOT register gtm's predicate as settled and does not rule on the entry): design's voiding condition **is CHECKED, not a statement of principle**, and its instrument is named above. D9's three-way disagreement has narrowed by one seat's retraction, not by the matrix resolving it; if D9 still rules, the ruling lands on this row as a read. **Round-16 strengthening of that instrument, which matters here rather than only in F-25:** P-14's guards were skipping in every installed tree (spec §27a). A pre-flight that returns green because it never ran would have handed a witness sitting a false clearance and produced a record this row would then have flipped on — the exact failure mode P-14 exists to prevent, arriving through the instrument itself. T-VEND-03/04/06 now run wherever their subject exists; T-VEND-05 never skipped |
| F-18 | README epistemics: priors are stated editable policy; 0→1 no accuracy claim; "the LLM's job was at build time" | SC-05, SC-09 | §7 | `README.md` | T-PKG-02c (`test_readme_epistemics_substrings` in `tests/test_packaging.py` — GREEN against the shipped README); M-DOC-01 checklist | gtm (author), compliance (review) | verified — T green; M-DOC-01 PASS (states.md §6.5: all three commitments verbatim in README.md) |
| F-19 | 0→1 permanent structure-not-prediction banner | SC-09, SC-15/R-04 | §1, §4, §22, §22b | `configs/zero_to_one.yaml` banner (loader REFUSES a bannerless 0→1 config); engine attaches to every result; `app.py` renders permanently + **position:fixed** (`#pwpm-banner` fixed/top/left/right/z-index rule via elem_id + Blocks css, §22b fallback LANDED round 9) with in-flow height reservation (`BANNER_SPACER_HTML`, hidden content-exact duplicate FIRST in layout, toggles with the banner) | T-CFG-01b (loader refusal); T-NEG-04 (banner always on 0→1 results, never on 1→N, no accuracy wording); **T-BANNER-01 REWRITTEN per §22b in the SAME change as the fallback** (`test_banner_scroll_persistent_static` — pins fixed+top+left/right+z-index, spacer presence, content-exactness, spacer-toggles-with-banner wiring, css wired into served Blocks; red-first by construction against the prior sticky build; docstring names session 4's browser check as acceptance owner); M-UX-03 (behavioral acceptance) | engineering (T + fix, delivered), design (M, session 4 delivered) | **verified — BROWSER-CONFIRMED round 10** (states.md §6.11, render session 4, 2026-08-31): the single §22b acceptance check PASSED — banner rect top 0 / bottom 77.2 fully within the 792px viewport at scrollY 1500 (and at max scroll), computed `position: fixed`, served 0→1 dark theme — after THREE prior FAILs (§6.5/§6.7/§6.9) and two defeated mechanisms. The row flipped on exactly the pre-stated check, never on the green guard. Height reservation and opaque background verified live (spacer 77.2 = banner height; no ghosting). T-BANNER-01 stays as the permanent §22b regression pin; a future FAIL routes as a defect against the accepted commitment. **ROUND-14 DELIVERY-SIDE INSTRUMENT REGISTERED (engineering's demand, spec §25, T-DELIV-01a/b):** the pin `position:fixed live at app.py:769` evidences the rule is **WRITTEN** — a separate claim from the rule being **DELIVERED**, and until round 14 every M-UX-03 artifact on the board was of the first kind. Verified from this seat, thinner than reported: on the constructed Blocks **`demo.css` is `None`**; the rule survives only in the private `demo._deprecated_css`, read by `launch()` at `gradio/blocks.py:2785`. A gradio major dropping that fallback serves the banner unstyled — no exception, every static pin green, §22b's browser-confirmed acceptance silently void. The major bound `gradio>=6.0,<7` (present in BOTH `requirements.txt` and `pyproject.toml [app]`, matching README `sdk_version: 6.26.0` — all verified this round) is the delivery evidence, and **T-DELIV-01 is its instrument**: 01a pins the bound in both declarations (a bare `>=X` is not a bound; a `!=` exclusion is not a bound), 01b pins that the CSS is on the object gradio actually serves and that the fallback still exists in the installed runtime. Widening the bound now reads as EVIDENCE LOSS and routes to a new render session, rather than passing as dependency housekeeping |
| F-20 | Prior weight magnitudes per D1/D2 — build on defaults, weights are config | SC-11 | §2 (PENDING SIGN-OFF) | `configs/*.yaml`; `leaves/decisions/decisions.yml` | T-CFG-01 pins the shipped defaults == spec §2 tables (regenerate on resolution); gate G-D1D2 | decisions (resolve), sequencing (gate) | pending D1, D2 |

### Exchange-round additions

| Row | Feature / mechanism | Spine anchor | Artifact | Test / check | Owner | Status |
|---|---|---|---|---|---|---|
| F-21 | **config_fingerprint in every log record** — partitions audits by policy version (architecture §4.1 data contract) | SC-08, SC-12 | `pairwisepm/config.py` (`config_fingerprint`, `ModeConfig.fingerprint` — sha256 over the canonical parsed YAML, format-insensitive, policy-sensitive); `pairwisepm/log.py` (`make_record(..., config_fingerprint=)` — null for pre-v1.1 callers); `app.py` stamps it on every logged decision | T-FPR (`test_config_fingerprint_stamped_and_canonical`: hex shape, per-mode distinctness, reformat-invariance, policy-sensitivity, stamping, pre-v1.1 tolerance) | engineering (implemented at integration), architecture (contract) | verified — GAP closed 2026-08-30 (DV-10 resolved in favor of implementing; `decisions.sample.jsonl` predates the key and doubles as the ignore-missing-key fixture) |
| F-22 | Honesty-gates-last invariant: verdict suppression (too_close) is applied at scoring, so no layer can render a suppressed winner | SC-15, SC-09 | `pairwisepm/engine.py` (`_score` sets verdict; `leverage_panel` refuses parity coaching on too_close); `app.py` renders only `result.active.verdict` | T-VERDICT-01/02 (verdict = rule, paths empty on too_close); design invariant S4 | engineering, design | verified (engine); UI side rides engineering's app-handler smoke suite |
| F-23 | requirements.txt whitelist as the no-LLM/no-network enforcement artifact | SC-05, SC-07, R-01 | `requirements.txt` (numpy, PyYAML, gradio only) | T-NEG-01c (whitelist), T-NEG-01a (import scan), T-NEG-01b (socket kill-switch) | engineering, compliance (audit) | verified |
| F-24 | Session-only log custody (gr.State; no HF persistence) as the no-server-storage enforcement artifact | SC-07, R-06 | `app.py` (log in `gr.State`, moves only via user download/upload through tempfile) | T-NEG-06 (`test_no_server_side_persistence_static` in `tests/test_packaging.py`: no DB/HF-persistence imports, gr.State present, tempfile downloads only, zero file writes in the engine package) | engineering, compliance (audit each release) | verified (static); behavioral session check M-UX-04 added to audit protocol |
| F-25 | **One-way string vendoring, byte-identical** — `leaves/design/strings.py` is the copy authority; `pairwisepm/strings.py` a verbatim mirror (architecture §4.2; serves the SC-09 honesty-copy chain states.md → config → tests) | SC-09, Traceability Anchor | `tests/test_vendoring.py` (engineering-implemented, per architecture's round-2 demand) | T-VEND-01 (`test_vendored_strings_byte_identical_to_design_copy`) — spec §17. Drift was OBSERVED, not hypothesized: additive keys 22:08, re-vendored 22:11, 2026-08-30; the boundary is no longer honor-system. **FIRST LIVE CATCH (R-10 mint, rounds 8–9): design's canonical edit turned the guard red mid-flow — the guard holding a coordinated change open, flow-conformant, distinct in kind from the round-2 drift episode — and engineering's byte-identical re-vendor closed it in the SAME change, the documented direction. Byte-identity re-verified round 9 from this seat (cmp: identical), and again round 10. **The boundary's arc, registered with DIRECTION so a flow-conformant red is never mistaken for a regression: drift-episode (round 2, honor-system failure observed live) → test-enforced (round 3, T-VEND-01 + P-9) → FIRST LIVE EXERCISE CLEAN (round 9, catch-and-release in the documented direction) — same guard red in rounds 2 and 8-9, opposite meanings, and the ledger says which is which**. **ROUND-14 GUARD-SCOPE CORRECTION (architecture's A-13-01, independently reproduced from this seat):** T-VEND-01 compares two paths it constructs from its own `__file__` and **never imports the module it guards**, so it certified the mirror-on-disk while an off-root interpreter bound an undeclared THIRD copy — a non-editable venv install, drifted at line 79 (no `str.empty.example_cta`, which `app.py:848` reads at layout construction; still carrying the pre-R-10 `"Recomputing…"` tail F-30 exists to kill). The guard reported PASS from either directory. Closed on BOTH halves the same round: the environment fix verified from this seat (`direct_url.json` now `editable: true`, `site-packages/pairwisepm/` gone, off-root bind resolves in-repo), and the guard scope closed in this leaf's own files by **T-VEND-02** (bound module identity + bytes) and **T-VEND-03** (loaded config dir — the wheel force-includes `configs/`, where D1/D2 resolve). Red-first shown at the predicate level with T-VEND-01 GREEN in the same run. T-VEND-01 is RETAINED unchanged: it honestly claims rule-APPLIED. **ROUND-15 TERMINAL-LINK SCOPE WORD (design's §6.14 demand, adopted verbatim and applied to every copy-integrity row on this board, including the ones design supplied):** the copy chain is states.md → strings.py → vendored copy → **BOUND MODULE** → browser, and therefore **file-identical is not copy-delivered** — any row whose artifact is a `cmp` of two paths is scope-limited exactly as T-VEND-01 was. This seat extends the word one notch, because the round-14 fix did not reach as far as it appeared to: **copy-delivered-in-a-checkout is not copy-delivered-on-an-install.** T-VEND-01/02 both SKIP when the design leaf is absent — the stripped install a user actually receives — so on that build nothing asserted anything about served copy at all. **CX-14-01 REGISTERED AND CLOSED THE SAME ROUND, on an artifact rather than on a re-run:** design's finding (a bindable copy carrying the pre-R-10 `"Recomputing…"` tail — R-10's own confidence overstatement live in served copy, distinct in kind from A-13-01's packaging defect) is no longer reachable on this machine — verified from this seat: the off-root bind is in-repo and its `str.verdict.stale` reads *"…Press Compare to recompute."* — and its recurrence is now guarded by **T-VEND-05** (spec §26), a value-level pin on the bound module that NEVER SKIPS. Closing it on a passing test rather than on any seat's memory is the difference design's own demand was pointing at: an editable install with a stale build artifact still binds bad copy, and only a value assertion catches it. **ROUND-16 SCOPE WORD, ONE LEVEL WIDER (design's §6.15 demand, accepted and applied to every copy-integrity row on this board including the ones this seat authored): this row's verified state is scope-limited to THE CATALOGUE'S STRINGS.** Every artifact it cites — a catalogue diff, a mirror `cmp`, a bound-module check — speaks about `leaves/design/strings.py` and its vendored copy, and about nothing else that renders. It does NOT cover `configs/*.yaml`'s seven rendered text fields (**F-32**) or the 20 literals in `app.py` (**F-33**), and so no reading of this row supports a general "copy integrity: verified". Every "nothing rendered changed" this seat certified from round 9 onward was true of the catalogue and untested for both other populations; that is stated here rather than left for a later audit. **ROUND-16 CENSUS ASYMMETRY (architecture's demand, accepted):** the two instruments this row shares with F-31 are NOT instances of one rule — **T-VEND-04 is a COUNT invariant whose scope is the PACKAGE authority only** (`pairwisepm/__init__.py` across `sys.path`), while **T-VEND-03 is a RESOLUTION invariant on the CONFIG authority, where a second copy is permitted by design**. Compressing them into "exactly one copy of everything" would either demote the package count to a preference or invite deleting the wheel's `force-include`, which is what lets an installed package find its schemas at all. Both docstrings now carry the distinction, so the asymmetry survives a reader who never opens this file. **ROUND-16 ACTIVATION FIX:** T-VEND-01/02 keep the design-leaf skip — correctly; that file IS their subject — while T-VEND-03/04/06 no longer gate on it (spec §27a) | engineering (re-vendor + editable install), compliance (guard scope + T-VEND-05 + skip predicates), architecture (contract, census), design (copy authority, CX-14-01, scope word) | verified — at the disk level (T-VEND-01), the bound-module identity level (T-VEND-02/03, spec §24, round 14) and the **served-value level (T-VEND-05, spec §26, round 15, no skip)**. **Arc:** drift-episode (r2) → test-enforced (r3) → first live exercise clean (r9) → guard-scope defect found and closed (r14) → **fifth stage: terminal link instrumented where it actually ships (r15, T-VEND-05, no skip)**. The boundary was never breached; the instrument was narrower than the claim it was carrying, and the ledger now says so |
| F-26 | **Custody nudge counts session appends only** — `{n_session}` in `str.log.unsaved_nudge` = records appended this sitting, never total log size; suppressed at 0 (design S10b binding; states.md §6.4 R-1) | SC-07, SC-15 | `app.py` (`render_audit(log, n_session)`, `do_log`/`do_upload` thread the session count) | T-CUST-01 (`test_custody_nudge_counts_session_appends_only` in `tests/test_packaging.py`, gradio-gated) — spec §18; incl. end-to-end upload-only-session ⇒ no tab-only claim | engineering (fix, landed round 2), compliance (regression pin) | verified |
| F-27 | **S5 ceiling routing strip renders on the verdict card** — `str.ceiling.strip` formatted with the flagged idea's name (`str.ceiling.both` when both), alongside the engine's pinned note + `str.ceiling.mech_label`; absent when unflagged (design S5; states.md §6.4 R-3, landed round 2) | SC-09, SC-13, SC-15/R-03 | `app.py` (`render_verdict(..., ceiling=)`) | T-CEIL-03 (`test_ceiling_routing_strip_renders` in `tests/test_packaging.py`, gradio-gated) — spec §19; UI half of the T-CEIL pair (T-CEIL-01/02 = engine half) | engineering (render, landed round 2), compliance (regression pin) | verified |
| F-28 | **No-imputation input blocking holds in the SERVED UI** — an untouched factor never reaches the handler as a value; Compare on an incomplete form renders the S2 missing-list, never a fabricated verdict (delta (d), closed round 1 in code, proven browser-void round 3, fix+guard landed round 4) | SC-09, SC-15, SC-03 | `app.py` — factor inputs are `gr.Textbox` (untouched payload `""`), screened by `_coerce_raw`/`_screen_factors`; `gr.Number` (whose `value=None` serialized as a literal `0` under gradio 6.26) is out of the input path entirely; range/non-numeric problems surface in the same S2 list, no raw error toasts | **T-SER-01 — spec §20, IMPLEMENTED: `tests/test_packaging.py::test_untouched_factor_never_scores`, green 2026-08-31.** Drives the handlers with the exact frontend payloads (empty strings, never Python `None`); pins no-gr.Number-in-path, full-form and one-hole placeholders, S2 routing of bad entries, and explicit-0-is-a-score. Landed in the SAME change as the fix; red-first demonstrated by engineering round 4 AND verifiable by construction (clause (a) necessarily fails on the pre-fix `gr.Number` build) | engineering (fix + guard, delivered), design (defect owner R-8), compliance (acceptance contract §20 + registration) | **verified — BROWSER-CONFIRMED** (states.md §6.7, render session 2, 2026-08-31): all four R-8 acceptance behaviors PASS in a real Chrome session, dark theme forced — clean first paint, S2 blocking with the verbatim per-factor list, explicit-0-scores, handler-level range routing. The confirmatory close committed in round 5 has run; P-10 clear and browser-backed |
| F-29 | **Forced-background HTML blocks force their text color — INCLUDING every nested text-bearing element** — MP-1 probability token, TCTC headline, runner-up chip, amber strips legible in BOTH themes (states.md §6.4 R-9; residual R-9b) | SC-09 (via design MP-1 "must survive a squint") | `app.py` render functions — R-9b fix LANDED round 7 (verified by compliance's own read): every text-bearing element inside every forced-light block (S3/S4 headline div + `<b>` MP-1 token, runner-up chip span, S1/S2 placeholder inner divs, TCTC card lines) now carries its own inline `color:`, which outranks gradio 6.26's `.prose * { color: var(--body-text-color) }` rule by cascade | T-THEME-01 (block-level pin, stays) + **T-THEME-01b IMPLEMENTED: `tests/test_packaging.py::test_forced_light_blocks_color_every_nested_element`** (registered round 7, spec §21b) — render-level: parses the REAL rendered S1/S2/S3/S4/stale/banner surfaces with a nested-color audit; red-first honored by an in-test sensitivity self-test that MUST flag the exact pre-fix headline shape §6.7 caught (red-by-construction, the T-SER-01 pattern's fifth application); landed in the SAME change as the fix per §21b's pairing requirement | engineering (fix + guard, delivered round 7), design (defect owner, session-3 re-check DELIVERED §6.9), compliance (§21b acceptance contract + registration) | **verified — BROWSER-CONFIRMED round 8** (states.md §6.9, render session 3, 2026-08-31): rows (a)–(e) + overall PASS — S3 headline div AND nested `<b>` MP-1 token, runner-up chip, S4 headline/body, S1/S2 placeholder inner divs, stale notice ALL compute legible ink in the served dark theme (computed-style evidence per row), plus the S5 whole-screen parity rider. P-11 CLEARED (all three clauses). T-THEME-01b stays as the permanent §21b regression guard, validated in the browser it was written for |
| F-30 | **Count-copy honesty: a count of exactly 1 renders the singular catalogue variant, never plural-with-1 ("1 decisions", "1 factor scores" — the session-2 false-count defect class); the stale card states the as-built manual-Compare flow, never a phantom "Recomputing…"** (design §6.8 R-10(i)/(ii), minted round 8, wired round 9) | SC-09 (honest by construction — copy states what the build does), SC-07 (custody nudge singular), SC-15 | canonical `leaves/design/strings.py` (five `*_one` variants + corrected `str.verdict.stale` tail + `str.empty.example_cta`), vendored byte-identical to `pairwisepm/strings.py`; `app.py` `_S_n` selector (one call site per surface, full kwarg set — no desynchronization surface) | **T-STR-01** (`test_count_templates_select_singular_variant`, tests/test_packaging.py, spec §23): catalogue shape (every `*_one` has a plural counterpart), selection rule at `_S_n` for all four wired IDs, render-level S2 singular/plural, and the NEGATIVE pin — "Press Compare" present, "Recomputing" absent in the served stale card. T-CUST-01(b) + T-SER-01(c) strengthened same-change (both now assert the singular AND the absence of the defect shape they previously pinned as expected) | engineering (wiring + guard), design (copy authority), compliance (pin) | **verified — BROWSER-CONFIRMED round 10** (states.md §6.11 bonus rows): the S2 singular renders ON SCREEN ("1 factor score to go before the verdict: …") and the corrected stale tail renders ON SCREEN ("Press Compare to recompute." — the false 'Recomputing…' claim GONE from the served page). The copy chain states.md → strings.py → vendored copy → browser is verified end-to-end; red-first by construction (`_S_n` did not exist pre-wiring). `str.log.loaded/_one` and `str.m1.progress_zero` stay catalogued-but-unwired (no rendering call site — grep-verified round 9); NOT a matrix gap: an unwired catalogue entry ships no behavior, and wiring without a call site would be untraceable surface area |
| F-31 | **Policy-value copy authority: the mode schemas the engine LOADS are the repo's, and no second copy of them may go stale** — `configs/one_to_n.yaml` and `configs/zero_to_one.yaml` are the authority for factor sets, prior weights and the 0→1 banner; the wheel force-includes `configs/` at the site-packages root, so an install legitimately creates a SECOND copy (that is what makes `default_config_dir()`'s `Path(__file__).parent.parent / "configs"` resolve on a non-editable install) | SC-01/SC-03 (the model applies the PM's own policy), SC-06 via D1/D2 prior weights, SC-09, Traceability Anchor | `configs/*.yaml`; `pairwisepm/config.py::default_config_dir`; `pyproject.toml` `[tool.hatch.build.targets.wheel.force-include] "configs" = "configs"` (verified from this seat, round 15) | **T-VEND-03** (the config dir the engine actually loads resolves inside the repo checkout) + **T-VEND-04** (exactly one importable package copy — the mechanism by which a shadowed `configs/` arrives) + **T-VEND-06** (spec §26, round 15: any `configs/*.yaml` under another `sys.path` entry MUST be byte-identical to the repo authority). The invariant is deliberately **not** "no second copy" — packaging needs it — but **"no STALE second copy"**; zero duplicates is a passing state, a drifted duplicate is not. **ROUND-16 CENSUS ASYMMETRY, REGISTERED AS THE ROW'S OWN WORDING (architecture's demand, accepted whole):** this row's two shared instruments carry DIFFERENT invariants and must never be filed as instances of one rule — **T-VEND-03 = RESOLUTION invariant** (which directory the engine LOADS; a second `configs/` tree is *permitted by design* and load-bearing on every non-editable install), **T-VEND-04 = COUNT invariant, PACKAGE AUTHORITY ONLY** (it counts importable `pairwisepm/__init__.py`, and says nothing about `configs/`), **T-VEND-06 = FRESHNESS invariant** (a permitted duplicate may not drift). Architecture's reciprocal refusal is recorded and this seat agrees with it: **no fifth guard comparing the frozen `site-packages/configs` bytes to the repo's as an identity requirement** — that artifact is a snapshot that is *supposed* to be replaced on reinstall, and a guard asserting sameness-forever there would teach the wrong invariant. T-VEND-06 asserts the right one: if the duplicate is on `sys.path` it must be current, and the remedy on red is reinstall or uninstall, never edit. **ROUND-16 ACTIVATION FIX — this row's guards were inert in the only tree where its hazard exists:** T-VEND-03/04/06 gated on the DESIGN LEAF's presence, and `pyproject.toml`'s sdist include ships `tests` without `leaves`, so on an installed/sdist tree all three skipped. The frozen second copy of `configs/` is created by exactly that install. Corrected (spec §27a): T-VEND-03/06 gate on `<root>/configs`, T-VEND-04 does not skip at all. Measured before/after in an sdist-shaped tree: `1 passed, 5 skipped` → `1 failed, 3 passed, 2 skipped`, the RED a true positive. **ROUND-17 PREMISE CORRECTION — this row's stated MECHANISM was wrong in the direction that costs something (architecture's demand, re-derived from this seat before acceptance):** this row and three guard docstrings said the second `configs/` tree is created by a NON-EDITABLE install, and round 16's activation fix was justified by "the frozen duplicate is created by the very install where `leaves/` is absent". **Every install of this project creates it, editable included** — hatchling's editable target derives from the wheel target and inherits the `force-include`. Evidence, recomputed here rather than cited: `direct_url.json` = `{"dir_info": {"editable": true}}`, `site-packages/pairwisepm/` absent (only the `.pth`), and that same dist-info's RECORD listing both YAML files at sha256 values identical to the repo's; two `configs/` trees are on `sys.path` in this session. **Why the correction is not cosmetic:** a reader holding the old mechanism will read a T-VEND-06 red the day after the D1/D2 write as evidence that somebody broke the venv, and the cheapest way to make that red go away is to hand-edit or delete `site-packages/configs` — the exact action this row's remedy line forbids, and one step from deleting the `force-include` and silently breaking `pip install pairwisepm`. **The true consequence is stronger than the one this row claimed for its own guard:** T-VEND-06 reds on the NEXT suite run after the D1/D2 write, on the install this repo has today, with no reinstall involved. Demonstrated, not predicted: a divergent duplicate placed on `sys.path` in scratch reds it with the stale-weights message (`1 failed, 5 passed`), no repo file mutated. **ROUND-18 ANCHOR CLAUSE — what T-VEND-06 asserts is not the same statement in every tree (architecture's demand, accepted whole; verified from this seat against `pyproject.toml` and this machine's dist-info RECORD before being written as fact):** the guard's authority is `ROOT / "configs"` where `ROOT` derives from the TEST FILE's own location, so it asserts **mutual agreement among the reachable copies, anchored to whichever `configs/` sits beside `tests/`** — which is the repo authority only in a repo checkout. Round 16 moved the predicate from another leaf's file to the guard's own subject, which was right and is kept; the residue architecture caught is that the anchor is POSITIONAL, so the predicate now names the right KIND of thing while what it resolves to varies. Three trees, all three shipped by this project: **repo checkout** — anchor IS the authority, clause means what it says (7 passed, 0 skipped, two live comparisons); **unpacked sdist** — `[tool.hatch.build.targets.sdist] include` ships `pairwisepm`, `configs`, `app.py`, `tests` and NOT `leaves`, so the guard RUNS and anchors on the sdist's own `configs/`: a redistributed copy compared against another copy with no authority present anywhere in the tree, and green there means "these copies agree", never "this is the approved policy"; **wheel install** — `packages = ["pairwisepm"]` plus force-included `configs` and no `tests`, and this machine's `pairwisepm-0.1.0.dist-info/RECORD` carries the two YAML files, the `.pth`, four metadata entries and **zero `tests/` entries**, so the guard is **ABSENT, not skipped**. That last distinction earns its line for the reason architecture gave and this seat agrees with: a skip and an absence are different observable states, only one is ever seen by whoever is standing there, and a reader holding "it skips on a wheel" will go looking for a skip line that cannot exist. Clause written into T-VEND-06's docstring and into `_repo_config_authority`'s, so the row survives a reader who never opens architecture's census | engineering (packaging + YAML values), compliance (guards + predicates), architecture (copy census + anchor), decisions (D1/D2 values) | **verified round 15, and live rather than hypothetical** — T-VEND-06 currently compares two real duplicates on this machine (`site-packages/configs/{one_to_n,zero_to_one}.yaml`, byte-identical, install-time frozen), and T-VEND-03 confirms the editable install resolves in-repo from an off-root interpreter. **Promoted out of F-25's prose** (engineering's round-15 demand (c)): F-25's claim is about STRINGS, and a second invariant carried inside another row's narrative is the honor system with extra steps — this is a distinct authority, with distinct artifacts and a distinct failure mode. **Why this row is the more consequential half of the round-14 defect class:** a stale strings copy crashes loudly at `app.py:848`; a stale configs copy serves OLD PRIOR WEIGHTS with no error, no exception and no failing engine test — a plausible wrong verdict, arriving as a number nobody would question, which is the Spine's forbidden confidence overstatement reaching the user by the quietest possible route. **Standing effect on the D1-D6 resolution round:** the instant resolved values are written into the repo YAML while an install-time snapshot survives, T-VEND-06 reds — the alarm fires when the hazard becomes live, not after a release. Without it, the failure is silent by construction: repo YAML edited with `resolution_source` per value, every fixture regenerated, suite green, provenance lines citing values the engine never loaded |
| F-32 | **Rendered text in `configs/*.yaml` is written copy, and it is under NO COPY AUTHORITY** — seven fields reach the browser from the mode schemas: `label`, `factors[].name`/`.scale`/`.rationale`, `flags[].name`/`.description`, `evaluative_inputs[].name`/`.note` (design's §6.15 census, CX-15-01) | SC-09 (honest by construction — copy states what the build does), SC-01/SC-03, Traceability Anchor | `configs/one_to_n.yaml`, `configs/zero_to_one.yaml`; rendered via `app.py`'s factor block and evaluative panel | **T-COPY-01** (`test_config_rendered_text_is_written_not_stubbed`) + **T-COPY-01b** (`test_config_rendered_text_is_not_a_bare_key_echo`), tests/test_copy_surfaces.py, spec §27b. Prior coverage was `test_engine.py::test_config_shapes`, which asserts `rationale.strip()` and `scale.strip()` — **non-empty, not correct**: a rationale replaced with `"TBD"` passed every test in this repository, and reds here. Red-first demonstrated, own run: three mutations (rationale → `TBD`, a `(not scored)` deleted, a note reduced to `"captured"`) red 3 of 5 clauses here while `tests/test_engine.py` stays entirely green **ROUND-18 — THE AUTHORITY HALF, CLOSED (spec §27e): T-COPY-02** (`test_config_rendered_text_matches_design_ratified_fixture`) diffs every ratified field against `leaves/design/copy-authority.yaml` **in both directions** — ratified-but-absent, present-but-unratified, and any value mismatch all red, because a one-way diff is how a copy guard goes quietly empty; **T-COPY-02c** (`test_exempted_rendered_text_names_a_live_instrument`) checks that a field exempted from the fixture cites a guard that still EXISTS and still references the authority key it is cited for; **T-COPY-02d** (`test_every_rendered_config_text_field_has_a_named_authority`) derives the population from the dataclass annotations instead of a hand-written list, so a text field added to a schema type must acquire an authority in the same change. Red-first demonstrated, eight mutations, scratch tree, no repo file mutated (spec §27f table) | design (copy authority question — RULED), engineering (YAML values + text), compliance (instrument) | **PARTIAL — the authority question is CLOSED; one field's census gap is the remainder.** Round 16 registered this row OPEN because whether the text is the text design approved was unanswerable without a ruling, and this seat refused to invent one: a test encoding an unratified expectation makes a preference look like a requirement. **Design ruled it round 17** (states.md §6.17, F-32 answer (a)) and this seat wrote the diff in round 18, which was the deal. What is now tested: the text exists, is not a placeholder, is not a leaked machine key, **and is byte-equal to design's ratified copy**, with the fixture deliberately policy-free so the D1/D2 round cannot red it — the failure mode is exactly one event, a rendered string moving without ratification, which is design's §6.12(b6) per-line notification converted from a promise into an instrument. **THE REMAINDER, FOUND FROM THIS SEAT WHILE WRITING THE DIFF AND FILED AGAINST FOUR CENSUSES INCLUDING THIS ROW'S OWN: `banner` is not in any of them.** Design's §6.15 seven-field census, their round-17 four-field correction, this row's header sentence and the fixture's own `render_map` all enumerate the `configs/*.yaml` text population, and **none lists the permanent 0→1 claim-limiting banner** — the most Spine-load-bearing string in either schema (Spine, Out: no accuracy claims in 0→1 mode). It is NOT unwatched: `test_zero_to_one_banner_mandatory` and `test_banner_attached_and_wording` both pin it byte-equal to `STRINGS["str.banner.01"]`, which this seat discovered by demonstrating a red BEFORE proposing a new clause — the first draft of T-COPY-02c asserted the quotation on the premise that nothing did, and that premise was false in the direction that flatters a new test. So the field is covered and the CENSUS was wrong, which is the more interesting defect: four independent enumerations of one population, produced by three seats, all missing the same field. The clause became the thing actually missing (a checked citation for an exemption), the field is exempted from the fixture with its two real guards named, and **the ruling that remains is design's: ratify `banner` into `copy-authority.yaml` or confirm the catalogue exemption in writing** — filed as this round's one demand. **This row is dated:** the D1-D6 resolution round edits these files, and in a schema block a policy value and a rendered string are neighbouring lines — so "YAML only, no new surface" and "no rendered surface" are different statements, and five seats have been reading the first as the second. Design's bright line (six numeric/policy fields change freely; the six text fields are a copy change and a per-line notification) is registered here as the closing condition, honored through that round. Registering the row OPEN with a partial instrument is the honest state: a matrix that said "copy integrity: verified" while these seven fields sat outside every guard would be measuring the half that has one. **ROUND-20 SCOPE WORD ON THIS ROW'S OWN SENTENCE (architecture's demand, accepted whole; it is a citation alignment, no test touched).** This row must not be quotable as *"the rendered config copy is diffed against design's ratified text"*, because T-COPY-02's population is both WIDER and NARROWER than that sentence. Wider: the diff's population is the **NINE declared config text names** — `label`, `factors[].name`/`.scale`/`.rationale`, `flags[].name`/`.description`, `evaluative_inputs[].name`/`.scale`/`.note` — **rendering or not**, of which only FIVE reach a screen; four are declared-and-dead today and are diffed anyway, correctly, because a dead field is one call site away from live. Narrower: **`banner`, the fifth rendering field, is NOT in that diff at all** — design ruled option (b) in §6.19, so its authority is the catalogue's `str.banner.01` and it routes to Authority A, asserted by `app.py:73`'s import assert (guarded by T-COPY-02e), by `test_zero_to_one_banner_mandatory` / `test_banner_attached_and_wording`, and by T-COPY-02c's citation check. So the true sentence is: **all declared config text is diffed, rendering or not, minus `banner`, which routes to Authority A.** The header cell's "seven fields" numeral above is struck by this clause with the false figure left legible — the declared population is nine names over eight declared fields, and the fixture's `render_map` carries ten rows of which five render, which is the arithmetic a reader can check against the file. This matters for exactly one reader: whoever consults this row to ask whether a config text change is watched, and would otherwise get "yes" for a dead flag description on one instrument and "yes" for the banner on a mechanism they were never told about. **ACTIVATION ASYMMETRY, measured rather than counted (architecture's second clause):** the two governance forms INVERT off a checkout. T-COPY-02 / T-COPY-02b SKIP where `leaves/` is absent — honest, their subject IS design's fixture — while T-COPY-02c / T-COPY-02d and the banner's two engine clauses run in ANY tree carrying `tests/`. Own run, sdist-shaped scratch tree, no repo file mutated: `tests/test_copy_surfaces.py` = **10 passed, 2 skipped**, the two skips being exactly the fixture-governed pair, against 12 passed / 0 skipped in a checkout. **The field whose authority survives off-checkout is the one delegated to the catalogue; the four that needed a fixture invented go silent** — which is the strongest argument on this board for cross-reference over fixture, and it is recorded here as a fact about this row rather than as a case for reopening design's ruling, which this seat does not reopen |
| F-33 | **Rendered literals in `app.py` sit outside the string catalogue — and four of them carry a SPINE REFUSAL**: the `(not scored)` marker on the evaluative inputs (design's §6.15 census, CX-15-02; 20 literals by design's AST census, of which these four and the `Compare` button label are the load-bearing ones) | **Spine Scope Boundaries (Out): "evaluative factors (brand, strategic fit) inside the mechanical score — they are captured and displayed as labeled override inputs only"**; SC-09; Traceability Anchor | `app.py` evaluative panel (`gr.Textbox(label="A · Strategic fit (not scored)")` ×4); `configs/*.yaml` `evaluative_inputs[].note`; `pairwisepm/config.py::EvaluativeInput` | **T-NEG-08** (`test_evaluative_inputs_are_labelled_not_scored_on_screen`) — censuses the four labels **by AST, not regex**, so a moved line or reflowed call cannot silently empty the check, and pins the count at four so a restructured panel is a deliberate diff rather than a vacuous pass; **T-NEG-08a** (the same refusal in both schemas' `note`); **T-NEG-08b** (the refusal is STRUCTURAL — `EvaluativeInput` may never gain `prior_weight`/`sign`/`tag`/`seed_mean`/`seed_std`, and no key may be both a scored factor and an evaluative input). tests/test_copy_surfaces.py, spec §27b. Red-first demonstrated: deleting one `(not scored)` reds T-NEG-08 and leaves the rest of the suite green. **ROUND-18 (spec §27e/f): T-COPY-02b** (`test_app_evaluative_labels_match_design_ratified_fixture`) pins the four labels' WORDS against design's ratified `app_py_candidates` set — T-NEG-08 pins the marker and the count and is silent about the rest of the string, so `A · Strategic fit (not scored)` → `A · Strategic Fit (not scored)` passed it (demonstrated); **T-COPY-03** (`test_the_copy_guards_cannot_be_quietly_weakened`) asserts from this file's own AST that T-NEG-08 cannot be softened silently — required clauses present by name, the census still `ast.parse`-based, the count still pinned at four, no skip marker on any clause, every `pytest.skip` in a helper naming its own subject, and a counted floor of clauses that never skip | design (copy authority question — RULED), compliance (negative tests + guard-the-guard), engineering (render surface), gtm (relies on T-NEG-08) | **PARTIAL, and the authority question is CLOSED for the CANDIDATES set; the REFUSAL ITSELF stays verified.** Design ruled F-33 round 17: CANDIDATES (4) → answer (a) with the fixture as interim target and the catalogue move as its closing condition; CROSS-REFERENCED (1) closed on engineering's import assert; STRUCTURAL (16) permanently partial by decision, owner design, with two named revisit events. **Registered here as ruled, and the STRUCTURAL 16 are registered as PERMANENTLY PARTIAL BY DECISION rather than as an open row** — which is the honest state: a decision not to instrument is a decision, and a row waiting on nobody was the M-UX-02b defect this seat pressed design about for two rounds. **GTM'S DELETION TRIGGER, ACCEPTED AND MADE STRUCTURAL:** gtm deleted a presenter eyes-on check from the witness pre-flight on the strength of T-NEG-08 and asked to be notified per line if that test is ever weakened, renamed, made skippable or removed. The notification duty is registered here and owed by this seat. It is also now unnecessary as a memory: T-COPY-03 reds on every weakening gtm named by hand, in the change that makes it, naming what went missing — a promise about an instrument two other seats have retired checks against should not rest on anyone remembering. **This row's one honest caution, stated rather than left to inference:** T-COPY-02b diffs the labels against design's ratified set, so when ENG-COPY-EVALLABELS-01 fires after the sitting and the four move into the catalogue, gtm's byte-identical-move demand on engineering becomes machine-checkable — a mechanical move that also tidies the phrasing reds in the push that does it, which is what gtm asked for and could not previously have. Why this row exists rather than being folded into F-30: these four strings are the point in the UI where the Spine's hardest scope boundary becomes visible to a user. The engine has always honored it structurally, but a PM cannot read a dataclass — what tells them is the parenthetical, and it is the exact beat a presenter points at when they say the model refuses to score strategic fit. Until this round it could be deleted with the suite green, leaving two unmarked judgment fields beside the scored ones: **the tool implying it weighed something it explicitly refused to weigh — the Spine's forbidden overstatement arriving as an omission rather than a claim.** What remains open is only the authority question design raised (do these literals move into the catalogue, and when); design has deferred that to the first release AFTER the M-UX-02a sitting, which this seat supports — a mint plus a mirror update in front of a timed witness sitting is exactly the change that should not be made on the eve. The refusal is guarded in the meantime, which is what makes the deferral safe rather than convenient |
| F-34 | **`app.py` has TWO rendering surfaces and every copy census on this board has measured ONE** — the CONSTRUCTION surface (`gr.*` calls with constant arguments, design's §6.16(vi) predicate, 21 literals, partitioned in §6.17(ii)) and a RUNTIME-HTML surface: six builders (`render_placeholder`, `render_stale`, `render_verdict`, `render_leverage`, `render_ladder`, `render_audit`) whose output reaches the browser through `gr.HTML(...)`, from which the census predicate contributes ZERO literals. The audit view alone paints thirteen uncatalogued strings, three of them honesty-carrying — `accumulating — needs 3 ideas`, `n/a — no decisions yet`, and `free intercept {b} (z = {z}) — no measured order bias`, the last a negative diagnostic finding stated in the app's own voice with no catalogue entry behind it | SC-09 (honest by construction); Spine Traceability Anchor; **Spine Scope Boundaries (Out): accuracy claims in 0→1 mode** (via the audit caption, F-35) | `app.py` `render_*` builders → `gr.HTML` | **T-NEG-09** (`tests/test_audit_honesty.py::test_audit_0to1_caption_renders_only_when_the_log_carries_0to1`, round 19) closes the sharpest instance — the 0→1 no-prediction caption's ARRIVAL on the surface, both directions. The population itself is **open** | design (owner), compliance (rows) | **OPEN — registered round 19 as a SCOPE CLAUSE ON F-33, at design's own demand and against their own ruling.** §6.17(ii)'s partition and §6.17(iv)'s "STRUCTURAL (16) → permanently partial" both say "the census", and this matrix registered that ruling verbatim on design's word one round ago. It is true of sixteen widget nouns on the construction surface and **false of thirteen strings that were never in the population**. So the row reads: *permanently partial ON THE CONSTRUCTION SURFACE; the runtime-HTML surface is a second, uncensused population.* Closing condition, design's own: enumerated in §6.18(i) next round or in the first release after the M-UX-02a sitting, whichever comes first. **This is the fourth instrument-scope defect this cycle and the first one a seat filed against a ruling in its own favour** — design gained nothing by narrowing their own ruling, which is what makes the correction worth registering as method rather than as an errand. No gate opens on it: nothing here is a defect in the build, and the sitting is untouched (§1c logs no decision, so every log-derived string renders its locked or `n/a` text at the hour) |
| F-35 | **The audit view's four statistics render POOLED ACROSS MODES, one line above a caption that scopes itself to 0→1** — `render_audit` calls `log.kendall_zeta()`, `log.brier()`, `log.outcome_brier()` and `log.override_rate()` with no `mode` argument (each method takes one) while the same table splits the count row, loops M1 and reliability per config, and gates `str.audit.01_caption` on `log.n("zero_to_one")`. None of the four denominators is on screen, and the one count that IS on screen is not any of them | **Spine Scope Boundaries (Out): "accuracy claims in 0→1 mode"**; SC-05 (ζ and Brier accumulate from decision 1 — per mode is how they are defined); SC-09 | `app.py::render_audit` (statistic calls); `pairwisepm/log.py` (every method already accepts `mode`) | **T-NEG-09b** (`test_audit_view_pooled_statistics_are_censused_and_classified`, round 19) — an AST CENSUS with an explicit classification, not a requirement: `n` is POOLED-DISCLOSED (it prints the split beside the total), the other four are POOLED-F-35. Passing a mode through — THE FIX — removes a call from the census and leaves the clause GREEN; adding a fifth undisclosed pooled statistic reds it in the change that adds it. When the POOLED-F-35 entries are gone the row closes and the clause is a two-line delete | engineering (fix, `render_audit`), design (copy, §6.18(iii) IDs reserved and unminted), compliance (row) | **OPEN — registered round 19 on design's demand, with both demonstrations attached and one reproduced from this seat before registering.** Demonstration A (design's, RE-RUN HERE — and the re-run carries one correction to the demonstration, in the direction that narrows it): three transitive 1→N comparisons (A≻B, B≻C, A≻C) display ζ = 1.00; ONE 0→1 comparison **of the A–C pair the other way** drops the DISPLAYED row to ζ = 0.00 while `kendall_zeta("one_to_n")` is still 1.00 — confirmed from this seat, own run. The correction: **it is not any cross-mode re-comparison, it is one that both overwrites an edge AND closes a circular triad.** This seat's first probe reversed the A–B pair instead and the displayed ζ stayed 1.00 (B≻A, B≻C, A≻C is still transitive), which does not weaken design's finding but does bound it — the wide reading, "a 0→1 comparison of any already-compared pair corrupts the displayed ζ", is false, and a row is worth less than nothing if the sentence a later reader quotes off it is not the sentence that reproduces. The MECHANISM is exactly as design stated and is visible in `log.py:198-206`: edges are keyed by unordered idea name over the whole log with most-recent-write-wins, so a mode-crossing re-comparison overwrites the earlier edge instead of asking a second question. Demonstration B is DESIGN'S, cited and not re-run here (their artifact disclosure, §6.18(ii), stands with it): live `render_audit` on 3×1→N + 2×0→1 with labeled outcomes renders `Brier (vs. labeled outcomes) 0.286` (per-mode 0.172 / 0.343) directly above *"…they do not predict outcomes. No outcome data about ideas like yours exists."* What this seat verified for B is the structural half T-NEG-09b asserts — `outcome_brier` takes a `mode` argument and `render_audit` passes none — which is the fact the row rests on. **THE FIX IS NOT ASKED FOR BEFORE THE SITTING and this row does not gate anything** — engineering's resolution round is YAML-only by ruling, nobody should be moving code this week, and the defect is unreachable at the demo hour (§1c logs no decision, so every one of these renders `n/a` or `accumulating`). What the row buys is that the finding exists with an owner, a demonstration and a closing condition instead of dying in a packet — and that the population cannot grow silently while it waits |

---

## 3. Negative traceability — refusals and their negative tests

Each refusal gets at least one test that **fails when the refused thing appears**.
These tests are permanent regression guards in `/tests/test_engine.py`, not
one-time checks.

| Row | Refusal | Spine anchor | Negative test(s) — implemented | What the test forbids, concretely | Verification owner | Status |
|---|---|---|---|---|---|---|
| N-01 | No LLM in the runtime loop; no API key; no network | R-01, SC-05, SC-07 | T-NEG-01a (fresh-interpreter import of `pairwisepm` pulls none of: openai, anthropic, transformers, litellm, langchain, httpx, requests, aiohttp, urllib3 — plus static source scan of `pairwisepm/*.py` and `app.py`); T-NEG-01b (socket creation monkeypatched to raise; full compare→record→round-trip→ζ/Brier→fit_m1 cycle in BOTH modes completes untouched); T-NEG-01c (requirements whitelist = numpy, PyYAML, gradio — DV-3). **ROUND-20 — T-NEG-01d, THE FLOOR UNDER THIS ROW** (`test_the_no_llm_guard_cannot_be_quietly_weakened`, design's demand, spec §27j): §27i's repair left a one-token exit that did not exist before it — T-NEG-01a's red now reads `importing the engine pulls in ['httpx']`, and the fastest edit that clears it is deleting `"httpx"` from `FORBIDDEN_IMPORTS`, which retires the Spine's offline promise with the whole suite green. T-NEG-01d reads this file's own AST and asserts: the tuple still names every module in `_NO_LLM_FLOOR` (it may GROW freely; it shrinks only by an edit that moves the floor in the same change), neither refusal clause carries a skip marker or calls `pytest.skip`, BOTH of T-NEG-01a's halves survive (child-process probe AND source scan naming `app.py`), and T-NEG-01b is still present and unskipped. It asserts SHAPE, never behaviour, so a strengthening keeps it green — a floor a legitimate improvement reds is a freeze. Red-first, four mutants, scratch copies, no repo file mutated: dropping `"httpx"`, adding `@pytest.mark.skip`, deleting the source-scan half, deleting the probe half — **each reds T-NEG-01d ALONE and in every one of the four T-NEG-01a itself stayed GREEN**, which is the exposure stated as a measurement. **SCOPE WORD ON T-NEG-01a (decisions' demand, and it corrects a sentence this seat wrote one round ago):** its docstring ended *"the source scan is unchanged and still covers `app.py`"* — true of the TEXT, false of the GRAPH. The scan is a regex over DIRECT `import`/`from` lines; the probe's subject is the ENGINE only. `app.py`'s TRANSITIVE graph is asserted by nothing here, deliberately (app.py → gradio → `httpx` is a legitimate UI dependency), and the runtime claim on that surface is held by **T-NEG-01b's socket kill-switch** instead. A reader asking whether a new app-side dependency is covered by T-NEG-01a must read **no**. The false sentence is struck in place with its text legible | Any import, dependency, or runtime call path that could reach a model API or the network | engineering (implement), compliance (audit each release) | verified — and, since round 20, verified with a floor under the verification: the two states this row can enter without an instrument moving (a name dropped from the tuple, a skip marker added) now red first |
| N-02 | No ranking of more than two ideas | R-02, SC-10 | T-NEG-02 (compare surface has exactly `raw_a`/`raw_b` idea slots, no `*args`, no collection param; public namespace contains no rank/tournament/round_robin/leaderboard name) | A `rank(ideas: list)` — or any n>2 entry point — in the public surface | engineering | verified — DV-4 resolved at integration: `compare` type-checks `m1_fit` and a smuggled third idea dict now raises a clean TypeError (tested in `test_strictly_two_ideas`) |
| N-03 | No portfolio/knapsack automation | R-03 | T-NEG-03 (no public name or module matching portfolio\|knapsack\|optimiz\|allocat); T-CEIL-01 (ceiling is a message, never a computation) | Turning the ceiling routing note into an automated portfolio decision | engineering, compliance (audit) | verified — boundary now formally tracked as decision D3 (decisions.yml), not an ambiguity |
| N-04 | No accuracy claims in 0→1 mode | R-04, SC-09 | T-NEG-04 (banner always set on 0→1 results and never on 1→N; banner text claims structure/consistency and contains no "accura*" wording); T-CFG-01b (bannerless 0→1 config refused at load); M-DOC-01 (README side) | Any UI state or document where 0→1 output is presented as a prediction of market outcome | engineering (T), design + gtm (M), compliance (review) | verified — T green; M-DOC-01 PASS (states.md §6.5). NOTE: no accuracy CLAIM appears anywhere, so this refusal holds; the banner's scroll-persistence failure is tracked as F-19 manual-FAILED, not here |
| N-05 | Evaluative factors never inside the mechanical score | R-05 | T-EVAL-01 (exclusion BY API SHAPE: `compare` has no evaluative parameter at all — stronger than a sweep; config types them out of the factor list; values still round-trip into the log record as labeled overrides). **ROUND-16 ADDITION — the refusal's USER-FACING half, which this row certified without an instrument for fifteen rounds: T-NEG-08 / 08a / 08b** (tests/test_copy_surfaces.py, spec §27b; row F-33) | Strategic-fit/brand leaking into w, d, or any score path — **and, added round 16, the refusal ceasing to be VISIBLE while remaining structurally true** | engineering (engine shape), compliance (visibility) | verified — **and the row's scope is now stated rather than assumed.** T-EVAL-01 proves the score path cannot reach these inputs; it says nothing about whether a user is told. What tells them is the `(not scored)` marker on four `gr.Textbox` labels in `app.py` and the `note` in each schema, none of which lived in the string catalogue and none of which any instrument watched: delete one parenthetical and this row, F-30, F-25 and the whole suite stay green while the screen offers two unmarked judgment fields beside the scored ones. **A refusal the build honors and the interface conceals is not the refusal the Spine wrote** — the Spine's sentence is "captured and **displayed** as labeled override inputs only", and *displayed as labeled* is half the commitment. Both halves are now negatively tested |
| N-06 | No server-side storage of user data | R-06, SC-07 | T-NEG-06 (static audit of `app.py`: no DB clients, no huggingface_hub/datasets persistence, log custody in `gr.State`, downloads via tempfile only) | Any persistence of factor scores, picks, or logs on the Space | engineering (implement), compliance (audit each release) | verified (static); behavioral spot-check M-UX-04 at each release |

---

## 4. Cross-leaf claim traceability (exchange round)

### 4.1 GTM tour claims (leaves/gtm/tour.html, seed-comparison.json)

Verified against the gtm leaf's own interface declaration; the claims map cleanly —
no unmapped claim found.

| Claim in tour | Spine anchor | Matrix hook | Finding |
|---|---|---|---|
| "under 5 minutes" framed as a design target only | SC-06 | F-17 / M-UX-02a+b; **T-NEG-07** (automated, round 13) | compliant — target framing, not a measurement claim; now automatically enforced on shipped copy (README.md, app.py): a measured-speed claim there goes red while F-17 is unconverted |
| Offline / no API key / no server storage | SC-07 | N-01, N-06, F-23, F-24 | compliant — now backed by green negative tests |
| M1 at ~decision 10; ζ and Brier from decision 1 | SC-08 | F-04, F-07, F-08 | compliant — "~decision 10" acceptable; engine constant is exactly 10 |
| Intervals always; too-close-to-call on straddle; 0→1 banner | SC-09 | F-06, F-19 | compliant |
| Refusals list mirrors Spine Out list | SC-15 | §3 rows | compliant |
| No outcome-accuracy claims anywhere; 1→N accuracy "earned via calibration, never asserted" | R-04, SC-09 | N-04 | compliant |
| Log-derived numbers (M1 weights, ζ 0.89, Brier 0.21, intercept +0.03) badged "sample: seeded demo log" | SC-15 (overconfidence refusal) | this row | **compliant per gtm's badge declaration — the badges satisfy the honesty commitment PROVIDED they render in every state where those numbers appear, including the audit-view tab variants; spot-check at M-DOC-01** |
| Tour weights = D1 proposed defaults | F-20 | G-D1D2 | compliant with "build on defaults"; tour must be recomputed if D1 resolves differently (gtm already flags this) |

### 4.2 Design invariants (leaves/design/states.md §4) → test IDs

| Design invariant | Matrix row | Automated by |
|---|---|---|
| No naked probabilities (p only ever with interval) | F-06 | T-VERDICT-03; UI side: design's (p, lo, hi)-only component contract, M-UX check |
| No forced winner across 50% | F-06 | T-VERDICT-01/02 |
| A/B-swap symmetry (exact 1−p) | F-03, F-05 | T-SYM-01/02/m1 |
| Ceiling-flag score exclusion | F-12, F-27 | T-CEIL-01 (bitwise, engine); T-CEIL-03 (strip + note rendered on the card, UI) |
| No cross-mode score reuse | F-02 | per-mode configs + `DecisionLog.for_mode` partitioning (T-LOG-03 trains per mode); UI clearing rule is design-owned (M-UX) |
| Evaluative inputs quarantined from computation | N-05 | T-EVAL-01 |
| Permanent 0→1 banner | F-19 | T-CFG-01b + T-NEG-04 + T-BANNER-01 (§22b rewrite, permanent regression pin) = rule-APPLIED; **T-DELIV-01a/b (§25, round 14) = rule-DELIVERABLE** (major bound intact + CSS on the served object + fallback present in the installed gradio); M-UX-03 **CLOSED browser-verified round 10** (§6.11 single-check PASS after three FAILs — S8 invariant 7 holds in the browser) = rule-EFFECTIVE. Three instruments, three distinct claims, none standing in for another |
| No naked/silent defaults — "the tool never guesses" (S2) | F-28 | T-SER-01 (spec §20, IMPLEMENTED and green — exercises the serialization boundary with real frontend payloads; the layer the suite was blind to until round 4) |

Note to design/engineering: the tests pin engine-emitted strings ("high-ceiling
outlier — portfolio decision, not averaged in", "re-estimate before committing",
the YAML banner text). Design owns final copy (states.md string IDs); the banner
in `configs/zero_to_one.yaml` states it mirrors `str.banner.01` — any copy edit
must go states.md → config → tests, in that order. As of round 2 the vendoring
half of this chain is test-enforced, not honor-system: T-VEND-01 (F-25) reds
the suite on any byte divergence between design's strings file and the package
mirror, and the T-NEG-04b banned-words sweep (`_self_check` over
`ZERO_TO_ONE_SCOPED_IDS`, now including `str.factor.ceiling_label`) runs at
import time on the vendored module — verified equivalent to design's copy.

### 4.3 decisions.yml consumption

Every decisions.yml entry carries a mandatory `spine_commitment` quote; consumed
here so open questions are live decisions, not ambiguities:

| Decision | Spine/spec hook | Matrix effect |
|---|---|---|
| D1/D2 prior weights | SC-11, §2 | F-20 pending; T-CFG-01/T-M0-01 constants regenerate on resolution; G-D1D2 blocks space-push |
| D3 portfolio/knapsack scope | R-03 | N-03 boundary now points at a live decision ("flagged, not decided" formally tracked) |
| D4 calibration cadence, reliability-curve n≥30 | SC-08, §4 | audit-view rows F-15; threshold must ship as config — no matrix change until resolved |
| D5 seed→log z-basis transition (Bayesian blend default) | §2 z-scoring | `log_derived_stats`/`with_updated_distributions` exist but are NOT wired by default (deliberate v1.1 flag) — consistent with build-meanwhile default; new tests due when wired |
| D6 fragility-flag threshold ("small plausible move") | SC-09, §5.4 | F-11 build-meanwhile default 0.75σ (engine as shipped); on resolution the epsilon becomes config, compliance regenerates every T-FRAG fixture, spec DV-5 closes |

### 4.4 Sequencing node mapping (leaves/sequencing/work-items.yaml)

Audited 2026-08-30: **every node in work-items.yaml carries a `spine_commitment`
field, and every one maps to a register ID above** (spot map: factor-configs→SC-11,
engine-m0→SC-01/05, engine-bootstrap→SC-09, engine-m1/m1-activation→SC-08,
decision-log→SC-07/12, metrics-zeta-brier→SC-08, leverage-panel→SC-13,
gradio-ui→SC-06, packaging/space-push/pip-release→SC-14, readme-epistemics→SC-15,
tests-green/traceability-matrix/release-audit→Traceability Anchor,
calibration-report→SC-09 "earned via calibration", m2-outcome-regression→§3 ladder).
No unmapped node ⇒ no scope creep detected in the graph. Spine refusals are
correctly ABSENT from the graph (adding one requires a Spine update first).

---

## 5. Success-metric verification summary

| Metric (SC) | Verified by | Kind | State |
|---|---|---|---|
| SC-06 under-5-minutes | M-UX-02a (1→N) + M-UX-02b (0→1); T-NEG-07 shipped-copy tripwire | manual, timed, pre-release + automated static | pending — a 1→N record converts the 1→N half only (round 13 scope split); T-NEG-07 green. **Coverage of the b-half (0→1): open — D8 (SLA 2026-09-02)** (round 15, decisions' demand): no instrument and no scheduled sitting is the true description of TODAY, but it is not a ruling, and leaving it as the row's disposition would record a permanent deliberate non-measurement of half a Spine metric that nobody decided. D8 does not gate the release path and does not defer the D1-D6 round; until it rules, every payload keeps the canonical phrase "designed so, not yet timed" for 0→1 and names the measured mode. **Three registered outcomes (round 14):** PASS ⇒ measured, mode named · **MEASURED, TARGET MISSED ⇒ `measured-FAILED (1→N)`, a first-class state, never a reversion to "designed so"** · WINDOW CLOSED ⇒ expired slot (not a terminal FAIL), canonical string retained, re-schedulable under the identical protocol |
| SC-07 fully offline | T-NEG-01b/01c, T-NEG-06 | automated + audit | green |
| SC-08 M1 at decision 10; ζ/Brier from decision 1 | T-ACT-01, T-ZETA-03, T-BRIER-02 | automated | green |
| SC-09 honest verdicts | T-VERDICT-01..03, T-NEG-04, T-CFG-01b; serialization/theme/copy layer: T-SER-01, T-THEME-01, T-THEME-01b, T-BANNER-01, T-STR-01 (§23); manual: M-UX-03 CLOSED, render sessions 2 (§6.7), 3 (§6.9), 4 (§6.11 — ledger CLOSED, retrigger only on copy/layout change) | automated + manual | **F-28 closed browser-confirmed** (§6.7). **F-29 closed browser-confirmed** (§6.9; P-11 cleared). **F-30 closed browser-confirmed** (§6.11 — copy chain end-to-end). **F-19 closed browser-confirmed** (§6.11 single-check PASS; P-5 cleared). **The SC-09 automated-and-manual chain is COMPLETE: zero open browser-refutations.** Sole SC-09-adjacent remainder is SC-06's M-UX-02 timed run (F-17) |

## 6. Audit protocol

- **When:** every release candidate, and any time the Spine version bumps.
- **What:** (1) `pytest tests/` fully green — all three files, including the
  T-PKG skips resolving to PASSES (a release candidate cannot ship while the
  README / pyproject checks skip, and a T-VEND-01 skip in the repo context is
  an unexpected skip); (2) clean-venv `pip install .` + `import pairwisepm`
  (T-PKG-01 release-gate step); (3) manual checks M-UX-01..04, M-DOC-01;
  (4) diff every Leaf artifact against this matrix — any element with no row is
  scope creep (remove it) or a missing Spine update (raise it to the Spine owner).
- **Manual checks:** M-UX-01 both ideas on one screen; **M-UX-02a timed ≤5:00 in
  1→N** (instrumented: gtm 1c-i template + design §6.12 protocol) and
  **M-UX-02b timed ≤5:00 in 0→1** (round 13: no instrument, no scheduled
  sitting — the honest state of the second half; **round 15: disposition is
  now "open — D8 (SLA 2026-09-02)", not settled by omission** — non-gating,
  and it defers nothing); M-UX-03 0→1 banner visible in every UI state; M-UX-04 behavioral
  no-persistence spot-check on the live Space (compare + download + upload,
  confirm nothing survives the session server-side); M-DOC-01 README epistemics
  checklist + GTM tour "sample data" badges render in all audit-view states.
- **Pending items:** D1/D2 (gate G-D1D2, held by sequencing, SLA 2026-09-01);
  D6 fragility threshold (T-FRAG fixtures regenerate on resolution; spec §0.1
  DV-5 tracks it as OPEN, not ratified). Fixture-staleness trigger is now
  WIRED, not honor-system: decisions.yml `on_resolution_notify` for D1, D2,
  and D6 names compliance with the exact regeneration duty (T-M0-01/T-PAR-01
  pinned constants, all T-FRAG fixtures) — verified in decisions.yml round 3,
  closing compliance's round-2 demand to decisions.
  Closed at integration 2026-08-30: F-21 config_fingerprint (implemented +
  T-FPR); DV-1 verdict boundary (engine ships the inclusive `lo <= 0.5 <= hi`
  rule, `test_verdict_rule_units` pins the touching case); DV-4 (compare now
  fails fast with TypeError on a non-M1Fit third argument).
  Closed in round 2 (2026-08-30): states.md §6.4 R-1 custody miscount —
  engineering landed the `n_session` fix and compliance pinned it same-round
  (T-CUST-01, F-26); strings vendoring drift — observed live (additive keys
  22:08, re-vendored 22:11) and now guarded (T-VEND-01, F-25). Design's
  §6.4 R-2/R-3 (string IDs adopted, ceiling strip rendered) verified landed
  in app.py; their UI render remains under M-UX-01..03 as before.
  Closed in round 3 (2026-08-30): the R-3 ceiling-strip render, previously
  verified only by a one-time code read, is now regression-pinned (T-CEIL-03,
  F-27, spec §19) — the UI half of the T-CEIL pair; re-verified byte-identity
  of the vendored strings (T-VEND-01 green) and 54/54 suite in the venv.
  Engineering's round-2 ask to register tests/test_vendoring.py was already
  satisfied when made: F-25 + spec §17 + gate P-9 have cited that file as
  canonical T-VEND-01 since round 2.
  Closed in round 4 (2026-08-30): the manual-side ledger is SETTLED against
  states.md §6.5 (browser render session 1, per-check-ID, citable — design
  delivered exactly the table demanded): F-01 flipped verified (M-UX-01 PASS),
  F-18 and N-04 flipped verified (M-DOC-01 PASS), F-17 stays manual-pending
  (M-UX-02 needs a fresh human + gtm witness), and F-19 flipped to
  **manual-FAILED** — a FAIL flips a row to failed, never to verified, and
  P-5 now blocks push on it. Opened in round 4: **F-28 (GAP, critical)** —
  the round-3 render proved the no-imputation blocking rule void at gradio's
  serialization layer (states.md §6.4 R-8) and the suite structurally blind
  to it; T-SER-01 specified (spec §20, red-first, same-change pairing) and
  pre-push gate P-10 added. **F-29 (GAP)** — MP-1 dark-theme illegibility
  (R-9); T-THEME-01 specified (spec §21). Gating/scheduling of the R-8/R-9
  fixes rides design's D-entry in the Decisions queue — this matrix does not
  schedule; it records that the rows are not verified and that no fix merges
  guard-less. After the fixes land, M-UX-01 and M-UX-03 re-run in one
  session (design's §6.5 commitment); §6.5 results append per session, never
  overwrite, so history stays citable.
  Closed in round 5 (2026-08-31): **F-28 and F-29 flipped verified** — the
  R-8/R-9 fixes landed round 4 in the same change as their guards, exactly
  per the §20/§21 acceptance contracts written before the fixes existed
  (the T-VEND-01/T-CUST-01 pattern, third and fourth application). T-SER-01
  registered as `test_untouched_factor_never_scores`, T-THEME-01 as
  `test_forced_light_backgrounds_force_text_color` (both
  tests/test_packaging.py); suite 56/56, compliance's own re-run 2026-08-31.
  Red-first: demonstrated by engineering round 4 and independently verifiable
  by construction (T-SER-01 clause (a) cannot pass on the pre-fix gr.Number
  build). Pre-push gate P-10 clears. Compliance hardening the same round:
  T-THEME-01 broadened from the two shipped hexes to the full §21
  any-forced-background contract, and T-SER-01's gradio import converted to
  a clean `importorskip` per P-8's skip discipline — both strictly
  strengthenings, suite green before and after. STILL OPEN: F-19
  manual-FAILED (the M-UX-03 sticky-banner fix is NOT in app.py —
  grep-verified round 5 — so P-5 still blocks), F-17/M-UX-02
  (human-gated), F-20 (D1/D2), and browser render session 2 as the
  confirmatory close on F-28/F-29.
  Round 6 (2026-08-31), on design's render session 2 evidence (states.md
  §6.7, new dated append-only row-set — the append-only discipline held
  exactly as demanded): **F-28 upgraded to browser-confirmed** (all four
  R-8 acceptance behaviors PASS live, dark theme forced) and **F-29
  DEMOTED verified→partial (R-9b residual)** — the MP-1 headline token,
  runner-up chip, and S1/S2 placeholder inner divs compute near-invisible
  in the served dark theme while T-THEME-01 stays green, because gradio's
  `.prose *` rule re-colors DESCENDANTS and the pin only checks the
  block-level style attribute (independently re-verified round 6: app.py
  ~lines 176/192 nested divs carry no own color; test line ~330 asserts
  only `src[m.end():].startswith("color:#")`). Third demonstrated
  green-guard/browser-false coexistence; the honor-system gap moved from
  serialization into CSS specificity. Response per the house discipline:
  strengthened contract T-THEME-01b written BEFORE the fix (spec §21b —
  descendant-level coverage, red-first by construction, same-change
  pairing), pre-push gate **P-11 added**, and a browser FAIL row is
  reaffirmed as senior to any green static pin. A demotion on evidence is
  the matrix working, not churn: verified means verified-as-served.
  Round 7 (2026-08-31): engineering's R-9b + M-UX-03 landing REGISTERED
  after independent verification, never on the claim — compliance read the
  as-built app.py (inline color on every nested text-bearing element in
  every forced-light block; `#pwpm-banner` sticky rule wired via elem_id +
  `gr.Blocks(css=_CSS)`), read both new tests in full, and re-ran the suite
  itself: **58/58 green, 1.25s, project venv, gradio 6.26.0**. New
  registrations: **T-THEME-01b** =
  `test_forced_light_blocks_color_every_nested_element` (render-level
  nested-color audit over the real S1/S2/S3/S4/stale/banner surfaces, §21b
  contract met, red-first honored via an in-test sensitivity self-test
  against the exact pre-fix headline shape — verifiable by construction,
  same standard as T-SER-01 round 5) and **T-BANNER-01** =
  `test_banner_scroll_persistent_static` (M-UX-03 static half: sticky rule
  on the component wrapper — not the inner div, where it would be a no-op —
  z-index, and css actually wired into the served Blocks; the banner's
  inner background is opaque `#0b7285` by construction). Same-change
  fix+guard discipline honored a fifth and sixth time. Engineering's
  gradio-6 constructor-css deprecation note is RECORDED: `css=` on the
  Blocks constructor deprecation-warns but is honored via the
  `_deprecated_css` fallback in the installed 6.26 package; deliberate,
  documented in-code, revisit if the pinned sdk_version drops the fallback
  — T-BANNER-01's wiring assertion is the tripwire. NOT flipped: F-29
  stays partial and F-19 stays manual-FAILED — both await render session
  3's citable per-check-ID PASS (§6.9 when recorded), per the standing
  rule that a fix alone never flips a browser-FAILED row. F-29's
  reconciliation demanded by decisions is on record: demoted round 6, held
  at partial round 7, matrix and render record in explicit agreement.
  Round 8 (2026-08-31), on render session 3's evidence (states.md §6.9,
  dated per-check-ID append-only row-set — verified from this seat, suite
  re-run 58/58 own run, 1.16s): **F-29 FLIPPED VERIFIED — browser-confirmed**
  on §6.9 rows (a)–(e) + overall PASS; **P-11 CLEARED**, all three clauses
  met, and it stays in §7 as a permanent regression gate. **F-19 held at
  manual-FAILED on the THIRD §6.9 FAIL row**, and the FOURTH
  green-guard/browser-false instance REGISTERED as spec §22b: T-BANNER-01
  green, browser confirms computed `position: sticky` — yet the banner
  scrolls away because `.gradio-container-6-26-0` computes `overflow:
  hidden` while the document is the scroller. Blindness ladder now
  three rungs: serialization (T-SER-01) → specificity (T-THEME-01b) →
  structural context (T-BANNER-01) — a static pin verifies rule-APPLIED,
  only the browser verifies rule-EFFECTIVE. Per the house discipline the
  §22b acceptance contract is written BEFORE the fallback lands:
  position:fixed + height reservation + T-BANNER-01 updated same-change,
  red-first against the current sticky build (verifiable by construction),
  F-19/P-5 clearing only on session 4's single banner-in-viewport check
  (§6.10 when recorded). M-UX-02's light-theme rider lifted per §6.9;
  design's new minor R-12 (S5 emphasis order: mechanical headline above the
  routing strips vs S5's strip-on-top spec) is noted as design-catalogued,
  copy complete and honest, post-pilot class — no matrix row opens, no
  gate touches it.
  Round 9 (2026-08-31), registered after independent verification of every
  claim (own suite run 59/59 in 1.24s; own cmp of the strings pair; own
  read of app.py's `_CSS`/spacer/wiring and of both rewritten tests in
  full): (1) **§22b clause (1) executed** — the position:fixed fallback and
  the rewritten T-BANNER-01 landed in ONE change, red-first by
  construction, docstring carrying the rule-applied-vs-rule-effective
  lesson and naming session 4 as acceptance owner; the seventh consecutive
  same-change fix+guard pairing. F-19/P-5 deliberately NOT flipped — the
  standing rule that a landed fix never flips a browser-FAILED row is the
  whole point of the blindness ladder. (2) **T-VEND-01's first live catch**
  registered on F-25: canonical mint → guard red mid-flow → byte-identical
  re-vendor same change; the vendoring flow's first content exercise ran in
  the documented direction, and the served stale notice now states the true
  manual-Compare behavior (the corrected tail verified in BOTH copies of
  strings.py — the old text was a false claim in the state that exists to
  prevent false claims). (3) **F-30/T-STR-01 registered** (spec §23) with
  T-CUST-01(b)/T-SER-01(c) strengthened same-change — two guards that had
  pinned the defect shape as expected output now pin its absence.
  (4) Engineering's refusal to wire `str.log.loaded/_one` and
  `str.m1.progress_zero` is ACCEPTED as compliant: no call site exists
  (grep-verified), so no behavior ships and no row opens — unwired
  catalogue entries are design-side inventory, not features. (5) Suite pin
  59/59; the sole remaining agent-checkable flip condition on the release
  path is render session 4's single check, plus M-UX-02's human sitting.
  Round 10 (2026-08-31), on render session 4's evidence (states.md §6.11,
  dated per-check-ID append-only — read in full from this seat; suite
  re-run 59/59 own run 1.21s; cmp byte-identical): (1) **F-19 FLIPPED
  VERIFIED — browser-confirmed — and P-5 CLEARED**, on the single §22b
  acceptance check and nothing else (banner rect top 0 / bottom 77.2 in
  the 792px viewport at scrollY 1500, computed position:fixed, served 0→1
  dark theme), after three FAILs and two defeated mechanisms; both riders
  (height reservation, opaque background) PASS. P-5 stays in §7 as a
  permanent regression gate. The matrix carries ZERO open
  browser-refutations for the first time; the render-session ledger is
  CLOSED (§6.11 conclusion 3 — a new session triggers only on copy or
  layout change). (2) **F-30 upgraded to browser-confirmed**: §6.11's two
  bonus rows put the singular selection and the corrected stale tail ON
  SCREEN — the states.md → strings.py → vendored copy → browser chain is
  verified end-to-end. (3) **R-12 sign-off RECEIVED explicit** (states.md
  §6.4 catalogue entry, round-9 classification block + §6.11 conclusion
  5): design-catalogued, post-pilot, no matrix row — the carried round-8
  question closes on the designer's own statement, not inference. (4)
  **F-25's arc registered with direction** per architecture's demand:
  drift-episode (round 2) → test-enforced (round 3) → first live exercise
  clean (round 9) — a flow-conformant red and a regression red are now
  distinguishable in the ledger. (5) Release-path remainder: F-17/M-UX-02
  (gtm's witness slot NAMED for today 2026-08-31, backstop first hour of
  2026-09-01) and D1-D6 (SLA executes 2026-09-01; regeneration duty ARMED
  — T-M0-01/T-PAR pinned constants and every T-FRAG fixture regenerate in
  the resolution round, each with a provenance line citing the per-entry
  resolution_source, before any push on new values).
- **Standing method — defects that cross the repo/browser seam** (registered
  round 11 per architecture's demand; source arc: architecture §5.10 R-8/R-9 →
  §5.11 R-9b → §5.12 R-10 → §5.13 M-UX-03 — four consecutive cycles, zero
  renegotiation): when a browser session refutes a green guard, the response is
  ALWAYS, in order: (1) the strengthened acceptance contract is written and
  pinned BEFORE the fix exists (red-first against the current build, verifiable
  by construction); (2) the fix lands in the SAME change as its guard, never
  guard-less; (3) the static pin claims only rule-APPLIED — the browser session
  alone verifies rule-EFFECTIVE, and the row flips only on a dated per-check-ID
  browser row, never on the green guard; (4) each half is closed by the
  instrument that owns it, and the close waits for both. The blindness ladder
  this method was forged on — serialization (T-SER-01) → CSS specificity
  (T-THEME-01b) → structural context (T-BANNER-01) → applied-vs-effective
  division (§6.11) — is the reusable doctrine, not episode history: a future
  seam defect enters at step (1), and a fix that skips the sequence does not
  flip a row in this matrix.
  **Round-14 extension — the ladder turns on the instruments themselves.**
  Two consecutive rounds have now found defects not in the build but in this
  matrix's own evidence: round 13, an instrument registered against a check
  broader than what it measured (M-UX-02's mode scope); round 14, instruments
  certifying a module they never identified (T-VEND-01's path comparison, and
  every suite count resting on it). These are one error at two altitudes —
  **verifying an instrument's internal quality and never verifying what it is
  attached to.** Registered as standing method, in addition to the four steps
  above: (5) **an instrument is not registered until it has been diffed against
  the claim it discharges — in SCOPE (round 13) and in SUBJECT (round 14).**
  Scope: does it measure everything the check asserts? Subject: does it assert
  on the artifact that actually runs, or on a proxy it constructed itself? A
  guard that rebuilds a path from `__file__`, greps a source file, or reads a
  declaration is evidence about a *representation*; only importing the module,
  inspecting the served object, or opening the browser is evidence about the
  *thing*. Both classes are legitimate and this matrix keeps both — but they
  must be labelled, and a rule-APPLIED instrument may never be cited for a
  rule-EFFECTIVE claim. Corollary, applied to this leaf without exception:
  **when the defective instrument is compliance's own, the collateral is
  priced in the record rather than quietly superseded** (see the round-14 entry
  downgrading rounds 9–13's own-run certifications to cwd-conditional).
- **Gate-protocol close (gtm demo gates), registered round 11:** gtm's
  banner-in-frame gate lifted round 10 on §6.11's single PASS line per the
  pre-wired per-line protocol, after holding through THREE guard-green repo
  landings (rounds 7, 9 fix landings; §6.5/§6.7/§6.9 FAILs standing) — no
  early lift on a green guard, no late drift after PASS. The demo surface
  carries ZERO gates and ZERO workarounds as of round 10. F-17/SC-06
  conversion is UNSOFTENABLE: it converts only on a dated timed record with
  the named witness (M-UX-02), identical whether the sitting runs in today's
  slot or the 2026-09-01 backstop hour; a slipped slot changes the date on
  the record, never the standard. **Round-12 extension:** the conversion's
  evidence vehicle is now pre-registered (launch-copy.md 1c-i template,
  verified verbatim from this seat; design's §6.12 protocol as the second
  instrument), and BOTH branches are priced in advance — a filled record
  flips F-17 as a read; a recordless or voided window leaves F-17
  manual-pending and SC-06 "designed so, not yet timed" with the miss logged
  as a dated scheduling fact. The ledger states what happens when the humans
  don't show, before anyone knows whether they do. **Round-13 corrections,
  both tightening:** (i) the registered instruments measure 1→N ONLY, so a
  filled record flips **M-UX-02a** and converts SC-06 for the measured mode
  only, naming it in every payload — **M-UX-02b (0→1)** has no instrument and
  stays unconverted regardless of tomorrow's outcome; (ii) the canonical
  non-conversion string is **"designed so, not yet timed"**, identical across
  this matrix, gtm's 1c-i and design's §6.12 (verified verbatim this round),
  so a recordless close is one string in three files rather than three
  paraphrases; (iii) T-NEG-07 now guards the shipped-copy side of the same
  refusal automatically, so the discipline no longer depends on every future
  copy edit remembering it.
- **Change control:** a new feature enters a Leaf only with a matrix row; a matrix
  row cites a Spine anchor or it does not merge.

## 7. Pre-push refusal checklist (release gate for sequencing node `space-push`)

Run immediately before any push to the Hugging Face Space. All automated items
are single commands; the push is blocked on any failure.

| # | Check | How | Backing |
|---|---|---|---|
| P-1 | No runtime LLM / network calls | `pytest tests/ -k "no_llm or no_network"` green. **ROUND-19 SUBJECT CORRECTION, found by running the suite rather than by reading it, and it is this cycle's fifth instrument-scope defect — on the Spine's FIRST refusal.** `test_no_llm_or_network_imports` asserted that no forbidden module appears in `sys.modules` **of the pytest process**, which is not the product: it is whatever every previously-collected test file happened to import. `tests/test_packaging.py` execs `app.py`, which imports gradio, which imports `httpx` — a legitimate UI dependency (T-PKG-02 keeps gradio out of the engine; `test_no_network_calls_at_runtime` kills the socket) — so the clause's green was an artifact of `test_engine` sorting before `test_packaging`. **Demonstrated on the unmutated repo before any edit: `pytest tests/test_packaging.py tests/test_engine.py` → FAILED … AssertionError: httpx.** The same clause passes alone. Two things were wrong at once and only one is the usual kind: the assertion was ORDER-DEPENDENT (a guard on the Spine's hardest refusal that reds on the order its own suite is invoked in is a guard nobody can act on — the honest reading of that red is "some other test imported gradio", and the fix a hurried reader reaches for at that hour is to delete the line), and it was measuring the TEST SESSION rather than the shipped package. Corrected in the direction that makes it stronger, not looser (spec §27i): the claim is now asserted **in a child process** — importing `pairwisepm` and every submodule in a fresh interpreter pulls in no LLM and no network client — which is order-independent, is the property a `pip install` of this project can actually break, and catches what the source-scan half cannot. **Red-first, both directions:** the old form's red is the ordering run above; the new form's red is a `_il.import_module("httpx")` at the bottom of `pairwisepm/engine.py`, which the regex source scan does NOT see and the child process does (scratch tree, control run beside it). The source scan over `pairwisepm/*.py` + `app.py` is unchanged. Suite 81/81, and 61/61 on the two-file ordering that was red an hour ago. **ROUND-20 — THE REPAIR NOW HAS A FLOOR, AND THIS GATE'S `-k` FORM HAS A STATED BLIND SPOT.** (a) T-NEG-01d (spec §27j, design's demand) asserts by AST that `FORBIDDEN_IMPORTS` keeps naming the network and LLM modules, that neither refusal clause acquires a skip, and that both halves of T-NEG-01a survive — because the fifteen-second exit from a red on this gate is a one-token deletion that leaves the gate green. Four mutants, each reddening T-NEG-01d alone with T-NEG-01a green beside it. **T-NEG-01d is inside this gate's `-k "no_llm or no_network"` selection** — its name carries `no_llm` — so the floor runs whenever the gate does; verified, not assumed: `pytest tests/ -k "no_llm or no_network"` reads **3 passed, 80 deselected**, own run. (b) Decisions' finding, recorded against this gate rather than only in their queue: under the OLD subject this gate was structurally blind to the defect it is named for — `-k` DESELECTS every polluter and the pollution was RUN-time, so P-1 read `2 passed / 78 deselected` GREEN in the same tree and the same minute the full suite was red. The child-process subject removes that blindness as a side effect, and it is the strongest evidence the correction was right. The general lesson is registered in spec §27i and belongs to this gate permanently: **a gate whose command narrows the run is a gate that cannot observe a defect the narrowing hides** | N-01 |
| P-2 | No server-side persistence in the app | `pytest tests/ -k "persistence"` green + M-UX-04 on the running Space after push | N-06 |
| P-3 | Interval always shown | `pytest tests/ -k "interval_always"` green | F-06 |
| P-4 | Too-close-to-call never forced into a winner | `pytest tests/ -k "verdict"` green | F-06 |
| P-5 | 0→1 banner permanent | `pytest tests/ -k "banner"` green + M-UX-03 — **CLEARED round 10, both §22b clauses met**: (1) fallback + rewritten T-BANNER-01 same-change round 9; (2) render session 4's single check PASS (states.md §6.11: banner rect in viewport at scrollY 1500, computed position:fixed, served 0→1 dark theme). Stays in this checklist as a permanent regression gate: T-BANNER-01 must be green at every push, and any banner rule/layout change triggers a new render session before it ships | F-19 / §22b |
| P-6 | D1/D2 resolved or defaults explicitly accepted (no real logs against unsigned priors) | decisions.yml status for D1/D2 ≠ pending, or written default-acceptance | F-20 / G-D1D2 |
| P-7 | Requirements whitelist unchanged | `pytest tests/ -k "requirements_whitelist"` green | F-23 |
| P-8 | Full suite green, zero unexpected skips | `pytest tests/` (only the gradio importorskips — T-PKG-03, T-CUST-01, T-CEIL-03, T-SER-01, T-THEME-01b, and T-STR-01 — may skip in a non-UI env; on the Space image they must pass, and they pass locally under gradio 6.26.0: 59/59, round-9 own run; 60/60 at round 13 with T-NEG-07 added. T-THEME-01, T-BANNER-01, T-NEG-07 and T-DELIV-01a are static and never skip; T-DELIV-01b is gradio-gated. T-VEND-01/02/03/04/06 must never skip in the repo context, and **T-VEND-05 must never skip anywhere** — it is the only clause on this board that asserts served copy on a stripped install. Round-15 count: **67/67**, own run, from the repo root AND from an off-root working directory — the count is anchored to a verified module by T-VEND-02 rather than to whatever the working directory happened to bind. **ROUND-16: the "zero unexpected skips" clause of this gate was itself cwd-shaped and this seat did not notice for two rounds.** "No unexpected skips *in the repo context*" is satisfiable by guards that skip everywhere else, and T-VEND-03/04/06 did exactly that — gated on the DESIGN LEAF, which `pyproject.toml`'s sdist include does not ship. Corrected at the predicate (spec §27a), and the gate's own wording is corrected with it: **each guard must run wherever ITS OWN subject exists, not wherever another leaf's file happens to be.** T-VEND-04 now never skips anywhere; T-VEND-03/06 skip only with no `<root>/configs`; T-VEND-01/02 skip only with no design authority, which is honest. New this round: **T-COPY-01/01b and T-NEG-08/08a/08b (tests/test_copy_surfaces.py) never skip in any tree carrying `configs/` and `app.py`.** Round-16 count: **72/72**, own run, repo root AND off-root. **ROUND-18 additions and their honest skips, measured rather than asserted:** T-COPY-02 and T-COPY-02b skip where `leaves/design/copy-authority.yaml` is absent — their own subject, the stripped install a user receives — and in an sdist-shaped tree the file reports **8 passed, 2 skipped**, exactly that pair; **T-COPY-02c, T-COPY-02d and T-COPY-03 never skip anywhere**, so this file, like `test_vendoring.py` since T-VEND-07, cannot return an all-skipped green. Round-18 count: **78/78**, own run, repo root AND off-root. **ROUND-19 additions, and the one honest skip they introduce:** `tests/test_audit_honesty.py` adds T-NEG-09 (which renders the audit view for real and therefore skips where gradio is absent — its own subject, gated exactly as `test_packaging.py::_load_app` is) and T-NEG-09b (an AST census of `app.py`, which NEVER skips), so this file too cannot return an all-skipped green; `test_copy_surfaces.py` adds T-COPY-02e, which never skips. Round-19 count: **81/81**, own run, repo root AND off-root, and in an sdist-shaped tree the two copy files report **11 passed, 2 skipped** — still exactly the fixture-dependent pair on their own subject. **One clause in this gate's own suite was ORDER-DEPENDENT and this seat found it by running the suite rather than reading it** — see P-1: `pytest tests/test_packaging.py tests/test_engine.py` reddened N-01's guard on the unmutated repo. "Zero unexpected skips" was never the only way a suite lies about itself; **a green that depends on collection order is the same defect one axis over**, and this gate's wording now says so: a count is evidence only if the same clauses assert in any invocation order | all |
| P-9 | Vendored strings byte-identical to design's copy authority | `pytest tests/test_vendoring.py` green — **all three clauses as of round 14**: T-VEND-01 (files on disk), T-VEND-02 (the BOUND module's identity and bytes), T-VEND-03 (the config dir the engine actually loads), T-VEND-04 (exactly one importable copy on `sys.path`), and **round 15: T-VEND-05 (the bound module's R-10 VALUES — CTA key present, stale card claiming no auto-recompute — which is the only clause here that does not skip on a stripped install)** | F-25 / §24 / §26 |
| P-12 | **Exactly one importable copy of the package** — `import pairwisepm` must resolve inside the repo checkout regardless of working directory | `pytest tests/test_vendoring.py` green — **fully automated as of round 14**: T-VEND-02/03 pin that this session bound the right copy, and **T-VEND-04 pins the COUNT** (no second `pairwisepm/__init__.py` anywhere on `sys.path`), which is the half the binding checks are silent about — from the repo root `sys.path[0]` wins and they stay green while a stale install waits for the first off-root launch. Round-14 origin: exactly that shadow existed, drifted, and every guard stayed green; an off-root launch would `KeyError` at `app.py:848` before first paint. A plain `pip install .` into the working venv recreates the condition in one command with no other symptom — **it now reds T-VEND-04 instead of passing silently**, so this gate no longer depends on anyone remembering to inspect `direct_url.json` | F-25 / §24 / architecture A-13-01 |
| P-13 | **Banner rule is DELIVERED, not merely written** — gradio major bound intact and the fallback still present | `pytest tests/ -k "gradio_major or banner_css"` green (T-DELIV-01a/b, spec §25). Widening `gradio>=6.0,<7` is EVIDENCE LOSS, not housekeeping: it reds here and routes to a new render session before shipping, because the `#pwpm-banner` rule reaches the page only via `_deprecated_css` (`demo.css` is `None`) | F-19 / §25 |
| P-14 | **Witness-sitting pre-flight: the build being timed is the build this matrix describes** — before an M-UX-02a sitting starts, `pytest tests/test_vendoring.py` must be green on the machine that will run the app, and the result recorded in the witness template | `pytest tests/test_vendoring.py` green (T-VEND-01..06), noted in gtm's 1c-i record beside theme, mode and working directory. **Round-15 origin:** gtm asked for a launch-directory precondition on the theory that an off-root launch binds a stale copy and dies before first paint. The substance is right — a run against a non-authority copy must produce NO RECORD, never a FAIL — but the stated mechanism is false for the documented launch (`python /abs/path/app.py` sets `sys.path[0]` to the SCRIPT's directory, not the cwd) and, since round 14, there is no stale copy to bind. So the precondition is registered as **the machine check the copy rows already own** rather than as a directory rule a presenter must reason about at the hour: the witness records a test outcome, not a guess. A red here voids the sitting BEFORE the clock starts, which costs a re-schedule; the same red discovered afterwards costs the record. **ROUND-17 SKIP-AWARE CLAUSE (sequencing's demand, accepted whole and then backed by an instrument): P-14 IS GREEN ONLY IF THE GUARDS RAN.** Operative form, machine-decidable and count-agnostic so a pin that moves every round cannot break it: **exit code 0 AND `0 skipped`**, and the witness line records the skip count beside the result (`N passed, 0 skipped`). Any skip in that file at the hour means the sitting does not start until it is explained. Their finding is exact and it is about the file, not the gate — **pytest exits 0 on an all-skipped file**, and engineering measured `4 skipped in 0.00s` in an sdist-shaped tree last round, so this gate's green was satisfiable by a run in which zero assertions executed. A false green here does not cost a re-schedule; it costs the RECORD, and F-17 would have flipped a Spine metric on it with no way to tell that from a genuine measurement. **What this seat added beyond the clause asked for: the clause is now enforced rather than trusted.** New guard **T-VEND-07** (spec §27c) asserts from the file's own AST that T-VEND-04 and T-VEND-05 can never acquire a skip predicate or marker, and that no clause may skip on a predicate that does not name its own subject — so the floor under P-14 survives a future edit made for convenience, and a green in any tree entails that the count and the served values were asserted. A caveat asking a presenter to count skips is the honor system with a stopwatch on it; this is the one gate whose failure mode is silent AND time-boxed. **Scope stated so the clause is not read wider than it holds:** T-VEND-01/02 skip where the design leaf is absent and T-VEND-03/06 where `<root>/configs` is absent, all four honestly; both wheel and sdist ship `configs`, and any tree the app can be launched from carries it, so `0 skipped` is achievable at the sitting — but if the presenter's tree is a stripped install lacking `leaves/`, the two design-authority clauses skip and P-14 is NOT green under this reading. **CONTESTED — D10, SLA 2026-09-02 (decisions' demand, accepted round 19; this seat's position below is UNCHANGED and stands as D10's option 1).** This cell is the one place in this matrix where a state rested on the seat that owns the row declaring its own consequence intended, and this matrix's own standard is that a row's state rests on a citable artifact rather than on nobody having contradicted it. Two artifacts now sit against it and both are cited here so the cell is falsifiable from itself: (i) design's §6.13 pre-flight box says the opposite in terms about the same command — *"the governing clause is T-VEND-05; T-VEND-02 is welcome when it runs and is not required, because it skips on a stripped tree"*; (ii) decisions reproduced the divergence on the tree this project actually ships (scratch, sdist shape, no repo file mutated: exit 0, 5 passed, 2 skipped, T-VEND-05 asserting) — and architecture's packaging census bounds it to exactly that one tree, since the wheel ships no `tests` and cannot run the pre-flight at all. **The position, kept at full strength beside the mark:** the sitting is timed against the build this matrix describes, the M-UX-02a record converts a Spine metric, and a pre-flight that returns green on a tree missing the design authority buys its green by not looking. **The cost of the position, stated because a position whose cost is unlisted is an assertion:** it makes the presenter's tree SHAPE a de facto precondition of this gate, which is a precondition of the class sequencing refused, arriving through an instrument rather than through a clause — decisions' demand on sequencing this round asks them to answer that in their own file, and this seat does not answer it for them. Nothing here gates anything, D10 cannot touch the sitting, and the scheduled sitting runs from a checkout where every reading agrees (`0 skipped`, 7 passed, own run). **ROUND-18 CLAUSE (a) — THE RE-OPENED SITTING (sequencing's demand, accepted, and narrowed in the one direction that keeps it a gate).** Under the encoded ordering there is no collision: the backstop M-UX-02a sitting convenes BEFORE the D1-D6 resolution round, so P-14 runs on a pre-write tree. But branch [3] WINDOW CLOSED leaves the sitting RE-OPENABLE by a newly scheduled dated sitting, and such a sitting falls AFTER the `configs/*.yaml` write — at which point T-VEND-06 reds on the expected post-write condition and this gate would fail a build that is correct. Operative form: **on a RE-OPENED sitting only, refreshing the install (or confirming zero duplicate `configs` trees on `sys.path`) is a PRECONDITION STEP that runs BEFORE the pre-flight, not an excuse read off a red afterwards.** Run the remedy, then run the command. If T-VEND-06 still reds after the refresh, that is a real defect and P-14 fails normally. **Why it is written as a step and not as an exemption:** sequencing asked for "a red traceable to the resolution-round write with the remedy not yet applied is not a P-14 failure", and that phrasing puts a judgment call in the presenter's hands at the hour — exactly the thing P-14 exists to remove, and the same species as the "green" this seat had to replace with `0 skipped` last round. Ordered as a step, the condition is machine-decidable (refresh, or confirm the duplicate count is zero) and the gate keeps its property: no red is ever read as expected by someone standing in front of a guest. Not on the scheduled sitting, not on the round, not on space-push. **ROUND-19 NOTE — sequencing's re-press is DISCHARGED, and it was discharged before it was re-pressed:** their round-18 packet reports "own grep finds no reopen language on or near the P-14 row", and clause (a) above IS that language, landed the same round their demand was written — our packets crossed both ways. Nothing further is owed and nothing is being withheld: the substance they asked for is registered whole (a re-opened branch-[3] sitting must not be voided by the expected post-write T-VEND-06 red), in the FORM this seat narrowed it to and stated openly at the time — an ordered precondition STEP rather than an exemption a presenter reads off a red. The narrowing is still open to dispute rather than assumed agreed: if sequencing judges that the step form loses something their branch-[3] path needs, this seat will take it as a dispute and rule on it, not treat their silence as consent. **Not on the scheduled sitting, not on the round, not on space-push.** **ROUND-18 CLAUSE (b) — WHICH CLAUSES DECIDE A D9 VOID (decisions' demand, accepted, with the two states distinguished because they are not the same question).** The command stays `pytest tests/test_vendoring.py` **entire** — an instrument that is a whole FILE cited for a predicate that is a SUBSET of it is scope wider than claim, which is the species this seat has caught twice in its own rows. So: **(i) PRE-FLIGHT, before the clock — ANY red or any skip means the sitting does not start.** That is unchanged and it is cheap: it costs a re-schedule. **(ii) VOIDING, on a red discovered AFTER a sitting ran — only the bound-copy clauses T-VEND-01/02/05 void the record**, because D9's ruled predicate is *which copy was served*, and those three are the clauses that answer it. A post-hoc red on T-VEND-03 (resolution), T-VEND-04 (package count) or T-VEND-06 (duplicate freshness) blocks a push and is a real defect to fix, but it does not void a completed measurement of a build whose served copy was the authority's. T-VEND-07 voids nothing: it is a guard on the instrument, and a red there means the pre-flight's own floor is gone, which is a reason not to trust a FUTURE green rather than a reason to discard a past one. The distinction is readable off the failure line, which was decisions' whole point | F-17 / F-25 / F-31 / D9 |
| P-15 | **The Spine's excluded-from-score refusal is visible on screen, and rendered config text is written copy** — no release ships with an evaluative input missing its `(not scored)` marker, or with a placeholder / key-echo in a mode schema's rendered text | `pytest tests/test_copy_surfaces.py` green — T-NEG-08 (four AST-censused labels in `app.py`), T-NEG-08a (both schemas' `note`), T-NEG-08b (structural: `EvaluativeInput` carries no weight field; no key is both scored and evaluative), T-COPY-01 / 01b (`configs/*.yaml` rendered text). **Round-16 origin:** design's §6.15 census found the copy chain certifying one population of three; the four parentheticals carrying the Spine's hardest scope boundary were watched by no instrument, and deleting one left the suite green. **This gate is armed for the D1-D6 resolution round specifically:** that round edits `configs/*.yaml`, where a policy value and a rendered string are neighbouring lines, so it is the single most likely moment for a text field to move under cover of "YAML only". **ROUND-18: the gate's file grew four clauses and a guard-the-guard, and the gate itself acquired an ENTRY PRICE.** New: T-COPY-02 (config text byte-equal to design's ratified `leaves/design/copy-authority.yaml`, both directions), T-COPY-02b (the four evaluative labels' WORDS, not just the marker), T-COPY-02c (an exempted field must cite a guard that still exists), T-COPY-02d (the rendered-text census derived from the dataclasses, never a hand list), T-COPY-03 (this file's own shape: required clauses present, T-NEG-08 still an AST census pinned at four, no unsanctioned skip, a counted no-skip floor). Command unchanged, `pytest tests/test_copy_surfaces.py`, now **10 clauses, 0 skipped** in a repo checkout and **8 passed / 2 skipped** in an sdist-shaped tree, the two skips being exactly the fixture-dependent pair on their own subject. **ADMISSION STANDARD ON THE D1-D6 RESOLUTION-ROUND PROCEDURE — registered here, at engineering's demand, as a RULE and not a feature:** no further gate, command or check enters that procedure without a **DEMONSTRATED RED** — the mutation that makes it fail, run and reported by the proposing seat. Engineering's reasoning is the operative reasoning and this seat had no counter to it: their procedure now runs two commands, an edit-class bright line, a two-recipient notification duty and an expected-red with a named prohibition — a correct ceiling reached in three rounds by seats each adding one cheap line, and the failure mode being priced is not any one of them but the fourth. **A check nobody can red is indistinguishable at 11pm from a check that already passed, and a procedure long enough to skim is a procedure that gets skimmed on the one day it matters.** Both of round 17's additions volunteered the standard unasked (this seat mutated a rationale to TBD, deleted one `(not scored)` and reduced a schema note: 3 failed with `test_engine.py` entirely green; architecture produced a dist-info RECORD and two digests engineering recomputed), so costing it into the row makes it the entry price rather than a courtesy. **This seat owed it first and paid it in the same round it registered it:** eight mutations for the five new clauses, scratch tree, no repo file mutated, tabulated in spec §27f — including the one that cost this seat a claim it had already written into a docstring (the banner premise, false, retracted before shipping). The standard is not "show a red if convenient": a proposal without one is refused, and this row is where that refusal is cited from. **ROUND-19 BOUNDARY ON THAT STANDARD (engineering's re-press, accepted whole and written as they asked — into the row, so their own edits cannot be cited as precedent for growth): THE STANDARD BINDS PROPOSALS THAT ADD A STEP, NOT PROPOSALS THAT FIX A SENTENCE.** A new GATE, COMMAND or CHECK on the D1-D6 resolution-round procedure requires a demonstrated red. A CORRECTION to a claim already in it — a scope word on a render claim, a narrowing of an activation claim, a pass-condition clarification, the three engineering landed in round 18 — requires no red and must not be slowed by asking for one, because the failure mode being priced is LENGTH and a rule that taxes honest fixes buys length while pretending to sell brevity. The test is countable rather than a matter of judgment, which is what keeps the boundary from becoming the loophole: **does the procedure's step count move?** Engineering's counts are the baseline (three constraints, two commands, unchanged across round 18) and a proposal that leaves both unchanged is a correction. **ROUND-19 CLAUSE ADDED TO THIS GATE'S FILE — T-COPY-02e (`test_banner_exemption_rests_on_an_import_time_assert`, spec §27h), with its red demonstrated first as this standard requires:** deleting `app.py`'s module-level `assert Z2O.banner == S["str.banner.01"]` reds this clause and NOTHING ELSE in the suite (scratch tree, no repo file mutated, control run beside it). **The scope word architecture demanded, and the reason it is now four-of-five rather than a hole:** T-COPY-02's diff covers the config text design RATIFIED — nine of the ten names in the fixture's `render_map`, and on the RENDERING half four of five (`label`, `factors[].name`/`.scale`/`.rationale`). The fifth is `banner`, and design ruled it in §6.19 by option (b): exempt from the fixture by AUTHORITY — the catalogue's `str.banner.01` owns those bytes — with the render_map row naming its guards. So a green T-COPY-02 means *the ratified config copy matches design's ratified text*, never *all rendered config copy is verified*, and the banner's own instruments are named where a reader stands: `app.py`'s import assert (which fires before first paint, cannot acquire a skip and cannot be deselected — architecture's point, and the reason it earned a guard of its own this round), plus `test_zero_to_one_banner_mandatory` / `test_banner_attached_and_wording`, whose continued existence T-COPY-02c checks by name. Command unchanged; the file now runs **11 clauses, 0 skipped** in a repo checkout. **ROUND-20 — ONE CLAUSE ADDED AND ONE FAILURE MESSAGE GIVEN AN OWNER; THE PROCEDURE'S STEP COUNT IS UNCHANGED, WHICH BY THIS ROW'S OWN BOUNDARY IS WHAT MAKES BOTH ADMISSIBLE** (engineering's countable test: three constraints, two commands, both unmoved). (a) **T-NEG-08c** (`test_the_pick_question_asks_for_the_users_own_pick`, design's §6.19(iii) demand, spec §27j) pins the literal `"Which do you actually pick?"` byte-exact on `app.py`'s `gr.*` construction surface, count pinned at one, plus its carrier (`gr.Radio` — a two-choice widget is what makes the logged pick one of exactly the two ideas compared). It is its OWN clause and deliberately NOT a fifth member of T-NEG-08's set: that census's `== 4` count pin is what makes a restructured panel rendering zero labels fail, and widening it would silently widen engineering's ENG-COPY-EVALLABELS-01 trigger, which they accepted on the strength of its boundedness. It reads a SEPARATE helper (`_app_widget_labels`, subject-named skip on `APP`, registered in `_PERMITTED_SKIP_HELPERS` — a fourth entry there is a deliberate act that T-COPY-03 reds on) so T-NEG-08's own census is untouched. **The honest history, because the row is about coverage and not about credit:** design recorded this literal as "covered in the interim by the eyes-on five", gtm correctly RETIRED that ritual in round 17 on the strength of executed censuses, design struck their own cover sentence in place when they found it named nothing that runs and DECLINED gtm's offer to reinstate one eyes-on line — trading an instrument for a ritual — and filed here instead. Between those rounds the literal had zero instruments. Red-first, two mutants, scratch trees, no repo file mutated: dropping `actually` from the wording, and `gr.Radio` → `gr.Dropdown`, each reds T-NEG-08c alone against a control run. (b) **THE FIXTURE'S THIRD OBSERVABLE STATE, given an owner at the point of failure** (engineering's demand, accepted; it is an error message, not a gate — it adds no command, no check and no step, which is exactly the boundary this row registered in round 19). `leaves/design/copy-authority.yaml` ABSENT skips honestly on the pair's own subject; PRESENT is diffed; **PRESENT AND UNREADABLE is now a red that names whose file it is** — it stays a red, because "design's ratified text is unreadable" is not the claim "this tree has no design leaf", and the re-raise says: that file belongs to the DESIGN leaf, it is outside every tree the D1-D6 resolution round writes to, FIRST ACTION is to re-run, and blanking it to obtain a skip converts a loud red into a quiet green while the config copy stops being diffed against anything. Engineering OBSERVED the state rather than constructing it (mid-save of the fixture, their own edits confined to two docstrings: 2 failed on a bare `yaml.scanner.ScannerError` naming `yaml/scanner.py`, green 40 seconds later) and priced the class without mutating a repo file: 855 of the fixture's 8593 single-byte prefixes fail to parse. `UnicodeDecodeError` is caught beside `yaml.YAMLError` for a reason found by demonstrating the red rather than by reasoning about it — a truncated save can cut a multi-byte character and raise out of `read_text` before pyyaml is ever reached. Red-first, two mutants: truncation mid-character and an unterminated quoted scalar, both surfacing the owned message with the underlying exception quoted inside it. **Command unchanged. The file now runs 12 clauses, 0 skipped in a repo checkout and 10 passed / 2 skipped in an sdist-shaped tree** (own runs) — the two skips still exactly the fixture-governed pair on their own subject, and T-NEG-08c runs in both trees because the sdist ships `app.py`, so its activation follows the cross-reference clauses rather than the fixture-governed ones | F-32 / F-33 / §27b / §27e / §27f / §27h / §27j / Spine Scope Boundaries |
| P-10 | No-imputation blocking holds in the SERVED UI — untouched fields never submit values | T-SER-01 (spec §20) implemented AND green — **CLEAR and BROWSER-CONFIRMED** (round 6: states.md §6.7 records all four R-8 behaviors PASS live). Stays a permanent regression gate: any future factor-input component change reds here before it ships | F-28 |
| P-11 | Verdict card legible in the served dark theme — every text-bearing element inside a forced-background block carries its own color | **CLEARED round 8 — all three clauses met**: (1) R-9b fix + (2) T-THEME-01b same-change, red-first honored (verified round 7, compliance's own read + re-run), + (3) render session 3 legibility PASS on EVERY §6.7-failing surface (states.md §6.9 rows (a)–(e), computed-style evidence, per-check-ID append-only). Stays in this checklist as a permanent regression gate: T-THEME-01b must be green at every push, and any future forced-background surface enters its audit list before it ships | F-29 |
