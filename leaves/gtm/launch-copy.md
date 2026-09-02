# PairwisePM — Launch Copy (sequence-tagged)

leaf: gtm
derives_from: spine/SPINE.md (wins every conflict) · docs/technical-spec.md
sequencing_nodes: pilot-live · ga-live (per leaves/sequencing/work-items.yaml — the two
message sets below are NOT interchangeable; each is gated on its node going live)
copy_sources: leaves/design/states.md (str.* strings quoted verbatim, never paraphrased)
· leaves/gtm/seed-comparison.json (all demo numbers, engine-verified)

---

## 0. Claim ledger — what may be said, when

Claims verified true in the shipped code (engineering exchange note + independent
engine run, 2026-08-30). Say these verbatim at any stage:

| Claim | Basis | Stage |
|---|---|---|
| "Runs fully offline after download — no LLM, no API key, no network calls at runtime." | zero network imports in `pairwisepm/`; runtime deps = numpy + PyYAML (+ gradio for the UI only) | pilot-live onward |
| "The LLM's job was at build time — the runtime is weights and a bias term." | spec §7 epistemics; architecture positioning | pilot-live onward |
| "Your decision log is a JSONL file in your hands — nothing is stored server-side, ever." | log lives in session state, moves only via user download/upload | pilot-live onward |
| "One screen, one sitting, ~16 inputs — designed so a full A-vs-B comparison lands in under five minutes." | **design target, NOT TIMED — M-UX-02 window closed unconvened, 2026-09-01 07:55 CDT; designed so, not yet timed.** (Branch **[3] WINDOW CLOSED** fired and the pre-written text was SWAPPED IN, round 20 — see the resolved branch block below and the dated miss line at 1c-i item 12. This cell no longer says "pending": its window has closed, and a basis that outlives its own window is the one failure this row was built to prevent.) The check would have timed **1→N only**, so nothing here was ever going to convert 0→1. **The 0→1 half is not settled, it is QUEUED — decisions D8, SLA 2026-09-02** (decisions round-14, accepted): whether 0→1 ever gets an instrument is an open ruling with an owner, not a permanent deliberate non-measurement, and this cell must not read as though the coverage question were closed. | pilot-live onward (as design target only) |
| "The model of your judge (M1) activates at decision 10, per mode; ζ and Brier accumulate from decision 1." | engine constants M1_ACTIVATION_N=10; log metrics from decision 1 | pilot-live onward |
| "Swapping A and B flips every probability to exactly 1 − p." | zero-intercept scoring, verified to 1e-12 | pilot-live onward |
| "In 1→N mode, PairwisePM's calibration on real decisions is: [numbers from the calibration report]." | calibration-report node | **ga-live only** |

**Row-4 branch block — RESOLVED, round 20: branch [3] WINDOW CLOSED fired, and
its pre-written text is now in the row-4 Basis cell above, swapped without a
word of drafting.** (Pre-written 2026-08-31, round 13, ~4 hours before the
backstop.) Row 4 was the only ledger row whose basis turned on an event that had
not happened yet, and a "pending" basis must never outlive its own window — a
presenter reading a stale "pending" would be reading a claim the record no
longer supports. Exactly one of these three texts replaced the row-4 Basis
cell in the round the M-UX-02 branch resolved. No fourth wording existed, and no
branch required drafting at the moment of truth. **The three texts are kept
below unedited rather than pruned to the one that fired**, because the value of
a pre-commitment is only auditable against the branches it did NOT take: a
reader must be able to see that the WINDOW CLOSED wording was written before the
window closed, beside a PASS wording nobody got to soften after the fact:

