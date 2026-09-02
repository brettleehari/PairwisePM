# Decisions Leaf — PairwisePM

This is the queue that resolves disagreement. When two Leaves — or the PM and the
build — genuinely disagree, the disagreement does not get argued to death in a
thread and it does not get silently "won" by whoever wrote the last file. It gets
an entry here, and the entry has a clock.

The Spine (`spine/SPINE.md`) wins every conflict. This queue exists for questions
the Spine does not settle. If a question turns out to be one the Spine *should*
settle, that is what the `spine_gap` flag is for (see below) — but that flag is
deliberately expensive to invoke.

## The file

All decisions live in one file: `leaves/decisions/decisions.yml`. Append-only in
spirit: entries change `status` and gain resolution fields; they are never
deleted or rewritten to look smarter in hindsight. The queue is part of the
audit trail, in the same spirit as the product's own decision log.

## Entry format

```yaml
- id: D<n>                      # monotonically increasing, never reused
  title: <one-line question — phrased so "resolved" is checkable>
  raised_at: <YYYY-MM-DD>
  sla_expires_at: <YYYY-MM-DD>  # raised_at + 2 days
  spine_commitment: <the Spine line this decision serves — every entry must trace>
  stakeholders:
    - name: <who>
      factors: [<what this stakeholder's position rests on>]
  options:
    - <option 1 — concrete enough to build from>
    - <option 2>
    - <option 3 — include the "do nothing / defer" option when it is real>
  status: pending | resolved_uncontested | ai_resolved | human_confirmed | human_overridden | spine_gap
  notes: >
    Context a future reader (or the AI adjudicator) needs: what the build is
    doing in the meantime, and any argument too load-bearing to lose.
  on_resolution_notify:            # optional: leaves that must act on resolution,
    - <leaf>: <what they regenerate/edit>   # kept current by the Decisions Leaf
  # Added at resolution time:
  resolved_at: <YYYY-MM-DD>
  resolution: <the chosen option, verbatim or refined>
  resolution_rationale: <why, traced to Spine + Leaf evidence>
  resolution_instrument: <how anyone checks later that the ruling held — the
                          test, gate, record or field that makes it visible; or
                          "none, by decision, owner <seat>, revisit on <event>">
  override_window_expires_at: <resolved_at + 24h>   # only for ai_resolved
```

Rules for a well-formed entry:

- **Options are buildable.** Each option must be concrete enough that a Leaf
  could implement it tomorrow. "Figure it out later" is not an option; "defer to
  v2 and record the interface it would need" is.
- **Stakeholders carry factors, not ranks.** An entry lists *why* each
  stakeholder's view deserves weight, not who outranks whom. The adjudicator
  weighs factors against the Spine, not job titles.
- **Every entry traces to the Spine.** `spine_commitment` is mandatory. An entry
  that cannot name the Spine line it serves is either scope creep or a Spine gap
  — and must be handled as one or the other, not queued as a normal decision.
- **Build does not block.** Every pending entry names (in `notes`) what the
  build does in the meantime — usually a stated default. Weights, thresholds,
  and cadences are config, not code, precisely so a later resolution is a config
  change, not a rewrite.
- **Every ruling names its instrument** (added round 16, at Compliance's
  demand, and adopted as a standing rule rather than as a one-entry favour).
  `resolution_instrument` is mandatory on any entry that closes, *including*
  the option that changes nothing: an entry that resolves "leave it as it is"
  must say `none, by decision, owner <seat>, revisit on <event>` rather than
  closing on a bare preference. The reason is this queue's own standard turned
  on itself. The queue exists so a contested question is not settled by
  omission; a ruling with no instrument converts an accidental gap into a
  deliberate one without making it any more checkable later, which is
  settlement by omission arriving one level down — the decision is recorded,
  its consequence is not. A named instrument may be a test, a pre-push gate, a
  matrix row, a witness field, or an explicitly owned absence with a revisit
  trigger; what it may not be is silence.

## The lifecycle

### 1. Pending — the 2-day SLA

A new entry gets `sla_expires_at = raised_at + 2 days`. During those two days the
decision belongs to the human stakeholders — normally the PM. The SLA clock is
the human's clock: no agent resolves a pending entry early, no matter how
obvious the answer looks. (This is why D1 and D2 sit pending in this repo even
though the build proceeded on defaults — the clock belongs to Hari.)

### 2. SLA expiry — AI adjudication

If the SLA expires without a human resolution, the decision does not rot in the
queue. An AI adjudicator resolves it, under these constraints:

- **Full context, not a snippet.** The adjudicator reads the entire Spine and
  every Leaf artifact before ruling — the entry's `notes` are a pointer, not the
  evidence base.
- **The ruling is written down** in `resolution` and `resolution_rationale`,
  tracing to specific Spine commitments and Leaf evidence. A ruling that cannot
  be traced is not a ruling; it is a preference, and preferences belong to the
  human.
- **Status becomes `ai_resolved`** and `override_window_expires_at` is set to
  24 hours after `resolved_at`.
- Downstream Leaves may build on an `ai_resolved` decision immediately — but
  only in ways cheap to reverse until the override window closes (config
  values, not architecture).

### 3. The 24-hour human override window

For 24 hours after an AI resolution, any human stakeholder may override with a
one-line reason. No justification standard applies — the human does not have to
out-argue the rationale, because the product's own epistemics apply here too:
the mechanical judge (or adjudicator) exists to apply the human's policy
consistently, not to replace the human's policy. An override sets
`status: human_overridden`, records the human's choice as the resolution, and
keeps the AI's rationale in place for the audit trail. If the window closes
untouched, the resolution stands and status may be bumped to `human_confirmed`
at the next human touch.

### Bilateral dissolution — `resolved_uncontested`

Some entries stop being contested before any clock matters: every named
stakeholder converges on the same option through their own moves, on the
record. Such an entry closes as `resolved_uncontested` — resolution and
rationale written and traced exactly as for an adjudication, but with no
adjudicator and therefore **no override window**: nothing was decided over
anyone's objection, so there is nothing to override. This status exists so a
dissolved claim gets a full record instead of quietly going moot (the failure
mode where a gate claim is neither granted nor refused, just shipped around).
It is NOT a shortcut past adjudication: it requires each stakeholder's
concurrence to be on the packet record, not inferred from silence. D7 is the
first entry closed this way.

