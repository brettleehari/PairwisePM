# PairwisePM — Interaction-State Catalogue & Trust Signals

leaf: design
derives_from: spine/SPINE.md (wins every conflict) · docs/technical-spec.md (locked contract)
status: finished halfway-draft for expert refinement
copy_convention: every user-visible string in this document is **exact copy**, given in
`code spans` or block quotes, with a stable string ID (`str.*`) so engineering can key
the UI off this file. Anything not in a code span or block quote is design annotation,
not copy.

---

## 0. Design doctrine — why trust signals ARE the honesty rules

The Spine's hardest commitment: *"A judge that overstates its confidence is worse than
no judge."* In an ordinary product, trust signals are decoration — badges, testimonials,
polish. In PairwisePM the trust signals are the **honesty rules of spec §4 made
visible**: the interval welded to every probability, the refusal to force a winner,
the permanent 0→1 banner, the order-bias confession, the M0-vs-M1 disagreement shown
rather than hidden. Every state below is therefore specified twice: what it looks like,
and which honesty rule it is enforcing.

Four global laws that no state may violate:

1. **No naked probabilities.** A win probability never renders without its interval,
   in the same visual token (MP-1). If the interval is not computable, the probability
   is not shown either.
2. **No rejected ideas.** The losing idea is never labeled rejected, killed, or losing
   as an identity — it is the runner-up *in this comparison*, always shown with its
   path to parity or the honest statement that no lever-path exists (MP-2).
3. **The math and the judgment never share a container.** Mechanical factors and
   evaluative overrides are visually separate regions with different backgrounds,
   borders, and vocabulary (S13). Nothing evaluative ever appears inside a score,
   a bar chart, or a probability.
4. **Modesty in the verbs.** The tool "computes", "applies your policy", "flags",
   "routes". It never "recommends", "believes", "knows", or "predicts" — except in
   1→N mode where calibration is earned, and even there only "estimates".

Vocabulary register: plain PM English, short declaratives, no statistics jargon in
primary copy. Statistical terms (ζ, Brier, intercept) appear only in the audit view,
each with a one-line plain gloss beside it. The user "is not a statistician and should
never need to be" (Spine).

---

## 1. Screen anatomy (reference for the states)

One screen, one sitting (spec §1). Top-to-bottom regions:

- **R1 — Mode toggle**: `1→N · Allocation` | `0→1 · Search`, with the mode banner slot
  directly beneath (permanent banner in 0→1, S8).
- **R2 — Idea headers**: two columns, `Idea A` and `Idea B`, each a name field.
  (v1 as-built ratified round 6, §6.8 R-10(iii): the one-line description field is
  post-pilot backlog — the log schema's description stays optional and empty until
  it ships.) A small `⇄ Swap A/B` control sits between them (feeds the order-bias
  hygiene habit, S7).
- **R3 — Factor questionnaire**: the mode's mechanical factors as rows, one input per
  idea per factor, each row carrying its lever/fact chip (MP-3) and an inline `why?`
  disclosure showing the factor's written rationale and prior weight from config.
- **R4 — Evaluative panel**: visually separate container (S13). Strategic fit, brand,
  free-text judgment. In 0→1 mode the Ceiling flag lives here too — it is unweighted
  and routes, never scores (S5).
- **R5 — Verdict card**: empty scaffold until computation unlocks; then one of S3, S4,
  S5. Hosts the M0/M1 disagreement strip (S6) and fragility flag when triggered.