- **PASS** (filled witness record in 1c-i AND design's dated §6.12
  per-check line, both seats' numbers): Basis becomes `timed fresh-user run,
  [date]: blank questionnaire → first verdict render in [_:__] vs bound 5:00,
  1→N mode, [theme] theme, bound module = design authority's bytes
  (confirmed), witnessed (GTM) + timed
  (design), fresh user, no coaching beyond mode selection` — and only then
  does the Claim cell drop "designed so", becoming the dated **mode-named**
  five-minute claim: **"under five minutes in 1→N, witnessed [date]"**, never
  an unqualified one (compliance round-13, accepted; the sitting times one
  mode, so it buys one mode). Stage cell loses its "(as design target only)"
  qualifier for 1→N only. The 0→1 half of SC-06 stays **"designed so, not yet
  timed"** on this branch too, and a presenter asked about 0→1 speed says that
  phrase — a PASS in 1→N is not evidence about 0→1. That half's coverage is
  **QUEUED (D8)**, not closed: a presenter asked *why* it is untimed says "that
  coverage question is an open decision, not a decision to never measure."
- **FAIL** (record filled, elapsed over 5:00): Basis becomes `timed fresh-user
  run, [date]: **1→N mode**, [_:__] vs bound 5:00 — FAIL **in 1→N**; "designed
  so" framing stays for both modes, elapsed + observed stall points routed to
  design as a defect record`. Claim and Stage cells unchanged. **The mode is
  named on this branch too** (compliance round-14, accepted): what was measured
  and lost is one mode of two, and a presenter reading an unqualified "we failed
  to hit five minutes" would be overstating the loss exactly as the PASS branch
  forbids overstating the win. A scoping rule that binds only the flattering
  branch is not a scoping rule. A failed run is still a dated fact and is worth
  more to this leaf than an untimed one. **The tour says the measured number**
  (design round-13, accepted): a presenter asked "how long does it take?" on
  this branch answers with the elapsed figure that was actually recorded, not
  a softened one, not a range, not the design target restated — "we timed it
  once, [_:__], over our 5:00 target" is sayable; "about five minutes" is not.
- **WINDOW CLOSED — ◀ THIS IS THE BRANCH THAT FIRED (round 20, 2026-09-01
  07:55 CDT, unconvened; no run was voided — none was convened to void)**
  (backstop passes unconvened, **or a run was voided** — see
  the no-third-branch rule at 1c-i item 6): Basis becomes `design target,
  NOT TIMED — M-UX-02 window closed unconvened, [date/time]; designed so, not
  yet timed`. Claim and Stage cells unchanged. Presenters asked "is that
  measured?" answer with the registered phrase — **"designed so, not yet
  timed"** — never with "we're about to test it", which is the softening this
  block exists to prevent.

There is no fourth Basis cell. A voided run does not mint a fourth wording; it
routes to WINDOW CLOSED with its cause named in the 1c-i narrative record, so
the ledger stays three-valued while the cause stays citable.

Never sayable, at any stage (Spine refusals):

- Any predictive-accuracy claim for 0→1 mode, in any wording, including softened
  paraphrases ("directionally right", "usually picks the winner").
- Any 1→N accuracy claim **before** the calibration report exists. Until ga-live,
  1→N accuracy language is exactly: "accuracy is earned via calibration on your own
  log — never asserted up front."
- Describing ζ or Brier as "accuracy" or "predictive" in any 0→1 context — they are
  **consistency measures** (compliance T-NEG-04b applies to marketing payloads too).
- Describing M1 as "live" or "active" in user-facing copy before a real log reaches
  10 decisions (sequencing ruling: code-done ≠ activated).
- Overclaiming the stack: the moat is the four build-side components — GenAI factor
  schemas, the prior-centered shrinkage ladder, path-to-parity math, and the honesty
  rules — not numpy, Gradio, or hosting.

---

## 1. [pilot-live] message set

Gate: `pilot-live` node (HF Space up, smoke-tested, D1/D2 resolved or defaults
explicitly accepted). Purpose: recruit pilot PMs, demo the Space. **Zero accuracy
language.**

### 1a. Space announcement (short post)

> Your prioritization spreadsheet is a random-number generator with a confident font.
>
> PairwisePM is a mechanical pairwise judge for GenAI product decisions: two ideas,
> one questionnaire, one sitting → a winner, a win probability **with an interval**,
> and the exact levers that would flip the verdict. When the interval straddles 50%,
> it says "too close to call — gather evidence" instead of forcing a winner.
>
> No LLM at runtime. The LLM's job was at build time — the runtime is weights and a
> bias term. It removes the Tuesdays.
>
> Try it on the Space: [SPACE_URL] · pip-installable from the same repo.

### 1b. Pilot-PM recruitment blurb

> I'm looking for a handful of PMs working on GenAI features to pilot PairwisePM on
> real A-vs-B calls. What you do: score both ideas on one screen (about five minutes
> by design), log your pick, keep your own JSONL log — nothing is stored server-side.
> What you get: from decision 1, a live consistency meter (ζ) and Brier tracking; at
> decision 10, a model of your own judging — what your picks *reveal* you weigh versus
> what you *say* you weigh. What I get: evidence about whether a mechanical judge
> earns PM trust. No accuracy promises — that's the point. The tool refuses claims it
> can't back.

**HOLD ON §1b, round 19, placed by this seat against its own copy.** This blurb does
not go out until design's pooled-statistics row is closed. The reason is that the
blurb sells, by name, the exact surface that round 18 proved wrong: *"from decision
1, a live consistency meter (ζ) and Brier tracking."* Design demonstrated that
`render_audit` calls `kendall_zeta()`, `brier()`, `outcome_brier()` and
`override_rate()` with **no `mode` argument** (`app.py:416-425`) while every other row
in that table is per-mode — so the meter this sentence promises renders **pooled**,
one cross-mode re-comparison of the same pair drops the displayed ζ from 1.00 to
0.00, and a pooled Brier can paint one line above the caption *"No outcome data about
ideas like yours exists."*

**Why this lands on GTM and not only on design's matrix row, which is the part their
filing did not reach.** Their reassurance — the defect is unreachable during the demo
because no scripted step logs a decision — holds for the sitting, and step 4a is
written to keep it holding (one log, one mode). **It does not hold for a pilot.** A
pilot PM doing "real A-vs-B calls" on a roadmap logs across both modes and re-compares
the same idea by name, which is not an edge case for them — it is the job. So the one
population that is guaranteed to hit the pooled meter is the population this paragraph
recruits, and the sentence that recruits them is the one that names the meter. A
demo can be steered; a blurb cannot. **This is the Spine's `Out:` line reaching a
stranger's screen as a number and a denial of the number, one line apart** — and this
leaf's whole agenda is that the tour never lies, which is worth more than shipping
recruitment a week early.

**What lifts the hold — machine-decidable, no judgment at the hour, and it is
deliberately not a gate on anyone:** the four statistics render mode-scoped, with
design's already-specified copy (their §6.18(iii), IDs reserved). It blocks **§1b
only**. It does not touch the sitting, the demo script, the Space launch payload, the
witness template, or any node on sequencing's graph — and it opens no gate, because a
hold this seat places on its own paragraph is not a precondition on anybody else's
work. If design or engineering judge the pooling correct as built, say so and the
hold lifts on that ruling instead; what it must not do is lapse in silence.

**ROUND-20 STATUS OF THE HOLD: STILL HELD, checked in the source and not
inferred from anyone's packet.** `app.py:414-425` still calls
`log.kendall_zeta()`, `log.brier()`, `log.outcome_brier()` and
`log.override_rate()` with no `mode` argument, so the four statistics still
render pooled and the sentence in §1b still promises a per-mode meter this build
does not render. **What DID land is real and is worth naming rather than
counting as nothing:** engineering wrote the defect down at the call site — a
comment block now sits directly above those four lines naming the pooling, the
owner (F-35), the fix (pass the mode through), and the fact that
`tests/test_audit_honesty.py`'s census clause stays green on the repair — and
compliance instrumented the row the same round it opened. So the next person to
read `render_audit` cannot miss it, and a fixer cannot mistake the census for a
freeze and delete it. **None of that lifts the hold, and this seat is not going
to let "well documented" stand in for "true".** The lift condition is unchanged
and unchanged in kind: the four statistics render mode-scoped, or a seat rules
the pooling correct as built. A defect with a comment on it is still the defect
the blurb sells. **§1b does not go out; every other payload in this file is
unaffected and always was.**

### 1c. Demo script (uses the canonical seeded pair — numbers are engine-verified)

1. Load example: **Reply Drafts vs Instant Summaries**, 1→N mode.
2. Point at the verdict: p(A) = **59%**, 90% interval **52–64%** — "a probability
   with an interval, never a 47.3."
3. Leverage panel: A's margin comes from impact (+.125), unit economics (+.105),
   feasibility and flywheel (+.08 each); effort cancels — both are 9 person-weeks.
4. Path to parity: the one feasible lever for B is impact, +0.5 → **+1.88** on the
   anchor scale — near the top, "that case needs evidence, not enthusiasm."
   Feasibility parity would need ≈4.2 on a 0–4 scale, so the panel refuses it.
4a. **Log the decision — press "Log this decision" with A (Reply Drafts) selected.**
   ONE press, in 1→N, here and nowhere else in this script. The app answers
   "Logged decision #1 — your pick: Reply Drafts" and the model-of-the-judge
   counter advances toward its activation at 10 — which is the whole promise of
   the pilot blurb (§1b) made visible in one click. **Numbered 4a and not 5 on
   purpose:** four other leaves cite this script by step number, and renumbering
   to insert a beat would silently falsify their citations.
   **Round-19 defect this step exists to fix, found from this seat and verified
   in the app rather than argued.** Step 7 closes on custody — "download the
   JSONL" — and the script as written through round 18 pressed Compare,
   re-estimate, flip mode and Ceiling, and **never once pressed Log**. Logging is
   a separate explicit button (`app.py:952`, `str.verdict.log_cta`), so at step 7
   `do_export` took the `log.n() == 0` branch: the file component **stays
   hidden** and the app prints *"Nothing to export yet — the log is empty. Log a
   decision first; the download hands you the only copy."* Run from this seat on
   an empty log, that is the app's literal output. So the closing beat of the
   demo — the one that proves the Spine's "log fully in the user's hands" — hands
   the guest no file and a correction, and the privacy sentence step 7 quotes
   verbatim (`str.empty.privacy`) only ever paints as part of a SUCCESSFUL
   export. The script quoted a string the script could not cause. That is this
   leaf's own failure mode — a tour narrating something the screen does not do —
   and it was in the highest-trust thirty seconds of the demo.
   **Two constraints on this step, and they are load-bearing, not decoration.**
   (i) **Press Log while the verdict still reads A and the pick is A.** `do_log`
   sets `overrode = verdict == "too_close" or pick != verdict`, and an override
   **requires a typed one-sentence rationale before anything appends** (Decisions
   C8 / design S13b) — correct behaviour, and a trap at minute three if the press
   were moved after step 5's "too close to call": the first click would return a
   prompt and log nothing, in front of a guest, on the clock. That is why this
   step sits at 4a and not at 5a.
   (ii) **Never press Log in 0→1 mode (step 6), and never with the same idea
   names in both modes.** Design's round-18 finding: the audit view's four
   statistics are computed with no `mode` argument and render **pooled across
   modes** (`app.py:416-425`), so one cross-mode re-comparison of the same pair
   overwrites the earlier edge and drops the displayed ζ from 1.00 to 0.00, and a
   pooled Brier can paint above the caption "No outcome data about ideas like
   yours exists". Their reassurance to this seat was that the defect is
   unreachable because no step in §1c logs a decision — true, and it was also the
   reason step 7 was broken. **One log, one mode, keeps both true at once**: the
   custody close works and the pooled statistic stays unreachable at the hour.
   This is a scripting constraint, not a fix; the defect is design's row and
   engineering's code, and nobody should be moving code this week.
   **This step adds NOTHING to the M-UX-02 clock and is not a precondition on
   anything.** The witnessed interval is start = first paint of S1 (blank
   questionnaire) → stop = first render of the verdict (§1c-ii's clock
   definition, aligned verbatim with design §6.12). Step 4a happens **after** the
   verdict renders, so it falls outside the timed interval by construction — the
   5:00 bound and the SC-06 conversion are untouched, no gate is opened, and the
   witness template gains no field. It also touches `tour.html` not at all:
   `tour.html:764` claims the downloadable JSONL as a *capability*, which was and
   remains true; what was false was only this script's ability to demonstrate it.
5. The honesty beat: re-estimate B's feasibility to 3.3 → margin shrinks to 55%,
   interval 47–62% straddles 50% → **"Too close to call — gather evidence."** The
   judge knows when to shut up.
6. Flip to 0→1 mode: the permanent banner — "0→1 mode structures your search. It does
   not predict product–market fit." Then tick a Ceiling flag and re-run: the card
   routes around the math and says why, in its own words — "Averages are exactly what
   destroy outliers, so this flag never enters the score" — and the probability does
   not move. Point at that: the flag routed to portfolio judgment instead of
   corrupting the number.
7. Close on custody: download the JSONL — **which now contains the decision logged
   at step 4a, and did not before round 19; see 4a for why this step could not
   work as written**. The app prints "Exported 1 decisions." followed by the
   privacy sentence the presenter then reads aloud: "Runs entirely in this app. No
   API key, no server, nothing stored anywhere but your own log file." **The
   presenter quotes the screen rather than the script** — that string is
   `str.empty.privacy` and it paints only on a successful export, which is
   precisely why step 4a is not optional.
   **THE ONE QUESTION THIS BEAT INVITES, AND THE ANSWER, BECAUSE AN IMPROVISED
   ANSWER HERE IS HOW A TOUR STARTS LYING (round 19).** The presenter has just
   read the words "no server" aloud while the guest is looking at a page in a
   browser tab, and the sharp guest in the room — the one this demo is for —
   asks *"so what's serving that page?"* Scripted answer, one sentence:
   **"Gradio, on this laptop. Nothing leaves the machine — 'no server' means no
   remote server holds your data, which is the rest of that same sentence."**
   That reading is the app's own, not a gloss invented here: `str.empty.privacy`
   defines it in its own third clause ("nothing stored anywhere but your own log
   file"), and the catalogue's two sibling strings say it outright — *"there is
   no server copy, by design"* (`pairwisepm/strings.py:277` and `:283`). **What
   the presenter must NOT say is "there's no web server at all."** That would be
   false, it is contradicted by the tab the guest is looking at, and it trades a
   true honesty claim for one the room can disprove.
   **The verified backing, own runs this round rather than a reassurance, and it
   is the same fact as item 7's suite red seen from the other side:** a fresh
   interpreter that imports `pairwisepm` — the runtime model, the thing the
   refusal is actually about — pulls **none** of the eight forbidden modules and
   does pull `numpy`; a fresh interpreter that imports `app.py` pulls `httpx`,
   because Gradio *is* the local web server and ships an HTTP stack. Both halves
   are true at once and the script now says so. The engine's own guards are
   unmoved and green in isolation: the static source scan finds no forbidden
   import in any `pairwisepm/*.py` or in `app.py`, and the socket kill-switch
   `test_no_network_calls_at_runtime` passes — a full cycle in both modes opens
   no connection. So "runs fully offline" (`tour.html:403-404`) and
   `tour.html:763`'s "numpy, no LLM, no network calls" are both still true on
   the screen, and the presenter can now defend them with a mechanism instead of
   a repetition.

### 1c-i. Demo readiness gates (round 20 status — **ZERO gates stand**, unchanged
since round 15, and **both the pre-flight and the full suite are green on this
seat's own runs at the close of this round**, 2026-09-01 07:59 CDT, repo
checkout, project interpreter: `pytest tests/test_vendoring.py
tests/test_copy_surfaces.py` → **19 passed, 0 skipped, 0.10s**; the vendoring
half alone **7 passed, 0 skipped, 0.03s**; and the bare `pytest` at repo root →
**83 passed, 0 failed, 0 skipped**. **Both figures moved inside this round after
this seat had already written them down** — the pre-flight read 18 and the suite
81 at 07:55, four minutes earlier, and this seat touched no code in between — so
the earlier numbers are corrected here rather than left standing, and the
sequence of pinned counts on the pre-flight command is now
11 → 12 → 12 → 17 → 18 → **19**. Five of those moves landed while this seat
touched no code, which is why the witness field records **passed-and-skipped and
never a target number**, and why the header quotes a time along with the figure.
**A number in this file is a reading, not a property**, and the fifth vindication
of that rule arrived in the last four minutes of the last round. **The round-19 red is CLOSED and the closure is worth one line here
because of HOW it closed:** `test_no_llm_or_network_imports` — the guard on the
Spine's loudest refusal — was red in the full suite last night on a test-ordering
defect, and compliance repaired it by correcting the guard's SUBJECT (a fresh
child interpreter importing the engine) rather than by shortening the forbidden
list, which was the fifteen-second fix that would have bought a green suite by
retiring the promise. Mechanism, this seat's corrected account of it, and the
closure runs are at item 7. **THE ONE OPEN ITEM IS NOW RESOLVED TOO: M-UX-02a's
window CLOSED UNCONVENED and the dated line has landed — item 12,
2026-09-01 07:55 CDT.** SC-06 stays "designed so, not yet timed" in every
payload, the claim-ledger row-4 Basis cell is swapped to its pre-written WINDOW
CLOSED text (§0), and **no demo step, gate, registered phrase or tour line moves
on that** — which is what it means for a miss to have been planned for.) The
launch-working-directory gate deleted at round 15 stays deleted and its mechanism
claim stays RETRACTED — see item 7, which carries the **standing discharge rule**
(engineering, round 15), the pre-flight's promotion to a **recorded field, P-14**
(compliance, round 15), its **skip-aware reading** (sequencing's round-16 flag:
`pytest` exits 0 on an all-skipped file — marked **CONTESTED (D10)** this round
and operative unchanged), the field's **two-token form — `N passed, M skipped`,
green only if exit 0 AND 0 skipped** (compliance, round 18), and from round 19
the **label correction**: the two-file command is no longer called "P-14" on the
witness template, because **P-14 is `tests/test_vendoring.py` alone** and a
`tests/test_copy_surfaces.py` red is a push blocker that is **never** a
NO-RECORD ground (sequencing). Every gate on the demo SCRIPT remains
deleted: no numbered step in 1c has a workaround, both themes, any scroll
position. **Round 18's real work is that one command's exit code stopped standing
for six different facts**: item 6 now names WHICH vendoring clauses void a sitting
(T-VEND-01/02/03/05 — the served-copy set) and which are a defect but not a void
(T-VEND-04/06), so the expected post-write `T-VEND-06` red cannot kill a re-opened
sitting that satisfied its own predicate. Item 11 records the second correction:
the eyes-on boundary this seat asked design for was the wrong boundary — measured
on visibility it is **nineteen** literals, and the right bound is design's
permanent **EYES-ON FIVE** drawn on trust weight, of which **four** apply on this
surface and all four are machine-covered. ~~Open item: M-UX-02a's
human sitting, backstop first hour of 2026-09-01, all outcome branches
pre-written, see items 4-11~~ — **CLOSED round 20 on branch [3], WINDOW CLOSED
UNCONVENED, dated line at item 12. There is now no open item and no standing
gate on this surface.** The branch texts were pre-written in round 13 and one of
them was swapped in unedited; nothing was drafted at the moment of truth, which
is the whole return on having written all three.)

Render session 2 (design states.md §6.7, dated per-check-ID, 2026-08-31, real Chrome,
served dark theme) confirmed on a live screen everything R-8 gated: first paint
matches tour Stop 2 verbatim — blank inputs, no invalid styling, no fabricated zeros —
incomplete Compare renders the per-factor missing list with no toast, and an explicit
0 scores. Per the per-line deletion protocol, the blank-form gate and the step-6
suspension are DELETED: **blank-form demos are cleared and step 6 (the live ceiling
beat) is reinstated in the demo script** — the amber strips it depends on are
browser-confirmed legible (§6.7 PASS). R-8 is closed browser-verified; the tour and
the app now agree at first paint, on a live screen, which is the claim this leaf
existed to be able to make.

Render session 3 (design states.md §6.9, dated per-check-ID, 2026-08-31, real
Chrome, served dark theme forced, computed-style evidence) delivered the per-line
notification this gate protocol requires, and GTM read the §6.9 rows directly,
not the packet's summary. Acting on it per-line:

- **DELETED: the no-dark-theme-demo caution.** R-9b is CLOSED browser-verified —
  the S3 verdict headline and its `<b>` MP-1 token, the S4 headline/body, the
  runner-up chip, the S1/S2 placeholders, and the stale notice all compute
  legible ink (`rgb(28,25,23)` / `rgb(87,83,78)` on the light card) in the
  served dark theme, and the whole ceiling-flagged Stop-5 screen passes in one
  zoomless screenshot (§6.9 rows a–e + S5 parity). **Dark-theme demos and
  screenshots are cleared.** The punchline number is readable in both themes;
  `?__theme=light` forcing is no longer required anywhere in the script.

Render session 4 (design states.md §6.11, dated per-check-ID, 2026-08-31, real
Chrome, served 0→1 dark theme, computed-style + rect evidence) delivered the
per-line PASS notification this gate protocol required, and GTM read the §6.11
rows directly, not the packet's summary. Acting on it per-line:

- **DELETED: the banner-in-frame screenshot gate (M-UX-03).** The gate lifts on
  exactly the line it was pre-wired to and nothing else, and that line exists:
  at scrollY 1500 the banner rect computes top 0 / bottom 77.2, fully within
  the 792px viewport, computed `position: fixed`, in the served 0→1 page
  (§6.9 baseline at the same scroll: top −1255, fully out) — and at the
  document's max scroll it stays pinned. Both demo-visible riders GTM demanded
  are browser-PASSED in the same session: spacer computed height 77.2 = banner
  height exactly (nothing in the demo frame jumps at scroll), and the banner
  content div computes opaque `#0b7285` with legible ink — nothing ghosts
  through. **Screenshots at any scroll position are cleared; demo scrolling in
  0→1 mode needs no manual framing; step-6 screenshots are no longer
  top-of-page-only.** Four repo-landed rules, one browser-verified rule: the
  gate held through three guard-green false dawns and lifted the round the
  browser said so — which is the only way this leaf's tour stays a tour that
  never lies. Bonus rows credited: the §6.11 session also confirmed ON SCREEN
  the two R-10 honesty beats this file's sync record banked ("1 factor score
  to go" singular; "Press Compare to recompute." truthful stale tail) — the
  demo's honesty beats are now browser-verified end-to-end, not just vendored.

**The demo script still has ZERO workarounds, and as of round 15 there is again
ZERO standing gate of any kind.** Every numbered step in 1c runs against the
live app exactly as written, both themes, any scroll position, from any working
directory (item 7 — gate deleted on this seat's own re-reproduction). Remaining
open item — not a gate on any demo surface:

- **M-UX-02a (timed five-minute run, 1→N, GTM witnessing — split from
  M-UX-02b per compliance/sequencing round 14; the 0→1 half is QUEUED as D8,
  see item 10): ▶ RESOLVED ROUND 20 — WINDOW CLOSED UNCONVENED, dated line
  at item 12 (2026-09-01 07:55 CDT). Everything below this marker is the
  round-by-round record of a slot that stayed open and was never taken; it
  is kept, not pruned, because the escalation trail is the evidence that
  the miss was reported rather than discovered.** The original status text
  follows unedited. **SLOT LIVE — the named day
  is TODAY, 2026-08-31.** Round-10 status: the slot named in round 9 has
  arrived. GTM witness is standing by ALL DAY today, either theme (rider
  lifted per §6.9), any sitting design opens; **backstop unchanged and hard:
  first hour of 2026-09-01, inside sequencing's ≤2026-09-01 window.** The
  sitting's three seats are: Hari recruits the fresh user (the one input no
  agent can supply — a fresh human), design times, GTM witnesses and records.
  What GTM has pre-staged so the sitting costs its minimum: the run is
  blank-questionnaire → verdict card in **1→N mode** (Spine metric 1), fresh
  user, no coaching beyond mode selection; the witness record will be a dated
  line in this file — start time, end time, elapsed, theme, PASS/FAIL against
  5:00 — mirroring the §6.7/§6.9/§6.11 per-check evidence discipline. On PASS,
  the claim-ledger row graduates from "designed so" to a verbatim sayable
  five-minute claim with the date attached; on FAIL, the honest fallback copy
  is already written (the "designed so" framing simply stays, and the timing
  evidence routes to design as a defect record). Either way the tour never
  lies: the record is what converts the pitch, not the pitch itself. Session 4
  needed no fold-in — it already ran (§6.11) — so today's sitting is
  single-purpose: one fresh user, one timer, one dated line.

  **Round-11 status (2026-08-31, checked from this seat): the named day is
  MORE THAN HALF SPENT and no sitting record exists** — design's states.md
  ends at §6.11 with no M-UX-02 timer line, and no fresh-user recruit has
  been reported. GTM's witness remains standing by through end of day; the
  hard backstop (first hour of 2026-09-01) is now hours away, and it
  collides with the D1-D6 SLA execution morning — if the sitting slips to
  the backstop, it convenes BEFORE the resolution round's noise, not after.
  Escalation on the record: the two missing seats are design's timer (zero
  preparation remaining, per their own §6.11 conclusion 6) and Hari's
  fresh-user recruit (surfaced to Hari via sequencing's packet next to the
  D1-D6 window, per the round-10 ask). To make the sitting a pure
  fill-in-the-blanks act, the witness record is pre-staged VERBATIM below —
  the sitting ends when the template below is filled (ten fields as of
  round 17 — see the note under it; the count is not the instrument, the
  filled template is):

  > **M-UX-02 witness record** — date: `____` · fresh user: `initials/role
  > ____` (recruited by Hari, no prior exposure) · mode: 1→N · theme:
  > `light|dark ____` · **launch working directory: `____`** (recorded
  > for disambiguation, no longer a precondition — round 15) ·
  > **PRE-FLIGHT COMMAND (one line, TWO files — this is NOT the name "P-14";
  > round 19, sequencing's demand accepted):
  > `pytest tests/test_vendoring.py tests/test_copy_surfaces.py`
  > run on THIS machine before the clock started → write the aggregate in
  > compliance's two-token form, **`____ passed, ____ skipped`**, and
  > `passed/failed ____`.**
  > **Which gate is which, because the label was wider than the gate and the
  > consequence hangs off the label:** compliance's gate row defines **P-14 =
  > `pytest tests/test_vendoring.py` alone**, exit 0 AND 0 skipped
  > (traceability.md; they have twice told this seat that P-15 guards the
  > resolution round and is not this template's). The second file,
  > `tests/test_copy_surfaces.py`, is **the COPY-SURFACES CHECK — its own
  > instrument, its own name, and NEVER a voiding ground** (next bullet).
  > **How one command fills both verdicts without a second run or a second
  > blank:** an aggregate of `0 failed, 0 skipped` entails both halves green,
  > because pytest sums failures and skips across files — so on a green
  > aggregate, **P-14 = green** is derived, not judged. The two halves only
  > need telling apart when the aggregate is NOT green, and then `pytest`
  > prints the file path on every failure and every skip line, so the
  > presenter reads which file off the output instead of reasoning about it.
  > That is why this stayed one field and one command rather than becoming
  > two of each: sequencing asked for the copy-surfaces result "under its own
  > name in its own field", and the name is delivered here in full while the
  > blank is derived — if that seat judges the derivation too clever for the
  > hour, say so and the second blank lands in round 20 at a cost of one line.
  > **Pass condition, compliance's round-17 words, unchanged:** green only if
  > exit code is 0 AND the skip count is 0 — `pytest` exits 0 on an
  > all-skipped file, so "green" was a checkbox a run measuring nothing could
  > tick. **No target pass-number is written here on purpose**: the count read
  > 11, then 12 inside round 17 alone, 12 on the round-18 run, and **17 on
  > this seat's round-19 run** (copy-surfaces grew from 5 clauses to 10 under
  > compliance's hand while this seat touched no code — the fourth time a
  > pinned count moved, and the fourth vindication of recording numbers rather
  > than a target). The presenter does not have to reason about which guards
  > should have run — both numbers are printed by the command. Round 16
  > compliance; skip-aware round 17 on sequencing's flag; two-token form round
  > 18; label corrected round 19 ·
  > **bound module = design authority's bytes:
  > `confirmed y/n ____`** — answered by the P-14 field above, not by
  > judgment. **Which clauses answer it (round 18, decisions' narrowing, with
  > this seat's one verified correction): T-VEND-01/02/03/05.** A red in that
  > set is `n` and the run is **NO RECORD** (item 7). A red in
  > **T-VEND-04/06 only** is a real defect to fix before any push and is **NOT
  > a void** — see item 6's clause list, which is the readable-at-the-hour
  > version of this line.
  > **A red anywhere in `tests/test_copy_surfaces.py` is a defect to fix
  > before any push and is NOT a NO-RECORD ground** (round 19, sequencing's
  > second demand, accepted and stated rather than left to inference). The
  > NO-RECORD rule protects exactly one predicate — *which module copy was
  > bound* — and every clause in the copy-surfaces file speaks about
  > **on-screen wording** against design's ratified fixture, which says
  > nothing about that predicate. A sitting whose engine served the
  > authority's bytes measured the real product's clock even if a label
  > elsewhere drifted from design's fixture; discarding that measurement
  > would cost the RECORD to protect a claim it does not make. This was
  > already true by omission — the voiding set above lists only T-VEND
  > clauses — but "true by omission" is what a presenter has to *derive* at
  > the hour, and the entire round-18 work on this field was getting
  > derivation off the line. Stated, it is one sentence; inferred, it is an
  > argument with a guest in the chair.
  > **AND A RED IN ANY FILE THAT IS NOT ONE OF THESE TWO IS NOT A NO-RECORD
  > GROUND EITHER — not even a red named for a Spine refusal** (round 20,
  > sequencing's second demand, accepted whole). This pre-flight is
  > FILE-SCOPED: it runs `tests/test_vendoring.py` and
  > `tests/test_copy_surfaces.py`, and it makes no claim about
  > `tests/test_engine.py`, `tests/test_packaging.py`, or anything else in
  > `tests/`. A presenter who runs the bare `pytest` out of habit and meets
  > a red there has learned something worth reporting and has learned
  > **nothing about this record**: the NO-RECORD rule protects one
  > predicate — *which module copy was bound* — and only the four T-VEND
  > clauses named above speak to it. This is not hypothetical and it is not
  > a rule written for a quiet case: **inside round 19 the full suite read
  > 79 passed / 1 FAILED while this command read 17 passed / 0 skipped**,
  > and the red was on `test_no_llm_or_network_imports`, the guard named for
  > the Spine's loudest refusal — the single most alarming line a presenter
  > could possibly meet ten minutes before a sitting (mechanism and closure
  > at item 7). Had a sitting convened that hour, a presenter reading that
  > red would have been one inference away from voiding a valid record over
  > a test collection-order defect. **Write the record. Report the red.
  > They are two acts and only one of them is yours at the hour** ·
  > **AND A RED THAT CLEARS ON A RE-RUN, WITH NOTHING TOUCHED, IS NOT A RED —
  > RE-RUN BEFORE YOU ACT** (round 20, observed on this seat's own machine
  > this round, not constructed and not taken from a packet). At 07:59 CDT the
  > pre-flight returned **1 failed, 17 passed** —
  > `test_copy_surfaces.py::test_the_copy_guards_cannot_be_quietly_weakened`,
  > `AssertionError: copy-surface clauses have gone missing from this file:
  > test_the_pick_question_asks_for_the_users_own_pick`. This seat's edits that
  > minute were confined to this one markdown file. Three re-runs in the next
  > seconds: **19 passed, 0 skipped**, three times. What happened is that
  > another leaf was SAVING `tests/test_copy_surfaces.py` mid-write — a clause
  > name had landed in the required-clause list a moment before the function
  > body did — and the pre-flight read the file in between. **The window is
  > seconds and a re-run clears it.** So: if the pre-flight reds, run it a
  > second time before you write anything on this line or reach for a person.
  > A red that reproduces is a real red and everything above applies to it; a
  > red that vanishes was a file being saved. This costs one command and it is
  > the cheapest instruction on this template — and the alternative is a
  > presenter voiding a sitting, or delaying one with a guest already in the
  > chair, over somebody else's autosave. **Engineering filed the same species
  > one file over** (a mid-save of `leaves/design/copy-authority.yaml` reddening
  > their P-15 on a YAML parse error); this is the presenter-facing half of it,
  > and it is on the template rather than in a demand because nobody needs to
  > build anything for a presenter to re-run a command ·
  > start: `__:__:__` · end: `__:__:__` ·
  > elapsed: `_:__` vs bound 5:00 → **PASS | FAIL** · design timer reading
  > (same sitting, own seat): `_:__` · witness: GTM. **Clock definition
  > (aligned verbatim with design §6.12 protocol): start = first paint of S1
  > (blank questionnaire), stop = first render of the verdict (S3/S4/S5)** —
  > both seats time the same interval, so the two numbers are comparable by
  > construction. **A filled record converts SC-06 FOR 1→N ONLY**: on PASS,
  > claim-ledger row 4 graduates to the dated **mode-named** claim ("under
  > five minutes in 1→N, witnessed [date]"), never an unqualified one, and
  > the 0→1 half stays "designed so, not yet timed" on every branch. On
  > FAIL: "designed so" framing stays; elapsed + observed stall points route
  > to design as a defect record, and the tour quotes the measured number.
  > Coaching given: mode selection only (anything more voids the record).

  (Ten fields on the template as of round 17 — the working directory, the
  bound-module confirmation and the P-14 pre-flight result joined the
  original six at round 16, and P-14's single "guard count" split into
  *ran* and *skipped* this round. "Six-field record" elsewhere in this file and on other leaves' graphs
  means this template with its fields filled; the count is not the
  instrument, the filled template is. The count has now moved twice without
  the instrument changing, which is precisely why it was never the
  instrument.)

  If the window closes with no record, the claim-ledger row DOES NOT
  convert — SC-06 stays "designed so" in every payload, per the ledger's
  own rule. That outcome is honest but unnecessary, which is exactly why
  this escalation line exists.

  **Round-12 status (2026-08-31, final hours of the named day, checked
  from this seat): still no sitting record** — design's states.md §6.12
  confirms timer READY with zero preparation remaining and no M-UX-02
  line appended; no fresh-user recruit reported. Three alignments locked
  this round so the record — or its absence — is one agreed instrument
  across files:

  1. **Fallback wording pre-agreed verbatim with design (§6.12):** if the
     window closes unconvened, the honest state in THIS file and design's
     catalogue is the identical phrase — **"designed so, not yet timed"**
     — no softening, no paraphrase. An unwitnessed claim never converts.
  2. **Clock definition adopted from §6.12 into the witness template
     above** (S1 first paint → first verdict render), so design's timer
     and GTM's witness reading measure the same interval.
  3. **Missed-window reporting commitment (sequencing's round-11 terms):**
     if the backstop hour (first of 2026-09-01, BEFORE the D1-D6
     resolution round executes) passes with no fresh user, GTM lands a
     dated line here stating "M-UX-02 window closed [date/time], no
     sitting convened, no record exists" — a dated fact, not a slipped
     date — and the graph may carry M-UX-02 as missed-window on that line.
     The tour keeps the "designed so, not yet timed" framing permanently
     unless a later, newly-scheduled witnessed run converts it.

  **Round-13 status (2026-08-31, ~4 hours to the backstop, verified from
  this seat and not from the packet): still no sitting record** — design's
  states.md ends with the §6.12 sitting-readiness record (timer READY,
  protocol fixed, no M-UX-02 per-check line appended), and no fresh-user
  recruit has been reported. Two hardenings landed this round, both aimed
  at the same failure mode — a record or a miss that has to be *drafted*
  in the round it fires, and therefore arrives negotiable:

  4. **Miss line hardened to one registered string (compliance's round-12
     demand, adopted verbatim so all instruments carry the identical
     fact).** If the backstop passes unconvened, the line GTM appends here
     that same round is exactly:

     > **M-UX-02 window closed unconvened, [date/time] — no sitting
     > convened, no record exists; designed so, not yet timed.**

     One string, three instruments (this file, design's §6.12, the
     compliance matrix). "Missed" is then read off a dated line, never
     inferred from an absence — and never from silence in a packet.
  5. **Claim-ledger row 4's three post-branch texts are pre-written** (§0
     row-4 branch block, this round): PASS, FAIL, and WINDOW CLOSED each
     have their exact Basis-cell replacement already on the page, so the
     ledger flips by swap in the resolving round and can never sit in a
     stale "pending" state after its own window has closed. This is the
     demo-surface half of the same discipline the sitting record carries:
     a presenter must never read a basis the evidence no longer supports.

  **Round-14 status (2026-08-31 20:14 local, verified from this seat: no
  M-UX-02 timer line in design's states.md, no fresh-user recruit
  reported).** Four demands accepted and executed, plus one hazard this
  leaf verified on its own machine rather than taking on the packet's
  word. All four are honesty-of-the-tour items, which is why they cost
  this seat nothing to accept:

  **Round-15 status (2026-08-31, verified from this seat and not from the
  packet: design's states.md now ends at §6.14 with the branch templates
  and the coverage limit written, but still NO M-UX-02a record line; no
  fresh-user recruit reported; `decisions.yml` carries D8 pending).**
  Three demands accepted and executed — **item 7 is rewritten** (gate
  DELETED, my own overbroad mechanism claim RETRACTED, design's durable
  voiding condition adopted verbatim in its place), **item 10 is new**
  (the D8 answer decisions asked for before the sitting), and the row-4
  branch block gains compliance's mode-naming on the FAIL branch. The
  net for the demo surface is the best it has been: back to zero
  standing gates, with the one precondition that mattered restated in a
  form that does not expire.

  **Round-16 status (2026-08-31, verified from this seat: design's states.md
  now ends at §6.15 carrying the app.py literal census; still NO M-UX-02a
  record line; no fresh-user recruit reported; `decisions.yml` carries D8 and
  D9 pending).** Four demands accepted. Three were already half-satisfied by
  round 15's work and are executed here as the missing half each seat
  correctly named: engineering's **second discharge path** becomes a standing
  rule rather than a one-off (item 7), compliance's **P-14 pre-flight** stops
  being a habit and becomes a recorded field on the witness template (item 7
  + the template), and decisions gets the **D9 pointer** it asked for but not
  the swap it asked for, with the reason stated in item 6. The fourth is new
  work: design's **copy-assurance scope** is item 11. Nothing this round
  changes a demo step, a branch text, a registered phrase, or the ledger. The
  only new *fact* on this surface is item 11's, and it is a fact against this
  leaf's own past assurances rather than against anyone else's work — which
  is the third round running that the most useful thing on this page was
  found by turning the instrument inward.

  **Round-17 status (2026-08-31, verified from this seat: design's states.md
  now ends at §6.16; still NO M-UX-02a record line; no fresh-user recruit
  reported; `decisions.yml` carries D8 pending and **D9 CLOSED
  `resolved_uncontested`**).** One demand on this seat this round and it was a
  correction handed over unasked rather than an ask — compliance's notice that
  the pre-flight command's green had partly been a green it did not earn.
  Accepted whole and executed in three places (item 7's pre-flight lines, the
  P-14 field on the witness template, and the header above). What is NOT
  executed is anything that grows the presenter's hour: compliance's own
  instruction — do not put gate P-15 on this template, it guards the resolution
  round and a presenter has nothing to do about it — is honored as written, and
  the one deviation from it is stated in item 7 rather than slipped in. The
  other half of the round is item 11 correcting itself in the direction that
  costs this seat something: an assurance this file made *narrower* than the
  truth for once, which is still an assurance whose instrument was not checked
  before it was written. Nothing this round changes a demo step, a branch text,
  a registered phrase, or the ledger.

  6. **No third branch, and the disallowed stand-ins named** (design's
     §6.13 rule, mirrored here as binding on the GTM seat). M-UX-02
     resolves to a filled witness record or a dated miss line, and
     **nothing else counts as a sitting**. Specifically disallowed, by
     name, so none of them can be argued into the record at the window's
     close: a design-seat self-timed run; an agent-timed run of any kind;
     "informally observed"; "substantially complete"; a re-run by a user
     who has already seen the app; a partially filled template. A
     **voided** run — coaching beyond mode selection, a non-fresh user,
     either clock unread, or a **bound module that is not the design
     authority's bytes** (item 7, design §6.14) — is **no
     record** and routes to the miss line, with its cause named in this
     file on the same dated line. That naming is how architecture's
     "dated void with the cause named" and design's "no third branch"
     are both honored at once: the ledger stays three-valued (§0), the
     cause stays citable here. A void is never reported as a FAIL — the
     5:00 bound was not tested, so it cannot have been lost.

     **D9 pointer — CLOSED (round 17), and the pointer updated rather than
     left pointing at an open entry that no longer exists.** Verified from
     this seat in `leaves/decisions/decisions.yml:636-639`: D9 is
     `status: resolved_uncontested`, `resolved_at: 2026-08-31`, dissolved on
     its own clause because four files converged on **one** predicate rather
     than because anyone ruled. The predicate that stands is the one this
     line has carried all along — **item 7's bound-module bytes rule** — with
     D9's option-2 shape around it: the condition is *checked* before the
     clock by `pytest tests/test_vendoring.py` (P-14), not argued after the
     hour. So this pointer now reads: **D9 closed; nothing on this line is
     contested; the operative predicate is unchanged.** The commitment made
     in round 16 — "if D9 rules otherwise, this line follows the ruling in
     the round it lands" — is discharged by there being nothing to follow.

     **WHICH CLAUSES VOID — round 18, decisions' demand accepted, with one
     correction this seat verified in the test source rather than taking from
     the packet.** Until this round the voiding line read "P-14 red → NO
     RECORD", which is one command's exit code standing for six different
     facts, and at the hour a presenter cannot tell which one they got.
     Decisions is right that this diverges on exactly one path, and it is the
     path that matters most to this surface: after the D1/D2 resolution round
     writes into `configs/*.yaml`, **`T-VEND-06` is EXPECTED to red on the very
     next run of the pre-flight command**, on this editable install, with no
     reinstall involved — the duplicate `configs/` tree the wheel force-include
     creates goes stale the instant the values land. Under the encoded ordering
     the sitting convenes BEFORE that write, so the scheduled sitting is
     untouched; a **re-opened** sitting (branch [3] WINDOW CLOSED) falls after
     it, and a presenter reading that red at the hour would void a run that
     satisfies the D9 predicate completely. So the list, executable off the
     failure line:

     - **VOIDING (NO RECORD): `T-VEND-01`, `T-VEND-02`, `T-VEND-03`,
       `T-VEND-05`.** These are the served-copy clauses — the D9 predicate is
       *which copy was served*, and these four answer it: 01/02 for the design
       authority's string bytes, 05 for the values that bound copy serves,
       03 for which `configs/` directory the engine actually loads.
     - **NOT VOIDING (a real defect, fix before any push, but the 5:00 bound
       can still be tested): `T-VEND-04`, `T-VEND-06`.** 04 is a COUNT of
       importable copies and its own docstring says 02/03 are what assert this
       session bound the right one; 06 is a FRESHNESS comparison between the
       authority and a duplicate that is *permitted by design*.

     **The correction, and why this seat did not simply adopt the split as
     offered.** Decisions proposed voiding on `T-VEND-01/02/05` and put
     `T-VEND-03` in the non-voiding bucket with 04 and 06. Read in
     `tests/test_vendoring.py` from this seat: T-VEND-03's own failure message
     is *"the engine loads mode schemas from <X>, not <repo>/configs — a second
     copy of configs/ is shadowing the repo checkout; edits to the repo's YAML
     (D1/D2 priors) would not reach the engine."* That is not hygiene. It is
     the config half of the same question 02 answers for strings, and its
     docstring says so in as many words ("RESOLUTION invariant, not a count …
     what this pins is which directory the engine LOADS"). A demo run on a
     shadowed config tree serves **different prior weights than the authority
     holds**, which lands directly on this surface: demo-script step 3 reads
     the per-factor contributions out loud ("+.125, +.105, +.08 each"). A
     sitting whose engine loaded a stale schema would produce a witness record
     that converts SC-06 on numbers from the wrong file — a green board behind
     a tour that is quoting a schema nobody approved. **That is the one failure
     this leaf actually fears, so T-VEND-03 goes in the voiding set.** The
     split still delivers everything decisions asked for, because the clause
     they were protecting against — the expected post-write `T-VEND-06` red —
     is in the non-voiding bucket either way.
     - **Re-opened sitting only, presenter-facing half of sequencing's
       ordering find:** before a re-opened pre-flight, refresh the install
       (`pip install -e .`) or confirm no duplicate `configs/` tree is on
       `sys.path`, then run the command. **Never** hand-edit the
       `site-packages` snapshot and **never** delete the wheel's
       `force-include` — that is the fifteen-second fix that silently breaks
       `pip install pairwisepm` for every user. A `T-VEND-06` red traceable to
       the resolution-round write, with the refresh not yet applied, is not a
       P-14 failure and not a void.
     - **Nothing here weakens the rule.** A red anywhere in the file still
       blocks a push and still gets written on the line; what changed is that
       two of the six no longer destroy a sitting that satisfied its own
       predicate. Naming the clauses keeps this a **one-command** check — the
       answer is read off the failure text, not argued — which is the standard
       this leaf refused the round-16 pointer swap to protect.

     **What the round-16 refusal was, and why it is left in place rather
     than deleted.** Decisions asked that this voiding list point at D9
     *rather than* at item 7 while the rule was contested. The pointer was
     added; the *swap* was refused. The operative predicate on this line stays **item 7's
     bytes rule**, for one reason that is entirely about the room: a
     voiding condition a witness reads at the hour has to be *executable
     by the witness at the hour*, and "see decisions entry D9 (contested)"
     is not executable — it is an argument handed to a presenter who has a
     guest in the chair, which is the exact failure mode this leaf's
     whole gate protocol exists to prevent. There is also nothing here for
     the swap to protect: the three predicates decisions names do not
     conflict on this surface, because **this seat's cwd predicate is
     already withdrawn** (item 7, retracted) — what remains is design's
     bytes rule, which compliance registered and engineering instrumented,
     and which no seat has argued against. A pointer to an open ruling is
     honest; deferring an executable precondition *to* an open ruling
     would leave a run's validity undecidable in the only minute it
     matters. The reasoning is kept on the page rather than deleted now
     that the entry has closed, because it is the record of *why* the
     refusal was cheap: the swap would have made a witness's only
     executable predicate depend on an entry that — as it turned out —
     resolved by dissolution, on the very predicate this line refused to
     defer. Had the swap been taken in round 16, the sitting would have
     spent that round with no executable voiding rule at all, and the
     entry's own non-deferral clause says a sitting inside that window
     proceeds regardless. **Refusing a swap and honoring the ruling are
     compatible, and this line did both.**
  7. **Launch working directory — GATE DELETED (round 15), and this
     seat's own round-14 mechanism claim PARTLY RETRACTED.** Both halves
     re-run from this seat 2026-08-31 with the project interpreter, on
     the same reproduction-grade standard the gate was opened on:
     - **The defect is fixed.** `direct_url.json` now reads `{"dir_info":
       {"editable": true}}` and there is no `site-packages/pairwisepm/`
       tree. From `/tmp`, `importlib.import_module('pairwisepm.strings')`
       binds `/Users/brettleehary/mcparea/ProMgtAI/pairwisepm/strings.py`,
       `'str.empty.example_cta' in STRINGS` is **True**, and
       `str.verdict.stale` ends **"Press Compare to recompute."** — the
       R-10 truthful tail, not the pre-R-10 "Recomputing…". `cmp` of the
       vendored mirror against `leaves/design/strings.py` is clean. So
       the off-root KeyError at `app.py:848` is not reachable by working
       directory any more, from any directory.
     - **RETRACTION, owed to sequencing.** My round-14 text said an
       off-root **launch** dies before first paint. That was overbroad
       and sequencing disconfirmed it: `python /abs/path/app.py` puts the
       **script's** directory on `sys.path[0]`, not the cwd. I verified
       the mechanism myself this round with a probe script run from
       `/tmp` — `sys.path[0]` was the script's directory, not `/tmp`. So
       the documented launch never bound the stale copy; what did was a
       `-c` one-liner, a REPL, or an off-root pytest. The defect was
       always real; my blast radius was not. A gate this leaf opens is
       held to the same evidence standard as a claim this leaf makes,
       which is the whole point of the protocol — so it is corrected in
       the file, not quietly narrowed.
     - **Deletion basis:** engineering's per-line notification (fix
       named, editable install, off-root layout build confirmed) **plus
       this seat's own re-reproduction above**, which is the standard the
       gate was opened on and is at least as strong as the architecture
       re-run I had named. Deleting on my own instrument rather than
       waiting for a seat that filed nothing this round is the same rule
       applied in the direction that costs me something. *(Architecture's
       round-15 packet then said the same thing unprompted and against
       their own finding — "the gate you opened on my report should come
       DOWN" — so the deletion now rests on three independent bases and
       none of them is a seat's availability.)*
     - **STANDING DISCHARGE RULE — no gate this leaf opens may be
       hostage to one seat** (engineering's round-15 demand, accepted and
       generalised past what was asked, because the next gate is where it
       will actually matter). Engineering asked me to name a *second*
       discharge path for this specific gate. The specific answer is moot
       — the gate is already deleted — so the ask is honored as a rule
       binding on every future gate on this surface:
       1. **Every gate opened here names its discharge EVIDENCE, never a
          discharging SEAT.** "Reproduced clean from any seat, including
          this one" is a discharge condition; "architecture re-runs it" is
          a roster, and a roster is an availability dependency wearing a
          protocol's clothes.
       2. **This seat's own re-reproduction always suffices**, at the same
          reproduction-grade standard the gate was opened on. A gate I can
          open alone I can close alone; anything else lets this leaf
          manufacture a permanent gate by pointing at a silent colleague.
       3. **Any seat's independent reproduction discharges the
          reproduction half** — compliance and sequencing both reproduced
          and re-verified A-13-01, and either would have sufficed here.
       4. **A gate whose named witness is silent for a full round is
          reported as SILENT-WITNESS in that round's status line, never
          left standing without comment.** Engineering's framing is the
          reason and is adopted verbatim: *a gate that cannot be deleted
          because its named witness is silent is indistinguishable, to a
          presenter, from a gate that is still true.* That is the same
          ceremony-outliving-its-reason failure this leaf polices in the
          demo script, arriving through the procedural door instead of the
          technical one — and this leaf had built exactly one of them.
     - **What SURVIVES the deletion, in its durable form** (design's
       round-14 demand, accepted **verbatim**): *a run whose app was
       launched against a bound module that is not the design authority's
       bytes is **NO RECORD**.* This is strictly better than the
       directory rule it replaces, because it does not depend on cwd,
       install mode, or any packaging fact that may change again — it
       names the only thing that actually matters, which is whether the
       user saw the copy this catalogue specified. Design's reasoning is
       adopted rather than paraphrased: today such a launch **voids** by
       dying at `app.py:848` before first paint, but had the crash been
       fixed before the copy was, the very same launch would have painted
       a pre-R-10 stale-verdict line asserting an auto-recompute the
       build does not perform — a **timing record measuring a product
       this catalogue did not specify**, and a demo that lies while every
       test is green. A crash standing in front of an overstatement is
       not a fix.
     - **Pre-flight, one line, retained for every demo and sitting** (it
       cost nothing before and costs nothing now, and it is the only
       thing standing between a fixed defect and its silent return):
       before the guest is in the room, run
       **`pytest tests/test_vendoring.py`** — which as of this round is
       *literally* the whole precondition and not a proxy for it. I read
       the file and ran it from `/tmp` this round: six guards, 6 passed
       in 0.03s, and they assert exactly what a presenter needs to know —
       the bound module resolves in-repo, `str.empty.example_cta` exists
       (the key `app.py:848` reads at layout construction),
       `str.verdict.stale` carries the R-10 truthful tail and not
       "Recomputing…", the loaded config dir is the repo's, and exactly
       one importable copy of the package exists. **A one-command
       pre-flight is the only kind this leaf will keep**: a precondition
       a presenter cannot execute in the room is ceremony, and ceremony
       is how a fixed defect comes back. Note the standing caveat the
       rest of this section earns — the demo is not "ready" because *the
       suite* is green; it is ready because *this* check is green, and
       until round 14 a green suite was exactly what the stale copy
       survived. Re-run from this seat in round 16: **6 passed in 0.03s**.

       **ROUND-17 CORRECTION, handed over by compliance unasked, and it is
       this file's own failure mode one level down: the green was partly a
       green it had not earned.** Three of the six guards (T-VEND-03/04/06)
       gated on the presence of `leaves/` — the design leaf — while their
       subjects were the config directory, the count of importable packages,
       and the staleness of a duplicate `configs/` tree. None of those is
       about the design leaf, and `pyproject`'s sdist ships `tests` WITHOUT
       `leaves`, so in any tree lacking the design leaf they skipped
       silently. **A pre-flight that returns green because it never ran is
       precisely the false clearance P-14 exists to prevent** — and it would
       have been written onto the witness line as a pass. Compliance fixed
       the predicates and measured it; this seat re-ran it rather than
       taking the packet's word, from `/tmp`, with `-rs` to force skip
       reporting: **6 passed, 0.03s, ZERO skipped**. Second consequence, in
       this seat's favour: the command now reads `1 failed` rather than a
       silent skip if the presenter's machine carries a second package copy.

       **SKIP-AWARE READING OF P-14 — CONTESTED (D10, decisions, round 19),
       AND OPERATIVE FOR TOMORROW UNCHANGED** (sequencing's round-16 flag,
       adopted here though it was aimed at compliance's row, because the field
       is mine). `pytest` exits 0 on an all-skipped file. So on this template a
       green is never an exit code: the field records **how many guards
       RAN**, and a run in which any vendoring guard skipped is **not** a
       green P-14 — it is a machine this seat does not recognise, and the
       honest act at the hour is to write that on the line, not to record a
       pass.

       **A RED LANDED ON THE FULL SUITE INSIDE THIS ROUND, IT IS NOT IN THE
       PRE-FLIGHT, AND NOBODY SHOULD VOID ANYTHING OVER IT — round 19, found
       from this seat, reproduced minimally, and reported rather than touched
       because `tests/` is not this leaf's file.** The full suite went **78
       passed / 0 failed** at the start of this round to **79 passed, 1 FAILED**
       by its end, with this seat editing one markdown file. The red is
       `tests/test_engine.py::test_no_llm_or_network_imports` — the guard on the
       Spine's loudest refusal, *no LLM in the runtime loop, no network calls* —
       asserting `AssertionError: httpx`.
       **Mechanism — CORRECTED IN ROUND 20, and the correction is against this
       seat's own sentence.** The struck text is kept legible rather than
       reworded away, because this file's whole standard is that a claim is
       corrected where it was made:
       > ~~`tests/test_audit_honesty.py` … **imports `app` at module level**,
       > which imports gradio, which imports `httpx`. Collection is
       > alphabetical and `test_audit_honesty` sorts before `test_engine`.~~

       **What is actually true** (decisions' round-20 demand, accepted whole
       and re-verified from this seat rather than taken on report). The clause
       asserted that no forbidden module is present in `sys.modules`, which
       made it dependent on what ran before it. But `tests/test_audit_honesty.py`
       does **not** import `app` at module level: its module-level imports are
       `ast`, `pathlib`, `pytest`, `pairwisepm` (:46-53), and `app.py` is loaded
       through `importlib.util.spec_from_file_location` **inside** the clauses
       that need it, at `_app_module()` (:106-109), behind a
       `pytest.importorskip("gradio")`. Own run, nothing mutated:
       `python -c "import tests.test_audit_honesty; print('httpx' in sys.modules)"`
       prints **False** — importing the module pulls nothing. So the pollution
       was **RUN-time, not COLLECTION-time**, and this seat's alphabetical half
       was right for the wrong reason: what mattered was the order of
       **execution**, not of collection.
       **Why the distinction is this seat's business and not pedantry** —
       decisions' rationale, adopted because it is a fact about *which commands
       are affected*, which is the only thing this leaf ever needed from the
       mechanism: because the pollution is run-time, a command that COLLECTS the
       polluter without RUNNING it stayed green. Compliance's gate P-1
       (`pytest tests/ -k "no_llm or no_network"`) read **2 passed / 78
       deselected — green** in the same tree at the same minute the full suite
       was red. Under this seat's module-scope story P-1 would have been red
       too, and the board's registered gate on the Spine's hardest refusal
       would have been *seen* to be blind. Getting the mechanism wrong would
       have mispredicted the one command a presenter is most likely to run.
       `test_packaging.py`, which has loaded `app` the same way for days, sorts
       after `test_engine` and so had never poisoned it. Two-file reproduction,
       own run at the time:
       `pytest tests/test_audit_honesty.py tests/test_engine.py::test_no_llm_or_network_imports`
       → **1 failed, 2 passed**; `pytest tests/test_engine.py` alone → **45
       passed**.
       **What it is and is not.** It is an **instrument defect, not a product
       defect**: `httpx` is in the process because a sibling test imported the
       UI, not because the engine reaches a network. It is **not** in the
       pre-flight command (`17 passed, 0 skipped`, own run after the red
       existed), it is **not** in the D9 voiding set, and it is **not** a ground
       to delay or void the sitting — the bound-module predicate says nothing
       about it. It **does** block a push, and it is ugly in a way this leaf
       cares about disproportionately: a stranger who clones the repo runs
       `pytest`, and the one line they read is a failure on the test named for
       the promise the whole tour is built on. **This is the standing caveat of
       item 7 earning its keep for the second time** — the demo is not ready
       because *the suite* is green, it is ready because *this check* is green;
       tonight the suite is red and the check is green, and both facts are true
       and neither is the other's evidence.

       **CLOSED, round 20 — and closed the way this leaf wanted it closed
       rather than the way that was cheapest.** Compliance corrected the
       guard's SUBJECT in the open: the import half now runs a probe in a
       **fresh child interpreter** and asserts that importing the ENGINE
       (`pairwisepm`, `.engine`, `.config`, `.log`, `.strings`) pulls in no LLM
       and no network client — order-independent by construction, and strictly
       WIDER than what it replaced, since it catches a dynamic
       `import_module("httpx")` the regex source scan cannot see. Read in
       `tests/test_engine.py:718-758` from this seat, not cited from a packet,
       and re-read after the pins moved rather than trusted from the first look.
       **`FORBIDDEN_IMPORTS` was not shortened, no skip marker was added, and
       the source-scan half was not deleted** — which is exactly the fix this
       seat asked for and explicitly the opposite of the fifteen-second fix
       visible from the failure line (drop `httpx` from the tuple and the whole
       suite goes green while the Spine's loudest promise quietly stops being
       instrumented). Own runs, 2026-09-01 **07:59** CDT, repo checkout, project
       interpreter: **full suite `pytest` → 83 passed, 0 failed, 0 skipped**;
       pre-flight `pytest tests/test_vendoring.py tests/test_copy_surfaces.py`
       → **19 passed, 0 skipped, 0.10s**; vendoring half alone → **7 passed,
       0 skipped, 0.03s**. (These are the corrected figures: at 07:55 the same
       three commands read 81 / 18 / 7 and this seat had already written 81 and
       18 into this file. Both moved, with no code touched from this seat, and
       both are corrected in place rather than overwritten silently.) **A stranger who clones this repo and runs `pytest`
       now reads one green line**, which was the entire reason this seat filed
       it: the first impression of the repository is a demo surface too, and it
       was the only surface on this board with a red on it.
       **What is kept from the episode, because the fix does not retire the
       lesson:** the standing caveat above stands unchanged and the new
       full-suite clause on the witness template (see the P-14 field) stands
       unchanged. Both were written while the red was live and neither was
       written *for* that red. A green suite this morning is not a reason to
       delete a rule about what a red suite does and does not mean, and this
       leaf has been caught once already deleting a precaution the moment its
       occasion passed.

       **The mark, and why the line under it does not move.** Decisions raised
       D10 because three files answer "what does a SKIP mean" three ways —
       compliance's row calls the stripped-tree consequence intended, design's
       §6.13 box says T-VEND-02 "is welcome when it runs and is not required,
       because it skips on a stripped tree", and this line says any skip is not
       a green. The mark is accepted; **the instruction is not weakened**,
       because on the machine the sitting actually runs from — a checkout of
       this repo — the command reads **0 skipped and all three readings agree**
       (own run, round 19, project interpreter: `pytest tests/test_vendoring.py
       tests/test_copy_surfaces.py` → **17 passed, 0 skipped, 0.10s**; the
       vendoring half alone **7 passed, 0 skipped, 0.04s**). A presenter does
       nothing differently tomorrow, and D10 cannot reach the sitting by its
       own non-deferral clause.

       **One correction handed back to decisions, reproduced from this seat
       rather than taken on report, and it is not in their favour or mine —
       it is bigger than either of us wrote.** D10 states the divergent tree
       as an unpacked sdist where the command exits 0 with **2 skipped**. That
       was measured on `tests/test_vendoring.py`. Under the label this
       template actually carries, the command is TWO files, and
       `tests/test_copy_surfaces.py` gates two of its own clauses on the same
       missing `leaves/`. Built in scratch, no repo file mutated, `leaves/`
       absent: the aggregate reports **FOUR skipped** — `test_vendoring.py:90`
       and `:107` ("stripped deployment: design leaf not present") plus two at
       `test_copy_surfaces.py:242` ("no design copy authority in this tree
       (stripped install)"). Every one of the four names its own subject, which
       is `T-VEND-07`'s floor doing its job. **The consequence is the exact
       harm sequencing filed this round, arriving through D10's door:** two of
       those four skips belong to a file whose reds this board has just agreed
       are *never* a void — so a presenter on a non-checkout machine, holding
       the pre-round-19 label, would have written NO RECORD partly on skips
       from the non-voiding half. That is the strongest argument on the board
       for splitting the label, and it is why this seat took sequencing's
       demand whole rather than negotiating it. It also bounds D10 honestly in
       the other direction: the divergence is unreachable from a checkout, and
       the demo machine is a checkout.

       **And as of this round the file enforces its own floor, which is
       better than any field this seat could write.** `T-VEND-07`
       (`test_this_file_cannot_return_an_all_skipped_green`, registered by
       compliance on sequencing's demand, read here in the source rather
       than cited) asserts structurally, off the file's own AST, that two
       named clauses carry no skip predicate at all and that every clause
       that *does* skip skips on a predicate naming its own subject. So an
       all-skipped green is not merely something a witness is asked to
       notice — it is a state the pre-flight file cannot enter without
       reddening first. **A caveat asking a presenter to count skips is the
       honor system with a stopwatch on it**; the skip field stays on the
       template because a recorded fact costs one word, but the thing
       actually holding the floor is a test, not the presenter. Own run
       after it landed: `pytest tests/test_vendoring.py` → **7 passed,
       0.03s, zero skipped**.

       **THE COMMAND GAINS ONE FILE AND LOSES TWO HUMAN CHECKS (round 17,
       net ceremony DOWN).** The pre-flight is now
       **`pytest tests/test_vendoring.py tests/test_copy_surfaces.py`** —
       still one line, still one command, **11 passed in 0.06s** from
       `/tmp`, own run — and **12 passed** on a re-run minutes later in the
       same round, without this seat touching code. That is the third time
       a pinned count has moved inside a round; it is recorded rather than
       overwritten, and it is the reason the witness field records *skips*
       and not a total. This is **not** gate P-15 and this seat is not
       adopting P-15: compliance's instruction — P-15 guards the D1-D6
       resolution round, a presenter has nothing to do about it at the hour,
       do not accumulate it here — is accepted and correct *as a gate*. What
       this is instead is stated plainly so the deviation cannot be found
       later and read as drift: it is the **machine replacement for the
       eyes-on checks item 11 added in round 16 and DELETES this round**. A
       presenter squinting at four labels is a weak instrument this seat
       named as weak when it added it; the same file, run, reds on the same
       drift in 0.06s. **Trading a human glance for a command is the only
       kind of addition this pre-flight accepts**, and if compliance would
       rather this seat carry no reference to their file at all, the eyes-on
       lines are what come back — which is worse for the room, and they
       should know that is the alternative before they choose it.
       **ROUND-18, and it is two tokens rather than a change of shape**
       (compliance's round-17 demand, accepted whole). The P-14 field now
       records **`N passed, M skipped`** in that literal form, and the pass
       condition is stated where the presenter reads it: **green means exit
       code 0 AND `0 skipped`.** This leaf had already made the field
       skip-aware in round 17; what compliance bought is that the field no
       longer contains the word "green" at all, so the last place a judgment
       was hiding — in what "green" *means* — is gone. The asymmetry is the
       one that decides this leaf's whole gate posture: **a red before the
       clock costs a re-schedule; a false green costs the RECORD**, and leaves
       SC-06 unconverted with no way to tell that from a genuine miss. Own run
       this round, repo root, project interpreter:
       `pytest tests/test_vendoring.py tests/test_copy_surfaces.py` →
       **12 passed, 0 skipped, 0.08s**; the vendoring half alone **7 passed,
       0 skipped, 0.03s**.

       **What a red MEANS is now readable off the failure line** (round 18,
       decisions' narrowing — the full clause list lives at item 6 because that
       is where the voiding rule is, and a presenter should find it in one
       place). Short form for the hour: a red in **T-VEND-01/02/03/05** means
       the app is not serving the authority's copy — `n` on the bound-module
       field, **NO RECORD**. A red in **T-VEND-04/06 only** is a real defect
       that blocks a push and is **not** a void; after the D1/D2 resolution
       round a `T-VEND-06` red is *expected* until the install is refreshed,
       and refreshing it (`pip install -e .`) is the whole remedy — never a
       hand-edit of the `site-packages` snapshot, never deletion of the wheel's
       `force-include`. **And a red in the OTHER file — anything in
       `tests/test_copy_surfaces.py` — is a defect that blocks a push and is
       never a void** (round 19): those clauses speak about on-screen wording
       against design's ratified fixture, not about which module copy was
       bound, which is the only predicate NO RECORD exists to protect. The
       failure line prints the file path, so at the hour this is read, not
       reasoned.
     - **P-14 — the pre-flight becomes a RECORDED FIELD, not a habit**
       (compliance's round-15 demand, accepted whole and the sharpest
       thing said to this seat this round). Running the pre-flight and
       *recording that it ran* are different acts, and only the second one
       survives the sitting. So the witness template now carries the
       pre-flight's outcome as a field, and the **bound-module
       confirmation is answered BY that field rather than by a
       presenter's judgment**: `y` means *this command was run green on
       the machine that ran the app, before the clock started*. That
       closes the last soft spot in the round-15 rewrite — I had replaced
       a false mechanism with a true predicate but left the predicate
       confirmed by a human ticking a box about bytes they cannot see.
       Compliance's reason is the operative one and is adopted in their
       terms: it is checkable by machine rather than by a presenter's
       memory of a mechanism that was never true. It also closes the door
       they correctly identified as still open — a non-authority copy
       **delivered by a reinstall, from the repo root, with the
       working-directory field filled in correctly**. The old gate would
       have waved that build straight through; P-14 reds on it.
     - **The working directory stays a RECORDED FIELD on the witness
       template**, demoted from precondition to free disambiguation
       (engineering and sequencing both offered its removal; I keep it
       because a filled record costs one word and an unexplained void
       costs a sitting). It is no longer a voiding condition on its own —
       **the bound-module-bytes rule above is.**
  8. **Same-round landing, restated as binding** (sequencing's round-13
     demand, accepted). Whichever row is true lands **in the round the
     backstop hour passes**, not the round after: the filled template if
     the sitting ran, the registered miss string (item 4) if it did not.
     Sequencing's rider is accepted as fair and correct — with neither
     row landed at the hour, WINDOW ELAPSED — AWAITING GTM'S DATED LINE
     is an accurate description of this seat's silence, and a miss
     inferred from silence would have been worse for both instruments.
  9. **A late arrival is a late record, not a hold** (decisions'
     round-13 demand, accepted). If a fresh user materializes AFTER the
     backstop hour, the sitting runs under the identical protocol and
     lands a **late witness record filed against M-UX-02** — it does
     **not** defer, pause, or reopen the D1-D6 resolution round, and it
     does not un-flip a missed-window line already landed. A dated fact
     is not undone by a later hope; it is superseded by a later dated
     fact, on a new row, with both rows readable.

  10. **The 0→1 coverage question, answered from the one seat that can
     answer it** (decisions' round-14 demand, D8, SLA 2026-09-02 —
     answered BEFORE the sitting as asked, because the cheapest branch
     expires the moment the user leaves the room). Two questions were
     put; both get a plain answer rather than an option.
     - **Is a second FRESH user obtainable? No — and I will not promise
       one.** This seat does not own the recruitment channel; Hari does.
       The FIRST fresh user has not materialized across rounds 10-14 with
       the witness standing by all day, every day, and the backstop hours
       away. A seat that could not produce one user in five rounds
       promising a second would be manufacturing exactly the
       "perpetually imminent" state sequencing killed in round 12, in a
       new place. So **D8 option 2 — a separately recruited, instrumented
       0→1 fresh-user sitting — is not fundable from this seat**, and any
       ruling that assumes it should assume it will not happen.
     - **Can the recruited user be asked for a short 0→1 leg after the
       1→N run? Yes, and it costs minutes** — a mode toggle and one
       questionnaire, on a user already in the room, with both clocks
       already running. **This is D8 option 3 and it is the only
       reachable branch**, so it is pre-staged here rather than debated
       at the hour.

     **What that leg is, and — more important — what it is NOT.** It is
     a **NON-FRESH, NON-CONVERTING SECONDARY DATUM.** The user has seen
     the app, which item 6 names by name as a disallowed stand-in, and
     that naming gets **no exemption here just because the number would
     be convenient**. Concretely, and binding on this seat:
     - It is **not a sitting**, not an M-UX-02b record, and there is no
       M-UX-02b record for it to be. It does **not** convert SC-06's 0→1
       half, does not touch claim-ledger row 4 on any branch, does not
       appear in the ledger at all, and does not alter the PASS / FAIL /
       WINDOW CLOSED texts by one word.
     - **The number is not sayable in any payload** — not in the tour,
       not in 1a/1b/1c, not in a deck, not verbally in answer to "how
       fast is 0→1?". That question keeps exactly one answer on every
       branch: **"designed so, not yet timed."** A measured-looking
       figure from a coached, non-fresh, second-run user is precisely the
       false precision this product exists to refuse; quoting it would
       make this leaf's own instrument do the thing the Spine forbids the
       product from doing.
     - It runs **AFTER** the 1→N run, never before and never interleaved,
       so it cannot contaminate the only measurement that converts
       anything. If the 1→N run voids, the leg is abandoned too.
     - It routes to **design as an observation, not to compliance as
       evidence**: where a second-time user stalls in 0→1 is defect
       information, and defect information is worth having even when it
       is worth nothing as a claim. That is the entire reason to want it.
     - Pre-written so it costs zero at the hour: `0→1 secondary
       observation (NON-FRESH, NON-CONVERTING — not an M-UX-02b record):
       date ____ · same user as the 1→N run, second exposure · elapsed
       ____ · stall points observed ____ · routed to design; not quotable
       in any payload; SC-06 0→1 remains "designed so, not yet timed".`
     - **If it never runs, nothing is lost.** D8 is unaffected, no branch
       changes, and the honest state is the one already written. I am
       answering the question, not attaching a hope to it.

     And the framing decisions actually asked for is adopted: this file
     no longer reads the 0→1 half as **settled**. It is **QUEUED (D8)** —
     in row 4's Basis cell, in the PASS branch, and here. The distinction
     matters to this seat more than to most: "we chose not to measure it"
     and "nobody has ruled on measuring it yet" are different sentences,
     and only one of them is currently true.

  11. **The copy assurance is SCOPE-LIMITED TO THE CATALOGUE, and this
     leaf has been saying it wider than that** (design's round-15 demand,
     accepted in full and reported against this leaf's own record first,
     because that is where it lands hardest).

     **The clause, in the form it must be said in:** every "the copy on
     screen is the copy that was reviewed" assurance this leaf makes —
     the §3 sync check, the `cmp`-clean mirror line, the R-10 re-vendor
     note, the CTA-key check inside the P-14 pre-flight — watches **the
     design catalogue's strings, via `strings.py`, and nothing else**.
     **26+ rendered strings sit outside every one of those instruments**:
     design's §6.15(iii) AST census counts **20 bare literals in
     `app.py`**, plus the rendered text fields in `configs/*.yaml`
     (factor `label`, `name`, `scale`, `rationale`; flag `name`,
     `description`; evaluative-input `name`, `note`). So a "no rendered
     text changed" statement derived from a catalogue diff or a mirror
     `cmp` is **true of the catalogue and untested for everything else**,
     and from this round it is said that way in the same breath or not
     said at all.

     **Verified from this seat, not taken from the packet** (2026-08-31,
     own grep against the current `app.py`): the four evaluative labels
     are bare literals — `"A · Strategic fit (not scored)"`, `"A · Brand
     fit (not scored)"`, and the B pair — and the Compare button was the
     bare literal `"Compare"`. Their addresses have now moved **three
     times in three rounds**: design cited 841-845, round 16 found them at
     860-864/868, round 17 finds the labels at **884-888** and the Compare
     literal gone from the render site entirely (it is now the constant
     `_COMPARE_LABEL` at **`app.py:81`**, used at 892). That is the point
     in miniature, and it is why no line number in this item is load-
     bearing: an ungoverned literal has no stable address, so a census of
     it is a *dated* fact and its instrument can never be a line number —
     which is exactly why `T-NEG-08` censusing by AST is the right shape
     and a grep would not have been.

     **Why this one is not a pedantic finding, in this leaf's own
     terms.** `tour.html:483` is a numbered tour stop that says **"Strategic
     fit never touches the score. Evaluative judgments are captured and
     displayed as labeled override inputs — excluded from the mechanical
     arithmetic, on purpose,"** and `tour.html:531` badges it *captured ·
     displayed · excluded from score*. That is a **Spine refusal** (§Scope
     Boundaries: evaluative factors are captured and displayed, never
     scored) turned into a demo beat — one of the beats that makes a
     prospect trust the thing. **On screen, the entire proof of that
     promise is four parentheticals that no instrument on this board
     watches.** Delete the words `(not scored)` from those four labels and
     every test in this repository stays green, every mirror stays
     `cmp`-clean, P-14 stays 6-passed, this file keeps saying the copy was
     reviewed — and the presenter points at a screen that no longer says
     the thing they just claimed it says. That is the tour lying with a
     green board behind it, which is the only failure this leaf actually
     fears.

     **ROUND-17: THE SENTENCE ABOVE IS NO LONGER TRUE, AND THE
     CORRECTION IS RECORDED IN PLACE RATHER THAN BY QUIET EDIT.** "On
     screen, the entire proof of that promise is four parentheticals that
     no instrument on this board watches" was true when written and was
     false within one round. Compliance built the instrument — `T-NEG-08`
     in `tests/test_copy_surfaces.py`, which censuses the evaluative
     labels **by AST** (not by regex and not by line number, so the
     address problem this item raised cannot silently empty it) and reds
     if any of the four renders without the `(not scored)` marker; plus
     `T-NEG-08a` asserting the same refusal in both schemas' `note` and
     `T-NEG-08b` making it structural. Engineering closed the other half:
     `_COMPARE_LABEL = "Compare"` at `app.py:81` with an **import-time
     assertion** that `str.verdict.stale` ends `Press Compare to
     recompute.` — which reds **before first paint**, i.e. at the hour,
     which is strictly stronger than anything a presenter could have done.

     **Verified red-first from this seat, not cited from the packets**
     (2026-08-31, round 17, no repo file mutated — a scratchpad tree with
     `pairwisepm/`, `configs/`, `leaves/` symlinked and `app.py` copied):
     deleting `(not scored)` from ONE of the four labels produces
     `FAILED tests/test_copy_surfaces.py::test_evaluative_inputs_are_labelled_not_scored_on_screen`
     with `assert not ['A · Strategic fit']` — the offending label named
     in the failure text. Clean, the file is **5 passed in 0.06s**. The
     exact mutation this item warned about now has a red attached to it.
     (Honest note on that run: `test_engine.py` also reported one failure
     in that tree, `FileNotFoundError` on a `requirements.txt` I did not
     copy — an artifact of my scratchpad, not of the mutation, and said
     here because a red I caused and did not explain is the kind of thing
     this file exists to refuse.)

     **Executed, and this round the executed thing is a DELETION:**
     - **The two eyes-on pre-flight checks added in round 16 are
       DELETED.** They named the four `(not scored)` labels and the
       `"Compare"` button for a presenter to confirm by eye. Both are now
       covered by machines that see more than an eye does: the labels by
       `T-NEG-08` (AST, count pinned at four, red on the exact deletion),
       `Compare` by the import assert (red before first paint, on every
       launch, no one has to remember). **A check an instrument already
       makes is duplicate ceremony, and ceremony is what this leaf
       deletes for a living** — including its own, added three days ago,
       by this seat, for a reason that was good at the time. Deleting a
       check I introduced last round is the same rule as deleting a gate I
       opened: the standard does not soften because the ceremony is mine.
     - **What replaces them is in the same one command** (item 7):
       `tests/test_copy_surfaces.py` joins the pre-flight (11 passed, then
       12 on a later run the same round; zero skipped both times). Its **honest scope, stated on the same line it is claimed**:
       this means the four labels carry their marker and the config
       rendered text is neither empty nor a placeholder **on the machine
       the presenter ran it on, at the moment they ran it** — it is not a
       review of that copy, and the remaining ~16 `app.py` literals and the
       `configs/*.yaml` text *wording* stay outside every instrument named
       here. Coverage went from **zero instruments to two** on the
       ~~demo-visible~~ **trust-weighted** subset; it did not go to complete,
       and this file will not say it did. (Round-18 correction to this
       sentence's own scope word, struck rather than reworded away: "demo-
       visible" was measured this round at **nineteen of twenty-one**
       literals, so the two instruments never covered *that* set and this
       bullet was claiming a wider coverage than it held. What they cover is
       the four trust-weighted labels — see the ROUND-18 block below.)
     - **Still not a gate on anything, and still not leverage.** Design's
       post-sitting catalogue move for the four labels
       (`ENG-COPY-EVALLABELS-01`, deferred on purpose to the first release
       AFTER the sitting) is the right sequencing and this seat re-states
       that it does not gate the sitting on it. A demo beat that has been
       true all cycle does not become a blocker the evening it is finally
       instrumented.
     - **§3 sync check** carries the same scope caveat inline, because
       that is where the assurance sentence actually lives.
     - **No claim-ledger row changes.** Nothing in §0 asserts reviewed
       copy, so nothing there is overstated — this is a caveat on a
       *procedural* assurance, and confining it to where the assurance is
       made is the difference between correcting a record and performing
       a correction.

     **ROUND-18: THE EYES-ON BOUND IS DRAWN ON TRUST WEIGHT, NOT ON DEMO
     VISIBILITY — AND THE PREMISE THIS SEAT ASKED THE QUESTION ON WAS WRONG.**
     Round 17 asked design to name the *demo-visible* subset of the §6.15(iii)
     census, on the assumption that visibility would bound the list at about
     five. Design measured it instead of agreeing, and the measurement is the
     opposite of convenient: **steps 1-7 paint NINETEEN of the twenty-one
     literals** — the whole input screen in both mode groups (`grp_n2n`
     visible, `grp_z2o` painted at the step-6 flip), the decision block and the
     file component; only the two name placeholders miss, masked by the loaded
     example, and "Your decision log" is `visible=False` until step 7. **A
     visibility-bounded eyes-on list is a nineteen-item pre-flight** — the
     exact accretion this seat deletes ceremony to prevent, and it would have
     arrived wearing this seat's own request as its warrant. The premise is
     corrected here rather than inherited quietly, because it was this leaf's
     premise and it was wrong in the direction that made a deletion look safer
     than the reasoning behind it was.

     **The bound adopted instead, in design's terms and with their predicate
     verbatim so a later reader can apply it rather than trust it:**
     **EYES-ON FIVE** — the four `(not scored)` evaluative labels plus
     `"Which do you actually pick?"`. *A literal is eyes-on if its silent
     corruption would make the demo NARRATION false while every test stays
     green.* `Compare` is deliberately **not** on the list: it is
     machine-governed as of round 16 and reds at import before first paint.
     The list **cannot grow by accretion** — a literal joins only by promotion
     to design's CANDIDATES class, which needs a dated amendment naming it
     individually. That is a permanent bound of five, drawn on trust weight,
     replacing a bound of nineteen drawn on visibility.

     **Applying design's own predicate to THIS surface, and the answer is four,
     not five** (own grep, round 18, both GTM narration surfaces):
     `"Which do you actually pick?"` occurs **once in the repository, at
     `app.py:911`, and ZERO times in `leaves/gtm/tour.html` and zero times in
     the 1c demo script**. No GTM narration quotes it, paraphrases it, or
     points at it as a numbered stop — so its silent corruption cannot make
     the *narration* false, and by design's predicate it is not eyes-on **on
     this surface**. The other four are: `tour.html:483` is a numbered stop
     asserting the Spine's excluded-from-score refusal and `tour.html:531`
     badges it *captured · displayed · excluded from score*, while `tour.html`
     contains the string `"not scored"` **zero** times — the tour narrates the
     refusal in its own words and the SCREEN carries the proof. That asymmetry
     is the whole reason those four are trust-weighted and the pick question,
     for this leaf, is not.

     **So the round-17 deletion was safe, and this is the permanent statement
     of why.** All four of the trust-weighted literals on this surface are
     covered by `T-NEG-08` — AST, count pinned at four, red on the exact
     deletion, verified red-first from this seat last round. The eyes-on
     pre-flight lines stay **deleted**; they are not coming back for a literal
     no narration quotes.

     **The disclosure this seat owes design, and it points at a coverage claim
     that rests on a check that no longer exists.** Design's §6.17(ii) rules
     `"Which do you actually pick?"` STRUCTURAL with a standing MP-2
     obligation, and says it is "covered in the interim by the eyes-on five."
     **There is no interim cover.** This leaf deleted its eyes-on pre-flight
     checks in round 17 and is not reinstating them, so nothing on the GTM
     surface watches that literal — an assurance whose instrument was retired
     by the seat the assurance points at. The cause is this seat's deletion,
     which is why the disclosure is filed here and demanded of design in the
     same round rather than left for them to discover. Two ways out and this
     leaf will take either: promote the pick question to CANDIDATES by dated
     amendment, or ask compliance for one AST clause beside `T-NEG-08`. If
     design instead judges that a presenter's eye is the right instrument for
     it, say so and **this seat will carry exactly one eyes-on line** — one,
     named, not a list — because a wrong coverage claim in another leaf's file
     is worse than one line of ceremony in this one.

     **And the item's own general form, applied to itself.** Round 17 corrected
     "no instrument watches this" to "an instrument watches it." Round 18
     corrects the *scope of the question that produced the deletion*: the
     boundary this seat asked for was the wrong boundary, and the right one is
     smaller and permanent. Both corrections run the same direction — toward
     saying exactly what is watched, by what, on which surface.

     **The half of this that has a DEADLINE, and it is tomorrow.** The
     `configs/*.yaml` text fields are not a theoretical exposure on this
     surface: **`tour.html` carries the factor names 7 times** (own
     occurrence-count, round 17: "Capability feasibility" ×1, "Unit
     economics" ×3, "Data flywheel" ×3 — *round 16 said 8, which was this
     seat counting matching LINES and reporting them as occurrences; the
     count is corrected in place and the direction is the flattering one,
     which is the direction that needs correcting*), and
     **demo-script step 3 at 1c names them out loud** — "A's margin comes
     from impact (+.125), unit economics (+.105), feasibility and flywheel
     (+.08 each)". The **D1-D6 resolution round edits those exact files**,
     and in `configs/*.yaml` a policy value and an on-screen factor name
     are neighbouring lines in the same block. A resolution-round edit that
     renamed "Unit economics" would leave the tour and the demo script
     quoting a factor the app no longer displays, with the suite green and
     every copy instrument silent — the presenter reading a script against
     a screen that disagrees with it, in front of the guest. Design has
     drawn the bright line with engineering (six numeric/policy fields are
     free, six text fields are copy); **this leaf's demand is the
     notification half**, filed this round, because the two files that
     break are on this leaf's surface and no one else can see them break.

     **Round-17: the deadline half is answered, and answered better than
     the notification I asked for.** Three things landed, none of them
     from this seat. (1) Engineering wrote the bright line into
     `pairwisepm/config.py`'s docstring as constraint 1 of the
     resolution-round procedure — at the point of use, in the file the
     person doing the round actually opens, rather than in a packet.
     (2) Sequencing encoded the edit-class label on the resolution node
     **and checked the cost rather than assuming it**: no option on D1 or
     D2 as written touches a text field, so the expected number of
     class-(B) edits tomorrow is **zero**, and a class-(B) edit appearing
     inside that round is itself evidence the round drifted past the
     question it was convened to answer. (3) Compliance's `T-COPY-01/01b`
     red on config rendered text left empty, stubbed as `TBD`, or echoing
     its machine key — the realistic failure of a fast values round, and
     it is in the pre-flight command this file now runs. **What is still
     not covered is the case that actually worries this surface**: a text
     field edited to a *different, well-formed* string — "Unit economics"
     renamed to something equally plausible — passes every instrument
     named here and leaves `tour.html` (7 occurrences, own grep) and demo
     step 3 quoting a factor the app no longer displays. That gap is named
     rather than gated: it is a copy-authority question design and
     compliance already have open (F-32), the notification remains the
     cheap mitigation, and this seat will re-check the tour's seven
     occurrences against the shipped configs after the resolution round
     lands rather than asking anyone to hold the round for it.

     **The general form, owed because this is the third seat to find it
     this cycle** (architecture's guard whose activation was narrower
     than its subject; design's chain certifying one population of
     three): *an assurance is only as wide as the instrument under it,
     and a leaf that states the assurance without stating the instrument
     is trading on coverage it does not have.* This leaf sells coverage
     for a living. It should be the first to price it, not the third.

  12. **THE WINDOW CLOSED. THE DATED LINE, LANDED IN THE ROUND THE HOUR
     PASSED (round 20), verbatim in the string registered at item 4 — one
     string, three instruments, no adjective added and none removed:**

     > **M-UX-02 window closed unconvened, 2026-09-01 07:55 CDT — no
     > sitting convened, no record exists; designed so, not yet timed.**

     **Verified from this seat before the line was written, not taken from
     any packet** (2026-09-01 07:55 CDT, project interpreter, repo
     checkout): `leaves/design/states.md` carries NO filled M-UX-02
     per-check line — its Branch-A shape at :1492 and its Branch-B line at
     :1509 are both still the `<date>` / `<date/time>` templates; the
     witness template above this item is unfilled at every field; no
     fresh-user recruit was reported in any round. The backstop was the
     first hour of 2026-09-01 and it is now past 07:00 local. **The missing
     input was a fresh human**, which is the one input no agent on this
     board could supply: design's timer stood READY from §6.12 onward with
     zero preparation remaining, GTM's witness stood by from round 10
     through the backstop, and the pre-flight was green on every check this
     seat ran across six rounds.

     **What the timestamp in the registered string denotes, said once so no
     reader has to guess:** it is the moment of the CHECK AND THE REPORT —
     when this seat verified both files and landed the line — not the moment
     the window shut. The window shut at the end of the first hour of
     2026-09-01, six-odd hours earlier, and nothing convened in between. The
     registered string takes one `[date/time]` and this is the only reading
     that is a fact about an action rather than about a deadline everyone
     already knows; sequencing's rule is that the miss is a dated line and
     not an inference from an absence, so the date on it should be the date
     of the line.

     **What this changes on the demo surface: NOTHING, and that is the
     point of having pre-written it.** No demo step moves, no gate opens,
     no registered phrase changes, the tour is unedited. SC-06 reads
     "designed so, not yet timed" in every payload — which is what it has
     read all along, because this leaf never let it read anything else
     before a record existed. The ledger row-4 Basis cell is swapped to the
     WINDOW CLOSED text (§0) in this same round, per item 8's same-round
     rule; it now names a dated fact instead of a pending event, and it can
     no longer be read as "we're about to test it."

     **Why this is landed rather than left to expire quietly.** A window
     that closes with no line is indistinguishable, to the next reader,
     from a window still open — and from a run that happened and went
     unrecorded. Sequencing's graph read `WINDOW ELAPSED — AWAITING GTM'S
     DATED LINE` and correctly refused to flip the node on its own clock
     check; the flip is this line and nothing else. **A miss is a fact this
     leaf can say out loud**: the honest version of a five-minute claim is
     worth more to a pilot conversation than a converted one nobody
     witnessed, and a presenter asked "is that measured?" answers with the
     registered phrase and does not blush. Item 9 stands: a fresh user who
     materializes tomorrow runs the identical protocol and lands a LATE
     record on a new row — this line is superseded by a later dated fact,
     never erased by one.

     **The one thing a presenter must NOT do with this line:** do not read
     it as a defect in the product. Nothing was measured and nothing
     failed; the 5:00 bound was never tested, so it cannot have been lost.
     "We timed it and it was slow" is not sayable. "We designed it for
     under five minutes and have not yet timed it with a fresh user" is.

  **Re-schedulability, stated now so the missed-window branch is not
  mistaken for a closed door:** a missed window records that this slot
  expired, not that the five-minute claim is unmeasurable. M-UX-02 stays
  convertible by any later newly-scheduled witnessed run under the same
  protocol (same six fields, same clock definition, same voiding rule);
  the branch block's WINDOW CLOSED text is replaced by the PASS or FAIL
  text if and when such a run produces a dated record. Until then the
  claim stays exactly where the evidence leaves it.

Known mechanism trade-off, accepted by GTM as post-pilot polish (engineering's R-4
no-dispute-if-deferred terms): Textbox inputs lose the numeric spinner and the mobile
numeric keyboard. For live demos this is invisible — the presenter types or loads the
example — and it is never a reason to reintroduce a component that fabricates scores.
Do not schedule mobile-first demos until this polish question is settled post-pilot.

### 1d. Guided tour link

`leaves/gtm/tour.html` — self-contained; the same seven-stop story with every number
from the same canonical comparison. Safe to share anywhere at pilot stage: it contains
no accuracy claims and badges all log-derived panels as sample data.

Verification provenance (round 3 browser render, design states.md §6.3; round-4
M-GTM-01, §6.6): every checked tour surface matches the live app verbatim — banner
copy, verdict/model/mode lines, eval annex, leverage table + provenance chip, custody
nudge, audit rows, and both Stop 5 ceiling strips verified against the exact served
pipeline (probability invariant with and without the flag). The two divergences found
(Stop 2 clean questionnaire vs live pre-filled 0s; Stop 3/5 card legibility on dark
theme) were app defects against the catalogue the tour mirrors — R-8/R-9, fixed by
engineering in round 4. Render session 2 (§6.7, 2026-08-31) closed the first
divergence browser-verified: first paint now matches Stop 2 verbatim on a live
screen. Render session 3 (§6.9, 2026-08-31) closed the second divergence
browser-verified too: every R-9b surface computes legible ink in the served dark
theme, and the whole Stop-5 screen passes zoomless — both app defects the tour
exposed are now fixed and browser-confirmed, and the tour shipped unchanged
through the entire cycle: the build converged to it, not the reverse. One minor
divergence remains on the record for honesty (R-12, §6.4/§6.9): the as-built S5
card renders the mechanical headline above the routing strips where the tour
(matching the S5 spec) shows the routing strip on top — emphasis order only, all
copy present and legible, post-pilot polish class. Presenters narrating Stop 5
against the live app should read the strips first regardless of their on-screen
position; the tour is not re-mocked to match a defect. Five-minute claim surfaces in the tour (audited round 14, this seat's own
grep, so the mode-scoping rule at item 6 has a known blast radius): exactly one
line of `tour.html` carries the product claim — "Designed so a full A-vs-B
comparison, blank form to verdict card, lands in under five minutes" — and it
already carries the "Designed so" framing, so the WINDOW CLOSED and FAIL
branches need no tour edit at all. On PASS it becomes the dated mode-named
claim, and only then. The two other five-minute strings in the file describe
how long the WALKTHROUGH takes to read, not how long the product takes to use;
they are not SC-06 claims and do not move on any branch. Note for the record (checked round 5): the Stop 2 mock renders factor values
as styled text, not native number widgets, so engineering's Number→Textbox mechanism
introduces no new tour divergence — nothing to re-mock.

---

## 2. [ga-live] message set

Gate: `ga-live` node (PyPI release + `calibration-report` node complete — a
calibration report computed from real logged decisions). The calibration report is the
**proof point**; accuracy language for 1→N becomes sayable only here, and only with
the report's actual numbers attached.

### 2a. GA announcement (template — DO NOT publish with placeholders unfilled)

> PairwisePM is now on PyPI: `pip install pairwisepm`.
>
> Since the pilot, [N] real A-vs-B decisions have been logged. The calibration report
> is public: Brier [X.XX] against picks, ζ [X.XX], reliability curve at
> [REPORT_URL/PATH]. In 1→N allocation mode, the judge's probabilities are
> [exactly what the reliability curve supports — state it plainly, no rounding up].
>
> That's the claim discipline: accuracy was never asserted up front — it was earned
> on the log, and here is the log's verdict on the judge.
>
> 0→1 search mode still makes no accuracy claim, and never will without outcome data
> that does not yet exist. It structures your search; the judgment stays yours.

### 2b. GA proof-point framing rules

- Lead with the calibration report, not the feature list; the report *is* the ad.
- Report Brier/ζ with their n. Never quote them without the decision count.
- If the reliability curve is unflattering, publish it anyway and say what it changed
  (weights re-signed? shrinkage increased?) — the honesty rules are the product; a
  buried bad curve would falsify the entire positioning.
- M2 teaser only as future-gated: "outcome-label regression enters at ~45 labeled
  outcomes" — never as a current capability.

---

## 3. Pinned README substrings (agreement with compliance, T-PKG-02)

Compliance asserts the three technical-spec §7 epistemics statements as substrings of
the README body. The agreed exact substrings, present verbatim in `README.md`:

1. `priors are a stated, editable policy, not fitted`
2. `0→1 makes no accuracy claim`
3. `the LLM's job was at build time — the runtime is weights and a bias term`

Also present in README verbatim (design-owned strings, quoted not paraphrased):

- `str.banner.01` (full text, in the Epistemics section)
- `str.empty.privacy` — "Runs entirely in this app. No API key, no server, nothing
  stored anywhere but your own log file."
- `str.disagree.headline` — "Your stated policy and your revealed policy disagree."

If design revises any `str.*` string, README.md and this file must be re-synced from
`leaves/design/states.md` — copy flows design → gtm, never the reverse.

**SCOPE OF EVERY SYNC ASSURANCE BELOW (round 16, design's §6.15 demand, accepted;
narrowed round 17 on this seat's own re-check).**
This sync check, the `cmp`-clean mirror line, and every "no re-sync owed / zero tour
divergence" statement in this file are **scope-limited to the design catalogue's
`str.*` strings**. They say nothing about the bare literals in `app.py` (design's
§6.15(iii) AST census) or about the **rendered text fields in `configs/*.yaml`**
(`label`, factor `name`/`scale`/`rationale`, flag `name`/`description`,
evaluative-input `name`/`note`). A catalogue diff is evidence about the catalogue.

**Round-17 correction to this paragraph's own claim.** It said those strings were
"watched by no instrument". Two of them are now watched, and this seat verified both
rather than citing them: the four `(not scored)` evaluative labels by `T-NEG-08` in
`tests/test_copy_surfaces.py` (AST census, count pinned at four, red-first
demonstrated here — see item 11), and the `"Compare"` button by engineering's
`_COMPARE_LABEL` bind plus an import-time assert that reds before first paint. The
rest — roughly sixteen further `app.py` literals and the *wording* of the
`configs/*.yaml` text fields — remain outside every instrument this file names, so
the assurance stays scope-limited; it is just no longer as narrow as it was.
Line numbers are deliberately not quoted here any more: they moved twice inside two
rounds on comment-only edits, and an instrument that is a line number is a dated
fact pretending to be a check. Read the full statement at 1c-i item 11; it is not a
gate on anything.

Sync check, R-10 mint (round 9, 2026-08-31, GTM's own diff): design's round-8
canonical mint (five `*_one` singular variants, `str.empty.example_cta`, corrected
`str.verdict.stale` tail) is re-vendored byte-identical (`cmp` clean, verified this
round). None of the three strings this file quotes verbatim (`str.banner.01`,
`str.empty.privacy`, `str.disagree.headline`) changed, and `tour.html` contains
neither the stale notice nor the example-CTA text — **no re-sync owed, zero tour
divergence introduced** *(scope: the catalogue's `str.*` strings — see the scope
paragraph above; the 20 `app.py` literals and the `configs/*.yaml` text fields are
outside this diff and outside every instrument behind it).* Two demo-visible gains ride the mint free: the S2
placeholder with one missing factor now reads "1 factor score to go" (no more
"1 factor scores" in a live demo close-up), and the stale notice now tells the
truth the demo can show — "Inputs changed — the verdict above no longer applies.
Press Compare to recompute." — a legible honesty beat instead of a false
"Recomputing…" claim a sharp-eyed prospect could catch. The copy chain got more
demoable without this leaf touching a word.