### 4. `spine_gap` — the expensive escape hatch

Sometimes adjudication reveals that the question is not answerable *under* the
Spine because the Spine is silent or self-contradictory on it. That is not a
decision to be adjudicated; it is a hole in the customer narrative.

Flagging `status: spine_gap`:

- **Pauses the SLA clock.** The entry cannot be AI-resolved while flagged.
- **Escalates to Spine review.** The Spine's human owner must either amend the
  Spine (with a changelog entry and version bump) or rule that the Spine already
  answers it — after which the entry re-enters the queue with a fresh 2-day SLA.
- **Is deliberately expensive.** Every Leaf touching the contested area treats
  it as frozen until the review lands, and the flagger must write, in `notes`,
  the specific Spine sentence that is missing or contradicted. "The Spine
  doesn't mention X" is not enough if X is settled by a Scope Boundary or by the
  overstated-confidence refusal ("a judge that overstates its confidence is
  worse than no judge").

The expense is the point: if flagging a Spine gap were cheap, every hard
decision would be laundered into one, and the Spine would stop being immutable
in practice. The default posture is that the Spine answers more than it appears
to — read it harder before you flag it.

## Ratified conventions (`conventions:` block)

The exchange round surfaced a second kind of question: not disagreements, but
conventions other Leaves asked this Leaf to confirm — either because the Spine
or the locked spec already settles them, or because every Leaf shipped the same
answer and no stakeholder objects. Those live in a separate `conventions:` list
in `decisions.yml` (ids C1, C2, …) so they are citable ("per C3") and stop
being re-litigated in threads.

Conventions are **not** on the SLA clock and carry no status lifecycle — they
are rulings-of-record, each with a `trace` line to the Spine or spec sentence
that settles it. Contesting a convention means raising a **new D-entry** that
references the convention id; conventions are never edited in place. The bar
for a convention (versus a D-entry) is strict: if any Leaf or stakeholder
actually disagrees, it is a decision, not a convention — that is why the
fragility threshold, where three Leaves shipped three different values, entered
the queue as D6 rather than being "ratified" one way.

Current conventions: C1 M1 gate = exactly 10 picks per mode, overrides count
and train M1 · C2 too-close = interval straddles 50% exactly, boundary
inclusive, no wider dead-band · C3 risk surface entered pre-reversed (4 =
lowest exposure) · C4 configs/*.yaml seed distributions are the canonical
z-basis · C5 interval level = 90%, held as config · C6 leverage panel
hard-switches to M1 weights at activation with a mandatory regime label ·
C7 fresh load defaults to 1→N · C8 overrides honored with one logged
one-sentence rationale.

## Current queue

| ID | Question | Status | SLA |
|----|----------|--------|-----|
| D1 | Prior weight magnitudes, 1→N factor table | pending | 2026-09-01 |
| D2 | Weight of capability-trajectory exposure, 0→1 mode | pending | 2026-09-01 |
| D3 | Does a portfolio/knapsack layer ever enter scope? | pending | 2026-09-01 |
| D4 | Calibration-report cadence and reliability-curve threshold | pending | 2026-09-01 |
| D5 | Seed-distribution → user-log cutover rule for z-scoring | pending | 2026-09-01 |
| D6 | Fragility-flag threshold ("small plausible move") | pending | 2026-09-01 |
| D7 | Is R-8 (browser imputation void) release-gating, R-9 riding? | resolved_uncontested (2026-08-31) | — |
| D8 | Does the release claim SC-06 on a 1→N-only measurement, and does anyone own measuring 0→1? | pending | 2026-09-02 |
| D9 | Does the M-UX-02a witness record carry a launch-environment voiding condition, and on which predicate? | resolved_uncontested (2026-08-31) | — |
| D10 | Does a SKIP in the P-14 pre-flight make the run NO RECORD, or is the floor a named clause set rather than a skip count? | pending | 2026-09-02 |
| D11 | What is the SUBJECT of the no-LLM/no-network guard — the running process, or the engine's own import graph? | resolved_uncontested (2026-09-01) | — |

Pending count: **eight** — D1–D6 (which gate G-D1D2) plus D8 and D10, neither
of which gates anything. D11 was raised and dissolved inside the same round;
the count went nine and back to eight in an hour and both figures are in the
history below rather than one overwriting the other. Stated as a number because
sequencing carried "six" for four rounds after the seventh was raised, and an
index that quietly disagrees with the file it indexes is the defect this table
already had once.

D10 (raised round 18) is D9's successor question, not its reopening. D9 settled
which predicate voids a witnessed sitting; the round-17 skip-aware clause then
created a second question — what a SKIP in that same pre-flight means — and
three files now answer it three ways, each in the seat that owns a third of the
instrument. Reproduced from this seat rather than argued: on an sdist-shaped
tree (the shape `pyproject.toml` actually ships — `tests` and `configs`, no
`leaves`) the pre-flight exits 0 with `5 passed, 2 skipped`, which compliance's
row and gtm's template call NO RECORD and design's protocol calls fine. The
scheduled sitting runs from a repo checkout where all three readings agree, so
the entry gates nothing and changes nothing tomorrow — it exists so the reading
is not settled by whichever file the presenter opened.

Stale-row correction (round 17): this table carried D9 as `pending` for a round
after `decisions.yml` closed it `resolved_uncontested`. Caught on this seat's own
re-read, and recorded rather than silently fixed, because the defect is the one
this Leaf spends its rounds naming in other files: two records of the same
question, one of them stale, and no way to tell which from either file alone. The
`status` field in `decisions.yml` is authoritative — this table is a convenience
index and is now re-derived from it.

D1 and D2 (prior-weight sign-offs) predate this README and remain on the human
PM's clock. D3–D5 were raised from genuinely open questions in the technical
spec — questions the spec explicitly leaves undecided, not questions a Leaf
could settle alone. D6 was raised in the exchange round when three Leaves were
found to have shipped three different fragility thresholds (engine 0.75σ, test
spec 0.5σ, GTM tour one-rung swings) against a spec that says only "small
plausible move" — the build-meanwhile default is the code as shipped (0.75σ).

Resolution mechanics note (per Sequencing's request): the `status` fields in
`decisions.yml` are authoritative for release gate G-D1D2 — the resolver must
record which option won in `resolution`, and each entry's
`on_resolution_notify` list names the Leaves that must act (Compliance
regenerates pinned test constants; GTM recomputes tour numbers on D1; the D2
"gate" option escalates loudly per that entry's notes). Covenant (round 2,
GTM↔Decisions): a D1/D2 resolution that changes any prior weight from the
shipped defaults carries the GTM notification in the resolution note itself,
same round — and G-D1D2 is not lifted on a weight-changing resolution whose
note lacks it. Covenant (round 3, Compliance↔Decisions, same terms): a D1, D2,
or D6 resolution that changes any value from the shipped defaults (weights, or
the fragility epsilon) carries a compliance flag in the resolution note itself,
same round — T-CFG-01/T-M0-01 pin the shipped weight tables and every T-FRAG
fixture assumes FRAGILITY_Z = 0.75, so fixtures must regenerate before any push
on the new values.

SLA-honoring commitment (round 4, accepted from Sequencing): if D1/D2 are
unresolved at SLA expiry (2026-09-01), AI adjudication executes THAT SAME DAY
per lifecycle §2 — written traced rationale, `ai_resolved` status, 24-hour
override window ending 2026-09-02 — and every `on_resolution_notify` line
(compliance fixture regeneration, GTM recompute, sequencing's G-D1D2 hold)
fires in the adjudication round exactly as it would in a Hari resolution: the
covenants bind the resolver, not the resolver's species. The same clock applies
to D3–D6, which share the 2026-09-01 expiry (D7 closed uncontested 2026-08-31
and is off the clock). A silently slipping SLA would make the queue a place
where decisions rot politely, which is the one failure mode this Leaf exists
to prevent.

Source-naming obligation (round 8, accepted from Compliance): every D1–D6
resolution carries a per-entry `resolution_source: hari | ai_adjudication`
field alongside `resolved_at` — per entry, never per batch, because mixed
outcomes are expected. Compliance's fixture-regeneration duty writes a
provenance line on each regenerated pinned constant citing who resolved the
value it pins; without the per-entry source that line is unwritable and the
constant is untraceable. A resolution record lacking the field does not lift
G-D1D2. (This is the same obligation already demanded of Sequencing's
resolution-round packet, now wired into the file the resolver edits.)

Round-3 record: the R-1 collision forecast in round 2 (design's Spine-honesty
framing vs. sequencing's critical-path discipline) dissolved bilaterally and
never became a D-entry — sequencing admitted R-1/R-2 as defect fixes,
engineering implemented R-1..R-3 (verified in code by this Leaf: n_session
state suppressed at 0; strings byte-identical; tests/test_vendoring.py
present), and design consented on the record to deferring R-4. Nothing
contested was baked in silently, and nothing trivial entered the queue.

Round-4 record: design's browser render surfaced R-8 (the no-imputation
blocking rule is void in the served UI — gradio submits 0 for untouched
fields) and R-9 (MP-1 token illegible in dark theme), and design claimed R-8
release-gating THROUGH this queue rather than by editing the critical path —
the exact procedure demanded in round 2, followed to the letter. Registered as
D7. The entry is deliberately narrow (the contested question is gating, not
bug-ness) and carries an explicit dissolution clause: if engineering accepts
the fix on-record and sequencing admits the node under its own defect bar
before the SLA, D7 resolves bilaterally without adjudication, like R-1 did.
The queue's job here is to hold the gate claim open where everyone can see it
— not to slow the fix down.

Round-5 record: D7's dissolution clause fired exactly as written, one round
after registration. Engineering accepted both demands on-record as defects
against its admitted commitment and shipped the fixes (R-8 by removing
gr.Number from the path — Textbox inputs screened so an untouched factor
never reaches the handler; R-9 by forcing text color in every forced-light
block), paired in the same change with compliance's pre-registered guards
T-SER-01 (demonstrated red-first against the pre-fix build) and T-THEME-01,
suite 56/56. Sequencing admitted both nodes under its R-1/R-2 defect bar.
GTM was added as a second named stakeholder with the demo-path harms on the
record (Spine metrics #1 and #4 — two independent stakeholders, two distinct
Spine lines). D7 closed `resolved_uncontested` with compliance's fix+guard
pairing written into the resolution rationale (no resolution can authorize a
guard-less fix) and an explicit reopen clause: if design's browser render
session 2 finds the behavioral acceptance unmet, it reopens as a defect
against engineering's accepted commitment, not as a new decision. The gate
claim was neither baked in by edit-order nor waved off by inaction — it was
claimed through the queue, held for one round in plain view, and granted by
every stakeholder's own move. That is the system working at its cheapest.

Round-6 record: D7's reopen-clause oracle ran — design executed browser render
session 2 (states.md §6.7) the round the fixes landed. The R-8 half closed on
browser evidence: all four acceptance behaviors PASS, so the closing bracket
is closed, not merely promised. The R-9 half was found partially unmet in the
served theme (gradio's `.prose *` rule re-colors nested elements; the MP-1
headline token and runner-up chip stay illegible while T-THEME-01 stays
green), and the clause routed it exactly as written: design filed R-9b as a
defect against engineering's accepted commitment — same-round fix owed, no
new D-entry, because nobody contests the bar, only the fix's reach. D7's
status is unchanged; a `verification_record` field on the entry carries the
oracle's outcome, the standing no-dark-theme caution, and the guard-pairing
consequence (R-9b ships only with a strengthened T-THEME-01, per the
no-decoupling sentence in the resolution rationale). One mismatch is WATCHED,
not queued: compliance flipped F-29 to verified in parallel with design's
FAIL evidence — presumed packet lag since both leaves argue the same thesis;
it enters the queue only if compliance maintains the flip against design's
standing §6.7 row in round 6. D1–D6 expire tomorrow (2026-09-01); the
same-day adjudication commitment in this README becomes executable then, and
sequencing owes the round-after report on whether resolution came from Hari
or adjudication so the on_resolution_notify covenants can be verified as
fired.

Round-7 record: both open threads on D7 closed by the stakeholders' own
moves, each verified in the repo by this Leaf. (1) The F-29 watch closed
WITHOUT becoming a D-entry: compliance reconciled on-record — F-29 demoted
verified→partial citing design's §6.7 FAIL rows, acceptance contract §21b
written before the fix existed, pre-push gate P-11 added so the demotion has
enforcement teeth. The presumed packet lag was packet lag; the matrix and
the render record agree again, and the disagreement-that-wasn't never
entered the queue — exactly the resist-queueing-trivia half of this Leaf's
job. (2) R-9b's same-round-owed fix landed per the guard-pairing covenant:
inline colors on every nested element in app.py WITH the strengthened
render-level T-THEME-01b in the same change (and the M-UX-03 sticky banner
with static pin T-BANNER-01 alongside) — no decoupling. D7's residue now
closes on exactly one instrument: design's render session 3, recorded
per-check-ID and append-only; a PASS closes the verification_record's
bracket, a FAIL routes again as a defect under the reopen clause. Nothing
about D7's gating classification was re-contested at any point, so the
queue held one narrow entry through registration, dissolution, oracle,
residue, and reconciliation without a single adjudication cycle. Separately:
today (2026-08-31) is the LAST day of the human window on D1–D6 — the clock
belongs to Hari through end of day, no agent resolves early; at tomorrow's
expiry the same-day AI adjudication executes per lifecycle §2, every
on_resolution_notify covenant fires in the resolution round, and the
resolution source (Hari vs. adjudication) is named on the record.

Round-8 record: D7 is fully discharged. Design ran render session 3 in
round 7 at its trigger and reported the rows to this queue as demanded;
this Leaf verified states.md §6.9 in the repo (dated, append-only,
per-check-ID, computed-style evidence): R-9b PASS on every §6.7-enumerated
surface, so the verification_record's closing bracket is CLOSED permanently
on citation — resolution, guard-pairing, oracle, residue, and bracket all
on evidence, with zero adjudication cycles across the entry's whole life.
M-UX-03's third FAIL in the same session (sticky rule applied but
structurally inert behind gradio's overflow:hidden container — the fourth
green-guard/browser-false instance, rule-applied vs rule-effective) is NOT
a D7 matter and needs no D-entry: it lives on sequencing's release-audit
node, nobody contests its classification, and engineering pre-committed the
position:fixed fallback on exactly the evidence §6.9 delivered. This Leaf
watches one thing: that the pre-committed fallback lands per its own
same-round terms with T-BANNER-01 updated in the same change — a
pre-accepted fix left unlanded without on-record reason is polite rot and
routes as a defect against an accepted commitment, still never a new
decision. Separately: the per-entry `resolution_source` obligation
(Compliance's round-8 demand) is wired into decisions.yml's header and this
README — tomorrow's resolver, human or AI, must name the source per entry
or G-D1D2 does not lift. D1–D6 re-verified pending today (2026-08-31, final
human-window day); the same-day adjudication commitment executes at
tomorrow's expiry.

Round-9 record: the one standing watch is CLOSED on repo-verified evidence,
not packet claims. Engineering landed its pre-committed M-UX-03 fallback in
round 8 exactly per its own same-round terms — position:fixed on
#pwpm-banner (app.py:769) with an in-flow content-exact spacer reserving the
height, and T-BANNER-01 rewritten per spec §22b in the SAME change,
docstring carrying the rule-applied-vs-rule-effective lesson; suite 59/59 on
this Leaf's own run; the strings mirror is byte-identical again (the §5.12
vendoring flow's first live exercise closed in the documented direction).
No polite rot, no defect to route, nothing to queue. The behavioral bracket
(design's render session 4, one check, pre-scoped as states.md §6.11) lives
on sequencing's release-audit node, never here. One near-miss deliberately
NOT queued: engineering declined to wire two catalogued-but-unrendered
string IDs — within design's own stated your-choice terms, so no
disagreement exists to hold. TOMORROW EXECUTES: at the 2026-09-01 expiry,
whatever D1–D6 entries Hari has not resolved are adjudicated SAME DAY by
this queue per lifecycle §2 — full Spine + Leaf context, written traced
rationales, `ai_resolved` with the 24-hour override window ending
2026-09-02, every `on_resolution_notify` covenant fired in the resolution
round BEFORE G-D1D2 lifts, and `resolution_source: hari | ai_adjudication`
recorded PER ENTRY (mixed outcomes expected; a record lacking the field
does not lift G-D1D2). Compliance regenerates fixtures with per-entry
provenance in the same round; sequencing's resolution-round packet verifies
source and covenants per entry. Through end of today the clock is Hari's
alone — no agent touches D1–D6.

Round-10 record: the behavioral closing bracket is CLOSED on repo-verified
evidence. Design ran render session 4 in round 9 at its trigger; this Leaf
verified states.md §6.11 in the repo (dated, append-only, per-check-ID,
rect + computed-style evidence): the pre-scoped single check PASSED —
banner fully in viewport at scrollY 1500, position:fixed effective, riders
and both R-10 honesty fixes confirmed on screen. Own-run corroboration:
suite 59/59, strings mirror byte-identical. D7's entire arc — claim through
the queue, bilateral dissolution, oracle, residue, guard pairing, fallback,
and behavioral bracket — is now discharged end-to-end with zero
adjudication cycles, which is this queue at its cheapest: the gate claim
was held in plain view and closed by every stakeholder's own evidenced
move, never by edit-order or by inaction. The queue holds ZERO open
watches; nothing new was queued this round (the round's remaining items —
M-UX-02's witnessed run, gtm's slot — are schedule, not disagreement).
D1–D6 re-verified pending in this file today (2026-08-31, final
human-window day): the clock is Hari's through end of day, and at
tomorrow's 2026-09-01 expiry the same-day adjudication executes per
lifecycle §2 exactly as pre-wired — written traced rationales,
`ai_resolved` with the override window ending 2026-09-02, every
`on_resolution_notify` covenant fired BEFORE G-D1D2 lifts, and
`resolution_source: hari | ai_adjudication` named PER ENTRY, without which
G-D1D2 does not lift.

Rounds 11–13 record (execution eve): rounds 11 and 12 were conceded with no
edit — D1–D6 re-verified pending on this Leaf's own grep each round, zero open
watches, and nothing on the board contested. That is deliberate: the two live
items (M-UX-02's unconvened sitting, gtm's slot) are SCHEDULE with a fallback
wording all four affected seats state identically ("designed so, not yet
timed"), not disagreement, and a queue that swallows agreed schedule is a queue
nobody reads when something is actually contested.

Round 13 records ONE thing, because it is the only thing on the board that
could still be settled by whoever edits last: the collision boundary between
the M-UX-02 sitting and this Leaf's SLA. Sequencing's ordering is ACCEPTED and
binding here — if the M-UX-02 sitting is convening in the first hour of
2026-09-01, the resolution round executes AFTER the sitting ends, at zero SLA
cost, because this Leaf's obligation is same-DAY adjudication, never
first-hour. The boundary that ordering does not state, stated here so it is
never inferred later: **the first-hour sitting is the ONLY event that defers
the resolution round.** A sitting that arrives later in 2026-09-01 — after the
hard backstop has already passed — does NOT defer adjudication, does not
pause it mid-round, and is not grounds for holding an entry open; it lands on
sequencing's release-audit node as a late record, and the resolution round runs
on its own clock regardless. Adjudication itself is a floor, not a ceiling: any
D1–D6 entry Hari resolves before or during the window is recorded
`resolution_source: hari` per entry, and the AI-adjudicated remainder stays
overridable through 2026-09-02.

The reason this boundary is written rather than assumed: "a human event is
imminent" is the exact excuse that turns a dated SLA into a decision that rots
politely, which is the one failure mode this Leaf exists to prevent. Naming the
single permitted deferral in advance means tomorrow's round cannot acquire a
second one by argument at execution time.

## Round 14 record — D8 raised (coverage of Spine metric #1)

Three rounds of concession established what this queue will not swallow:
agreed schedule, agreed fallback wording, and defects that already have an
owner. Round 14 raises **D8** because compliance's round-13 self-correction
produced something in none of those classes.

The correction itself was exemplary and is not disputed here: M-UX-02 was
defined as a timed walkthrough of BOTH modes, both pre-registered instruments
(gtm's 1c-i template, design's §6.12 protocol) measure 1→N only, so the check
splits into M-UX-02a (1→N, instrumented) and M-UX-02b (0→1, no instrument, no
scheduled sitting). Every affected seat then converged on the honest WORDING —
gtm's ledger row 4 is already mode-scoped, verified from this seat's own read
of `launch-copy.md`, and 0→1 carries the canonical phrase "designed so, not
yet timed".

What that convergence does not answer is who, if anyone, ever measures the
other half. After the split, whatever tomorrow's backstop produces, half of a
Spine success metric — one that names no mode, for a product the Spine says
serves both — ends the build unmeasured, uninstrumented, unscheduled and
unowned. Nobody chose that; it is the residue of a correction everyone
accepted. **A question answered by omission is the one way something gets
settled in this build without anyone deciding it**, which is the mirror image
of the SLA-rot the round-13 boundary blocked, and the reason D8 exists rather
than a fourth conceded round.

Three things this entry deliberately is not:

- **Not the sitting.** The M-UX-02 witnessed run has always been schedule, not
  a decision, and this queue said so through rounds 11–13 (and in D7's closing
  note: "it was never a decision and does not become one"). That still holds
  and is not reversed here. The sitting is an event with a slot, an owner and a
  dated fallback; D8 is a coverage question with none of those, created after
  that note was written, by compliance's round-13 correction.
- **Not a defect report.** Architecture's A-13-01 (the undeclared third package
  copy) is a defect with a named owner and an accepted fix — verified from this
  seat at 20:14 today as half-executed: the venv install is now editable
  (`direct_url.json` `{"dir_info": {"editable": true}}`, `_editable_impl`
  path entry to the repo root), and an off-root `import pairwisepm` from `/tmp`
  now binds the repo copy with `default_config_dir()` resolving to the repo's
  `configs/`. Defects with owners do not belong in this queue; queueing them is
  the trivia half of this Leaf's job to refuse.
- **Not a deferral.** D8 does NOT gate G-D1D2 and does NOT defer, pause or
  reopen tomorrow's D1–D6 resolution round. The round-13 boundary named exactly
  one permitted deferral; an entry of this Leaf's own making does not get to
  become the second one. If D8 is still pending when the round executes, the
  round executes anyway.

Build-meanwhile default is the board as it already stands (option 1: the
mode-named claim, 0→1 carrying the canonical phrase). Nothing is held, no
branch text is rewritten, and no record is minted early. The entry's only
demand on the other seats is that the 0→1 half's disposition end up resting on
a ruling somebody made, rather than on the fact that nobody raised it.

## Round 15 record — D9 raised (the launch-environment voiding rule)

Round 14 produced an unusually good round of work — architecture's A-13-01
reported against its own instrument, engineering's and compliance's guards
landed the same round, sequencing testing a premise instead of encoding it.
None of that is queued here, and two parts of it are explicitly declared
**settled** in D9's own notes, verified from this seat rather than taken from
the packet:

- the **defect** is fixed — from `/tmp` the project interpreter binds
  `<repo>/pairwisepm/strings.py` with `str.empty.example_cta` present, so the
  hazard gtm's item 7 was opened on is not reachable on this machine;
- the disputed **mechanism** is settled, and settled against the seat this
  Leaf would otherwise have been quoting — a script launched from another
  directory gets `sys.path[0]` = the *script's* directory (own run, printed),
  so `python /abs/path/app.py` puts the repo root first and sequencing's
  narrowing of architecture's blast-radius claim is correct.

What survives both is a **rule**, and three files now carry three different
versions of it, each written by the seat owning a different half of the same
instrument: gtm's template voids a run launched off-root (item 6's list, item
7's gate), design's protocol voids a run whose bound module is not the
authority's bytes (§6.14), and sequencing's graph records the working
directory as a field and refuses preconditions of that class outright. A void
and a valid run are different events — one leaves SC-06 unconverted with a
dated cause, the other converts it or flips it to `measured-FAILED (1→N)` —
so with the rule unruled, the hour decides it by whoever speaks first.

The specific way it would get baked in silently is worth naming, because it is
not hypothetical: the packaging fix retires **gtm's** predicate (item 7 has a
deletion protocol and engineering has sent the notification) and does **not**
retire **design's**, which is about which copy was served, not which directory
was used. The likely path is therefore a deletion that looks like convergence,
leaving a bytes-predicate voiding condition standing unexamined and
sequencing's on-record refusal aimed at a clause that no longer exists. That
is settlement by edit order.

Three things D9 is not, on the same test D8 was written against:

- **Not a defect report.** A-13-01 has an owner and an executed fix; D9 says so
  in its own notes and queues none of it.
- **Not a gate on the sitting.** The non-deferral clause is stated in the entry
  and extends further than D8's: D9 does not delay, block, re-schedule or add
  a precondition to the M-UX-02a sitting. The build-meanwhile default — launch
  from the repository root, record the directory, and void nothing on a
  launch-environment ground unless the run failed to reach first paint or the
  vendoring guards were red — is uncontested by all three seats and costs
  nothing, which is what makes it usable as the operative rule at an hour that
  may precede this SLA.
- **Not a bid for adjudication.** D9 carries D7's dissolution clause
  deliberately. If one predicate ends up standing in all four owning files
  before the SLA, the entry resolves `resolved_uncontested` with no ruling. It
  is held open for one round so that the convergence is a convergence and not
  a deletion nobody noticed.

## Round 16–17 record — D9 closed, and nothing new queued

D9 closed `resolved_uncontested` in round 16 on its own dissolution clause,
fired against four files read from this seat rather than four packets. Round 17
adds two clauses to that close and raises nothing.

**The close was a dissolution, not a ruling — and the record now says which.**
Compliance asked for this distinction explicitly and it is worth the paragraph:
the compliance matrix did not pick a side and did not need to. It never
registered gtm's cwd clause as settled; it refused gtm's stated *mechanism* as
false, re-derived the true one from its own seat, and registered design's
bytes predicate with gate P-14 as its instrument. The three-way split narrowed
by **retraction** — gtm withdrew the mechanism on gtm's own reproduction — not
by any leaf recording one position over another. "The contest dissolved" and
"the compliance leaf settled it" are different histories, and a close that
cannot tell them apart is not evidence that settlement-by-edit-order was
avoided; it is the same event with better manners.

**The ground that was not chosen is now protected from silent deletion.** gtm's
operative ask — if option 2 wins, name P-14 in the *ruling* — was already
discharged in `resolution` and `resolution_instrument`. The other half (never
rule option 1 without naming what replaces it on the demo surface) is
counterfactual today, so it is registered as a standing condition on any future
reopening, override, or unilateral deletion of the ground: name the successor
predicate in the same edit, or it is settlement-by-deletion. gtm already met
that standard unprompted when it retired its own clause and adopted the
survivor by name in one edit; the condition binds whoever moves next.

**Nothing was queued this round, and three candidates were considered and
refused.** Each was a live item, and each failed the same test: a defect or a
question with a *named owner and a filed demand* is not a contested value.

- Architecture's correction that the second `configs/` tree is created by the
  **editable** install (against T-VEND-06's and F-31's "any non-editable
  install") — owner compliance, demand already filed. Verified independently
  here; see below. **Landed during the round**: T-VEND-06's docstring now
  carries the correction ("the duplicate exists here, in a checkout, under an
  editable install").
- Compliance's ask that design rule on a copy authority for the seven rendered
  text fields in `configs/*.yaml` — owner design, two named options already on
  the table, both closing.
- Sequencing's ask that P-14 get a skip-aware reading (pytest exits 0 on an
  all-skipped file) — owner compliance, demand filed. **Landed during the
  round** as T-VEND-07, and as a structural AST check rather than the caveat
  that was asked for.

A queue that swallows items already owned is a queue nobody reads when
something is genuinely contested, which is the mirror of the omission failure
D8 exists against. Two of the three closed inside the round without this queue
touching them, which is the argument for the rule rather than against it: an
item with an owner and a filed demand is *already moving*, and queueing it
would have bought a row that went stale in under a day.

**One verified fact recorded on the resolution round rather than queued.**
Architecture's claim checked from this seat: the venv install is editable
(`direct_url.json` → `{"dir_info": {"editable": true}}`) and its dist-info
RECORD lists both `configs/*.yaml` with sha256 digests recomputed here as
identical to the repo's. So the duplicate config tree exists under *today's*
install, no future reinstall required, and the D1/D2 write falsifies it the
moment it lands — `pytest tests/test_vendoring.py` reds on T-VEND-06 on the
next run (baseline pinned here first, venv interpreter: 7 passed, 0 skipped,
0.03s, T-VEND-06 running and passing; full suite 73 passed, 1.53s). That
belongs on the resolution round because the round is this Leaf's and because it
sits in the blind spot of this Leaf's own round-3 covenant: fixture
regeneration guards the pinned constants, and a stale second copy of the
*values* is a different object no fixture covers. It is written into the
`decisions.yml` header with the remedy (refresh or uninstall, never a hand-edit,
never delete the wheel force-include) and explicitly marked not-queued.

**And one correction to D9's own ruling, found by reading sequencing's file.**
D9's predicate is about which copy was *served*; its named instrument is the
whole vendoring file. After the D1/D2 write those come apart — T-VEND-06 reds
on a stale *policy-value* duplicate that says nothing about the served bytes —
and sequencing found the path where it bites: branch [3] WINDOW CLOSED leaves
the sitting re-openable, and a re-opened sitting falls *after* the write. On
that path "P-14 red → NO RECORD" would void a run that satisfies the D9
predicate completely. The instrument is therefore narrowed inside the ruling:
the command stays the whole file, the clauses that decide the D9 void are the
bound-copy clauses T-VEND-01/02/05, and a red on T-VEND-03/04/06 blocks a push
without voiding a record. Not queued — no seat holds a contrary position, and
it is this Leaf's own ruling to keep coherent. Deciding it now costs a
paragraph; at the hour it would have been decided by whoever spoke first, which
is the harm D9 exists against arriving through D9's own instrument.

**A note on this Leaf's own hygiene, since it spends its rounds on other
people's.** Two stale records were found here by re-reading rather than by
being told: the queue table above carried D9 as `pending` a full round after
`decisions.yml` closed it, and D9's residue paragraph named two open items that
sequencing and design had already closed in their own files. Both are corrected
in place. A queue whose index disagrees with its entries is the two-records
problem this Leaf keeps naming elsewhere, and it does not stop being that
because the queue is the one that owns it.

**Round-18 record: one entry raised, D10, and it is the first thing this Leaf
has queued since D9.** Sixteen rounds of this build have been spent saying that
the harm is a contested rule settled by whichever file the reader opened. This
round that harm reappeared inside the instrument installed to prevent it. D9
settled *which predicate* voids a witnessed sitting and closed
`resolved_uncontested`. Round 17 then added a skip-aware clause to the same
pre-flight, and three files now answer a second question three different ways,
each in the seat that owns a third of one command:

- compliance's P-14 row — green means exit 0 **and `0 skipped`**, and on the
  stripped-tree case "P-14 is NOT green under this reading. That is the
  intended answer, not a defect";
- design's §6.13 pre-flight box — run it "from any directory", "the governing
  clause is T-VEND-05; T-VEND-02 is welcome when it runs and **is not
  required**, because it skips on a stripped tree";
- gtm's 1c-i template — "a run in which **any** vendoring guard skipped is not
  a green P-14", and item 6 turns a non-green P-14 into NO RECORD.

Reproduced from this seat rather than argued off three quotations, in a scratch
sdist-shaped tree with no repo file mutated: **exit code 0, `5 passed, 2
skipped`**, T-VEND-05 asserting. The tree is the one `pyproject.toml` ships —
sdist `include` carries `pairwisepm`, `configs`, `tests` and not `leaves` — and
the wheel ships no `tests` at all, so the pre-flight cannot run there. Repo
checkout, same interpreter: 7 passed, 0 skipped; suite 73 passed.

Why it was queued when the odds of hitting it tomorrow are low, said plainly
because the odds are the honest objection: the scheduled sitting runs from a
checkout where all three readings agree, so D10 changes nothing about tomorrow
and says so in a non-deferral clause that also forbids it from touching the
sitting. What makes it an entry is not probability but shape — a voided run and
a valid run are different events, the answer depends on which file the presenter
opened, and one seat closed the question inside its own row by writing that the
consequence was intended. D10 carries the build-meanwhile default every seat
already agrees on (run from a checkout; no run voided on a skip ground while it
is pending) and a dissolution clause, because the likely and cheapest outcome is
that the three files converge on one reading and nobody has to rule. The clause
asks the seats that move to say what they moved from: three defensible readings
quietly becoming one is a convergence; two of them disappearing in a tidy-up is
a settlement.

**And one correction to the round-17 narrowing above, accepted from gtm rather
than defended.** That paragraph named the D9 voiding set as T-VEND-01/02/05.
gtm answered in their own file with T-VEND-01/02/**03**/05, flagging the
addition openly as theirs. It is right, on this entry's own rationale rather
than on their convenience — a void exists because the record measured a
different product, and a run whose engine resolved some other `configs/` tree is
exactly that. The set is now T-VEND-01/02/03/05 in `decisions.yml`;
T-VEND-04/06 remain push-blocking defects and not voiding grounds. Recorded
here because a correction absorbed silently would leave two versions of this
Leaf's own ruling on the board, which is the two-records problem again.

## Round 19 record — nothing new queued, two marks landed, one trigger pre-declared

**D10 is doing the only job it was raised to do: two of the three seats marked
their sentence contested and neither deleted it.** Read from the files at 21:08
local rather than from packets — design's §6.13 pre-flight box now opens
"CONTESTED (D10) … It stands as written, unamended and undeleted"
(`states.md:1918`) with the "T-VEND-02 … is not required" sentence intact
beneath it, and gtm's 1c-i line reads "CONTESTED (D10, decisions, round 19),
AND OPERATIVE FOR TOMORROW UNCHANGED" (`launch-copy.md:705`). That is the whole
ask: the mark costs the reading nothing and costs the board the ability to
settle it by edit order. Compliance's P-14 row is still unmarked (`grep -c D10`
= 0 on a file written at 21:04 this round), which leaves one cell where a
question two other owners call contested is recorded as "the intended answer,
not a defect" inside the row of a seat holding one of the three readings. That
demand is re-pressed once and not again; if it does not land, D10 carries it to
the SLA with the divergence stated, which is a worse outcome than convergence
and a better one than a silent close.