- **R6 — Leverage panel**: signed contribution bars, path to parity, lever/fact filter
  (spec §5). Renders only alongside a verdict. Always carries a **provenance chip**
  naming which regime produced the bars (architecture invariant: the panel uses the
  active model's weights and must say so):
  - `str.leverage.provenance_m0` — > weights: M0 — your stated prior policy
  - `str.leverage.provenance_m1` (template) — > weights: M1 — revealed by your 14
    logged picks, shrunk toward your stated policy
- **R7 — Log & audit strip**: log status (S10), model-of-the-judge progress (S9),
  ζ + Brier meters, order-bias diagnostic when triggered (S7), download/upload controls.

---

## 2. State catalogue

Each state: **Trigger → Visual → Exact copy → Exits → Honesty rule enforced.**

---

### S1 · Empty state

**Trigger.** Fresh load, no log uploaded, no fields filled.

**Visual.** Questionnaire fully visible (never hidden behind a wizard — the "one
sitting" promise is made by showing the whole job up front). Verdict card R5 renders
as a dashed-outline placeholder, deliberately modest — no grayed-out fake verdict.
Mode defaults to `1→N · Allocation` (the mode with earned accuracy claims; 0→1 is an
explicit choice, so its no-accuracy banner is always a chosen context, never a default
surprise).

**Copy.**

- `str.empty.headline` —
  > Two ideas. One questionnaire. One sitting.
- `str.empty.sub` —
  > Score both ideas together, on this screen, now. Scoring them on different days adds
  > noise the math can't remove; scoring them side by side cancels it.
- `str.empty.verdict_placeholder` (inside the dashed verdict card) —
  > The verdict appears when every factor is scored for both ideas. It will be a win
  > probability with an interval — never a bare number.
- `str.empty.privacy` (small print, R7) —
  > Runs entirely in this app. No API key, no server, nothing stored anywhere but your
  > own log file.
- `str.empty.example_cta` (button beneath the idea headers; catalogued round 6 per
  §6.4 R-10(iv) — the control already exists as-built and is the demo path) —
  > Load example (canonical seeded pair)

**Exits.** Any keystroke in R2/R3 → S2. Log upload → S10c (then S2 with progress
counter updated).

**Honesty rule.** Occasion-noise cancellation (spec §1) is stated as the *reason* for
the one-sitting design, not as a rule imposed on the user. The placeholder pre-commits
to the interval before the user has seen a single number (law 1).

---

### S2 · Partially-filled

**Trigger.** At least one field filled; not all computation-blocking fields filled.

**Blocking rule (exact).** Computation requires **every mechanical factor in R3, for
both ideas** — 7 factors × 2 ideas in 1→N, 6 factors × 2 ideas in 0→1 (Ceiling flag
excluded; it is unweighted). Non-blocking: idea names (default to `Idea A` / `Idea B`
in the log), descriptions, all of R4 (evaluative inputs, Ceiling flag), override
rationale. A skipped factor is never defaulted: a silent default of "average" (z = 0)
would be the tool guessing, and the tool never guesses.

**Visual.** Per-column progress counters under each idea header. Unfilled blocking
rows carry a quiet left-edge marker (not red — nothing is *wrong* yet). The verdict
placeholder updates to enumerate what is missing. No partial or "preview" probability
is ever shown.

**Copy.**

- `str.partial.progress_a` / `str.partial.progress_b` (template) —
  > Idea A — 5 of 7 factors scored
- `str.partial.verdict_placeholder` (template; lists factor names) —
  > 3 factor scores to go before the verdict: Reach (Idea B), Effort (both ideas).
- `str.partial.no_default` (tooltip on any unfilled blocking row, and in the `why?`
  area) —
  > Skipped factors aren't scored as zero — that would quietly mean "exactly average."
  > The verdict waits until you've said what you actually think.
- `str.partial.eval_optional` (R4 header suffix) —
  > optional — never enters the score

**Exits.** Last blocking field filled → compute → S3, S4, or S5. Invalid entry → S11
(row-local). Mode toggle → S12.

**Honesty rule.** No hidden imputation; the mechanical score is built only from
statements the user actually made.

---

### S3 · Computed verdict

**Trigger.** All blocking fields valid; bootstrap interval computed; interval does
**not** straddle 50%; no Ceiling flag set (0→1).

**Visual.** Verdict card fills. Winner's column header gains a subtle accent; loser's
header gains the "runner-up" treatment (MP-2) — same weight, no dimming, no strike.
Probability + interval rendered as one token (MP-1), largest text on the card.
Beneath: model line, mode line, then the leverage panel R6. Log-this-decision action
is primary; override action is secondary but equally discoverable (S13b).

**Copy.**

- `str.verdict.headline` (template) —
  > **Idea A wins this comparison — 68% (55–79%)**
- `str.verdict.prob_gloss` (fixed sub-line, always directly under the headline) —
  > win probability under your policy, with its 90% bootstrap interval
- `str.verdict.model_line_m0` —
  > Computed by M0 — your stated prior weights, applied identically to both ideas.
- `str.verdict.model_line_m1` (once M1 active and agreeing; disagreement is S6) —
  > Computed by M1 — the weights your own logged picks reveal, shrunk toward your
  > stated policy.
- `str.verdict.mode_line_1n` —
  > 1→N allocation verdict. Accuracy is earned: check the Brier meter below to see how
  > this policy has actually done.
- `str.verdict.mode_line_01` — (the permanent S8 banner is already on screen; the card
  repeats the modest register)
  > 0→1 structural verdict — consistency, not prophecy.
- `str.verdict.log_cta` —
  > Log this decision
- `str.verdict.fragility` (template; conditional strip on the card, spec §5.4;
  contains the compliance-pinned phrase verbatim, factor name interpolated) —
  > ⚠ Margin rests on the *Capability feasibility* estimate — re-estimate before
  > committing. One plausible step on that factor alone flips this verdict.
- `str.verdict.audit_footer` (reserved slot, template — per Decisions D4 the audit view
  is on-demand only in v1 and this footer ships EMPTY; the card layout reserves one
  quiet line above the log CTA so D4 options 2/3 can later surface it without redesign) —
  > Your policy so far: ζ 0.86 · Brier 0.19 across 14 decisions — details in audit.
- `str.verdict.ablation_toggle` (audit-view control, spec §3) —
  > Equal-weight check — rerun with all weights equal (signs kept). If the winner
  > changes, your weights are doing the work; if not, the factors are.

**Exits.** `Log this decision` → record appended → S10b, progress counter (S9)
increments. Override path → S13b. Any input edit → card clears back to S2-style
placeholder with `str.verdict.stale`:
> Inputs changed — the verdict above no longer applies. Press Compare to recompute.

(Never leave a stale verdict on screen; a wrong-but-visible number is a confidence
overstatement. Tail revised at the round-8 R-10 mint (§6.8(ii), §6.10): the
as-built flow recomputes only on a manual Compare click, and the stale state
exists precisely to prevent false claims — so it may not make one itself. If
engineering wires auto-recompute, the tail reverts to "Recomputing…" in the
same change as the wiring.)

**Honesty rule.** Interval always welded on (law 1); model provenance named on every
verdict; fragility confessed on the card itself, not buried.

---

### S4 · Too close to call

**Trigger.** Bootstrap interval on the win probability straddles 50% (spec §4).

**Visual.** The verdict card renders in a deliberately *neutral* treatment — neither
column gets the winner accent. No trophy iconography, no tie-breaking. The probability
token is still shown (law 1) but demoted to secondary size beneath the headline. The
leverage panel reframes from "path to parity" to "cheapest evidence" (both ideas get
lever suggestions).

**Copy.**

- `str.tctc.headline` —
  > **Too close to call — gather evidence.**
- `str.tctc.body` (template) —
  > Win probability 56% (44–67%). The interval straddles 50%, so this comparison
  > doesn't separate these ideas — and a forced winner here would be noise wearing a
  > number.
- `str.tctc.next` —
  > The cheapest way to break the tie is below: the lever whose real-world change moves
  > this furthest per unit of effort.
- `str.tctc.log_cta` —
  > Log as too-close-to-call
- `str.tctc.force_note` (beneath an optional "pick anyway" affordance; picking anyway
  is allowed — the PM owns the decision — but it is logged as an override) —
  > You can still pick one — people ship on Tuesdays too. Your pick will be logged as
  > your call, not the model's.

**Exits.** Log → S10b. Editing inputs (after gathering evidence) → S2 → recompute.
Pick-anyway → S13b override flow with pre-filled context `against a too-close-to-call
verdict`.

**Honesty rule.** The core refusal of spec §4: never a forced winner. This state is a
success state, not a failure state — visually calm, forward-pointing, never apologetic.

---

### S5 · High-ceiling routing (0→1 only)

**Trigger.** Ceiling flag set on either idea (0→1 mode). Overrides S3/S4 presentation
for the flagged idea.

**Visual.** The verdict card splits: a routing strip on top (distinct texture — this is
a *routing* message, not a score), the mechanical comparison beneath it, computed as
usual but explicitly labeled as excluding the flag. If both ideas are flagged, the
routing strip covers both and the mechanical verdict is labeled as secondary context.

**Copy.**

- `str.ceiling.strip` (template) —
  > **High-ceiling outlier — portfolio decision, not averaged in.** You flagged
  > *Idea B* as a possible top-box outcome. Averages are exactly what destroy outliers,
  > so this flag never enters the score. Take Idea B to portfolio judgment: what does
  > the portfolio look like if it works?
- `str.ceiling.mech_label` —
  > Mechanical comparison below, ceiling flag excluded — use it as context, not as the
  > decision.
- `str.ceiling.both` (both flagged) —
  > Both ideas are flagged high-ceiling. This pair is a portfolio conversation, not a
  > weighted average. The mechanical comparison below is context only.

  (Rendering note, RESOLVED as-built round 3: the card strip now formats the full
  `str.ceiling.strip` (idea name interpolated) and `str.ceiling.both` when both are
  flagged, with the engine's terse pinned note kept alongside on the card —
  T-CEIL-02 unaffected. Verified in app.py render_verdict, §6.4 R-3.)

**Exits.** Unflag → S3/S4. Log → record carries `ceiling_flag` per spec §6 schema.

**Honesty rule.** Spec §2: "The Ceiling flag never enters the score." The design makes
the exclusion *legible* — the user must see that flagging did not move the number.

---

### S6 · M0-vs-M1 disagreement

**Trigger.** M1 active (≥ ~10 logged decisions) and M0 and M1 disagree on the winner,
or agree but with intervals telling materially different stories (M1's point estimate
outside M0's interval).

**Visual.** A two-row strip on the verdict card, one row per model, identical layout so
the eye does the comparison — each row: model chip, winner, probability + interval
token (MP-1). Neither row is styled as "the real one." A `compare weights` disclosure
opens the divergence view (paired bar chart per factor: stated weight vs revealed
weight).

**Copy.**

- `str.disagree.headline` —
  > **Your stated policy and your revealed policy disagree.**
- `str.disagree.row_m0` (template) —
  > What you *say* you weigh (M0): Idea A — 61% (52–70%)
- `str.disagree.row_m1` (template) —
  > What your last 14 picks *reveal* you weigh (M1): Idea B — 57% (46–68%)
- `str.disagree.body` —
  > Neither is automatically right. Your stated weights are your policy; your revealed
  > weights are your behavior. Open the weight comparison to see which factors drifted —
  > then either update your policy or admit the drift.
- `str.disagree.compare_cta` —
  > Compare weights
- `str.disagree.weights_caption` (in the divergence view) —
  > Revealed weights are shrunk toward your stated policy (ridge, centered on M0), so
  > early differences are real signal, not small-sample noise.
- `str.disagree.log_note` —
  > Whichever you pick, the log records both model outputs.

**Exits.** Pick either side → normal log flow (record carries both M0 and M1 outputs
per spec §6). Weight comparison → audit view.

**Honesty rule.** Spec §3: divergence is *displayed*, never silently resolved. The
tool refuses to pick between the user's mouth and the user's hands.

---

### S7 · Order-bias diagnostic surfaced

**Trigger.** The unconstrained-intercept diagnostic fit (spec §3) finds a significantly
nonzero free intercept over the accumulated log. Surfaces in the audit strip R7, and as
a one-time toast when first crossing significance.

**Visual.** Audit-strip row with a small directional glyph (→A or →B). Never a modal —
this is a mirror, not an alarm. The `⇄ Swap A/B` control in R2 gains a subtle
highlight while the diagnostic is active.

**Copy.**

- `str.orderbias.headline` —
  > **Presentation-order bias measured.**
- `str.orderbias.body` (template) —
  > Across your 23 logged decisions, the idea you entered in slot A wins more often
  > than symmetry allows (free intercept +0.41, beyond noise). Your verdicts are
  > unaffected — scoring forces this term to zero, so swapping A and B flips every
  > probability exactly. But your *raw picks* lean toward whichever idea you typed
  > first.
- `str.orderbias.advice` —
  > Cheap fix: enter the incumbent or your own idea as B sometimes. The ⇄ swap button
  > exists for this.
- `str.orderbias.clear` (when a later fit drops below significance) —
  > Order-bias no longer detectable over your current log. Kept in the audit history.

**Exits.** Persistent audit row until the diagnostic clears; toast dismissible.

**Honesty rule.** The tool confesses a measured bias in its user *and* explains why
its own output is immune (zero-intercept constraint) — auditability over reassurance.

---

### S8 · 0→1 permanent banner

**Trigger.** Mode = 0→1. Always present, from first paint to last; not dismissible,
not collapsible, no "got it" button. Sits in R1, above the fold, and is echoed in the
verdict card mode line (`str.verdict.mode_line_01`) and in every exported log record's
mode field.

**Visual.** Calm, high-contrast band — informational tone, not warning-yellow (this
banner is a feature of the mode, not an apology). Persistent across scroll.

**Copy.**

- `str.banner.01` —
  > **0→1 mode structures your search. It does not predict product–market fit.** There
  > is no dataset of ideas like yours, so this tool makes no claim about which idea
  > will succeed. What it does: makes your comparison explicit, applies your policy
  > identically to both ideas, and shows you the levers. The judgment stays yours.

  (The bolded pair carries the same load-bearing predicate the GTM tour commits to —
  "…structures your search. It does not predict product–market fit." — with one
  deliberate difference: in-app the subject names the mode explicitly ("0→1 mode…")
  because the banner must be self-identifying in a screenshot, while the tour says
  "This mode…" because its screen has just named the mode. The pinned constant
  `PINNED_BANNER_01` uses the in-app form; the GTM tour adopted it in the exchange
  round, so tour, app, README, and config now share one banner — the predicate must
  never drift. RESOLVED at integration 2026-08-30: `configs/zero_to_one.yaml`'s
  `banner:` field now mirrors this string verbatim (the engine attaches the config
  banner to every 0→1 result; `app.py` asserts config == `str.banner.01` at import,
  and compliance T-NEG-04a asserts on it). Copy edits still flow states.md →
  strings.py → config → tests, in that order.)

**Honesty rule.** Spine success metric #4 and scope boundary: "0→1 mode never claims
predictive accuracy." Permanence is the point — a dismissible banner is a claim that
the caveat eventually stops applying.

---

### S9 · Model-of-the-judge progress

**Trigger.** Always visible in R7 while decision count < activation threshold (~10);
transforms into the M1-active chip at threshold.

**Visual.** Thin progress meter, 0→10, with count. Not gamified — no confetti at 10;
activation is announced in the modest register.

**Copy.**

- `str.m1.progress` (template, n < 10) —
  > Model of the judge activates at 10 decisions — you have 4. Until then, verdicts use
  > your stated weights (M0).
- `str.m1.progress_zero` (n = 0; shares the slot with S10a) —
  > Model of the judge activates at 10 decisions — you have none yet. Every logged
  > decision teaches it what you actually weigh.
- `str.m1.activated` (one-time, at n = 10) —
  > Model of the judge is now active. From here, each verdict also shows M1 — the
  > weights your own picks reveal. When it disagrees with your stated policy, you'll
  > see both.
- `str.m1.active_chip` (persistent replacement) —
  > M1 active · trained on your 14 picks
- `str.m1.consistency_note` (tooltip on ζ meter, from decision 1) —
  > ζ and Brier don't wait for 10 — they accumulate from your first decision. ζ is your
  > consistency: how often your own picks form circular contradictions (A over B over C
  > over A).

**Exits.** n reaches ~10 → M1 fits → chip state; S6 becomes reachable.

**Honesty rule.** Spine metric #3. The threshold is explained as a data requirement,
not a paywall-like tease; the copy is explicit about what runs meanwhile (M0).

---

### S10 · Log states — empty / loaded / uploaded

The log strip R7 is the product's custody statement: the log is *the user's*, full
stop (Spine: "log fully in the user's hands").

**S10a — Empty** (no decisions this session, nothing uploaded)

- `str.log.empty` —
  > No decisions logged yet. Your log is a local file you download and keep — this
  > Space stores nothing after you leave. If you have a log from before, upload it and
  > your history (ζ, Brier, model of the judge) comes back.
- Controls: `str.log.upload_cta` — > Upload log (.jsonl) · download control hidden
  (nothing to download).

**S10b — Loaded** (n ≥ 1 decisions in memory this session)

- `str.log.loaded` (template) —
  > 12 decisions in the log (3 from this sitting). ζ 0.86 · Brier 0.19 — see audit.
- `str.log.download_cta` — > Download log (.jsonl)
- `str.log.unsaved_nudge` (appears when session adds records; repeated, quietly, near
  session end signals — never a blocking modal) —
  > 3 decisions from this sitting exist only in this browser tab. Download to keep
  > them — there is no server copy, by design.

  **`{n_session}` semantics (binding).** The interpolant is the count of records
  **appended this session only** — never the total log size. Uploaded records
  already exist in the user's own file; counting them here would make the tool
  claim they are tab-only, which is false. When the session has appended nothing,
  this nudge does not render (use `str.log.loaded` / `str.log.empty` instead). A
  custody statement that miscounts is worse than none — it teaches the user the
  tool's honesty copy is decorative.

**S10c — Uploaded** (user restored a log file)

- `str.log.uploaded_ok` (template) —
  > Log restored — 23 decisions. ζ, Brier, and the model of the judge recomputed from
  > your history. New decisions append to this log.
- `str.log.uploaded_merge` (template; upload while session already has records) —
  > Merged: 23 uploaded + 3 from this sitting = 26 decisions, ordered by timestamp.
  > Duplicate records (same timestamp and inputs) were kept once.
- `str.log.uploaded_bad` (schema-invalid file; see also S11) —
  > That file isn't a PairwisePM log (line 7 is missing the `pick` field). Nothing was
  > changed — your current session log is intact. Export a fresh log from the tool that
  > made this one, or check the schema in the README.
- `str.log.uploaded_mode_note` (log contains other-mode records) —
  > 9 of these decisions are 1→N and 14 are 0→1. Each model trains only on its own
  > mode; ζ and Brier are reported per mode.

**Honesty rule.** No server-side storage (Spine scope) is turned into a visible
custody ritual: the tool repeatedly, calmly says *you hold the only copy*.

---

### S11 · Error / invalid-input recovery

**Trigger.** A field receives input the factor scale can't accept (text in Reach,
out-of-range step value, negative person-weeks, malformed upload — upload copy in
S10c).

**Visual.** Row-local, inline, immediate. The row gets the error edge; everything else
on screen is untouched — an error in one cell never grays out the questionnaire, never
clears other inputs, never scrolls the page. The verdict card, if computed, reverts to
placeholder with `str.verdict.stale` (a verdict must never coexist with a known-bad
input). Recovery = fix in place; no reset buttons anywhere near the error.

**Copy.** (templates; one per scale family)

- `str.err.number` (Reach, Effort, Cost-to-test) —
  > Reach needs a number — users affected per quarter, e.g. 4500. The z-scoring can't
  > do anything with "lots".
- `str.err.range_step` (0–4 scales) —
  > Capability feasibility is a 0–4 step (pass rate on your evals/prototype). 7 is off
  > this scale — if it feels like a 7, the scale's anchors are in the `why?` note.
- `str.err.range_signed` (−2..+2 scales) —
  > Impact is scored −2 to +2 against the named past feature. Pick the anchor that
  > fits; the comparison feature is your ruler.
- `str.err.effort_positive` —
  > Effort needs positive person-weeks. If it's truly zero, it isn't a comparison —
  > ship it.
- `str.err.preserved` (fixed suffix on every inline error) —
  > Everything else you've entered is untouched.

**Exits.** Valid value → error clears instantly → S2/S3 recompute path.

**Honesty rule.** Errors explain *why the scale exists* (each message teaches the
measurement), and recovery never costs the user prior work — trust is destroyed
fastest by a tool that loses five minutes of scoring.

---

### S12 · Mode-toggle transition

**Trigger.** User switches `1→N ⇄ 0→1` in R1.

**What changes and what is preserved (exact contract — ratified to the as-built
form at negotiation round 2, 2026-08-30).**

| Element | On mode switch |
|---|---|
| Factor rows R3 (schemas differ per spec §2) | **Replaced** with the other mode's factor set |
| Factor scores already entered | **Retained per mode** — each mode's factor block keeps its own scores, hidden while the other mode is active and restored on return; a score is never carried across schemas or read by the other mode's computation |
| Idea names + descriptions (R2) | **Preserved** |
| Evaluative inputs (R4 text: strategic fit, brand, judgment) | **Preserved** |
| Ceiling flag | Exists only in 0→1: hidden-but-retained when switching to 1→N, restored on return; never scored in either mode |
| Verdict card / leverage panel | **Cleared** to placeholder (they referenced the old factor space) |
| Decision log, ζ, Brier, M1 | **Preserved**; per-mode partitioning per `str.log.uploaded_mode_note` |
| 0→1 banner (S8) | Appears/disappears with the mode, instantly |

**Visual.** Instant switch, always — no confirmation dialog. Under the ratified
retained-per-mode contract nothing is destroyed by switching (each mode's scores are
hidden and restored, never cleared), so there is no at-stake work to confirm; a
dialog here would be a false claim of danger. The toast states the new ruler.

**Copy.**

- `str.mode.confirm` / `str.mode.confirm_go` / `str.mode.confirm_stay` — **RETIRED**
  (kept in the constants module for ID stability; MUST NOT be wired). Their copy
  described clearing factor scores, which the ratified retained-per-mode contract —
  and the as-built app — no longer does; rendering them would be a false statement.
- `str.mode.switched_toast` (template) —
  > 0→1 · Search mode. Same two ideas, new ruler: structure and consistency, no
  > claim about what will succeed.

  (The `{mode_promise}` interpolants are constants in `strings.py` —
  `MODE_PROMISE_01` / `MODE_PROMISE_1N`. The 0→1 promise deliberately avoids the
  words "accuracy"/"predictive" even in negation: compliance T-NEG-04b is a
  substring assertion on 0→1-scoped strings.)

**Honesty rule.** No silent cross-mode reuse of scores (that would be fabricating
data); the preserved/cleared boundary is stated in the dialog, not discovered later.

---

### S13 · Evaluative-override visual separation

Two sub-states: the standing panel (S13a) and the override act (S13b).

**S13a — The evaluative panel (R4), always.**

**Visual.** A container that cannot be mistaken for the questionnaire: distinct
background tint, its own border, its own header, physically below the mechanical
factors, and *no numeric inputs styled like factor inputs* — evaluative entries are
select-plus-text, never bare number boxes (a number box implies it feeds the math).
Nothing from R4 ever appears in R6's bar chart.

**Copy.**

- `str.eval.header` —
  > Outside the math — on the record
- `str.eval.sub` —
  > Strategic fit, brand, taste. Captured here, shown on the verdict card as labeled
  > judgment, and never — never — inside the score. If these end up deciding it,
  > that's allowed: it just happens in the open.
- `str.eval.card_echo` (how evaluative inputs render on the verdict card — a clearly
  bordered annex under the probability, template) —
  > Your judgment notes (not scored): Strategic fit — "extends the platform bet" ·
  > Brand — "no concerns."

**S13b — The override act.**

**Trigger.** User picks against the computed verdict (or picks a side under S4).

**Visual.** The override is honored, not fought: one rationale field, required,
then logged. No guilt UI, no "are you sure," no re-showing the probability in a bigger
font. The logged record marks the pick as an override with rationale (spec §6).

**Copy.**

- `str.override.cta` (secondary action on the verdict card) —
  > Pick the other idea
- `str.override.rationale_prompt` (template) —
  > You're picking Idea B against the mechanical verdict (A — 68% (55–79%)). Say why,
  > in a sentence. The rationale goes in the log — future-you gets to check whether
  > this kind of call ages well.
- `str.override.rationale_placeholder` —
  > e.g. "B unlocks the enterprise segment we've committed to for Q2 — strategic fit
  > outweighs the score here."
- `str.override.logged` —
  > Logged as your call, with your rationale, alongside both model outputs. The model
  > of the judge learns from picks — including this one.

**Honesty rule.** Spine scope boundary: evaluative factors are "captured and displayed
as labeled override inputs only." The design's job is to make the boundary *felt* —
different container, different vocabulary ("notes", "judgment", never "score"), and an
override path that treats the PM as the accountable adult the Spine says they are.

---

### S14 · Audit view — three lifecycle states (all first-class from day one)

The audit view (reached from R7) is **on-demand only** in v1 — Decisions D4
build-meanwhile default: no push cadence, no verdict-card interruptions; the reserved
`str.verdict.audit_footer` slot ships empty. MVP1 ships entirely in S14a, so the
locked states are designed as real states, never as broken-looking gaps, and **never
with fake or sample data** (sequencing rule: the divergence panel shows an explicit
not-yet-active state, not illustrative numbers — illustrative numbers exist only in
the GTM tour, where every log-derived panel carries a `sample` badge).

**S14a — Pre-M1** (n < 10 decisions in the current mode)

Always shows, live from decision 1: decision count (per mode), ζ with plain gloss,
Brier with plain gloss, override rate, the S9 progress meter. The revealed-vs-stated
divergence panel renders as a locked placeholder:

- `str.audit.m1_locked` (template) —
  > Revealed-policy panel not yet active — it activates near decision 10 (you have 4
  > in this mode). Until then verdicts use M0, your stated weights; nothing here is
  > simulated.
- `str.audit.zeta_gloss` — > ζ is your consistency: how often your own picks form
  circular contradictions (A over B over C over A). 1.00 = perfectly transitive.
- `str.audit.brier_gloss` — > Brier scores the model's probabilities against your
  actual picks — lower is better; 0.25 is what coin-flipping earns.

**S14b — M1 active** (n ≥ ~10 in the mode)

The divergence panel populates: paired stated-vs-revealed weight bars per factor
(the S6 `compare weights` view and this panel are the same component), the
order-bias diagnostic row (S7) with its significance gate, and the M1 training count.
The leverage panel's provenance chip (R6) switches to `str.leverage.provenance_m1`
in the same release of information — the audit view and the verdict surface must
never disagree about which regime is live.

**S14c — Calibration report** (per Decisions D4: reliability curve unlocks at n ≥ 30,
threshold in config)

- Below threshold, the curve slot is a locked placeholder, same doctrine as S14a:
  - `str.audit.curve_locked` (template) —
    > Reliability curve unlocks at 30 decisions in this mode (you have 14). With fewer,
    > the bins would be noise drawn as a line.
- At threshold: Brier trend over time, reliability curve **with per-bin counts shown
  on the chart** (D4: bin counts visible so thin bins can't masquerade as signal), ζ
  history. In 0→1 mode every one of these is labeled a consistency measure —
  compliance T-NEG-04b — via a fixed caption:
  - `str.audit.01_caption` —
    > 0→1 mode: these measure the consistency of your judgments — they do not predict
    > outcomes. No outcome data about ideas like yours exists.

    (Worded without "accuracy"/"predictive" — even negated uses would fail
    compliance T-NEG-04b's substring assertion on 0→1-scoped strings. "predict" as
    a verb is permitted; the pinned banner itself uses it.)

**Honesty rule.** Spine metric #3 (ζ/Brier from decision 1, M1 near decision 10) with
the sequencing mandate that empty states are explicit and truthful — a locked panel
that says why it is locked, never a mockup pretending to be history.

---

## 3. Micro-patterns (apply everywhere)

### MP-1 · The probability token: interval always adjacent

The win probability is one atomic visual token: `68% (55–79%)` — point estimate and
interval in the same text node, same line, no line break permitted between them,
interval in the same color at reduced weight (never gray-on-gray; it must survive a
squint). Engineering contract: the rendering component takes `(p, lo, hi)` and has
**no** call signature accepting `p` alone. Everywhere a probability appears — verdict
card, S6 strip, log table, audit view, exported README examples — the token is used.
If bootstrap fails or is not yet computable, render `str.mp1.nointerval`:
> interval unavailable — probability withheld

(withholding the point estimate too; a naked number is the one thing this product
never shows).

### MP-2 · The runner-up: never "rejected"

Banned vocabulary anywhere in UI or log-facing copy: *rejected, loser, killed,
eliminated, failed*. The losing idea's column header chip reads
`str.mp2.chip` — > Runner-up in this comparison —
("in this comparison" is load-bearing: the status is scoped to this pair, this
policy, today). The runner-up always renders with its forward path, from spec §5:

- `str.mp2.parity` (template, lever path exists) —
  > Path to parity: +1 step on *Evidence of pull* (from 2 to 3 — roughly, a waitlist
  > with real sign-ups) brings Idea B to 50/50. To 60/40 in its favor: that plus one
  > step on *Cost to test*.
- `str.mp2.fundamentals` (template, all paths run through facts; contains the
  compliance-pinned phrase verbatim and contiguous) —
  > Idea B loses on fundamentals — no working-harder path flips this comparison:
  > every path to parity runs through facts (*Reach*, *Data flywheel*) or leaves the
  > plausible range. That's worth knowing before anyone spends a quarter trying.

Parity paths are stated in **raw units** (interviews, weeks, pass-rate steps), never
in z-shifts — the z-math (Δz = L/w_j) stays under the hood (spec §5.2).

### MP-3 · Lever vs fact: two visual languages

Every factor row, every leverage bar, every parity suggestion carries its tag as a
chip:

- **Lever** — `str.mp3.lever_chip` → > lever — accent-colored chip, "changeable"
  affordance; levers are the only factors the parity explorer will propose moving, and
  the only bars in R6 that are interactive (drag/step to preview the flip point).
  Tooltip `str.mp3.lever_tip` —
  > Lever: you can move this by working — build, test, sell, de-risk.
- **Fact** — `str.mp3.fact_chip` → > fact — neutral/stone chip, static texture, no
  interactive affordance anywhere; R6 bars for facts render solid and undraggable.
  Tooltip `str.mp3.fact_tip` —
  > Fact: it is what it is. The tool will never suggest "improving" this — it will
  > tell you when a verdict rests on it.

The two chips must remain distinguishable in monochrome (shape or texture difference,
not color alone — accessibility floor).

---

## 4. State-transition summary (for engineering)

```
S1 empty ──input──▶ S2 partial ──all blocking valid──▶ compute
compute ──interval clear of 50%───────▶ S3 verdict
compute ──interval straddles 50%─────▶ S4 too-close
compute ──ceiling flag (0→1)─────────▶ S5 routing (wraps S3/S4 as context)
S3/S4 ──M1 active & disagrees────────▶ S6 strip on card
S3/S4/S5 ──log──▶ S10b ──n≥10──▶ M1 fit ──▶ S9 chip · S6 reachable
any ──invalid field──▶ S11 (row-local) ──fixed──▶ prior state
any ──mode toggle──▶ S12 ──▶ S1/S2 in new factor space (log/eval preserved)
audit fit ──|free intercept| significant──▶ S7 row in R7
S8 banner: function of mode, not of state — permanent in 0→1
edit after compute ──▶ verdict cleared (str.verdict.stale) ──▶ S2
```

Invariants to test against (each is a Spine/spec commitment):

1. No render path exists where a probability appears without its interval (MP-1).
2. No render path shows a winner when the interval straddles 50% (S4).
3. Swapping A and B flips every displayed probability to exactly 1−p (spec §3
   zero-intercept; also the S7 immunity claim — copy lies if this breaks).
4. Ceiling flag toggling changes routing copy but never any number (S5).
5. Mode switch never carries a factor score across schemas (S12).
6. Evaluative inputs appear in exactly two places — R4 and the verdict-card annex —
   and never in R6 or any computed value (S13).
7. In 0→1 mode, `str.banner.01` is present in every screenshot, every scroll
   position, every state (S8).

---

## 5. Copy-string index

All strings above, by ID, for the engineering leaf to key on: `str.empty.*` (5
incl. `example_cta`), `str.partial.*` (5 incl. `verdict_placeholder_one`),
`str.verdict.*` (10 incl. `stale`, `audit_footer`),
`str.tctc.*` (5), `str.ceiling.*` (3), `str.disagree.*` (6), `str.orderbias.*` (4),
`str.banner.01`, `str.m1.*` (6 incl. `progress_one`), `str.log.*` (16 incl. the 5
handler messages minted at reconciliation — `pick_first`, `pick_missing`,
`appended`, `export_empty`, `upload_none`, §6.4 R-2 — and the 3 singular
variants minted round 8: `loaded_one`, `unsaved_nudge_one`, `uploaded_ok_one`),
`str.err.*` (5),
`str.mode.*` (4, of which `confirm`/`confirm_go`/`confirm_stay` are RETIRED — S12),
`str.eval.*` (3), `str.override.*` (4), `str.leverage.provenance_m0/m1` (2),
`str.audit.*` (5), `str.mp1.nointerval`, `str.mp2.*` (3), `str.mp3.*` (4),
`str.factor.*` (2: `risk_label_suffix` §6.2, `ceiling_label` §6.4 R-2 — the
0→1 Ceiling checkbox label, T-NEG-04b-scoped).
Round-8 note: the six R-10 strings (`str.empty.example_cta`, the five `*_one`
singular variants) and the revised `str.verdict.stale` tail are NOW LANDED in
canonical `leaves/design/strings.py` (§6.10) — the design half of the
coordinated change, per the §5.12 routing agreed with architecture; engineering's
byte-identical re-vendor into `pairwisepm/strings.py` completes it same-round
per their round-7 commitment (T-VEND-01 red in the interim is the guard
enforcing the flow, not a defect).
Templates interpolate: idea names, counts, percentages (always as the MP-1 token),
factor display names from the mode config, and raw-unit parity amounts from the
leverage engine. Numeric examples in this document (68% (55–79%), counts of 4/12/23,
intercept +0.41, ζ 0.86, Brier 0.19) are illustrative placeholders for template slots,
not constants.

**Canonical machine-readable source: `leaves/design/strings.py`** — an importable,
dependency-free constants module holding every string above by ID, plus the five
compliance-pinned constants (`PINNED_TOO_CLOSE`, `PINNED_FUNDAMENTALS`,
`PINNED_CEILING`, `PINNED_FRAGILITY_TMPL`, `PINNED_BANNER_01`) that
T-VERDICT/T-PAR/T-CEIL/T-FRAG/T-NEG-04 assert on. Engineering should vendor it as
`pairwisepm/strings.py` (design cannot write inside the package) and key all four
render functions off it; this document remains the human-readable authority, the
module the assertable one — they are maintained together.

---

## 6. Exchange-round alignment notes

**6.1 Tour palette continuity (GTM, non-binding, adopted).** The app's visual system
adopts the tour's semantic color set so the demo story and the product read as one:
teal `#0B7285` = Idea A, copper `#B0561C` = Idea B, amber = honesty states (fragility,
ceiling routing, order-bias, unsaved-log nudge). The too-close-to-call card uses a
neutral (stone) treatment distinct from both the winner accent and amber — a withheld
verdict is a calm success state, not a warning. Intervals draw as a band on a 0–100%
track with a 50% midline wherever a graphic (not just the MP-1 text token) appears.
Color is never the only channel (MP-3 monochrome floor applies everywhere).

**6.2 Risk-surface direction label (engineering convention, pending Decisions
ratification).** Engineering ships Risk surface entered **0–4 REVERSED (4 = lowest
exposure)**, sign +1. A reversed scale is a classic slip point, so the input row must
state direction in the label itself, not only in `why?`:

- `str.factor.risk_label_suffix` — > 4 = lowest exposure, 0 = highest
- and the `why?` note leads with: > This scale is reversed on purpose: higher is
  safer, so every factor points the same way — bigger number, better idea.

If Decisions re-ratifies to natural direction (enter exposure, engine reverses), the
suffix flips to "0 = lowest exposure" and the engine convention changes — either way
the label and the math must be stated in the same direction.

**6.3 Manual release checks owned by design (compliance matrix, release-blocking).**
M-UX-01: both ideas visibly on one screen, no wizard splitting A from B across
occasions. M-UX-02: timed blank-to-verdict ≤ 5:00, both modes, fresh user (gtm
witnesses). M-UX-03: `str.banner.01` visible in every 0→1 UI state — entry, verdict,
audit, error, log states — matching invariant 7. Run per traceability.md §5 on every
release candidate.

**Scheduling (agreed with sequencing, round 2 — EXECUTED round 3).** The browser-render
half ran 2026-08-30 round 3: app.py served live (gradio 6.26.0, port 7861) and was
driven in a real Chrome session — empty state, partial state, Compare blocking, 1→N
verdict, too-close-to-call, 0→1 banner states, mode toggle, log append, audit strip.
Per-check-ID results in §6.5; new browser-only defects catalogued in §6.4 R-8..R-10.
M-UX-02 (timed fresh-user run, gtm witnessing) is the only check that cannot be
self-run by the auditing agent and remains scheduled.

**Tour cross-check (adopted from GTM, round 2 — divergence list DELIVERED round 3,
non-gating).** Checked against the live render. Divergences where the live UI differs
from the catalogue the tour mirrors (all are app defects, not tour errors — the tour
matches the catalogue; the build diverges, §6.4 R-8/R-9):

- Stop 2 (input screen): live factor inputs render pre-filled `0`, not blank — and
  Effort/Cost-to-test show red invalid borders on first paint (0 < min 0.5). The
  tour's clean empty questionnaire is what the catalogue specifies; the live app
  does not match it (R-8).
- Stop 3 (verdict) and Stop 5 (too-close): in Gradio's dark theme the live verdict
  headline (the MP-1 token) and runner-up chip are near-invisible pale-on-white;
  the tour's readable verdict card does not match the live dark-theme render (R-9).
- Stop 5 / banner: the 0→1 banner is a static top block, not persistent across
  scroll — a tour screenshot of a scrolled 0→1 verdict would show no banner (R-9
  adjacent; catalogue invariant 7).
- All other checked surfaces match: banner copy verbatim, verdict/model/mode lines,
  eval annex, leverage table + provenance chip, custody nudge, audit rows.

**6.4 As-built reconciliation (verified against app.py, negotiation round 2,
2026-08-30).** Design re-read app.py line by line per the integrator flag ("verify
the catalogue matches what app.py actually builds, not what it intended"). The
original deltas (a)–(j) are **all resolved as-built**: rationale required before an
override append (`do_log`); upload merges by timestamp with dedupe (`do_upload`);
stale-verdict clearing wired to every input's change event (`do_stale`); unfilled
factors block computation with no defaulting (`_missing_factors`,
`gr.Number(value=None)`); `⇄ Swap A/B` present and full-state (`do_swap`); R6
provenance chip rendered (`render_leverage`); UI keyed off the vendored constants
module; atomic `prob_token(p, lo, hi)` with half-up rounding; contiguous
`str.mp2.fundamentals`; config banner mirrors `str.banner.01` with an import-time
assertion. Credit where due — engineering built the honesty layer as specified.

**Resolved residuals (closed round 3 — independently verified by design, not taken
on engineering's word):**

- **R-1 — RESOLVED as-built.** Session-appended count is a separate `session_n`
  state (app.py:767), incremented only on append (app.py:555), fed to
  `{n_session}` (app.py:422), and the nudge is suppressed at 0 — uploads pass the
  count through unchanged (app.py:580-604). Verified in code AND live in the
  browser (logged one decision → "1 decisions from this sitting exist only in this
  browser tab"). Regression-pinned by compliance T-CUST-01. Dispute B1 with
  sequencing is moot: the fix landed pre-pilot exactly as design held out for.
- **R-2 — RESOLVED as-built.** `pairwisepm/strings.py` re-vendored — verified
  byte-identical to `leaves/design/strings.py` by file diff this round (T-VEND-01
  enforces it in the suite, 53 passed). All five handler messages and both Ceiling
  checkbox labels keyed off the new IDs (app.py:521-604, 713, 717).
- **R-3 — RESOLVED as-built.** Full `str.ceiling.strip` (idea name interpolated)
  and `str.ceiling.both` render on the card's routing strip alongside the engine's
  pinned note (app.py:213-233); T-CEIL-02 untouched.

**Verified residual gaps (updated round 5 after browser render session 2, §6.7 —
R-8 closed, R-9 partially closed with a precise residual):**

- **R-8 — RESOLVED as-built (browser-verified, render session 2, 2026-08-31).**
  Engineering's mechanism (their call, as offered): `gr.Number` removed from the
  factor path entirely — factor inputs are Textboxes whose untouched payload is
  the empty string, screened by `_coerce_raw`/`_screen_factors` before
  `compare()` is ever called (missing-ness stays a UI concept per architecture
  §5.10). Verified live in a real Chrome session against the served app: (a)
  fresh form first paint shows blank inputs, no pre-filled `0`s, no red invalid
  borders — matches tour Stop 2; (b) Compare with only Effort filled rendered
  `str.partial.verdict_placeholder` verbatim with the per-factor list ("6 factor
  scores to go before the verdict: Impact on primary metric (both ideas), …"),
  zero Gradio error toasts, no fabricated verdict; (c) an explicit `0` scored as
  a value (Reach A = 0 computed a verdict — an S4 too-close, correctly — rather
  than blocking); (d) non-numeric and out-of-plausible-range entries surface
  through the same S2 list (T-SER-01(d), handler-level with real frontend
  payloads). Guarded by T-SER-01 (demonstrated red-first against the pre-fix
  build; pre-push gate P-10). The round-1 delta (d) commitment is now true in
  the browser, not just in the suite. D7 candidacy is moot — accepted and
  shipped, nothing contested.
- **R-9 / R-9b — RESOLVED as-built (browser-verified, render session 3,
  2026-08-31, §6.9).** Engineering's round-6 fix (inline color on every
  text-bearing nested element inside forced-light blocks, incl. the headline
  `<b>` carrying the MP-1 token) verified legible in the served dark theme on
  every surface §6.7 enumerated: S3 headline+token and runner-up chip, S4
  headline/body, S1/S2 placeholder inner divs (missing-factor list included),
  stale notice, and the whole S5 ceiling card. Computed `rgb(28,25,23)` /
  `rgb(87,83,78)` ink on the light cards throughout. Guarded by T-THEME-01b
  (render-level, every-nested-element). The stone `#57534e` leverage/audit
  annotation rider remains catalogued below as the surviving minor. The
  round-5 record of the residual follows, kept as history: The shipped fix forces text color on every block that forces a
  light background (T-THEME-01 green), and it works exactly as far as CSS
  inheritance reaches: text sitting DIRECTLY in a forced-color element is now
  legible in dark theme (gloss/model/mode lines, amber ceiling/fragility strips
  — all direct-text with inline color — plus banner, eval annex, stale notice).
  But Gradio 6.26 ships `.gradio-container-6-26-0 .prose * { color:
  var(--body-text-color) }` — a universal descendant rule that beats
  *inheritance* on every NESTED element, so any child element without its own
  inline color reverts to near-white (`#f4f4f5`) on the forced-light block.
  Verified illegible live (computed styles + zoom screenshot, §6.7): the S3
  verdict headline (`<div style='font-size:1.25em'><b>` — the MP-1 token
  itself), the runner-up chip span, the S4 too-close headline and body (which
  carries S4's MP-1 token), and the S1/S2 placeholder inner divs — including
  the R-8 fix's own missing-factor list, which currently renders near-invisible
  in dark theme. Fix direction (engineering's call): inline `color` on every
  text-bearing element inside forced-light blocks (children included — a nested
  `<b>` needs it too), or a scoped `<style>` rule that outranks `.prose *`
  (e.g. a card class with `!important`). T-THEME-01 must be strengthened in the
  same change: the current static check (background⇒color on the same element)
  stays green while the browser shows an invisible headline — the third
  demonstration that a green guard can coexist with a browser-false behavior.
  Rider (minor, same theme family): leverage/audit annotations use inline
  `color:#57534e` (stone, chosen for light ground) on the page's dark
  background — low contrast, catalogued for the same fix pass.
- **R-4 (minor, standing).** Equal-weight ablation renders on every verdict card as
  a second probability line competing with the MP-1 token; S3 places
  `str.verdict.ablation_toggle` in the audit view (spec §3 "available as scientific
  control" — either placement honors the spec, so this is polish, not compliance).
- **R-5 (minor).** S2's live per-column progress counters
  (`str.partial.progress_a/b`) are not rendered; the missing-factor list appears
  only on Compare. (Round-3 correction: in the browser even the Compare-time list
  never renders because R-8 defeats blocking first — R-5 stays open but its fix is
  downstream of R-8.)
- **R-6 (design-side, fixed round 2).** S12's own prose still described a
  clear-scores confirmation dialog, contradicting the ratified retained-per-mode
  table that app.py correctly implements. Corrected: no dialog, `str.mode.confirm*`
  retired (see S12). The catalogue was the stale artifact here, not the build.
- **R-7 (minor).** The S10b loaded state's custody line (`str.log.loaded` — count,
  session count, ζ/Brier) is never rendered: when the log has records but the
  session appended none, app.py renders an empty custody line (app.py:424) rather
  than `str.log.loaded`. The audit table shows the counts, so no false claim is
  made — the loaded-state custody ritual is merely absent. Deferred polish.
- **R-10 (minor, design-side copy batch — exact copy pending mint).** Round-3
  render surfaced four copy/catalogue gaps that are design's to fix: (i)
  pluralization — the live app printed "1 decisions from this sitting";
  `str.log.unsaved_nudge` (and the count templates in `str.log.loaded`,
  `str.log.uploaded_*`, `str.m1.*`) need singular variants (round-5 addition:
  `str.partial.verdict_placeholder` joins the list — session 2 rendered
  "1 factor scores to go before the verdict: Reach (Idea A)."); (ii)
  `str.verdict.stale` ends "Recomputing…" but the as-built flow recomputes only on
  a manual Compare click — the tail becomes "Press Compare to recompute." unless
  engineering wires auto-recompute; (iii) the R2 anatomy promises a one-line
  description field per idea; as-built has name fields only — catalogue and build
  must converge one way or the other; (iv) the `Load example (canonical seeded
  pair)` button is real and useful but uncatalogued — S1 gains it as a catalogued
  affordance. NOTE: the new/changed strings are deliberately NOT yet added to
  `leaves/design/strings.py` — T-VEND-01 asserts byte-identity with the vendored
  copy, so the mint and the re-vendor must land in one coordinated change with
  engineering (the same one-PR discipline architecture demanded for R-2). Exact
  copy will be written here first, then minted+re-vendored together.
  **ROUND-6 UPDATE: the exact copy is now written — staged in §6.8, ready for
  the coordinated mint+re-vendor whenever engineering picks it up (no urgency;
  R-10 remains post-pilot backlog except where a string rides an R-9b-touched
  render path anyway).** Item (iii) is resolved design-side: v1 ships name
  fields only, description is backlog (R2 anatomy in §1 updated); item (iv) is
  catalogued (`str.empty.example_cta`, S1).
  **ROUND-8 UPDATE: MINTED.** The full §6.8 batch — five `*_one` singular
  variants, `str.empty.example_cta`, and the corrected `str.verdict.stale`
  tail — is landed in canonical `leaves/design/strings.py` at engineering's
  round-7 request and per architecture's §5.12 routing (§6.10). Remaining:
  engineering's same-round byte-identical re-vendor plus the `_one` selection
  wiring (their committed half); the stale-tail fix needs zero wiring. The
  `_one` wiring itself stays post-pilot-backlog class; the stale tail is a
  correctness fix and goes live with the re-vendor.
  **ROUND-9 UPDATE: CLOSED browser-verified.** Engineering's half landed in
  full (byte-identical re-vendor verified by own `cmp` this round; `_one`
  selection wired at the rendering call sites; `str.empty.example_cta`
  routed), and render session 4 (§6.11) confirmed the copy ON SCREEN: the
  S2 singular renders "1 factor score to go before the verdict: …" with
  exactly one factor missing, and the corrected stale tail renders "Inputs
  changed — the verdict above no longer applies. Press Compare to
  recompute." — the false auto-recompute claim is gone from the served
  page. All four R-10 items are now resolved: (i) wired+browser-verified,
  (ii) live, (iii) resolved design-side round 6, (iv) catalogued+wired.

- **R-12 (minor, post-Pilot polish — catalogued from render session 3,
  §6.9).** The as-built S5 card renders the mechanical verdict headline
  ABOVE the ceiling routing strips; the S5 spec puts the routing strip on
  top ("a routing strip on top, the mechanical comparison beneath it").
  Every string is present, legible, and honest — the divergence is emphasis
  order only. Either the card reorders or S5's visual note is ratified to
  the as-built order; no copy changes hands either way. R-4
  no-dispute-if-deferred terms.
  **ROUND-9 CLASSIFICATION SIGN-OFF (for compliance's audit log):** the
  registration "design-catalogued, post-pilot class, no matrix row" matches
  this seat's intent EXPLICITLY, not by inference. Rationale: R-12 is an
  emphasis-order divergence with zero copy or honesty content — every
  trust surface (headline, token, interval, routing strips) is present and
  legible in the as-built order, so no Spine commitment is degraded and no
  gate is warranted. If a future S5 rework touches the card, the reorder
  rides it; until then the catalogue entry is the record.

- **R-11 (minor, post-Pilot polish — catalogued from engineering's round-4
  mechanism note, on R-4's no-dispute-if-deferred terms).** The R-8 fix's
  Textbox mechanism loses the numeric spinner and the mobile numeric keyboard
  on factor inputs. Accepted trade-off: an input affordance is never worth a
  component that fabricates scores. If restored later (e.g. `inputmode=
  "numeric"` attributes or a serialization-safe numeric component), the R-8
  acceptance behavior (untouched ⇒ never a value; explicit 0 ⇒ a score) is the
  regression bar, enforced by T-SER-01.

None of these change the engine contract — every open item is UI-layer or doc-layer.

**Gating classification (round 3 — full per-item answer to sequencing's and
decisions' standing questions).**

- **R-1, R-2, R-3 — RESOLVED as-built this round.** No classification needed;
  dispute B1 with sequencing is closed as moot.
- **R-4, R-5, R-7, R-10 — post-Pilot backlog, confirmed and re-confirmed.**
  Bilateral design↔engineering items, not attached to space-push, release-audit,
  or pilot-live. Uncontested backlog; no D-entries unless a fix is refused
  outright. (R-5's fix is technically downstream of R-8 but the counters
  themselves remain backlog.)
- **ROUND-5 STATUS on the two claims below: R-8 is CLOSED — fix accepted,
  shipped, and browser-verified (§6.7); the gate claim dissolved uncontested
  exactly as D7's dissolution clause anticipated. R-9's claim carries forward
  narrowed to R-9b: the residual illegible surfaces are the MP-1 token itself
  (S3 and S4 headlines) and the S1/S2 placeholders, so the pre-pilot priority
  and the dark-theme demo caution stand until R-9b lands. The paragraphs below
  are kept as the round-3 record of how the claims were made.**
- **R-8 — claimed as release-gating (pre-pilot-live), via the agreed process.**
  Spine lines served: success metric #4 "The verdict is honest by construction"
  and the scope-boundary refusal "A judge that overstates its confidence is worse
  than no judge" — a verdict computed from 12 silently-defaulted scores the user
  never entered is a fabricated-input verdict, the exact confidence overstatement
  the Spine refuses; spec §1's "both ideas MUST be scored together" is likewise
  void when 12 of 14 scores are imputed zeros. Per the round-2 agreement with
  decisions and sequencing, design does NOT attach this to the critical path
  unilaterally: it is handed to the Decisions queue as a D-entry candidate with
  sequencing named as stakeholder. Design's position within that process: this is
  a *defect against an already-admitted commitment* (§6.4 delta (d), closed round
  1 as "unfilled factors block computation with no defaulting", now shown
  browser-broken) — the same defect-not-new-scope admission bar sequencing wrote
  into its graph for R-1/R-2, and it costs zero elapsed time in parallel with the
  human-gated D1/D2 path.
- **R-9 — pre-pilot fix requested, same process, second in priority.** Catalogue
  line served: MP-1 — the interval-welded probability token "must survive a
  squint", and it is currently near-invisible in the theme Gradio serves by
  default. A demo or pilot on dark theme shows an unreadable verdict headline.
  One-line CSS fixes; design accepts a Decisions-queue routing if sequencing
  contests gating, and will not attach it unilaterally.

**Reconciliation status (for compliance, round 3).** The catalogue-vs-code half
matches as-built app.py except R-4, R-5, R-7 (R-1..R-3 closed, verified). The
round-3 BROWSER render additionally established that two behaviors verified true
in code are false in the served UI (R-8 blocking, R-9 legibility) — recorded here
so M-UX audits keep auditing a true description. Per-check-ID results: §6.5.

**6.5 Manual release-audit results — browser render session 1 (2026-08-30,
negotiation round 3).** Per-check-ID pass/fail, citable by the compliance matrix
(compliance's round-2 ask). Method: app.py served live (gradio 6.26.0, venv,
port 7861), driven in a real Chrome session; states exercised: S1, S2 (blocking
attempt), S3 (seeded-pair verdict), S4 (too-close), S8 (banner, entry + scrolled),
S10a/S10b (append + custody line), S12 (mode toggle both directions), audit strip.

| Check ID | Result | Evidence |
|---|---|---|
| M-UX-01 (both ideas one screen, no wizard) | **PASS** | Live render: full two-column questionnaire, eval panel, verdict scaffold on one page; no step-splitting. |
| M-UX-02 (blank-to-verdict ≤ 5:00, both modes, fresh user, gtm witnesses) | **PENDING** | Requires a fresh human user and a witness; cannot be self-run by the auditing agent. Remains scheduled. |
| M-UX-03 (`str.banner.01` visible in every 0→1 state) | **FAIL** | Banner renders verbatim at top (teal band) but is a static block: scrolled 0→1 states show no banner, violating S8 "persistent across scroll" / invariant 7. Fix: sticky positioning (or equivalent). |
| M-DOC-01 (README epistemics per spec §7) | **PASS** | README.md carries all three commitments verbatim: priors as stated editable policy; 0→1 no-accuracy claim with the pinned banner predicate word-for-word; "the LLM's job was at build time" with zero-bias note. |

Additional live verifications this session (not matrix rows, recorded for
compliance's as-built chain): R-1 custody nudge counts session-appended records
only (append → "1 decisions from this sitting…"); `str.verdict.stale` renders
verbatim on input edit; mode-switch toast and eval-panel header/sub verbatim;
provenance chip `weights: M0 — your stated prior policy` present on the leverage
panel; equal-weight control line renders with its own MP-1 token; privacy line
present in footer. New defects found live: §6.4 R-8 (no-imputation blocking void
in browser — CRITICAL), R-9 (MP-1 token illegible in dark theme), R-10 (copy
batch). M-UX-01's PASS and M-UX-03's FAIL are both re-checkable in one session
once R-8/R-9 fixes land.

**6.6 Round-4 audit additions (2026-08-30, negotiation round 4).**

**M-GTM-01 — tour Stop 5 ceiling mock vs as-built verdict card (gtm's round-3
ask).** Method: the exact served pipeline executed directly — `do_compare` in
0→1 mode with every factor filled, Ceiling flag on Idea A, output HTML compared
byte-for-byte against `leaves/gtm/tour.html` Stop 5 and against
`pairwisepm/strings.py`. This is the handler → `render_verdict` path the browser
serves; only pixel legibility is theme-dependent (see the live-screen rider
below).

| Sub-check | Result | Evidence |
|---|---|---|
| Strip 1 copy (`str.ceiling.strip` formatted for Idea A) | **PASS** | Tour mock text `==` live strip text, verbatim including the "Averages are exactly what destroy outliers" line. |
| Strip 2 copy (engine pinned note, T-CEIL-02, + `str.ceiling.mech_label`) | **PASS** | The as-built card renders the engine note and the mech label inside ONE amber div; that combined div text `==` the tour's second mock strip verbatim. The tour's caption ("engine note + str.ceiling.mech_label") correctly names both sources. |
| Render order (strip → engine note + mech label) | **PASS** | Card indices 985 < 1346 < 1491; tour shows the same order. |
| Probability unchanged by the flag | **PASS** | Identical fixture with and without Ceiling on A: `93% (79–97%)` both runs — flag routes around the math, MP-1 token and interval untouched (T-CEIL-02 semantics confirmed at the handler-output level). |
| No ceiling copy when unflagged | **PASS** | Unflagged run contains no ceiling/portfolio copy — the strip is a state, not furniture. |

*Live-screen rider:* the one sub-check this method cannot close is pixel
legibility of the two amber strips in the served dark theme — which is exactly
R-9's root cause (forced `#fef3c7` background, no forced text color). Re-running
the browser render before the R-8/R-9 fixes land would re-observe the known-broken
screen and prove nothing new; therefore the Stop 5 live-screen confirmation is
**check #1 of browser render session 2**, scheduled for the round engineering's
R-8/R-9 fixes land, alongside M-UX-01 re-check and M-UX-03's fix verification.

**Standing-demand status (round 4):** R-8 and R-9 remain OPEN and carried —
`app.py` this round still has `gr.Number(value=None)` at line 671 with no
serialization guard (R-8) and no forced text color in the headline/runner-up/
amber blocks (R-9). Engineering received both demands in this round's packet;
no escalation while their response is pending. R-8's D-entry candidacy
(decisions queue) and graph admission (sequencing) stand as filed in §6.4.
*(SUPERSEDED round 5: engineering's fixes landed in round 4's parallel
response; browser render session 2 verified them — R-8 closed, R-9 partially
closed with residual R-9b. Current status in §6.4; session-2 evidence in §6.7.)*

**6.7 Manual release-audit results — browser render session 2 (2026-08-31,
negotiation round 5).** Append-only per compliance's round-4 demand: §6.5
session 1 is untouched and remains citable as dated. Method: as-built app.py
(post R-8/R-9 fixes, suite 56/56 incl. T-SER-01/T-THEME-01) served live
(gradio 6.26.0, project venv, port 7862), driven in a real Chrome session,
**dark theme forced** (`?__theme=dark` — the theme R-9 was found in); states
exercised: S1 fresh paint, S2 blocking (Effort-only Compare), S3 seeded-pair
verdict, S4 too-close (explicit-0 Reach), S12 mode toggle to 0→1, S8 banner at
top and scrolled. Evidence is computed-style readouts plus zoom screenshots.

| Check ID | Result | Evidence |
|---|---|---|
| R-8 acceptance (a): fresh first paint clean | **PASS** | Blank Textboxes, no pre-filled 0s, no red invalid borders, no toasts (screenshot + DOM scan: `toastCount: 0`, `anyRedBorder: false`). Matches tour Stop 2. |
| R-8 acceptance (b): incomplete Compare blocks | **PASS** | Effort-only Compare rendered `str.partial.verdict_placeholder` verbatim: "6 factor scores to go before the verdict: …" naming all six unfilled factors "(both ideas)"; no verdict, no toast. |
| R-8 acceptance (c): explicit 0 is a score | **PASS** | Reach A set to literal `0` → verdict computed (S4 too-close, "Win probability 48% (27–64%)"), no blocking — the exact distinction Number's None-as-0 destroyed. |
| R-8 acceptance (d): range/numeric errors via S2 list | **PASS (handler-level)** | T-SER-01(d) drives the handlers with real frontend payloads ("lots", out-of-range "0" for effort) and asserts the S2-list rendering; not separately re-driven in the browser. |
| M-UX-01 re-check (one screen, no wizard) | **PASS** | First-paint screenshot: full two-column questionnaire, single page, unchanged by the Textbox migration. |
| R-9 acceptance: verdict card legible in served dark theme | **FAIL — residual R-9b** | S3 headline + MP-1 token and runner-up chip computed `rgb(244,244,245)` on `rgb(250,250,249)` (zoom screenshot: near-invisible); S4 headline/body identical; S1/S2 placeholder inner divs identical (the new missing-factor list is itself near-invisible). Root cause: gradio's `.prose * { color: var(--body-text-color) }` beats inheritance from the block's forced inline color. |
| R-9 acceptance: amber strips + direct-text lines legible | **PASS** | Blocks whose text sits directly in the forced-color element are legible: gloss/model/mode lines computed `rgb(87,83,78)` (inline beats `.prose *`); ceiling/fragility/both strips are escaped direct text inside `color:#1c1917` divs — same verified mechanism. Closes M-GTM-01's live-screen rider for the strips themselves; whole-screen Stop 5 parity still blocked by the headline (R-9b). |
| M-UX-03 re-check (`str.banner.01` persistent across scroll) | **FAIL (stands)** | 0→1 banner renders verbatim at top but `position: static`; at scrollY 1500 its rect is fully out of viewport (`visibleInViewport: false`). The sequencing verdict-legibility-fix node bundled this; it did not land with the R-9 CSS. |
| M-UX-02 (timed fresh-user blank-to-verdict, gtm witnessing) | **PENDING — now schedulable** | Its R-8 blocker is verified closed: a fresh user now sees a clean form and honest blocking. Recommend running on light theme until R-9b lands (dark theme currently hides the verdict headline the user must read to finish). |

**Session-2 conclusions.** (1) R-8 is closed with browser-verified evidence —
the honesty layer's blocking rule is now true in the served UI, and the S2
missing-list is the error surface for everything (no raw toasts anywhere in
the mechanism). (2) R-9's fix validated its own premise but under-reached:
`.prose *` overrides inheritance, so the residual R-9b enumerates exactly the
nested elements still illegible — among them the MP-1 token, the catalogue's
first law, in both S3 and S4. A fix that leaves the probability token
unreadable in the served default theme is not yet done, however green
T-THEME-01 is. (3) M-UX-03's FAIL row from session 1 stands unchanged. (4)
release-audit still cannot flip: two FAIL rows (R-9b, M-UX-03) and one
pending human check (M-UX-02, now unblocked).

**6.8 Round-6 status, per-line GTM notification, and R-10 copy mint
(2026-08-31, negotiation round 6).** Append-only; §6.5 and §6.7 untouched.

**Round-6 residual verification (repo check, not a render).** As of this round
app.py still contains neither fix demanded after session 2: no
`position:sticky` (or equivalent) anywhere in the file — M-UX-03's banner is
still `position: static` — and the S3/S4 headline divs at app.py:176 and
app.py:192 still render `<div style='font-size:1.25em'><b>` with no inline
color, so the R-9b nested-element illegibility stands exactly as §6.7 recorded
it. Browser render session 3 would therefore re-observe known-broken screens
and prove nothing new (the same doctrine as §6.6's live-screen rider);
**session 3 is committed for the round BOTH residuals land in one change**, so
one sitting closes R-9b acceptance, M-UX-03 re-run, F-29 browser confirmation,
and whole-screen Stop 5 parity together. `pairwisepm/strings.py` remains
byte-identical to `leaves/design/strings.py` (diff-verified this round).

**Per-line notification to GTM (their round-5 oracle, answered line by line
from §6.7 so the launch-copy.md 1c-i gates can be edited selectively):**

| GTM oracle line | Result | 1c-i consequence (design's read) |
|---|---|---|
| (a) First paint matches tour Stop 2: blank inputs, no invalid styling, no pre-filled 0s; incomplete Compare renders the per-factor missing list, no toast | **PASS** (§6.7 rows R-8(a), R-8(b)) | Every gate citing first-paint cleanliness or blocking behavior can delete. |
| (b) Amber strips legible in served dark theme without zooming | **PASS** (§6.7 amber-strips row; closes M-GTM-01's live-screen rider for the strips) | Strip-legibility gates can delete. |
| (b) MP-1 probability token legible in served dark theme | **FAIL — R-9b** (§6.7: token computes rgb(244,244,245) on rgb(250,250,249) in S3 and S4) | The no-dark-theme-demo caution stays until R-9b lands and session 3 confirms. Light-theme demos are unaffected. |
| (c) M-UX-03 re-check (banner persistent across scroll) | **FAIL (stands)** (§6.7: `position: static`, out of viewport at scrollY 1500) | The banner-in-frame screenshot gate stays. Top-of-page 0→1 screenshots remain safe (banner verbatim at top). |

GTM's saved input is accepted with thanks: the Stop 2 mock renders factor
values as styled text, not native number widgets, so the Textbox mechanism
introduces no tour divergence and no re-mocking is needed — recorded here so
the tour-parity ledger stays complete.

**R-10 exact copy mint (staged — written here first per the §6.4 discipline;
lands in strings.py only in one coordinated change with engineering's
re-vendor, T-VEND-01).**

- (i) Pluralization. Binding rule for every count template: the singular
  variant is a distinct string ID with suffix `_one`, selected when the
  interpolated count is exactly 1; no runtime "(s)" hacks — a custody
  statement with broken grammar reads as decorative, and decorative honesty
  copy is the failure mode this catalogue exists to prevent. Exact copy:
  - `str.log.unsaved_nudge_one` —
    > 1 decision from this sitting exists only in this browser tab. Download
    > to keep it — there is no server copy, by design.
  - `str.partial.verdict_placeholder_one` (template) —
    > 1 factor score to go before the verdict: Reach (Idea A).
  - `str.log.loaded_one` (template; n = 1 total) —
    > 1 decision in the log (1 from this sitting). ζ and Brier accumulate
    > from here — see audit.
  - `str.m1.progress_one` (template; exactly 1 logged decision) —
    > Model of the judge activates at 10 decisions — you have 1. Until then,
    > verdicts use your stated weights (M0).
  - `str.log.uploaded_ok_one` —
    > Log restored — 1 decision. ζ, Brier, and the model of the judge
    > recomputed from your history. New decisions append to this log.
  - Mixed-count templates (`str.log.loaded`, `str.log.uploaded_merge`,
    `str.log.uploaded_mode_note`, `str.partial.progress_a/b`) pluralize each
    slot independently by the same rule ("1 of 7 factors scored" stays plural
    on the total: the total is 7).
- (ii) `str.verdict.stale` — revised tail matching the as-built manual-Compare
  flow (current tail "Recomputing…" claims an automatic recompute that does
  not happen — a false statement in the stale state, which exists precisely to
  prevent stale claims):
  > Inputs changed — the verdict above no longer applies. Press Compare to
  > recompute.
  If engineering instead wires auto-recompute, the original tail is restored;
  either way the copy and the wiring must state the same behavior in the same
  change.
- (iii) RESOLVED design-side: R2 ships name fields only in v1; the one-line
  description field is post-pilot backlog (§1 anatomy updated; log schema
  description stays optional).
- (iv) `str.empty.example_cta` minted (see S1) —
  > Load example (canonical seeded pair)

**Round-6 conclusions.** (1) Nothing in §6.7 is superseded: R-9b and M-UX-03
FAIL rows stand, verified still-unfixed in the repo this round. (2) The GTM
notification loop is closed per-line above — gates delete selectively, not
wholesale, which is the honest shape: the build earned (a) and half of (b).
(3) M-UX-02 remains schedulable now, light theme until R-9b lands. (4) All
R-10 copy is now exact and staged; the coordinated mint is engineering's to
schedule, and no string changes hands until it does.

**6.9 Manual release-audit results — browser render session 3 (2026-08-31,
negotiation round 7).** Append-only; §6.5, §6.7, §6.8 untouched. Trigger
condition met: repo check confirmed BOTH residuals landed before the session
started (inline color on every nested element in `render_verdict`/
`render_placeholder`/`render_stale`; `_CSS = "#pwpm-banner { position:
sticky; top: 0; z-index: 100; }"` at app.py:744, wired via `elem_id` +
Blocks css; suite 58/58 in 1.15s, own run, incl. T-THEME-01b and
T-BANNER-01). Method identical to §6.7: as-built app.py served live
(gradio 6.26.0, project venv, port 7863), driven in a real Chrome session,
**dark theme forced** (`?__theme=dark`); evidence is computed-style
readouts plus screenshots. States exercised: S1 fresh paint, S3 seeded-pair
verdict, S4 too-close (explicit-0 Reach), `str.verdict.stale`, S12 toggle to
0→1, S2 blocking in 0→1 (empty factors → missing list), S5 ceiling-flagged
verdict, S8 banner at top and at scrollY 1500/3000.

| Check ID | Result | Evidence |
|---|---|---|
| R-9b (a): S3 verdict headline div + nested `<b>` (the MP-1 token) | **PASS** | Both compute `rgb(28,25,23)` on card `rgb(250,250,249)` ("Reply Drafts wins this comparison — 59% (52–64%)" fully legible in zoomless screenshot). Inline color beats `.prose *` by cascade, as designed. |
| R-9b (b): runner-up chip span | **PASS** | Computed `rgb(28,25,23)`; chip text "Instant Summaries: Runner-up in this comparison" legible. |
| R-9b (c): S4 headline + body (body carries S4's MP-1 token) | **PASS** | Headline div and `<b>` `rgb(28,25,23)`; body "Win probability 48% (27–64%). The interval straddles 50%…" `rgb(28,25,23)`. |
| R-9b (d): S1/S2 placeholder inner divs | **PASS** | S1: both inner divs `rgb(87,83,78)` on `rgb(250,250,249)`. S2 (0→1, empty factors): missing-factor list "6 factor scores to go before the verdict: Problem severity × frequency…" and `str.partial.no_default` both `rgb(87,83,78)` — the R-8 error surface is now legible in dark theme. |
| R-9b (e): stale notice | **PASS** | `str.verdict.stale` computed `rgb(87,83,78)` on the dashed card. |
| S5 / Stop 5 whole-screen parity (closes §6.6 live-screen rider entirely) | **PASS** | Ceiling-flagged 0→1 verdict: both amber strips `rgb(28,25,23)` on `rgb(254,243,199)`; wrapped too-close headline/body legible; judgment annex legible; whole card readable in one screenshot, no zoom. |
| **R-9b acceptance overall** | **PASS — CLOSED** | Every surface §6.7 enumerated as illegible now computes legible ink. F-29 can flip on this row-set; the no-dark-theme demo caution can delete. |
| M-UX-03 re-check (`str.banner.01` persistent across scroll) | **FAIL (stands, third row) — mechanism evidence below** | Banner renders verbatim in 0→1, correctly absent in 1→N. Computed style IS `position: sticky; top: 0px; z-index: 100` — the CSS landed and applies (constructor `css=` honored despite the deprecation warning). But sticky never engages: at scrollY 1500 the banner rect top is −1255 (fully out of viewport; −1580 at scrollY 3000). |
| M-UX-03 clipping-ancestor report (engineering's pre-wired contingency clause) | **DELIVERED** | Exactly one clipping ancestor between banner and body: `div.gradio-container.gradio-container-6-26-0`, computed `overflow: hidden` / `overflow-y: hidden`. The document is the scroller (`documentElement.scrollTop` 1824.5 while `.gradio-container.scrollTop` stays 0), so the sticky's nearest scrollport is a container that never scrolls — sticky is structurally a no-op here regardless of rule correctness. **Fallback viability confirmed:** zero fixed-position breakers between banner and root (no `transform`/`filter`/`perspective`/`contain: paint|layout`/`will-change: transform` on any ancestor), so `position: fixed` will work as engineering committed to land on this evidence. |

**Session-3 conclusions.** (1) **R-9b is CLOSED browser-verified** — the MP-1
token, the catalogue's first law, is legible in the served dark theme on
every surface, and the whole-screen Stop 5 parity rider closes with it. (2)
**M-UX-03 stands FAIL a third time, with a new lesson for the guard
doctrine**: T-BANNER-01 pins a rule that the browser *applies* but that never
*takes effect* — computed `position: sticky` coexisting with a banner that
scrolls away is the fourth green-guard/browser-false instance, one layer
deeper than R-9b (rule-applied vs rule-effective). The fix is engineering's
own pre-committed fallback (`position: fixed`), owed same-round per their
round-6 packet, with T-BANNER-01 updated in the same change. (3) Session 4
is scoped to exactly ONE check: banner-in-viewport at scroll, after the
fixed fallback lands — minutes, not a sitting. (4) M-UX-02's light-theme
rider is LIFTED: with R-9b closed, either theme now times the design, not a
CSS bug. The run needs only gtm's witness slot. (5) One new minor catalogued
as R-12 (§6.4): the as-built S5 card renders the mechanical headline ABOVE
the routing strips, while S5 specifies the routing strip on top ("a routing
strip on top, the mechanical comparison beneath"). All copy is present,
legible, and honest — the divergence is emphasis order only; post-pilot
polish class, R-4 terms.

**6.10 Round-8 — R-10 copy mint EXECUTED, design half of the coordinated
change (2026-08-31, negotiation round 8).** Append-only; §6.5–§6.9 untouched.

**The mint (first string-content change since the vendoring boundary became
test-enforced).** At engineering's round-7 request ("promote the staged §6.8
copy into canonical `leaves/design/strings.py` — I will re-vendor
byte-identical the round it lands") and per the §5.12 routing pinned by
architecture, the full §6.8 batch is landed in `leaves/design/strings.py`
this round, copy exactly as staged (per the §5 convention, numeric examples
in staged template slots — e.g. `str.log.loaded_one`'s session count —
interpolate as named placeholders; the singular counts that ARE the string's
subject stay literal):

- `str.verdict.stale` tail corrected → "Press Compare to recompute." — the
  one correctness fix in the batch: the old tail claimed an automatic
  recompute the as-built flow does not perform. Zero wiring needed;
  `app.py:162` already renders this ID from the strings module, so the
  re-vendor alone puts the true statement on screen.
- Five `*_one` singular variants minted: `str.partial.verdict_placeholder_one`,
  `str.log.unsaved_nudge_one`, `str.log.loaded_one`, `str.log.uploaded_ok_one`,
  `str.m1.progress_one` — selection rule in the module comment (distinct ID,
  chosen when the count is exactly 1; mixed-count templates pluralize each
  slot independently). Wiring is engineering's, same-change with the
  re-vendor or a later batch (their choice; backlog class).
- `str.empty.example_cta` minted (S1 affordance, R-10(iv)).
- Module self-check passes (98 IDs; pinned constants, banned-word and
  T-NEG-04b sweeps all green over the new strings).

**Routing honored (architecture §5.12, both pins).** The edit landed in
design's canonical file ONLY; `pairwisepm/strings.py` was not touched from
this seat and never will be. T-VEND-01 is expectedly red between my half and
engineering's byte-identical re-vendor of this exact content — that red is
the guard enforcing the documented direction (states.md → strings.py →
vendored copy → tests), not drift: the §6.8 staging and this section give
the re-vendor its verbatim target. No placeholder was renamed (the five
`*_one` IDs are new; `str.verdict.stale` has no placeholders), so no app.py
call-site updates are owed by §5.12(c).

**M-UX-03 status re-verified this round.** app.py:744 still carries the
sticky rule; the pre-committed `position: fixed` fallback has NOT yet
landed, so the third FAIL row stands unchanged and the §6.9 evidence packet
(clipping ancestor `.gradio-container-6-26-0` computed `overflow: hidden`;
zero fixed-position breakers banner-to-root) remains the complete input for
engineering's owed same-round landing. Reminder riding with it (§6.9):
fixed removes the banner from flow — reserve its height so it doesn't
overlap the mode toggle, keep the inner background opaque, and update
T-BANNER-01 in the same change with the rule-applied-vs-rule-effective
lesson in its docstring.

**Session 4 standing commitment.** Runs the round the fixed fallback lands:
ONE check — `str.banner.01` rect within viewport at scrollY 1500 (and 3000)
in served 0→1 dark theme — appended here as §6.11, minutes not a sitting.
F-19 flips only on that row, per compliance's acceptance framing.

**M-UX-02.** Fully unblocked, rider lifted (§6.9); waits only on gtm naming
their witness slot to sequencing's encoded window (≤ 2026-09-01). Design
times the run whenever the slot lands, either theme.

**6.11 Manual release-audit results — browser render session 4 (2026-08-31,
negotiation round 9).** Append-only; §6.5–§6.10 untouched. Numbering note:
several round-8 packets referenced "§6.10" for this record via packet lag —
§6.10 was taken by the round-8 mint record, so this session lands as §6.11
exactly as §6.10's standing commitment pre-stated.

**Trigger condition met, repo-verified before the session started** (the
do-not-start-early clause, third exercise): engineering's fixed fallback is
landed — `_CSS = "#pwpm-banner { position: fixed; top: 0; left: 0; right:
0; z-index: 100; }"` at app.py:769, height reserved by the content-exact
hidden duplicate `BANNER_SPACER_HTML` placed FIRST in the layout
(app.py:771/787), spacer toggling with the banner on mode change — and the
R-10 re-vendor is byte-identical (`cmp leaves/design/strings.py
pairwisepm/strings.py` clean, own run). Suite 59/59 in 1.21s, own run
(incl. the rewritten T-BANNER-01 pinning fixed+spacer+wiring, and the new
T-STR-01).

**Method identical to §6.7/§6.9:** as-built app.py served live (gradio
6.26.0, project venv, port 7864), driven in a real Chrome session, **dark
theme forced** (`?__theme=dark`); evidence is computed-style and
`getBoundingClientRect` readouts plus a screenshot. Viewport 1512×792.

| Check ID | Result | Evidence |
|---|---|---|
| **M-UX-03 session-4 single check** (`str.banner.01` rect within viewport at scrollY 1500, served 0→1) | **PASS — CLOSED** | 0→1 mode active, banner visible, computed `position: fixed`. At scrollY 1500: rect top **0**, bottom **77.2** — fully within the 792px viewport (§6.9 baseline at the same scroll: top −1255, fully out). At the requested scrollY 3000 the document clamps to its max scroll 1824.5: rect top 0, still fully in viewport. Screenshot: teal band pinned at viewport top, full `str.banner.01` copy legible, page content scrolling beneath it. The banner is persistent across scroll — S8's invariant 7 holds in the browser for the first time. |
| Height reservation / no-overlap rider (M-UX-01 regression guard) | **PASS** | At scroll 0: banner rect top 0, bottom 77.2; the mode-toggle block's top computes 238.5 — no overlap with header or toggle. Spacer computed height **77.2 = banner height exactly**: the content-exact duplicate reservation is verified live, no magic pixels. |
| Opaque-background rider | **PASS** | Banner content div computes `rgb(11,114,133)` (#0b7285, opaque) with ink `rgb(240,253,250)`; an opaque gradio wrapper (`rgb(39,39,42)`) sits behind it — nothing ghosts through at any scroll position. |
| Bonus (non-gating): R-10(i) singular live | **PASS** | S2 with exactly one factor missing renders "**1 factor score to go** before the verdict: Data / distribution advantage (Idea B)." — the `str.partial.verdict_placeholder_one` selection wiring works in the served page; ink `rgb(87,83,78)` (the §6.9-verified legible placeholder ink). |
| Bonus (non-gating): corrected stale tail live | **PASS** | After a factor edit post-verdict the stale notice renders "Inputs changed — the verdict above no longer applies. **Press Compare to recompute.**" — the false 'Recomputing…' auto-recompute claim is GONE from the served page; ink `rgb(87,83,78)`. The R-10(ii) honesty fix is confirmed on screen, end of the copy chain (states.md → strings.py → vendored copy → browser). |
| Incidental observation (recorded, no action) | PASS-class | Out-of-plausible-range entries surface through the S2 missing list with the bound named per line ("Problem severity × frequency (Idea A — outside 0–4)") — the S11-through-S2 recovery path behaves exactly as specified, no raw toasts, no red borders. |

**Session-4 conclusions.** (1) **M-UX-03 is CLOSED browser-verified** — the
last open FAIL row on the board. F-19 flips off manual-FAILED and P-5
clears on the single-check row per compliance's §22b acceptance framing;
gtm's banner-in-frame gate (1c-i) lifts on this PASS line — this section is
the per-line notification, delivered the same round the evidence was
produced. (2) The guard-doctrine arc resolves in the right direction:
`position: fixed` is viewport-anchored regardless of ancestor overflow —
the mechanism §6.9 predicted the browser could not structurally defeat was
not defeated, and the rewritten T-BANNER-01 now pins a rule whose applied
and effective halves were verified by the instruments that own each half.
(3) **The render-session ledger closes**: no further sessions are
scheduled; a new one triggers only if copy or layout changes land (a
banner-copy change self-propagates to the spacer by construction). (4) R-10
is CLOSED end-to-end (catalogue entry updated above) — every minted string
verified either on screen or by byte-identity plus wiring. (5) R-12
classification is SIGNED OFF for compliance: design-catalogued, post-pilot
polish, no matrix row (explicit, catalogue entry updated above). (6)
**M-UX-02 is the sole remaining agent-checkable item**: fully unblocked,
zero dependencies, waits only on gtm's witness slot inside sequencing's
≤ 2026-09-01 window; design times the run the sitting it lands, either
theme.

**6.12 Round-11 — retrigger clause bound BOTH directions (explicit), and
M-UX-02 sitting-readiness record (2026-08-31, negotiation round 11).**
Append-only; §6.5–§6.11 untouched.

**Retrigger clause, made exact (compliance's round-10 closing question,
answered in the affirmative and now binding as written).** §6.11 conclusion
(3)'s "copy or layout changes" was always intended to cover both directions;
this section removes the inference. The render-session ledger's retrigger
clause binds:

- (a) **Copy direction:** any landed change to a string that renders on a
  trust surface (banner, verdict card, placeholders, custody strip) — the
  standing states.md → strings.py → vendored copy → browser chain.
- (b) **Layout/rule direction:** any landed change to `app.py`'s banner or
  spacer rules, any forced-background or forced-color surface, any
  positioning/z-index/overflow rule on an ancestor of a trust surface, or
  any structural reordering of the card — **even when every static pin
  (T-BANNER-01, T-THEME-01/b, T-STR-01, and their successors) stays
  green**. The blindness ladder's terminal lesson is the reason stated in
  the clause itself: a green pin verifies rule-*applied*; only a browser
  session verifies rule-*effective* (§6.9's sticky-that-never-engaged is
  the standing counterexample). A closed ledger whose retrigger fired only
  on copy edits would quietly re-open the honor system for layout; this
  catalogue refuses that in writing.

Either trigger lands → one scoped session, per-check-ID, appended here —
the same discipline as sessions 1–4. No trigger → the ledger stays closed;
no ceremonial re-renders.

**M-UX-02 sitting-readiness record (gtm's and sequencing's round-10
demands, honored to the limit of this seat).** Today (2026-08-31) is the
live named slot; backstop first hour of 2026-09-01. Design-side state,
pre-stated so the sitting's record needs no setup paragraph when it lands:

- Timer READY; zero design-side preparation remaining (§6.11 conclusion 6
  stands). Either theme is valid — R-9b closed means the theme times the
  design, not a CSS defect (§6.9 conclusion 4).
- Protocol, fixed now so the record is comparable: one blank-to-verdict
  1→N run, fresh user per Hari's recruit, gtm witnessing; clock starts at
  first paint of S1, stops at first render of S3/S4/S5; bound 5:00.
- The record lands HERE as a dated per-check line (M-UX-02, PASS/FAIL,
  start/end/elapsed/theme, both seats' numbers — design's timer and gtm's
  witness reading), mirroring the §6.7/§6.9/§6.11 evidence discipline, with
  gtm's launch-copy.md 1c-i line carrying the same numbers.
- What this seat will NOT do: convene humans, or write the record before
  the run exists. A witness record minted without a witnessed run is the
  exact confidence overstatement this catalogue exists to prevent — SC-06
  converts on a dated fact or not at all. If the window closes unconvened,
  the honest state is recorded as such ("designed so, not yet timed"), and
  the tour keeps the framing gtm already holds.

**6.13 Round-13 — M-UX-02's two terminal branches pre-written with exact
copy, and the no-timing-claim scan that makes both branches honest
(2026-08-31, negotiation round 13).** Append-only; §6.5–§6.12 untouched.

Compliance and sequencing both asked the same thing from two seats: that
§6.12's fallback stop being a standing *intention* and become a dated
*appended line* the round its branch triggers, matching the append-only
evidence discipline of sessions 1–4. Accepted whole — and executed one
notch further, because a state this catalogue names is a state this
catalogue writes out in full: both branches are pre-drafted below with
their exact copy, so whichever fires, landing it is transcription with
dates and numbers filled in, never fresh drafting under time pressure.
Verified this round from this seat before writing: mirror byte-identical
(`cmp`, own run), suite 59/59 in 1.34s, `position: fixed` live at
app.py:769, and no M-UX-02 record exists in this file — the sitting has
not convened as of this revision (2026-08-31, evening of the named day;
backstop = first hour of 2026-09-01).

**Branch A — the sitting runs.** The line lands here the same round,
verbatim in this shape, every field filled or the record is void:

> M-UX-02 · <date> · PASS | FAIL · blank-to-verdict, 1→N, <theme> theme ·
> clock S1 first paint → first verdict render (S3/S4/S5) · start <hh:mm:ss>
> · end <hh:mm:ss> · elapsed <m:ss> vs bound 5:00 · design timer <m:ss> ·
> gtm witness reading <m:ss> · fresh user affirmed: yes · coaching given:
> none beyond mode selection · witness: GTM

A FAIL is as landable as a PASS and requires no negotiation to write: an
elapsed over 5:00 is a dated fact about this build, and SC-06 then reads
"measured at <m:ss>, over the 5:00 target" — the metric does not get
re-defined to fit the number. Voiding conditions (coaching beyond mode
selection, non-fresh user, either seat's clock unread) make the run
**no record**, not a soft record, and Branch B fires instead.

**Branch B — the backstop hour passes unconvened.** This exact line is
appended here that same round, dated, with no softening and no adjective
added:

> M-UX-02 · <date/time> · window closed unconvened — designed so, not yet
> timed. No sitting convened within the ≤ 2026-09-01 window; design timer
> stood READY throughout, gtm witness stood by throughout, missing input
> was a fresh user. SC-06 remains "designed so" in every payload; this is
> a dated scheduling fact, not a deferred pass.

The phrase "designed so, not yet timed" is the registered string, identical
in this file and gtm's 1c-i by prior agreement; it is not paraphrased in
either instrument. There is no third branch: no "substantially complete",
no "informally observed", no agent-run stand-in. A design-seat self-timed
run is explicitly **not** a Branch A record — the whole point of the check
is a user who has never seen this screen, and this seat is the worst
possible subject.

**Why the interface needs no surgery on either branch (scan, this round).**
Grepped the design string catalogue for every timing and speed claim —
`minute`, `5 min`, `under 5`, `fast`, `quick`: **zero hits**, confirming
what the catalogue has always asserted structurally. Not one rendered
string in the product promises a duration. The under-5-minute figure lives
only in the Spine's success metrics, the tour, and this catalogue's
measurement record — never on a trust surface where a user could read it as
a guarantee the build has not earned. So Branch B costs zero copy
retraction, and Branch A adds no boast: the number, measured, goes in the
record and the tour, not into the verdict card.

That is the same rule as MP-1 one level up. A probability never renders
without its interval; a performance claim never renders without its
measurement. An unmeasured claim on a trust surface is precisely a point
estimate with the interval stripped off — and this catalogue's refusal is
identical in both cases. §6.12's protocol, timer readiness, and no-early-
record rule all stand unchanged; §6.13 only guarantees that whichever
branch the humans hand us, the state is already written, exactly, in
advance of needing it.

**6.14 Round-14 — the copy chain's terminal link named, the delivery
runtime added to the retrigger enumeration, M-UX-02's coverage limit
written into the protocol, and one dated copy-integrity exposure opened
(2026-08-31, negotiation round 14).** Append-only; §6.5–§6.13 untouched.
§6.12(a)/(b) are amended by this section in the two places named below and
are otherwise unchanged; §6.13's two branches are unchanged in substance,
Branch A's line gains the mode-coverage fields.

**(i) §6.12(a) amended — the copy chain has a fourth link, and it is the
one that reaches the user.** The clause has read `states.md → strings.py →
vendored copy → browser` since §6.11. That chain names files. What a user
actually reads is whatever module the running interpreter *binds*, which is
not the same object as the file this seat compares. Architecture reported a
third, undeclared copy this round; this seat verified it rather than
accepting it on the packet, and it is a copy-authority matter, so it is
recorded here in copy terms:

```
$ cmp leaves/design/strings.py .venv/lib/.../site-packages/pairwisepm/strings.py
  differ: char 3663, line 79
$ cd /tmp && python -c "import pairwisepm.strings as s; print(s.__file__)"
  .../site-packages/pairwisepm/strings.py
  'str.empty.example_cta' in STRINGS → False
```

The chain therefore terminates, as of this section, on **the bound module**
— `importlib.import_module('pairwisepm.strings').__file__` — and a copy is
"in the chain" only if it is the one an interpreter can bind. A `cmp` of
two files is evidence about two files. Every "mirror byte-identical" this
seat has certified since §6.10, this round's included, was true of the
repo mirror and silent about the third copy; that is stated here rather
than left for a reader to discover, on the same rule this catalogue applies
to the product (a measurement is reported with its scope or it overstates).

**(ii) CX-14-01 — OPEN copy-integrity exposure, dated 2026-08-31.** The
stale bindable copy is not merely behind; it is behind *across the R-10
mint*, and the R-10 mint existed precisely to delete a confidence
overstatement. Verified byte-level, both sides:

| link | `str.verdict.stale` tail |
|---|---|
| authority (`leaves/design/strings.py:136`) | "…no longer applies. **Press Compare to recompute.**" |
| repo mirror (`pairwisepm/strings.py`) | identical to authority (`cmp`, own run) |
| bound copy from off-root (site-packages:121) | "…no longer applies. **Recomputing…**" |

Read as copy, that is the R-10 defect alive on a reachable surface: a
stale-verdict line that asserts an automatic recomputation the as-built
flow does not perform (§6.8(ii), §6.10 — the app recomputes only on a
manual Compare click). The state whose whole job is to prevent a false
claim would itself make one. The same copy is missing
`str.empty.example_cta` entirely, so in practice an off-root launch dies at
`app.py:848` before first paint rather than serving the bad tail — but that
is a crash standing in front of a copy defect, not a fix for it, and the
ordering could change with one edit. CX-14-01 stays OPEN in this catalogue
until the bound module is the authority's bytes; owner is engineering
(editable-or-absent install), and this seat closes the row only on its own
re-run of the two commands above.

**(iii) §6.12(b) amended — the delivery runtime joins the enumeration
(engineering's demand, accepted whole and stated in this seat's terms).**
(b) has enumerated `app.py`-side rule changes only: banner/spacer rules,
forced-background/forced-color surfaces, positioning/z-index/overflow on an
ancestor of a trust surface, structural reordering. Added as a fifth item:

- **(b5) Delivery-runtime direction:** any change to the runtime the rules
  are *honored through* — the Gradio major, README's `sdk_version`, or the
  dependency bound in `requirements.txt` / `pyproject.toml` — is itself a
  retrigger event, on the identical rule-applied-vs-rule-effective
  reasoning the clause already carries. The 0→1 banner reaches a browser
  only via `gr.Blocks(css=…)`, which Gradio 6 honors through a *deprecated*
  fallback; a major that drops it leaves this catalogue's pin green,
  engineering's source assertion green, and the structure-not-prediction
  banner unstyled. That banner is the Spine's "0→1 mode never claims
  predictive accuracy" made visible — an unstyled or unpainted banner is
  the accuracy disclaimer silently withdrawn, which is the one failure this
  catalogue exists to prevent. A trust surface delivered through a
  deprecation fallback is a trust surface on notice.

Both amendments follow one rule this section makes explicit for future
readers: **a pin proves the rule was written; only the delivered artifact
proves the rule was honored, and the delivered artifact is the bound module
in the browser's runtime.** (i) applies it to copy, (b5) applies it to
layout. They are the same sentence read twice.

**(iv) M-UX-02's coverage limit, written into the protocol (compliance's
demand, accepted whole).** §6.12's fixed protocol times **one 1→N run**.
Therefore, in terms:

- The dated record discharges **M-UX-02a (1→N) only**. Branch A's line
  names the mode measured and is a single-mode record by construction.
- **M-UX-02b (0→1) is untimed, with no instrument and no scheduled
  sitting.** No inference from a correct 1→N line extends to it.
- On either branch, 0→1 keeps the registered phrase **"designed so, not
  yet timed"** — on Branch B because nothing was timed, on Branch A because
  what was timed was the other mode. A PASS on 1→N converts SC-06 for 1→N
  and for nothing wider.

Branch A's line (§6.13) is amended by two fields and otherwise verbatim:

> M-UX-02**a** · <date> · PASS | FAIL · blank-to-verdict, **mode measured:
> 1→N** · <theme> theme · clock S1 first paint → first verdict render
> (S3/S4/S5) · start <hh:mm:ss> · end <hh:mm:ss> · elapsed <m:ss> vs bound
> 5:00 · design timer <m:ss> · gtm witness reading <m:ss> · fresh user
> affirmed: yes · coaching given: none beyond mode selection · witness: GTM
> · **coverage: 1→N only; M-UX-02b (0→1) remains "designed so, not yet
> timed"**

One voiding condition is added to §6.13's list, from (ii): **a run whose
app was launched against a bound module that is not the authority's bytes
is no record.** Under CX-14-01 that launch does not reach first paint, so
the clock never starts; the condition is written down anyway, because a
timing record produced from a build serving pre-R-10 copy would be a
measurement of a product this catalogue did not specify. Concretely: the
sitting is launched from the repository root, and the launch directory is
recorded beside theme and mode.

**Scope of this section.** No string minted, no state added, no rule
changed on any rendered surface — (i) and (ii) are evidence and an open
row, (iii) enumerates one more retrigger, (iv) narrows a claim. The
catalogue's honesty ledger is unchanged in content and one item longer in
what it admits it does not yet cover, which is the direction it is supposed
to move.

**6.15 Round-15 — CX-14-01 closed on this seat's own re-run, and the copy
census extended to the rendered text the catalogue never claimed
(2026-08-31, negotiation round 15).** Append-only; §6.5–§6.14 untouched.
§6.12(a) and §6.12(b) are amended in the two places named below and are
otherwise unchanged. No string is minted, no state added, no rendered
surface altered by this section.

**(i) CX-14-01 · CLOSED, 2026-08-31, on this seat's own re-run.** §6.14
opened it dated and OPEN, owner engineering, closing "only on my own
re-run" — that re-run is done and is recorded here with its outputs, not
with a citation of anyone's packet:

```
$ cd /tmp && .venv/bin/python -c "import importlib, pathlib; m=..."
FILE:                    /Users/…/ProMgtAI/pairwisepm/strings.py
CTA present:             True                 # str.empty.example_cta
str.verdict.stale:       'Inputs changed — the verdict above no longer
                          applies. Press Compare to recompute.'
bytes == authority:      True                 # vs leaves/design/strings.py
site-packages/pairwisepm/: absent (editable .pth only)
```

All four are the conditions §6.14(i) named. The pre-R-10 "Recomputing…"
tail — an auto-recompute this build does not perform — is no longer
reachable from any working directory on this machine, and the bound module
is the authority's bytes rather than a file that merely compares equal to
them. **CX-14-01 is closed.** Its lesson is kept, not retired: §6.12(a)'s
chain still terminates on the bound module, because what closed here is one
instance, not the class.

**(ii) One correction absorbed, from sequencing's measurement.** Sequencing
tested the launch claim rather than repeating it and found that
`python app.py` puts the *script's* directory on `sys.path[0]`, so the
documented launch bound the in-repo copy even before the fix; the stale
binding was reachable through `-c`, a REPL, or an off-root pytest session.
This catalogue's voiding condition survives that correction unchanged
**because its predicate was never the working directory**: §6.14(iv) voids
"a run whose app was launched against a bound module that is not the
authority's bytes." That is the right predicate and it stays. What is
narrowed is the *reason* the launch directory is recorded beside theme and
mode: it is a disambiguating field for a voided run, not a precondition of
a valid one. Recorded here so that no future reader inherits a stronger
claim than the one that was measured.

**(iii) §6.12(a) amended — the chain names one authority, and the interface
has three.** Since §6.11 the chain has read `states.md → strings.py →
vendored copy → bound module → browser`. Every link of it governs **the
catalogue's strings**. This seat audited what else reaches the browser as
text and found two populations the chain has never covered, both verified
from this seat this round:

**CX-15-01 · configs/\*.yaml carries rendered copy, under no copy
authority.** The mode schemas are described everywhere in this build as
*policy values* — the D1/D2 subject. They are also a text file that renders
to the user. Governed by nothing today:

| Field | Renders as | Trust weight |
|---|---|---|
| `label` | mode toggle option | mode identity |
| `factors[].name` | input label, leverage bars, path-to-parity, fragility line | names the lever the user is told to move |
| `factors[].scale` | input label suffix (`app.py:736`) | the anchor that replaces a soft 1–10 guess |
| `factors[].rationale` | the input's help text (`app.py:748`) | why this factor exists at all |
| `flags[].name/.description` | ceiling routing | the "not averaged in" refusal |
| `evaluative_inputs[].name/.note` | captured-not-scored inputs | the Spine's excluded-from-score boundary |

The 0→1 banner is the one config text field that IS governed — `app.py:73`
asserts `Z2O.banner == S["str.banner.01"]` at import. That single line is
the proof the mechanism is available and cheap; it covers one field of
seven. The rest are guarded only by `test_engine.py:201-202`, which asserts
`rationale.strip()` and `scale.strip()` — **non-empty, not correct**. A
rationale replaced with "TBD" passes every test in this repository.

The exposure is dated, not hypothetical: **the D1/D2 resolution round edits
these files tomorrow.** Engineering's duty there is explicitly YAML-only,
which is the correct scope — and it lands inside a file where a numeric
policy change and a copy change are the same edit to the same six lines,
with no per-line notification, no retrigger, and no test that would notice.

**CX-15-02 · twenty rendered strings are literals in `app.py`.** A complete
census this round (AST walk over every `gr.*` call's `label`, `info`,
`placeholder`, `value`, `choices`, and positional text), not a sample:

- Trust-bearing (4): `"A · Strategic fit (not scored)"`, `"A · Brand fit
  (not scored)"` and their B twins, `app.py:841-845`. The `(not scored)`
  suffix is the Spine's "evaluative factors … EXCLUDED from the mechanical
  score" made visible in the interface. Delete four parentheticals and the
  refusal is silently withdrawn from the screen while the engine still
  honors it, every test green — a build that keeps the promise and stops
  telling the user it is keeping it.
- **A cross-reference the catalogue cannot keep (1):** `str.verdict.stale`
  reads "Press **Compare** to recompute." The button it names is the bare
  literal `"Compare"` at `app.py:849`. The catalogue owns the sentence and
  does not own the noun in it. Rename that button and R-10's stale-state
  copy — minted precisely because it must state what the app actually does
  — instructs the user to press a control that no longer exists. Nothing
  fails. This is the R-10 defect class with the arrow reversed: not stale
  copy about a live control, but live copy about a renamed one.
- Structural/neutral (15): `"Mode"`, `"Idea A — name"` / `"Idea B — name"`
  and their placeholders, `"⇄ Swap A/B"`, four `"**Idea A/B**"` column
  headers, `"Compare"`, `"### Your decision"`, `"Which do you actually
  pick?"` with choices `["Idea A", "Idea B"]`, the rationale label, and
  `"Your decision log"`.

`"Which do you actually pick?"` is listed as structural but sits on the MP-2
line: it is the wording that makes the log a record of the *user's* pick
rather than of the model's, and it is a literal.

Accordingly **§6.12(a)'s chain is amended to name its own coverage**:

> `states.md → strings.py → vendored copy → bound module → browser`
> governs **the catalogue's strings only**. Two further populations reach
> the browser as rendered text: `configs/*.yaml` text fields (CX-15-01) and
> `app.py` literals (CX-15-02, census above, 20 as of round 15). Any
> certification of the form "no rendered text changed" that rests on a
> catalogue diff, a `cmp` of the mirror, or a bound-module check is
> **scope-limited to the catalogue** and must say so.

That restatement applies to this seat's own past certifications first: every
"nothing rendered changed" filed here since §6.10 was true of the catalogue
and untested for both populations above. Same correction shape as
§6.14(i), one level wider — an instrument certified against a check
narrower than the claim it was carrying.

**(iv) §6.12(b) amended — (b6) rendered text outside the catalogue.** A
change to any `configs/*.yaml` text field enumerated in CX-15-01, or to any
`app.py` literal in the CX-15-02 census, is a **retrigger event and a
per-line-notification event**, on the same footing as a catalogue mint. The
bright line for tomorrow's resolution round, stated before the round rather
than after it: **`prior_weight`, `sign`, `seed_mean`, `seed_std`,
`transform`, `plausible_range` are policy values and change freely under
the D1/D2 record with no design involvement. `label`, `name`, `scale`,
`rationale`, `description`, `note` are copy.** A resolution-round edit that
touches only the first list needs nothing from this seat; one that touches
the second is a copy change wearing a config change's clothes.

**(v) MP-1 re-verified from this seat, not assumed.** The one invariant this
catalogue would rather die than lose is that no probability renders without
its interval. Verified this round against as-built `app.py`: every
probability reaches the page through `prob_token(p, lo, hi)` — winner token
(`:145-146`), placeholder preview (`:196`), too-close line (`:229`),
equal-weight ablation, both ladder rows (`:368-373`), and the log-confirm
line (`:611`). There is no p-only call site, `str.mp1.nointerval`
("interval unavailable — probability withheld") is the defined behaviour
when the interval is missing, and the only bare percentage in the interface
is the audit view's override rate at `:413`, which is a frequency over the
log and not a model probability. **Zero naked-probability paths.** Stated
with its own scope: this is a source-level audit of call sites, one link
short of the browser, and it is not a substitute for a render session.

**(vi) D8 contingency — the 0→1 leg, pre-written and INACTIVE.** Decisions'
D8 asks who measures the 0→1 half; the entry is theirs and this seat does
not vote in it. What this section removes is the cost of one branch: if
option 3 wins (an 0→1 leg recorded as an explicitly non-fresh, non-
converting secondary datum), the protocol below is already written, so the
decision costs no design round and can be taken while the user is still in
the room.

> **§6.12-b leg (INACTIVE until D8 resolves).** Same clock definition by
> state ID: S1 first paint → first verdict render (S3/S4/S5), 0→1 mode.
> Run *after* the M-UX-02a run, same sitting, same witness. Line:
>
> M-UX-02b · <date> · SECONDARY, NON-CONVERTING · blank-to-verdict, mode
> measured: 0→1 · elapsed <m:ss> · **user was NOT fresh — had already
> completed a 1→N run this sitting** · therefore this datum does NOT
> discharge M-UX-02b and SC-06's 0→1 half continues to read "designed so,
> not yet timed" · recorded because a measured number with its limits
> stated is worth more than an absence, and less than a fresh run.

The qualifier is the point of the leg, not an apology attached to it: a
second-run figure measures a user who has seen the interface, which is a
different quantity from the one SC-06 names. Recording it *as* that
different quantity is the honest version; letting it quietly convert the
row is exactly the overstatement this catalogue exists to prevent. If D8
picks option 1 (deliberate non-measurement) this leg is deleted, not left
dormant — an inactive protocol that outlives its ruling is the ceremony
this seat warns others about.

**Scope of this section.** Two amendments (§6.12(a) coverage statement,
§6.12(b6)), one row closed on own evidence, two rows opened with exact
censuses, one invariant re-verified with its own limits named, one
contingent protocol held inactive. No mint, no mirror change, no red test
introduced anywhere, and nothing that touches the resolution round's
ordering or the M-UX-02a sitting.

**6.16 Round-16 — every catalogue state that was resting on a re-run is
re-based on an instrument, the voiding condition gets its command, one
retrigger is pre-priced with its check list, and the census is re-anchored
after it went stale in a single round (2026-08-31, negotiation round 16).**
Append-only; §6.5–§6.15 untouched in substance. §6.12(a) gains a third
scope word (i); §6.12(b5) gains a named pre-priced case (iii); §6.13/§6.14
Branch A gains one field (ii). No string minted, no mirror change, no
rendered surface altered.

Verified from this seat before writing anything below: mirror
byte-identical (`cmp leaves/design/strings.py pairwisepm/strings.py`,
clean, own run); from `/tmp` the bound module is
`/Users/…/ProMgtAI/pairwisepm/strings.py`, CTA key present, `str.verdict.stale`
tail `'…Press Compare to recompute.'`, bound bytes == authority bytes;
`pytest tests/test_vendoring.py` 6 passed in 0.03s run from `/tmp`; full
suite 67 passed in 1.50s.

**(i) CX-14-01's closure RE-BASED on the artifact, and what a re-run adds
— stated instead of implied (compliance's demand, accepted whole).**
§6.15(i) closed CX-14-01 on this seat's own re-run because §6.14 had
promised exactly that. Compliance's objection is correct and it is this
catalogue's own rule turned inward: **a row closed on a re-run is closed on
memory.** The re-run is a dated observation about one moment; it cannot
red tomorrow. So the closure is re-based:

> **CX-14-01 · CLOSED · closing instrument: T-VEND-05**
> (`tests/test_vendoring.py::test_bound_module_carries_the_r10_corrected_copy`).
> Read from this seat rather than cited: it asserts on
> `importlib.import_module("pairwisepm.strings")` that
> `str.empty.example_cta` is present and that `str.verdict.stale` ends
> "Press Compare to recompute." with no "Recomputing" — the two R-10 facts
> by name — and it carries **no skip predicate at all**.

What the re-run adds, since the demand asked and the honest answer is
"less than it looks": it established the dated *moment* of closure and it
confirmed a fourth fact T-VEND-05 does not assert — that the bound module's
bytes equal the authority's, i.e. that the whole catalogue and not only the
two pinned values arrived. That fourth fact is T-VEND-02's, and T-VEND-02
skips (below). So the re-run's residual contribution is: on a repo
checkout, on one day, the *whole* catalogue was delivered. It is a
snapshot, filed as a snapshot, and it is not what the row rests on.

**Third scope word on §6.12(a) (compliance's notch, accepted and applied to
this seat's own record first).** The chain's coverage statement now reads
in three parts, not two:

> file-identical ≠ copy-delivered (§6.14(i)); copy-delivered-**in-a-checkout**
> ≠ copy-delivered-**on-an-install** (this section); and every link governs
> the catalogue's strings only, not the CX-15-01/02 populations (§6.15(iii)).

The mechanism, verified by reading the guards rather than by report:
T-VEND-01 and T-VEND-02 both `pytest.skip("stripped deployment: design leaf
not present")` when `leaves/design/strings.py` is absent — which is precisely
the tree a user installs. So **every "mirror byte-identical" certification
this seat has filed, including the one four paragraphs above, is evidence
about a checkout and silent about a shipped install.** T-VEND-05 is the
only clause on this board that speaks about served copy on a stripped
install, which is the second reason the row is re-based onto it and not
onto a `cmp`.

**(ii) The voiding condition is CHECKED, and here is the command (decisions'
D9 demand, answered directly).** §6.14(iv) voids "a run whose app was
launched against a bound module that is not the authority's bytes."
Decisions asked whether that is adjudicated or executed. Answer:
**executed, by a command, before the clock starts.**

> **Pre-flight (design-side, M-UX-02a):** on the machine that will serve
> the sitting, from any directory, run `pytest tests/test_vendoring.py`.
> **CONTESTED (D10) — the next sentence is this seat's reading of what a
> SKIP in that command means; compliance's row reads it the other way and
> the entry is open with SLA 2026-09-02. It stands as written, unamended
> and undeleted, per §6.19(iv); nothing about the scheduled sitting changes,
> because from a checkout the command reads 0 skipped and all three readings
> agree.** The governing clause is T-VEND-05; T-VEND-02 is welcome when it
> runs and is not required, because it skips on a stripped tree. The result is
> recorded as a field on the Branch A line. This is the same command as
> compliance's gate P-14 and gtm's 1c-i pre-flight — one command, three
> instruments, no third procedure invented here.

Branch A's line (§6.13, amended §6.14(iv)) gains one field and is otherwise
verbatim:

> … · fresh user affirmed: yes · coaching given: none beyond mode selection
> · **pre-flight `pytest tests/test_vendoring.py`: green | red, run
> <hh:mm:ss> before clock start** · witness: GTM · coverage: 1→N only;
> M-UX-02b (0→1) remains "designed so, not yet timed"

Two consequences stated now so nobody rules on them at the hour. **If the
pre-flight reds, the sitting does not start** — and that is *not* a void.
A void is a run that happened and produced no record; a sitting that never
opened routes to Branch B (WINDOW CLOSED) with the cause named, which is
the routing sequencing already encoded. **And the pre-flight's own scope
is stated on the same line it is claimed**: green means the catalogue's
strings reached the bound module. It says nothing about `configs/*.yaml`
text or the `app.py` literals (CX-15-01/02). A presenter who reads a green
pre-flight as "the copy on screen is the copy that was reviewed" has
overstated it by exactly two populations, and this catalogue will not let
its own instrument be quoted wider than it measures — the §6.15(iii)
correction, applied the first time the instrument is used rather than in
the audit afterwards.

**(iii) ENG-CSS-MIGRATION-01 pre-priced as a named case under §6.12(b5)
(engineering's demand, accepted — with the two conditions that keep the
pricing honest).** Engineering's argument is right and it is a failure mode
this seat should have priced itself: *an unscoped retrigger on a one-line
delivery change is a standing reason never to make the change*, which is
how a deprecated private attribute becomes permanent load-bearing
infrastructure for the Spine's own accuracy disclaimer. §6.12(b5) is not
weakened — the migration still triggers — but its session is scoped in
advance:

> **Pre-priced case CSS-DELIVERY.** Moving `css=_CSS` from the
> `gr.Blocks(...)` constructor to `launch(css=...)` triggers a
> **DELIVERY-VERIFICATION session, explicitly NOT a copy session.** The
> check list is fixed now, lifted from the §6.9 mechanism evidence and the
> §6.11 session-4 rows, and is complete — no check is added at the hour:
>
> 1. `str.banner.01` painted **verbatim** in 0→1, absent in 1→N (S8).
> 2. Computed `position: fixed` on `#pwpm-banner` (rule *applied*).
> 3. Banner rect fully within the viewport at scrollY 1500 (rule
>    *effective* — the §6.9 sticky-that-never-engaged counterexample is
>    what this check exists for).
> 4. Spacer computed height **== banner height exactly** (content-exact
>    reservation, no magic pixels) and no overlap with the mode toggle.
> 5. Zero fixed-position breakers (`transform`/`filter`/`perspective`/
>    `contain: paint|layout`/`will-change: transform`) between banner and
>    root.
> 6. Opaque banner background — nothing ghosting through at any scroll.
>
> **The pricing holds only while both conditions hold**, and both are
> checkable by the person doing the migration: (α) the CSS **text** is
> byte-identical across the move — a `diff` of the old and new `_CSS`
> string is empty; (β) no catalogue string, `configs/*.yaml` text field, or
> `app.py` literal changes in the same push. If either fails, the
> pre-pricing lapses and the unscoped §6.12 trigger applies, because then
> the change is not the one that was priced.

Why this seat gives it away cheaply: the banner is the Spine's "0→1 mode
never claims predictive accuracy" made visible, and today it reaches the
browser through a deprecation fallback (`demo._deprecated_css`, read at
`gradio/blocks.py:2785` on the installed 6.26.0 — engineering's finding,
cited as theirs). A trust surface delivered through a deprecation fallback
is a trust surface on notice; a retrigger priced so heavily that the fix
never lands is this catalogue funding its own exposure. Six checks named
in advance is a smaller price than an unstyled disclaimer.

**(iv) Dispute B4 — RESOLVED, and engineering was right.** This seat asked
for a `STRINGS['str.verdict.stale']` assertion inside T-VEND-01;
engineering declined and filed it rather than burying it, which is the
correct handling and is recorded as such. The refusal was correct on the
merits: T-VEND-01 compares two *files* and skips on a stripped tree, so the
assertion would have been in the one guard least able to carry it. The
substance landed in a better instrument the same round — T-VEND-05, which
asserts the tail on the **bound module** and never skips. This seat asked
for the right assertion in the wrong home; the demand is discharged
stronger than it was made, and there is nothing outstanding between the two
seats on it.

**(v) The 0→1 secondary observation HAS a destination — named, and it is
not a number (gtm's demand, accepted).** Answer: **yes, this catalogue will
receive it**, and the line it lands on is created here so the leg is never
run with nowhere to send it.

> **§6.16-OBS · 0→1 second-exposure observation (INACTIVE until D8
> resolves; deleted, not left dormant, if D8 picks option 1).**
> Destination: appended to this catalogue as an **observation**, never as a
> record. Its content is **defect information keyed by STATE ID** — the
> state the second-exposure user stalled in (S1 empty, S2 partially-filled,
> S11 error recovery, S12 mode transition, S13 evaluative separation),
> what they looked for and did not find, and in which state they asked a
> question. Shape:
>
> §6.16-OBS · <date> · OBSERVATION, NON-CONVERTING · 0→1, second exposure ·
> stall states: <state IDs, in order> · what was sought: <verbatim, if the
> user said it> · **user was NOT fresh — had already completed a 1→N run
> this sitting** · this is defect information about states, NOT a
> measurement of SC-06; M-UX-02b continues to read "designed so, not yet
> timed" and no figure from this leg is sayable in any payload.

The division of labour with §6.15(vi) is deliberate and both halves are
non-converting: **(vi) holds the elapsed figure** with its disqualifier;
**§6.16-OBS holds where the user stalled**. Of the two, the second is the
one this seat actually wants — a second-exposure stall still names a state
whose copy or affordance is weak, and that is true regardless of freshness,
whereas an elapsed time from a coached second run is a quantity SC-06 does
not name. gtm bound this harder than asked (item 6 disallows a
seen-the-app re-run as a stand-in, with no exemption carved for this leg),
and that is why it can be received at all: a bounded observation with a
named destination is evidence about states; the same observation with no
destination becomes a quotable number by default, which is the failure both
seats exist to prevent.

**(vi) CX-15-02's cross-reference item CLOSED on an artifact, and the
census RE-ANCHORED because it went stale inside one round.** Two things
happened to the census this round and both are worth writing down.

*Closed.* §6.15(iii) named one cross-reference the catalogue could not
keep: `str.verdict.stale` says "Press **Compare** to recompute." and the
button was a bare literal. Engineering bound it — verified from this seat
by reading `app.py`, not by report:

```
_COMPARE_LABEL = "Compare"
assert S["str.verdict.stale"].endswith(f"Press {_COMPARE_LABEL} to recompute.")
```

Import-time, same mechanism as the banner assert. Rename the button now and
the app refuses to start rather than instructing a user to press a control
that does not exist. **CX-15-02's cross-reference item is CLOSED**; the
other 20 literals stay open, and the four `(not scored)` labels are
correctly deferred to the first release after the sitting
(ENG-COPY-EVALLABELS-01, registered in `app.py` by engineering at this
seat's request — this seat asked for that deferral and will not be heard
asking for it earlier).

*Re-anchored.* §6.15's census cited `app.py:841-845` and `:849`. Those
literals now sit at `:884-888` and `:892` — moved twice inside this single
round by comment-block edits that changed **nothing rendered**. A census
pinned by line number is an instrument that goes stale on an edit with no
rendered effect, which is the same species of defect as an instrument
narrower than its claim: it reds, or misleads, on the wrong event. The
census is therefore re-anchored **by identifier and literal text**, and its
count is re-based on a stated predicate so any seat can re-derive it:

> **Predicate:** AST walk of `app.py`; every `gr.*` call; positional string
> constants plus the keyword arguments `label`, `info`, `placeholder`,
> `value`, `choices` (list elements counted individually). One hit,
> `gr.Textbox(value="")`, is excluded as rendering no text.
> **Result, own run this round: 21 rendered strings** — 20 string constants
> plus `Compare`, which is no longer a constant (it is `_COMPARE_LABEL`,
> asserted at import).

That is **one more than the 20 this seat stated in §6.15**, and the
correction is filed against this seat's own record rather than left for a
later reader: the round-15 figure narrated the two `choices` elements
`["Idea A", "Idea B"]` as a single list item while counting them as one,
and a hand-narrated list is exactly the honor system §6.15 was written to
end one file over. The number was wrong by one in the direction that
flattered the census. **The census is now the predicate, not the list** —
the list is a rendering of it, and the figure is whatever the predicate
returns on the day it is run.

**Scope of this section.** One row re-based onto an instrument, one scope
word added, one voiding condition given its command and its own coverage
limit, one retrigger pre-priced with a fixed six-check list and two lapse
conditions, one dispute resolved in the other seat's favour, one
observation destination created inactive, one census item closed and the
census re-anchored with a self-correction of its count. No mint, no mirror
change, no red test, nothing that touches the D1–D6 resolution round's
ordering or the M-UX-02a sitting's protocol beyond adding one recorded
field to a line that was already pre-written.

**6.17 Round-17 — three of the seven "rendered" config fields do not render,
the census is partitioned so a trigger names a set rather than a census, the
copy authority is ruled (split, and only one third of it permanently
partial), and the fixture that makes the rendered half machine-diffable is
created (2026-08-31, negotiation round 17).** Append-only; §6.5–§6.16
untouched in substance. §6.15(iii)'s CX-15-01 table is corrected in place by
(i); §6.15(iii)'s CX-15-02 list is partitioned by (ii); no string minted, no
mirror change, no rendered surface altered, no test made red.

Verified from this seat before writing: full suite **72 passed in 1.49s**
(own run); the census predicate re-derived (below); the new fixture
round-trips **GREEN** against live `configs/*.yaml` and `app.py`. Re-run
after writing this section: **73 passed in 1.47s** — one clause landed from
another seat between the two runs, and both numbers are left visible rather
than overwritten, for sequencing's reason: a pin showing only the last number
hides the volatility that makes a pin worth distrusting. Neither of this
seat's two edits is a test; the delta is someone else's and is reported, not
certified.

**(i) SELF-CORRECTION, and it is the round's real finding: three of the seven
config fields this catalogue declared "rendered" do not reach a browser at
all.** §6.15(iii) published a table asserting that `flags[].name`,
`flags[].description`, `evaluative_inputs[].name` and
`evaluative_inputs[].note` render. This seat went looking for their call
sites this round rather than re-asserting the table, and there are none:

| Field | §6.15 claimed | Actually |
|---|---|---|
| `label` | mode toggle | **RENDERS** — `gr.Radio(choices=[N2N.label, Z2O.label])`, plus four audit rows |
| `factors[].name` | input label, leverage, parity, fragility | **RENDERS** — all four |
| `factors[].scale` | input label suffix | **RENDERS**, with one shadow: for `risk_surface` the suffix is replaced by `S['str.factor.risk_label_suffix']`, so that one config string never paints |
| `factors[].rationale` | input help text | **RENDERS** — side A only |
| `flags[].name` | ceiling routing | **DOES NOT RENDER** — the checkbox label is `S['str.factor.ceiling_label']`, a catalogue string |
| `flags[].description` | ceiling routing | **DOES NOT RENDER** — the routing copy is `PINNED_CEILING`, pinned in the engine under T-CEIL-02 |
| `evaluative_inputs[].name` | captured-not-scored inputs | **DOES NOT RENDER** — the four labels are `app.py` literals |
| `evaluative_inputs[].note` | the Spine's excluded-from-score boundary | **DOES NOT RENDER** — no call site anywhere; dead text |

The correction that matters is the last row, and it points the wrong way for
comfort. `note: 'not scored — labeled override input'` sits in both schemas
and reads exactly like the sentence that carries the Spine's refusal to the
user. It carries it nowhere. **The Spine's "evaluative factors … captured and
displayed as labeled override inputs only" reaches a screen through exactly
four `app.py` literals and through nothing else on this board.** Compliance's
T-NEG-08a asserts that refusal in both schemas' `note` — a true assertion
about a field no user can see, which is this cycle's recurring defect
(an instrument whose subject is narrower than the claim it is quoted for)
arriving one more time, in a guard written to close it.

Two consequences, both stated rather than left to be inferred. First, this
**raises** the stake on ENG-COPY-EVALLABELS-01 and this seat still does not
ask for it earlier: a mint plus a mirror update before a timed sitting is the
wrong risk, that was this seat's own ruling, and a finding that flatters the
ruling's reversal is exactly when to keep it. What the finding changes is the
interim, not the date — see (iii)'s eyes-on five. Second, it does not weaken
engineering's edit-class ruling one bit: those three fields are still COPY and
still owe a per-line notification if they move, because a field that is dead
today is one call site away from live and the catalogue is not in the business
of policing which dead text is safe to rewrite.

**(ii) The census PARTITIONED into three classes, so a trigger names a set
(engineering's demand, accepted whole and executed as a partition rather than
a split).** The demand is right about the dynamic: an unbounded trigger on a
21-item census is a standing reason never to fire it, which is how a deferred
fix becomes a permanent one. The census is therefore partitioned, exhaustively
and by identifier-and-text (never by line number — see (vi)):

> **Class (i) · CANDIDATES — literals carrying product meaning whose
> destination is the catalogue. Exactly four, enumerated, closed:**
> `"A · Strategic fit (not scored)"`, `"A · Brand fit (not scored)"`,
> `"B · Strategic fit (not scored)"`, `"B · Brand fit (not scored)"`.
> **This list IS ENG-COPY-EVALLABELS-01's set.** The trigger fires on these
> four and on nothing else; it does not inherit the census. A literal joins
> this class only by a dated amendment to §6.17 naming it individually —
> never by being in CX-15-02, never by resemblance.
>
> **Class (ii) · CROSS-REFERENCED — structural literals that a catalogue
> string names, governed WITHOUT a mint.** Today: `Compare` (CLOSED, §6.16(vi)).
> The mechanism is engineering's and is the pattern for this whole class: bind
> the literal to a module constant, assert the catalogue string's dependence on
> it at import, zero catalogue growth, zero mirror change, and it reds on the
> only drift that matters. **This class, not class (i), is where a structural
> literal goes when the catalogue starts depending on it.**
>
> **Class (iii) · STRUCTURAL — widget nouns and layout affordances that stay
> bare literals by design. Sixteen:** `"Mode"`, `"Idea A — name"`,
> `"Idea B — name"`, the two placeholders `"Idea A"` / `"Idea B"`,
> `"⇄ Swap A/B"`, the four `"**Idea A**"` / `"**Idea B**"` column headers (two
> per mode group), `"### Your decision"`, the two `choices` elements
> `"Idea A"` / `"Idea B"`, `"Which do you actually pick?"`, the rationale
> label, `"Your decision log"`. No mint, ever, absent promotion.

**21 = 4 + 1 + 16**, which is the predicate's own count, so the partition is
checkable rather than narrated. One WATCH note carried openly because burying
it would be the flattering version: **`"Which do you actually pick?"` is
STRUCTURAL by this ruling and it is the one structural literal carrying an
MP-2 obligation** — it is the wording that makes the log a record of the
*user's* pick rather than the model's. It is ruled structural because MP-2's
separation is enforced by the log schema and by the catalogue's own override
strings, not by that question; if that ever stops being true, it is promoted
by amendment. ~~It is covered in the interim by (iii)'s eyes-on five.~~
**STRUCK §6.19(iii) — FALSE WHEN WRITTEN, and the false sentence is quoted
rather than reworded away.** The eyes-on five is a design-side TRUST-WEIGHT
BOUND, not an executed check: gtm deleted its eyes-on pre-flight in round 17
and is not reinstating it, so "covered in the interim" named nothing that
runs. The pick question's interim coverage is re-homed in §6.19(iii); until
the clause named there lands, this literal is an OPEN, DECLARED RESIDUE with
zero instruments, and it says so on this line rather than in a packet.

**(iii) The DEMO-VISIBLE cut (gtm's demand) — answered, and the honest answer
is not the one that was hoped for; a better bound is supplied in its place.**
gtm asked whether the demo-visible subset is five, so the eyes-on check is
bounded permanently. Measured this round against demo-script steps 1–7 rather
than estimated: **it is nineteen of twenty-one, not five.** Steps 1–7 load the
example, compare, re-estimate, flip to 0→1 and re-run, then download the log —
which paints the whole input screen in *both* mode groups (`grp_n2n`
`visible=True`, `grp_z2o` `visible=False`, both painted across the flip at step
6), the decision block, and the file component. Only two literals miss: the two
name **placeholders**, masked from step 1 onward because the example loads
values over them. `"Your decision log"` is `visible=False` until a log write,
so it paints at step 7 and not before.

So **visibility cannot bound the eyes-on list** — bounding it that way would
have produced a nineteen-item pre-flight, the ceremony gtm's seat exists to
delete. The bound is therefore drawn on **trust weight**, which is this seat's
own axis and is permanently smaller:

> **EYES-ON FIVE (permanent, and it cannot grow by accretion).** At the
> pre-flight, look at exactly: the four `(not scored)` labels — class (i) — and
> `"Which do you actually pick?"` — the class-(iii) WATCH item. Nothing else on
> the census is an eyes-on item. **`Compare` is deliberately NOT on this list**:
> it is machine-governed as of §6.16(vi) and reds at import before first paint,
> and re-checking by eye what a machine already refuses to launch without is
> the ceremony this list exists to avoid. A literal joins the eyes-on five only
> by promotion to class (i), which requires a dated amendment naming it.

The predicate behind the five, so a later reader can apply it rather than trust
it: **a literal is eyes-on if its silent corruption would make the demo
narration false while every test stays green.** Delete four parentheticals and
the presenter's tour stop — "captured and displayed, excluded from the
mechanical arithmetic" — is spoken over a screen that no longer says it, with
the engine still honoring the refusal and the suite green. Rename `"Mode"` to
`"Modes"` and the demo is unaffected and the defect is visible in the same
glance the presenter already takes. That is the whole distinction, and after
(i) it is sharper than it was: those four labels are now known to be the
**sole** on-screen carrier of that Spine refusal, the config `note` having
turned out to carry it nowhere.

**(iv) F-32 / F-33 RULED (compliance's demand, answered with a split ruling —
and only one third of it is permanently partial).** Compliance is right that an
OPEN row with no closing condition is a row waiting on nobody, and right to
refuse to invent this seat's authority through a test file. The ruling, by
population, so each row gets a closing condition or a stated reason it has
none:

- **F-32 · `configs/*.yaml` rendered text → answer (a). Destination named and
  created this round: `leaves/design/copy-authority.yaml`.** It is a
  design-owned expected-values fixture, **generated from the live bytes rather
  than transcribed** (a hand-copied fixture is the honor system with extra
  steps), and ratified by this seat today after reading all seven fields in
  both schemas: none is a placeholder, none is a leaked machine key, each is
  the text this catalogue would approve. Compliance owns the diff test; design
  owns these bytes. Verified before filing: round-trip against live
  `configs/*.yaml` and `app.py` is **GREEN**, and the suite is **72/72**, so
  the fixture lands green rather than handing anyone a red on the eve of the
  resolution round.
  **Deliberate non-coverage, and it is what keeps the fixture safe:** the
  policy/numeric fields (`prior_weight`, `sign`, `seed_mean`, `seed_std`,
  `transform`, `plausible_range`) are **absent by design**, so the D1/D2
  resolution round cannot red this file. It reds on exactly one event — a text
  field moving without design ratification — which is §6.12(b6)'s per-line
  notification converted from a procedure into an instrument. That conversion
  is the thing this seat wanted most this cycle: the notification was a promise
  five seats had accepted, and a promise is not an instrument.
  The fixture also carries a `render_map` recording (i)'s finding per field, so
  the diff test's own scope is readable from the artifact: four fields ratified
  **and rendering**, three ratified **and not rendering**, one shadowed on a
  single factor.

- **F-33, class (i) CANDIDATES (4) → answer (a), with an interim instrument
  and a real closing condition.** Interim target: the fixture's
  `app_py_candidates` list, four exact strings, diffable today. Closing
  condition: the row closes when the four move into the catalogue at
  ENG-COPY-EVALLABELS-01, at which point the catalogue's own chain governs them
  and the fixture entry is deleted rather than left dormant.

- **F-33, class (ii) CROSS-REFERENCED (1) → CLOSED**, instrument = the
  import-time assertion at `app.py`'s `_COMPARE_LABEL`. Recorded in §6.16(vi).

- **F-33, class (iii) STRUCTURAL (16) → answer (b): PERMANENTLY PARTIAL by
  decision, owner design.** The reason, in the form compliance can register
  verbatim: *minting a catalogue entry for a widget noun buys a diff test and
  pays for it with a mirror-sync obligation on every layout edit, while the
  failure it prevents — a mislabeled button — carries no Spine refusal and is
  visible in the same glance a presenter already takes at the screen. The
  catalogue is for copy that makes a claim; these make none.* **Revisit
  events, both named so this is not a revisit-on-memory:** (α) a catalogue
  string acquiring a cross-reference to one of the sixteen — that promotes it
  to class (ii), governed by an import assert, not by a mint; (β) product
  meaning arriving on one — a dated amendment to (ii) above moving it to class
  (i). Absent (α) or (β), this third stays partial forever and that is the
  ruling, not a deferral.

**(v) Decisions' question answered in this file, in one line, as asked.**
Answer **(a)**: §6.14(iv)'s voiding condition is **CHECKED, by a command,
before the clock starts** — `pytest tests/test_vendoring.py`, governing clause
T-VEND-05, and its result is a **recorded field on the Branch A line**
(§6.16(ii), which is where the clause and the amended line already live; this
paragraph is the pointer decisions asked for, since a reader of §6.13 should
not have to reach §6.16 to learn that the condition is executable). The same
command is compliance's gate P-14 and gtm's 1c-i pre-flight: **one command,
three instruments, no third procedure.** Its scope travels with it, on the
same line it is claimed: green means the catalogue's strings reached the bound
module, and after (iv) it also means — for the first time — that the
`configs/*.yaml` rendered text is diffable against a ratified fixture. It
still says nothing about the sixteen structural literals, and that is now a
ruling rather than a gap.

**(vi) Census re-derived, and the line numbers moved a THIRD time inside a
single round.** Predicate unchanged from §6.16(vi) (AST walk of `app.py`;
every `gr.*` call; positional string constants plus `label`, `info`,
`placeholder`, `value`, `choices` with list elements counted individually;
one empty `value=""` excluded as rendering no text). **Result, own run this
round: 20 string constants + `Compare` (a constant reference, asserted at
import) = 21** — identical to §6.16's figure, so the count is stable while the
addresses are not. The four `(not scored)` labels sat at `:841-845` in round
15, `:884-888` earlier in round 16, and `:892-896` as of `app.py`'s 20:45
revision today. Three moves, zero rendered changes, one round. The
re-anchoring by identifier-and-text is doing exactly the work it was created
for, and the partition in (ii) is written the same way for the same reason: a
class defined by line number would have to be re-derived every time someone
adds a comment.

**Scope of this section.** One published table corrected against this seat's
own record on three of eight rows, one census partitioned into three classes
with an enumerated four-item trigger set, one eyes-on list bounded permanently
at five on a stated predicate, two matrix rows ruled (one instrumented with a
new design-owned fixture, one closed, one declared permanently partial with two
named revisit events), one pointer added for a question answered in §6.16. No
string minted, no catalogue entry added, no mirror change, no rendered surface
altered, no test made red, and nothing that touches the D1–D6 resolution
round's ordering or the M-UX-02a sitting's protocol.

---

**6.18 Round-18 — `app.py` has TWO rendering surfaces and this catalogue has
only ever censused one of them; the audit view's four statistics render pooled
across modes, one of them under a caption that denies the very data it is
computed from (2026-08-31, negotiation round 18).** Append-only; §6.5–§6.17
untouched in substance. §6.16(vi)/§6.17(vi)'s census predicate is corrected in
scope by (i); §S14a's row list is corrected by citation in (ii); no string
minted, no catalogue entry added, no mirror change, no rendered surface
altered, no test made red, `leaves/design/copy-authority.yaml` deliberately
not touched (compliance's diff test is being written against the bytes filed
last round, and a fixture that moves under its own instrument is worse than no
fixture).

Verified from this seat before writing: full suite **73 passed in 1.30s** (own
run, venv interpreter — a count reported without its interpreter is not a
pin, decisions' rule, adopted). Both findings below are DEMONSTRATED by
execution, not read off the source: the probes are in this seat's scratchpad,
no repo file mutated, and the honest artifacts of each probe are reported
alongside its result.

**(i) THE ROUND'S FINDING, and it is a scope defect in this seat's own
published census: `app.py` paints text through two surfaces, and the census
covers one.** §6.16(vi) fixed the census predicate as *an AST walk of `app.py`,
every `gr.*` call, positional string constants plus `label`/`info`/
`placeholder`/`value`/`choices`*. Every literal that surface builds is
therefore counted — 21, partitioned in §6.17(ii). But the app also paints text
that never passes through a `gr.*` constructor: six functions
(`render_placeholder`, `render_stale`, `render_verdict`, `render_leverage`,
`render_ladder`, `render_audit`) return HTML strings that reach the screen
through one component (`gr.HTML(render_audit(DecisionLog(), 0))`, `app.py:940`,
and its update siblings). To the census predicate that call site is a single
`gr.*` call with a *non-constant* positional argument, so it contributes
**zero** literals — while what it actually paints is a whole table of prose.

Enumerated this round, by AST walk of `render_audit` and by reading the live
rendered HTML from a real `DecisionLog` (both in scratch), the audit view alone
paints **thirteen** strings that exist in no catalogue and in no census:

> `Audit` · `Decisions logged` · the count template ` (1→N: {}, 0→1: {})` ·
> `ζ (consistency)` · `accumulating — needs 3 ideas` ·
> `Brier (model vs. your picks)` · `n/a — no decisions yet` ·
> `Brier (vs. labeled outcomes)` · `Override rate` ·
> `Model of the judge ({mode label})` · `Order-bias diagnostic ({mode label})` ·
> `free intercept {b} (z = {z}) — no measured order bias` ·
> `Reliability curve ({mode label})`

In the same table, **ten catalogue IDs** do render (`str.audit.m1_locked`,
`str.audit.curve_locked`, `str.audit.zeta_gloss`, `str.audit.brier_gloss`,
`str.audit.01_caption`, `str.m1.active_chip`, `str.orderbias.headline`,
`str.orderbias.body`, `str.log.empty`, `str.log.unsaved_nudge`). So the audit
view is a **mixed surface**: 13 uncatalogued literals interleaved with 10
catalogue strings, and nothing on the surface tells a reader which is which.
~~Three of the thirteen are honesty-carrying, not decorative —~~
`accumulating — needs 3 ideas` and `n/a — no decisions yet` are the refusals
that keep a locked metric from reading as a computed one, and
`— no measured order bias` is a **negative diagnostic finding stated in the
app's own voice** with no catalogue entry behind it.

> **STRUCK §6.20(i) — UNDERCOUNT, and the false clause is quoted rather than
> reworded away.** "Three of the thirteen are honesty-carrying" was this seat's
> own figure and it is wrong by three. The three named above are correct and
> are the whole of one tier — the tier where the app *withholds* a number. It
> missed the tier where the app *bounds* a number it does give, which is three
> more literals on the same table. The full closed list, its predicate, and the
> 6 + 7 = 13 arithmetic a reader can check against `app.py` are in **§6.20(i)**;
> the count was closed on compliance's demand in round 20 and the correction is
> against this seat, not against theirs.

The second tranche is real and is deliberately **not** given a number this
round, because this seat would be estimating it and an estimated census is the
thing §6.16(vi) exists to refuse. Three members verified by reading the
builders: the parity panel's refusal clause
`; the 60/40 target falls outside the plausible range` (`app.py:349`) — the
sentence in which the leverage panel declines to draw a path it cannot support,
i.e. an MP-3 refusal rendered from a bare literal; its sibling
`: 50/50 would need {x} — {note}` (`:357`); and the blank-name fallbacks
`name_a or "Idea A"` / `name_b or "Idea B"` (`:195-196`, `:292-293`), which put
an uncatalogued string into the **verdict headline** whenever a user leaves a
name empty. **Full enumeration of the five non-audit builders is OPEN, owner
design, closing condition: enumerated in the round after this one or in the
first release after the sitting, whichever comes first.** It is stated as open
rather than guessed.

Two corrections this forces on rulings already registered elsewhere, both owed
by this seat rather than discovered by the seats that hold them:

- **§6.17(ii)'s partition and §6.17(iv)'s F-33 ruling are correct but
  SCOPED**, and neither says so. Both speak of "the census" and the census is
  the `gr.*` construction surface. The "STRUCTURAL (16) → permanently partial"
  ruling is a ruling about widget nouns; it must not be read as a ruling that
  all uncatalogued rendered copy in `app.py` is structural, because thirteen
  strings that were never in the population include three refusals. This is
  precisely the defect species this cycle has been finding in other seats'
  instruments — a claim whose scope is narrower than the reading it invites —
  arriving in the ruling this seat filed one round ago, and it is filed as a
  demand on compliance to carry the scope word rather than left for a reader.
- **ENG-COPY-EVALLABELS-01's set stays exactly four.** §6.17(ii) says a
  literal joins class (i) only by a dated amendment naming it individually, and
  §6.18 is a dated amendment — so the temptation is live and is refused. The
  four `(not scored)` labels are what engineering agreed to move; growing that
  set from a finding filed after the agreement would make a bounded trigger
  unbounded again, which is the exact dynamic engineering's demand was about.
  The new population gets its own name and its own future trigger instead:
  **DESIGN-COPY-HTMLSURFACE-01**, defined in (iv), attached to nothing
  engineering has already accepted.

**(ii) The audit view's four statistics render POOLED ACROSS MODES, and the
mode-scoped caption underneath them contradicts one of the rows it captions.**
`render_audit` calls `log.kendall_zeta()`, `log.brier()`, `log.outcome_brier()`
and `log.override_rate()` (`app.py:416/419/422/425`) with **no `mode`
argument** — every one of those methods accepts `mode` and every one defaults
to the whole log. The surface around them is per-mode everywhere else: the
count row prints the split, the M1 and reliability rows loop `for cfg in (N2N,
Z2O)`, and the 0→1 caption gates on `log.n("zero_to_one")`. **Three scoping
regimes in one table**, and the four bold numbers are the pooled one.

Demonstrated, not argued. Probe A (`zeta_probe.py`): three ideas compared in
1→N, perfectly transitive (A>B, B>C, A>C) → the displayed row reads
**ζ = 1.00**. Add ONE 0→1 comparison of the same two ideas in the other
direction — a different factor set, a different question, not a contradiction —
and the displayed row reads **ζ = 0.00** while `kendall_zeta("one_to_n")` is
still **1.00**. The user is told they contradict themselves constantly at the
moment they were perfectly consistent inside each mode. The mechanism is that
the preference graph keys edges by idea NAME across the whole log, so a
cross-mode re-comparison silently overwrites the earlier edge rather than
being recognised as a different question.

Probe B (`audit_probe.py`, live `render_audit` output): a log of 3 × 1→N +
2 × 0→1 with labeled outcomes renders

> `Brier (vs. labeled outcomes)` **0.286**   … pooled; per-mode it is 0.172
> (1→N) and 0.343 (0→1)

directly above `str.audit.01_caption`: *"0→1 mode: these measure the
consistency of your judgments — they do not predict outcomes. **No outcome data
about ideas like yours exists.**"* The row is scored against 0→1 outcome data
on the same screen where the caption says no such data exists. That is not a
wording problem; it is the Spine's `Out:` line ("accuracy claims in 0→1 mode")
reaching the screen as a number and a denial of the number, one line apart.

Third, quieter, and true of all four rows: **none of the four denominators is
on screen, and none of them is the count that IS on screen.** "Decisions logged
5" is the base of no row — ζ's base is complete triads, Brier's is records
carrying a model probability, outcome-Brier's is labeled outcomes,
override-rate's is decisions with a decisive (non-`too_close`) verdict. In
Probe B the visible count was 5 and the outcome-Brier's base was 3. A bold
three-decimal number over an invisible base is false precision of exactly the
species the Spine's problem statement names ("47.3 versus 44.1 as if that gap
meant something"), rendered by the honesty surface itself.

*Honest artifact of Probe B, reported because a red this seat caused and did
not explain is what this file refuses:* the synthetic 0→1 records were copies
of 1→N records with the mode field changed, so their `z` vectors carry 1→N
factor keys; `training_data(Z2O)` correctly filters them and the row reads
"you have 0 in this mode" while the count row says 2. That mismatch is the
fixture's, not the app's, and is not part of the finding.

§S14a is corrected by citation, not rewritten: its row list —
"decision count (per mode), ζ with plain gloss, Brier with plain gloss,
override rate" — attaches "(per mode)" to the count and is **silent** on the
scoping of the other three. The silence is this catalogue's, the pooling is its
consequence, and (iii) ends the silence with copy rather than with a
complaint.

**(iii) SPEC — the audit statistics block, exact copy, IDs RESERVED and
deliberately NOT minted (see (iv)).** Every statistic row renders as
`VALUE · BASE`, one row per mode that has any decisions, and no row renders for
a mode with none. Wording throughout avoids the substrings `accuracy` and
`predictive`, including in negated form, because §S14c's rule is that even a
negated use fails compliance's sweep on 0→1-scoped strings.

> - `str.audit.row_zeta` — label: `ζ (consistency) · {mode_label}`
> - `str.audit.base_zeta` — value suffix: `· over {t} complete triads from {n}
>   comparisons in this mode`
> - `str.audit.row_brier` — label: `Brier (model vs. your picks) · {mode_label}`
> - `str.audit.base_brier` — value suffix: `· over {n} scored decisions in this
>   mode`
> - `str.audit.base_outcome_brier` — value suffix: `· over {n} labeled
>   outcomes in this mode`
> - `str.audit.base_override` — value suffix: `· over {n} decisions where the
>   model named a winner`
> - `str.audit.outcome_row_01` — **replaces the value, not the label**, on the
>   0→1 outcome row: `not scored against outcomes in this mode — see the note
>   below`
> - `str.audit.zeta_scope` — one line under the ζ rows: `Consistency is
>   measured inside a mode. A comparison you made in 1→N and a comparison you
>   made in 0→1 answer different questions, so they are never counted as a
>   contradiction of each other.`

The 0→1 outcome row is **withheld rather than pooled away**: withholding it
silently would leave the user unable to tell "we do not score this here" from
"you have no outcomes yet", which is the same failure as a locked panel drawn
as an empty one (§S14a's own doctrine, and MP-1's `str.mp1.nointerval` rule
one surface over — when the honest quantity is unavailable, say so in words and
withhold the number, never show a number that has to be mentally discounted).
The base suffixes are the audit surface's version of MP-1's welded interval: a
summary statistic and the base it was computed over are one token, and neither
appears without the other.

**(iv) RULING — none of this is minted, moved or executed before the sitting,
and the refusal is instrument-backed rather than asserted.** Red-first, this
seat's own hands, on a scratch clone with nothing in the repo mutated:
appending one `STRINGS[...]` entry to `leaves/design/strings.py` without a
matching mirror edit takes `tests/test_vendoring.py` from **6 passed to 4
passed, 2 new failures** — `test_vendored_strings_byte_identical_to_design_copy`
(T-VEND-01) and `test_imported_strings_module_is_the_in_repo_copy` (T-VEND-02).
(The clone also carries a pre-existing unrelated failure, T-VEND-04's
two-importable-copies clause, because a scratch tree beside an installed
package is two packages; it is present before and after the mutation and is not
part of the demonstration.) So a mint tonight is a suite that is red until
engineering syncs a vendored file during the round they are writing resolved
D1/D2 values into `configs/*.yaml`. That is the trade this seat refused for
ENG-COPY-EVALLABELS-01 when the finding was smaller, and a bigger finding is
not a reason to take a trade that was refused on its risk.

- **Copy: DEFERRED**, destination the catalogue, trigger name
  **DESIGN-COPY-HTMLSURFACE-01**, set = the thirteen enumerated audit literals
  in (i) plus whatever the open enumeration adds, fires in the first release
  after the M-UX-02a sitting, in a push that carries no other change. It is
  **not** ENG-COPY-EVALLABELS-01 and must never be folded into it.
- **Behaviour (the pooling): NOT design's to execute.** `render_audit` is
  engineering's file and per-mode scoping is code motion, which nobody should
  be doing before the sitting. Filed as a matrix row (demand on compliance)
  with the two demonstrations attached, so it is a row with an owner rather
  than a finding in a packet. It becomes a decisions entry only if a seat
  disputes that the statistics should be mode-scoped; absent a dispute it is a
  defect with a spec, not a contested value.
- **The eyes-on five does NOT grow, and the reason is verified rather than
  asserted.** The four statistics rows cannot paint a number during demo
  steps 1–7: every one of them returns `None` on a log with no records, and
  the demo script as written (§1c, gtm) contains no step that logs a decision —
  it loads the example, compares, re-estimates, flips mode, re-runs, and
  downloads. On a clean session the audit table renders its locked and
  `n/a` text and nothing pooled. The finding therefore costs gtm's pre-flight
  nothing, and §6.17(iii)'s permanent bound of five stands unamended. The one
  condition that would make it reachable on a demo machine is a presenter
  logging decisions in **both** modes with a repeated idea name — stated so it
  is on the record, not added to anyone's checklist.

**Scope of this section.** One census predicate corrected in scope against
this seat's own record, thirteen previously uncensused rendered strings
enumerated with three named as honesty-carrying, one open enumeration declared
open with an owner and a closing condition, one behavioural defect demonstrated
twice by execution with its own probe artifacts disclosed, eight strings
specified exactly and reserved without minting, one deferral ruled with a
red-first demonstration of what minting tonight would cost, and one permanent
bound (the eyes-on five) verified as unaffected rather than quietly extended.
No string minted, no catalogue entry added, no mirror change, no rendered
surface altered, no test made red, `copy-authority.yaml` untouched, and
nothing that touches the D1–D6 resolution round's ordering or the M-UX-02a
sitting's protocol.

---

**6.19 Round-19 — the one rendered field four censuses missed is ruled, the
one structural literal whose interim cover did not exist is re-homed, and both
corrections are made in place with the false sentences quoted
(2026-08-31, negotiation round 19).** Append-only; §6.5–§6.18 untouched in
substance. Three edits are made INSIDE earlier sections and each is a strike
with the struck text left legible, never a rewording: §6.13's pre-flight box
gains a CONTESTED (D10) mark and keeps its sentence (iv); §6.17(ii)'s "covered
in the interim by the eyes-on five" is struck as false-when-written (iii); and
`copy-authority.yaml`'s header numeral is corrected with the wrong figure
quoted beneath it (ii). A fourth strike is added late in the same round and it
is this seat's own: (v)'s green suite pin is struck by (vi), which reports the
Spine's offline-refusal clause failing at the repo root and names the file that
reds it as the one written for this seat's §6.18 finding.

**(i) `banner` RULED — compliance's F-32 residue answered with option (b), and
architecture's demand executed as a RENDER VERDICT rather than as a third
replica.** Two seats filed the same finding from opposite ends and they asked
for different things: architecture asked for the bytes and the map row;
compliance asked for a ruling and explicitly refused to pick. The answer is
one of each, and the reason the bytes are refused is not thrift.

Verified from this seat before ruling, not taken from either packet:
`configs/zero_to_one.yaml:17` holds the banner, `one_to_n.yaml:16` is `null`,
`app.py:91` escapes it into `BANNER_HTML`, `app.py:832` mounts it, `app.py:738`
toggles it visible in 0→1 — and `app.py:73` asserts `Z2O.banner ==
S["str.banner.01"]` at import, so the config field is a REPLICA of catalogue
copy and not an independent authority.

> **RULING.** The banner's copy authority is the catalogue's `str.banner.01`.
> It is **exempt from `copy-authority.yaml`'s `configs:` block** and it is
> **listed in that file's `render_map`** with its authority and its two guards
> named. Compliance's file needs no change: `_RATIFIED_ELSEWHERE` already
> registers exactly this exemption, and T-COPY-02c already checks the citation
> by AST.

**Why the bytes are refused, stated as a cost rather than a preference.**
Today a mint of `str.banner.01` is a TWO-file synchronized edit —
`leaves/design/strings.py` and `configs/zero_to_one.yaml` — held equal by an
import assert that stops the process before first paint. Ratifying the same
sentence here would make it a THREE-file edit held by four instruments, and
the third file is the one with no runtime consequence: a stale
`copy-authority.yaml` reds a test, while a stale config stops the app. Adding
a replica to the weakest-consequence copy raises the probability of the drift
it is meant to catch. **A trust surface is not made stronger by being
duplicated into a place with less consequence** — that is the same doctrine as
MP-1's welded interval read in the other direction, and it is why this seat
takes (b) while agreeing entirely with the finding that produced the demand.

**What architecture was right about, kept whole.** The fixture's `render_map`
announced itself as the statement of "which ratified fields actually reach a
browser" and omitted the one rendered field carrying a Spine refusal onto the
screen. That is a legibility defect of exactly the species this board has been
naming at each other for four rounds — an enumeration read wider than its
population — and it is fixed at the header as well as at the row: the map is
now explicitly the file's SCOPE STATEMENT, and a row without bytes means
*governed elsewhere, authority named*, never *unwatched*.

**(ii) `render_map` completed and the numeral corrected, with the wrong figure
quoted (architecture's demand, accepted whole).** Two rows added:
`evaluative_inputs[].scale` — ratified in these bytes as `0–4` in both schemas
and carrying no render verdict in either direction until tonight; it DOES NOT
RENDER, `cfg.evaluative_inputs` having no call site in `app.py` at all — and
`banner`, per (i). The header's "three of the seven fields design declared
rendered do not render" is struck in place: the declared population was EIGHT
and FOUR do not render. **7−3 and 8−4 both equal 4**, so two wrong premises
produced the right remainder, which is why three seats read past it — the
error was invisible because the arithmetic worked. The map now carries TEN
names and the split is **five renders / five do not**, an arithmetic a reader
can check against the file rather than take on report.

Corrected numbers, so no seat has to reconcile packets: the rendered
config-text population is **FIVE** — `label`, `factors[].name`,
`factors[].scale`, `factors[].rationale`, `banner` — of which four are
ratified in this fixture and one is ratified in the catalogue.

**(iii) `"Which do you actually pick?"` — interim coverage RE-HOMED, and the
old cover is struck as false-when-written (gtm's demand, accepted; gtm's third
option DECLINED and the reason is the agenda, not the cost).** gtm offered
three exits and disclosed that the cause was their own deletion, which is the
disclosure that made the defect findable at all. This seat verified the state
rather than inheriting it: the literal occurs **once in the repository**, at
`app.py:925` (it was `:911` before engineering's comment block moved it; the
line number is cited as a locator and is not load-bearing — §6.17(vi)), and no
clause in `tests/` asserts it.

> **ANSWER: an AST clause, not an eye, and not promotion.** Demand filed on
> compliance for one clause beside T-NEG-08. Promotion to CANDIDATES is
> refused because it would grow ENG-COPY-EVALLABELS-01's set from four to five
> using a finding filed AFTER engineering accepted that trigger on the
> strength of its boundedness — the exact dynamic §6.18 refused for thirteen
> strings, and it does not become acceptable for one. gtm's third option (one
> named eyes-on line, which they offered to carry) is DECLINED even though it
> is free to this seat and cheap to theirs: a presenter's glance is the
> weakest instrument on the board, it is the instrument gtm correctly retired,
> and asking a seat to reinstate the ceremony they deleted in order to cover a
> gap that deletion revealed is trading an instrument for a ritual.

**The residue is declared rather than closed, on the line where it lives.**
§6.17(ii)'s cover sentence is struck in place with the false text legible, and
the struck text now says what is true: until compliance's clause lands, this
literal has ZERO instruments and one standing MP-2 obligation. That is the
honest state and it is written on the surface, not held in a packet — which is
this seat's whole position about what an interface owes a reader, applied to
this seat's own catalogue.

**(iv) §6.13's pre-flight sentence MARKED CONTESTED (D10) and KEPT (decisions'
demand, accepted whole, executed as instructed).** The box's sentence — "the
governing clause is T-VEND-05; T-VEND-02 is welcome when it runs and is not
required, because it skips on a stripped tree" — stands unamended, with a
CONTESTED (D10) mark above it naming the SLA and stating that nothing about
the scheduled sitting changes, since from a checkout the command reads
`0 skipped` and all three readings agree. Decisions' framing is accepted
without reservation and is worth restating because it is the better statement
of this seat's own discipline: **a seat that changes its reading and says what
it moved from has converged; a seat whose sentence is quietly deleted has been
settled.** Marking before the withdrawal is the same discipline §6.15(i)
applied after one.

**(v) Own runs, this seat's hands, after every edit above.** ~~Full suite
**78 passed, 0 skipped** (1.37s, project interpreter, repo root);
`tests/test_copy_surfaces.py` and `tests/test_vendoring.py` green within it.~~
**STRUCK BY (vi), WITHIN THE SAME ROUND — the false pin is quoted rather than
overwritten.** It was true when run and it was false forty minutes later: the
suite is now **80 collected, 79 passed, 1 FAILED** at the repo root and
identically from `/tmp`. The failing clause is not mine and not caused by any
edit above; the pin is struck here rather than silently re-published, because
this seat's whole position is that a surface owes a reader its current state
and a green number left standing after it stopped being green is the
flattering version twice over. Corrected figures and the cause: (vi).
One honest note that goes in because it is the kind of thing this section
exists to record: the FIRST draft of the `render_map` rows **RED THE SUITE** —
`2 failed, 76 passed`, T-COPY-02 and T-COPY-02b — because a plain YAML scalar
containing `: ` broke the fixture parse, and a fixture that will not load
takes both diff clauses down with it. Nothing was mutated in the repo to
discover that; the edit itself was the mutation and the suite caught it in the
change that made it, which is compliance's own instrument working on this
seat's file within a minute of being written. It is recorded rather than
quietly fixed, because a section that reports only the green run is the
flattering version.

**(vi) THE SPINE'S OFFLINE REFUSAL IS RED AT THE REPO ROOT, and the file that
reds it was written for this seat's own §6.18 finding. Reproduced, bisected,
and disclosed here rather than filed only as a demand.**

The Spine's `Out:` line refuses *"any LLM in the runtime loop"* and its
Success-Metrics line promises *"runs entirely offline after download: no API
key, no server-side storage."* The instrument for both is
`tests/test_engine.py::test_no_llm_or_network_imports`. **It fails.**

```
$ .venv/bin/python -m pytest -q          # repo root, project interpreter
FAILED tests/test_engine.py::test_no_llm_or_network_imports
    AssertionError: httpx
1 failed, 79 passed, 8 warnings in 1.64s
```

Identical from `/tmp` (1 failed, 79 passed), so it is not a working-directory
artifact. **Bisected from this seat, four runs, no repo file mutated:**

| Command | Result |
|---|---|
| `pytest tests/test_engine.py` | **45 passed** — green alone |
| `pytest tests/test_copy_surfaces.py tests/test_engine.py` | **55 passed** — green |
| `pytest tests/test_audit_honesty.py tests/test_engine.py` | **1 failed**, 46 passed |
| `pytest tests/test_packaging.py tests/test_engine.py` | **1 failed**, 60 passed |

**The mechanism, stated as a fact and not as a theory.** The clause has two
halves. Half two is a source scan (`^\s*(import|from)\s+(openai|anthropic|…|
httpx|…)` over `pairwisepm/*.py` plus `app.py`) and is position-independent —
**it still passes, and the substantive refusal it guards is intact; no LLM or
network import has entered the shipped source.** Half one asserts that no
forbidden module is present in `sys.modules` *at the moment the clause runs*,
and that is a property of the whole process, not of this seat's product:
importing `app` imports `gradio`, and `gradio` imports `httpx` (verified in a
bare interpreter — `httpx._urlparse`, `httpx._content` and eight siblings land
in `sys.modules` on `import app` alone). So **any test file that loads `app`
and sorts alphabetically before `test_engine.py` reds this clause.**
`test_packaging.py` has loaded `app` for the whole cycle and was harmless
because `p` > `e`. `tests/test_audit_honesty.py` landed this round, loads
`app` through `_app_module()`, and begins with `a`.

**The disclosure this seat owes, first, before the demand.** That file was
written to close the F-34/F-35 rows — the pooled audit statistics and the
unwatched `str.audit.01_caption` gate — which are §6.18's finding, filed by
this seat, in this seat's favour. The new instrument is right, and it covers
the one honesty surface that renders as a NUMBER; nothing here asks for it to
be weakened or moved. **It is nonetheless why a Spine refusal now prints red,
and a finding that arrived through my own row is exactly the one I do not get
to leave for someone else to notice.**

> **THE HARM IS THE REMEDY, NOT THE RED.** The failure line reads
> `AssertionError: httpx` beside a `FORBIDDEN_IMPORTS` tuple. The fifteen-
> second fix visible from that line is to delete `"httpx"` from the tuple —
> and `"httpx"` is there because a *network client in the runtime process* is
> the observable form of the thing the Spine refuses. Deleting it turns the
> only instrument on the offline promise into a green that asserts less than
> it did, in the change that makes it, with the whole suite green behind it.
> **The remedy is process isolation or ordering, never a shorter forbidden
> list, and never `pytest.skip`.** This is the same shape as the vendoring
> board's own doctrine — refresh the install, never hand-edit the snapshot —
> and it is written here because the person who meets this red will be
> reading a failure line, not a packet.

**What this does NOT touch, verified rather than assumed, so no seat re-prices
their hour on it.** The M-UX-02a pre-flight command is
`pytest tests/test_vendoring.py tests/test_copy_surfaces.py` → **17 passed, 0
skipped** (0.09s, own run) — neither file loads `app`, both are AST-and-bytes
readers, and P-14's own file is **7 passed, 0 skipped**. So the sitting, the
witness template's `0 skipped` field, and D9's voiding set are all unaffected,
and the D1–D6 resolution round is untouched. What IS affected is every claim
of the form *"the suite is green"*: the honest sentence at this hour is **80
collected, 79 passed, 1 failed, 0 skipped**, and this seat is publishing that
number rather than the one that flatters the round.

Filed as a demand on compliance, who owns `tests/`. **No test file was edited
by this seat** — not the failing clause, not the new one, not a conftest — for
the reason this board has held all cycle: an instrument repaired by the seat
whose finding created the collision is a census adding rows to the authority
it points at.

**Scope of this section.** One rendered field ruled with its authority named
and its bytes deliberately not duplicated, two `render_map` rows added, one
header numeral corrected with the wrong figure quoted, one false interim-cover
sentence struck in place with the residue declared open, one contested mark
added to a sentence that keeps standing, one own green pin struck in place
within the same round because it stopped being true, one red Spine instrument
reproduced and bisected and disclosed against this seat's own row, two demands
filed on compliance and one gtm option declined with its reason. **No string
minted**, no catalogue
entry added, no mirror change, no policy or numeric field touched, no rendered
surface altered, no test written or weakened, and nothing that touches the
D1–D6 resolution round's ordering or the M-UX-02a sitting's protocol — the
fixture remains policy-free, so engineering's resolution write cannot red it.

---

**6.20 Round-20 — F-34's load-bearing half is closed: the honesty-carrying
literals on the audit surface are named as a CLOSED list of SIX, not three, and
the second population is refused a count pin because its census is open
(2026-09-01, negotiation round 20).** Append-only; §6.5–§6.19 untouched in
substance. One edit is made INSIDE an earlier section and it is a strike with
the struck text left legible: §6.18(i)'s "Three of the thirteen are
honesty-carrying" is struck as an UNDERCOUNT by this seat against itself.
No string minted, no catalogue entry added, no mirror change,
`leaves/design/copy-authority.yaml` NOT touched — these are `app.py`
runtime-HTML literals with no ratified bytes and §6.18(iv) deferred the mint;
writing them into the fixture tonight would be the mint by another door.

Verified from this seat before writing, own runs, venv interpreter, nothing
mutated: full suite **81 passed (1.80s)** — compliance's child-process subject
correction landed and the Spine's offline guard is green again — and the
M-UX-02a pre-flight `pytest tests/test_vendoring.py tests/test_copy_surfaces.py`
= **18 passed, 0 skipped (0.10s)**. Every line number below was re-read from
`app.py` this round rather than carried from §6.18, and they have MOVED
(engineering's and compliance's comment blocks pushed `render_audit` down ~23
lines); they are locators and are not load-bearing — §6.17(vi).

**(i) RULING, on compliance's demand — the honesty-carrying set over the
thirteen §6.18(i) audit literals is CLOSED at SIX.** The predicate first, so
the list is checkable rather than asserted, and so the next reader can classify
a fourteenth literal without asking this seat:

> A rendered literal is **honesty-carrying** iff, at the moment it paints, it
> states a LIMIT on what the tool knows — it (a) withholds a number and names
> the condition, (b) states a null or negative finding in the app's own voice,
> or (c) names the scope of a number rendered beside it. A literal that names a
> panel, a row or a statistic **without bounding a claim** is structural.

**TIER A — refusals and null findings (3).** The app declines to give a number,
or gives a negative result as a result:

> 1. `accumulating — needs 3 ideas` (`app.py:440`) — withholds ζ and names the
>    condition. Without it a locked meter reads as a computed zero.
> 2. `n/a — no decisions yet` (`app.py:443`) — withholds Brier, same shape.
> 3. `free intercept {b} (z = {z}) — no measured order bias` (`app.py:460-461`)
>    — the ONLY rendering of the null branch of the Spine §3 order-bias
>    diagnostic. Its positive branch is catalogued (`str.orderbias.headline` /
>    `.body`); its negative branch is a bare literal, which is the asymmetry
>    that makes it worth pinning: the app has a ratified sentence for *bias
>    found* and an unratified one for *bias not found*.

**TIER B — scope qualifiers (3).** The app gives a number and bounds what it is
a number OF. These are the three §6.18(i) missed:

> 4. `Brier (model vs. your picks)` (`app.py:442`) — the parenthetical is the
>    only thing on screen separating consistency-Brier from outcome-Brier. Strip
>    it to `Brier` and the Spine's `Out: accuracy claims in 0→1 mode` stops
>    being a distinction the user can see and becomes a denial in a caption
>    contradicted by a number three rows up.
> 5. `Brier (vs. labeled outcomes)` (`app.py:446`) — the other side of that
>    distinction, and the row §6.18(ii) demonstrated renders POOLED under
>    `str.audit.01_caption`. Its scope word is load-bearing while a live defect
>    (F-35) is open beneath it; a scope word doing that much work with no
>    instrument is the definition of an unwatched trust surface.
> 6. the count template ` (1→N: {}, 0→1: {})` (`app.py:414-415`) — the only
>    on-screen disclosure that the log is MIXED across two different questions,
>    and therefore the only place from which a reader could ever infer that the
>    four bold statistics above and below it are pooled over both. Delete the
>    parenthetical and F-35 becomes undetectable from the screen.

**STRUCTURAL — the remaining seven, named so the arithmetic is checkable:**
`Audit`, `Decisions logged`, `ζ (consistency)`, `Override rate`,
`Model of the judge ({mode label})`, `Order-bias diagnostic ({mode label})`,
`Reliability curve ({mode label})`. **6 + 7 = 13**, against §6.18(i)'s
enumeration, and a reader can check both halves against `render_audit` without
this file's permission.

Two rulings that come with the list, because a list handed over without them is
the furniture compliance was right to name:

- **The tie-break is stated and it runs toward inclusion.** Items 4–6 are the
  borderline ones. Where a literal is genuinely arguable, it is **INCLUDED**,
  and the reason is an asymmetry rather than a preference: a false positive
  costs one extra literal pinned in an AST clause and nothing else, while a
  false negative leaves a sentence that bounds a claim with **zero**
  instruments. This is the same asymmetry MP-1 already runs on one surface over
  — the interval is welded to the probability because the cost of showing it
  when it was not needed is nil and the cost of omitting it once is the whole
  judgment.
- **`ζ (consistency)` is structural and the near-miss is worth writing down.**
  Its gloss looks honesty-carrying and is not: the actual honesty work is done
  by `str.audit.zeta_gloss`, which is **catalogued and already governed**. The
  test for tier B is *is this literal the only carrier of the bound* — not *does
  it sound careful*. Same for `Reliability curve ({})`, whose limit statement is
  `str.audit.curve_locked`.

**(ii) REFUSED, and the refusal is the more important half: the second
population gets its members named but NOT a count pin.** §6.18(i) left the five
non-audit builders' enumeration OPEN, owner design, and it is still open — this
round did not walk them, and closing a census by writing a number at the end of
the last round is the estimate §6.16(vi) exists to refuse. Two members are
verified from source this round and can be instrumented immediately:

> - `; the 60/40 target falls outside the plausible range` (`app.py:349`) —
>   tier A. The leverage panel declining to draw a path it cannot support;
>   compliance identified this one and it is confirmed here from the builder,
>   not from their packet.
> - `: 50/50 would need {x} — {note}` (`app.py:357`) — tier A, and its sibling
>   in the same `else` branch, carrying the source's own rule (`# off-scale
>   target: shown and flagged, never clamped`). Shown-and-flagged instead of
>   clamped IS the refusal; the literal is where it is spoken.

**So the answer to compliance's question is: yes closed, and no — closed over
the thirteen at six, open over the builders with two named.** The instrument
that follows must be shaped to match, and this is a demand rather than a
preference: **pin the six with a count; pin the two WITHOUT one.** A `== N`
count pin is itself a claim — it asserts *this is all of them* — so putting one
on an open population would make the instrument state a completeness the census
does not have, which is this cycle's own defect species (an instrument quoted
wider than it measures) committed deliberately by the seat that has filed it
against four other seats. A membership clause with no count is honest on an
open set; it reds when a named refusal is deleted and stays green when the
enumeration grows, which is exactly the behaviour an open census wants.

**(iii) Architecture's two demands: both were already discharged in §6.19 and
the confirmation is restated here in the one line they asked for, because
"already done" is worth nothing without a citation attached.** In writing, and
this seat's ruling: **`banner`'s ratification authority is the catalogue's
`str.banner.01`, and its bytes stay OUT of `leaves/design/copy-authority.yaml`
— option (b)** — asserted byte-equal at import by `app.py:73` and named in the
fixture's `render_map` row with its two `test_engine.py` guards, which
compliance's T-COPY-02c checks by name and T-COPY-02e now guards at the assert
itself. The fixture's predicate is stated as what it actually is: *config text
fields with no counterpart in Authority A*. And the header numeral was
corrected in §6.19(ii) before their packet arrived — the false figure ("three of
the seven fields") is quoted inside a strike block in
`leaves/design/copy-authority.yaml`, the declared population is stated as EIGHT
with FOUR non-rendering, and the map now carries TEN names split five/five.
Their measured argument for (b) is the strongest one on the board and is
recorded as theirs: off a checkout the two governance forms invert, and the one
field they were asking this seat to move INTO the fixture is the one whose
authority survives where the fixture's does not.

**Scope of this section.** One open half of a compliance matrix row closed with
a stated predicate, a six-member list, a named structural remainder and a
checkable 6 + 7 = 13; one undercount struck in place against this seat's own
§6.18 with the false clause quoted; one count pin refused on an open population
with the reason; two members of that open population verified from source and
named; one ruling and one numeral confirmed with citations for architecture.
**No string minted**, no catalogue entry added, no mirror change, no policy or
numeric field touched, no rendered surface altered, no test written or weakened,
`copy-authority.yaml` untouched, and nothing that touches the D1–D6 resolution
round's ordering or the M-UX-02a sitting's protocol. The four statistics still
cannot paint a number during demo steps 1–7 (§6.18(iv), re-verified: §1c logs no
decision), so the eyes-on five stands unamended at five and gtm's hour is
unchanged.