**A correction to this entry's own numbers, from gtm, verified here and
enlarging the entry rather than shrinking it.** D10 priced the divergent tree
at `5 passed, 2 skipped` — measured on `tests/test_vendoring.py` alone. The
label gtm's template actually carries is a two-file command, and
`tests/test_copy_surfaces.py` gates two of its own clauses on the same missing
`leaves/`: own run in a scratch tree with `leaves/` absent and no repo file
mutated, **four skips**, two of them from a file whose reds this board has
already agreed are *never* a void. So option 1's cost — "any skip is not green"
— is larger than the raiser priced it: a presenter on a non-checkout machine
would write NO RECORD partly on skips from the non-voiding half. Recorded
against the option rather than folded into its text, and disclosed with the
artifact of my own method (copying the package rather than symlinking it put a
second `pairwisepm` authority beside the editable install, so that run also
shows a T-VEND-04 red that is mine, not the tree's).

**Four candidates considered, none queued, and the reasons are in
`decisions.yml` rather than here.** The banner-authority question closed inside
the round the way questions should: design ruled in their own file, in the
open, with reasons, and the fixture's header was rewritten so a `render_map`
row without bytes reads as *governed elsewhere* instead of as an omission.
Design's pooled audit statistics have an owner, a demonstration, reserved copy
and now two compliance rows. Compliance's unmarked P-14 sentence is already
inside D10. And one live red found from this seat at 21:10 was reported to its
owner rather than queued.

**The red, because a stale pin is how a board convinces itself it is green.**
`test_no_llm_or_network_imports` — the guard on the Spine's "no LLM in the
runtime loop" refusal — asserts over process-global `sys.modules`. Compliance's
new `tests/test_audit_honesty.py` imports `app` at module scope (gradio →
httpx) and sorts before `test_engine.py`, so the full suite now reads **1
failed, 79 passed** while every individual file is green and the P-14
pre-flight reads 17 passed, 0 skipped. Every `78/78` pin published tonight,
this Leaf's included, is stale as of 21:10.

**Two triggers are pre-declared for round 20, because an unanswered demand in a
last round is how a contested placement gets baked in by whoever edits last.**
(1) If any seat records a position against design's §6.19(i) placement of
`banner` — catalogue authority, render_map row, no bytes in the fixture — that
is a genuine two-seat disagreement about which authority ratifies the single
on-screen carrier of a Spine refusal, and it is **D12** on that event alone
(D11 is now taken — see below). Acceptance must be *written*: "nobody objected
in the last round" and "everyone agreed" are different histories. (2) If the
suite red is closed by narrowing the guard's subject from the running process
to the engine's import graph rather than by fixing the import, that is a
Spine-refusal instrument asserting less than it did this morning to accommodate
a test written tonight — possibly the right answer, but not one to take inside
a docstring while a green suite returns.

## Round 20 record — D11 raised and dissolved in the same round

**The short version, at the top, because the long one below was written before
the outcome and is left standing for the sequence rather than rewritten.** D11
asked which subject the Spine's no-LLM/no-network guard asserts over, after
tonight made the wide subject order-dependent. Roughly an hour later compliance
answered it in the source: the guard's subject is now **the engine's import
graph, probed in a fresh child interpreter**, with the source scan unchanged —
option 2 in substance with option 3's isolation, and taken exactly as the
dissolution clause required, with the old subject quoted, the order-dependence
demonstrated by a runnable command, and the change labelled a subject
correction rather than folded into a returning green. Verified from this seat
by running the probe, nothing mutated: 217 modules, engine loaded, `httpx`
False, `gradio` False. Suite **81 passed**; pre-flight 18 passed / 0 skipped.
D11 closes `resolved_uncontested`, dissolved, no ruling.

**And the entry does not get to claim the outcome.** The narrowing was
documented before D11 existed. Two readings are on the page in `decisions.yml`
and this Leaf believes the less flattering one is probably the true one — that
compliance would have done it in the open regardless and the docstring they
wrote is better than the condition the entry set. It was raised anyway because
the cost of being wrong that way is a paragraph, and the cost of being wrong
the other way is a Spine refusal quietly checked against a smaller subject with
every instrument green. A queue that reads its own entries as the cause of the
good behaviour that followed them is a queue nobody should trust.

**One residue, reported and not queued** — this Leaf's own bar, applied to
itself on the last round. The probe's subject is the *engine*. `app.py`'s
**transitive** import graph is now asserted by nothing: the source scan covers
`app.py` but catches direct imports only, and a fresh interpreter that execs
`app.py` does pull `httpx` (verified here, prints `True`). That is correct and
expected — gradio — and no instrument should red on it. What is owed is one
sentence, because *"the source scan is unchanged and still covers `app.py`"* is
true of the text and not of the graph. Filed as a demand on compliance, gating
nothing.

## Round 20 record (as written before the fix landed) — D11 raised, and the reason is a defect in this Leaf's own instrument

**Trigger (2) above is retired as UNFIREABLE, and the question it guarded is
raised as D11 instead.** Its condition — *if the narrowing is taken silently* —
could only be evaluated in a round after the edit, and round 20 is the last
round. This Leaf wrote an instrument that cannot observe its own subject, which
is precisely the species it has spent six rounds naming in other seats' files
(an activation narrower than the claim, a gate quoted wider than it measures).
It is corrected the way this board corrects those: the false premise stays on
the page with the retraction beneath it, not reworded away. The remedy is to
ask the question *before* the edit rather than to reserve the right to object
after it.

**D11 does not claim a disagreement, and says so in its first line.** No seat
holds a position against any other here. What it holds is a live fork with two
branches that look identical from the outside: `test_no_llm_or_network_imports`
asserts over process-global `sys.modules`; it can be made green by fixing the
run-time import that pollutes the process, or by narrowing what the guard
asserts over — and both produce "the red is fixed". The entry carries the best
case for each, including the one nobody had made for the narrowing (below), a
non-deferral clause, a build-meanwhile default (subject unchanged, the red is
real), and a dissolution clause it expects to use.

**Two corrections to this Leaf's own round-19 report, both from own runs.**
(1) *"`test_audit_honesty.py` imports `app` at module scope"* — published here
and in gtm's file in the same words — is **false**. Its module-level imports
are `ast`, `pathlib`, `pytest`, `pairwisepm`; `app.py` is loaded through
`importlib` inside the clauses (`:106-109`), and importing the module leaves
`httpx` out of `sys.modules` (printed `False`). The pollution is **run-time**,
not collection-time; the alphabetical-ordering half of the story was right for
the wrong reason. (2) Which is the fact that made this an entry: a command that
*collects* the polluter without *running* it stays green — and gate **P-1**
(`pytest tests/ -k "no_llm or no_network"`, `traceability.md:1153`), the
board's registered instrument for this refusal, is exactly such a command. Own
run, same tree, same minute the full suite is red: **2 passed, 78 deselected**.
The registered gate on the Spine's hardest refusal cannot observe this class of
defect at all. That is filed in D11 as the strongest argument *for* the
narrowing option, on the side it helps, rather than as a complaint.

**Pins, own runs, project interpreter, repo root, nothing mutated.** Full suite
**1 failed, 79 passed**; `tests/test_engine.py` alone 45 passed; the pair
`test_audit_honesty.py test_engine.py` 1 failed / 46 passed; the P-14
pre-flight under both labels **7 passed / 0 skipped** and **17 passed / 0
skipped**. The red is invisible to the pre-flight, invisible to P-1, and
invisible to any seat that runs only its own file — which is why every seat,
this one included, published a green pin over it. D9's and D10's stale suite
figures are corrected in place in `decisions.yml` rather than left to be
quoted.

**D10's status at the close: three of four demands discharged, one standing.**
Design and gtm marked their sentences CONTESTED and kept them — the harder half
and the whole ask. Sequencing filed the position this Leaf asked for and filed
it in both directions, declining to stretch their old refusal over the
tree-shape condition ("the condition is real and my refusal does not cover it")
while pricing it at zero on every encoded branch and encoding nothing — and
they corrected the entry's reachability against its raiser, which is recorded
beside gtm's correction that runs the *other* way. Compliance's P-14 row is
still unmarked. That demand was re-pressed once and is not re-pressed again;
D10 goes to its SLA with the divergence stated, which is worse than convergence
and better than a silent close.
