# PairwisePM — Negotiation Report (20 rounds, n×n leaf exchange)

**Verified 2026-09-01 · spine v0.1 · six leaves (architecture, compliance,
decisions, design, gtm, sequencing) · verification run by an independent seat
against the project venv at `/Users/brettleehary/mcparea/ProMgtAI/.venv`.**

---

## 1. Final state — verified, not reported

| Check | Result |
|---|---|
| `pytest` (project venv, repo root) | **83 passed, 0 failed, 0 skipped** (1.67s) |
| Same suite from `/tmp` (off-root) | 83 passed — equal both directions |
| Order-dependence probe `test_packaging.py test_engine.py` | 62 passed (was 1 failed at r19) |
| Order-dependence probe `test_audit_honesty.py test_engine.py` | 48 passed (was 1 failed at r19) |
| Gate P-1 `-k "no_llm or no_network"` | 3 passed / 80 deselected |
| Gate P-14 `pytest tests/test_vendoring.py` | 7 passed / **0 skipped** |
| `python -m py_compile app.py pairwisepm/*.py leaves/design/strings.py` | clean |
| `decisions.yml` YAML parse | valid; 11 entries, 8 conventions |
| Decision statuses | **D1–D6, D8, D10 pending** · D7, D9, D11 `resolved_uncontested` |

**No breakage was found and nothing was fixed.** The one red that existed
during this cycle — `test_no_llm_or_network_imports` failing on `httpx` — was
closed inside round 20 by the leaves themselves (see §4, D11). This
verification reproduces the fix independently: a fresh interpreter importing
`pairwisepm` + `.engine` + `.config` + `.log` + `.strings` loads 217 modules
with `httpx`, `gradio`, and all eight `FORBIDDEN_IMPORTS` **absent**.

The suite count matches sequencing's own final pin (r20.1, 07:59:52) exactly.

---

## 2. Convergence curve

```
round   edits  demands  disputes  conceded
 1        6      14        0        0    ── opening: demands >> edits
 2       13      16        1        0
 3       11      10        0        1
 4       11      20        0        0
 5       10      14        0        1
 6       11      20        0        0
 7        9      20        0        0
 8       14      24        0        0    ── peak demand volume
 9        8      18        0        1
10        7      13        0        2    ┐
11        5      11        0        3    │ concession trough:
12        4       8        0        4    ┘ edits ↓, concessions ↑
13       11      16        1        0    ── second wave opens
14       12      16        1        0
15       12      24        2        0    ── peak dispute count
16       13      20        1        0
17       13      16        0        0    ── last dispute closes
18       13      16        0        0
19       14      12        0        0
20       12       8        0        0    ── demands back to round-1 floor
```

**Three phases, and the shape is real rather than tidy.**

*Rounds 1–9, expansion.* Demands run 1.5–2.7× edits and peak at 24 in round 8.
This is the leaves finding each other's surfaces: six seats each discovering
what the other five had committed to in files they had not read. Only one
dispute opens (round 2) and it closes in round 3 — the expansion is
cross-referencing, not conflict.

*Rounds 10–12, the concession trough.* Edits fall 8 → 7 → 5 → 4 while
concessions climb 1 → 2 → 3 → 4. This is the only stretch where the board
looks like it is converging to a close, and it is the most misleading part of
the curve: the seats were clearing an inherited backlog, not running out of
findings.

*Rounds 13–20, the defect wave.* Demands jump back to 16–24 and **all six open
disputes of the cycle fall here** (rounds 13, 14, 15×2, 16). What broke the
plateau was not new scope — it was three real defects surfacing in files that
had already been declared terminal: the site-packages copy drift (`A-13-01`,
r14), the `M-UX-02` double-counted measurement (r14), and the order-dependent
no-LLM guard (r19). Every one was found by a seat reading another seat's
evidence rather than accepting its packet.

*Rounds 17–20, closure on evidence.* Zero disputes for four consecutive rounds
while edits stay high (13, 13, 14, 12). The board kept working after it stopped
arguing — the r19 red was found on round 19 and closed on round 20 with the
guard **strengthened**, not deleted.

**The honest read of the tail:** demands at 8 in round 20 matches round 3's
level, disputes are zero, and the last two rounds retired more than they
opened. That is convergence. It is not completion — see §5.

---

## 3. Deals struck

**Eight ratified conventions** (`decisions.yml: conventions`) — questions that
were genuinely settleable between agents, closed without escalation:

| | Convention |
|---|---|
| C1 | M1 activates at exactly 10 logged picks per mode; overrides **count** and are trained on |
| C2 | "Too close to call" = interval straddles 50%, endpoint at 0.5 included; no wider dead-band |
| C3 | Risk surface entered already reversed on 0–4 |
| C4 | Canonical seed z-scoring distributions |
| C5 | Interval confidence level |
| C6 | Leverage-panel weight handoff at M1 activation |
| C7 | Fresh-load default mode |
| C8 | Override honored, never fought |

**Process deals** — the rules the board wrote for itself mid-cycle, which is
where most of the convergence actually came from:

- **Round 2 — the claimed-gate rule.** A seat claiming its defect is
  release-gating routes it through the decisions queue with a Spine line and
  named stakeholders. Nobody attaches their own work to the critical path.
  This rule is why the r13–r16 dispute wave produced queue entries instead of
  deadlock.
- **Round 3 — the regeneration covenants.** Any resolution that moves a pinned
  constant obliges compliance to regenerate the fixtures and gtm to re-verify
  the tour numbers, stated per entry in `on_resolution_notify`.
- **Round 14 — the deferral boundary.** The first-hour M-UX-02 sitting is the
  *only* event that defers the D1–D6 resolution round. Nothing else pauses,
  reopens, or defers it. This removed a recurring argument outright.
- **Round 14 — MISSED-WINDOW is an expired slot, not a failure.** A missed
  sitting means *not yet timed*, never *tested and lost*; re-opening requires a
  newly scheduled dated sitting, so "re-openable" cannot decay into
  "perpetually imminent."
- **Round 14 — pricing off the critical path.** `A-13-01` (venv install drift)
  was admitted as a real node on an `informs` edge only, after the receiving
  seat *reproduced it* and *disconfirmed the claimant's second premise* rather
  than encoding it on their word.

**Reciprocal defect trades** — the shape that closed the hardest items:

- **D7 (r4–r6)** — design's browser-verified imputation void. Engineering
  accepted both demands on record as defects against its own round-1
  commitment and shipped them; `gr.Number` left the input path entirely.
  Dissolved bilaterally, then **verified by a second browser session** before
  the bracket was allowed to close.
- **D11 (r19–r20)** — the no-LLM guard. Compliance narrowed the guard's subject
  from the pytest process to the engine's import graph in a fresh interpreter.
  Design's counter-demand landed
  `test_the_no_llm_guard_cannot_be_quietly_weakened` as a **floor** — an AST
  assertion that `FORBIDDEN_IMPORTS` keeps all eight names, that the clause
  carries no skip marker, and that **both halves survive**. Decisions' demand
  landed a scope-word correction in the docstring, with the false sentence
  struck legibly rather than deleted.

---

## 4. Rulings

**No binding ruling was issued in twenty rounds.** Every contested entry that
closed did so by **bilateral dissolution on its own stated condition** — the
contested question stopped being contested — and each was recorded as
`resolved_uncontested`, never adjudicated:

| Entry | Question | Outcome |
|---|---|---|
| D7 | Does R-8 (browser-side imputation void) gate pilot-live? | Option 1 in substance; dissolved r6 after engineering conceded and shipped; closed on a browser verification record, not on the fix having landed |
| D9 | Does a launch-environment predicate void the M-UX-02a witness record? | Option 2 in substance (void on a *checked* predicate); resolution instrument registered as gate P-14 |
| D11 | Is the no-LLM guard's subject the process or the engine's import graph? | Option 2 with a piece of option 3; raised and dissolved inside one round without gating or deferring anything |

An adjudication mechanism exists and was never needed. That is the single most
load-bearing fact about this cycle: **six agents, twenty rounds, six opened
disputes, zero rulings.**

---

## 5. Spine refusals — independently spot-checked

Every refusal in `spine/SPINE.md` survived twenty rounds of editing, and each
is held by a live executable clause rather than by prose:

| Refusal | Instrument | State |
|---|---|---|
| No LLM in the runtime loop | `test_no_llm_or_network_imports` (child-process probe + source regex) + `test_the_no_llm_guard_cannot_be_quietly_weakened` (AST floor) | green; independently reproduced |
| No network calls | `test_no_network_calls_at_runtime` — socket kill-switch over a full cycle in both modes | green |
| No server-side storage | `test_no_server_side_persistence_static` (T-NEG-06) | green |
| Strictly two ideas | `test_strictly_two_ideas` | green |
| No portfolio/knapsack automation | T-NEG-03 namespace check | green |
| No accuracy claims in 0→1 | `test_zero_to_one_banner_mandatory` + audit-caption clause | green |
| Evaluative factors never scored | `test_evaluative_excluded_by_type`, `test_evaluative_inputs_carry_no_weight_by_construction`, T-NEG-08a/b | green |
| Intervals always shown | `test_interval_always_present` | green |

Direct source audit confirms the same independently of the tests: the only
imports in `app.py` and `pairwisepm/*.py` outside the stdlib are `numpy`,
`yaml`, and `gradio`; runtime deps are exactly `numpy`, `PyYAML`,
`gradio>=6.0,<7`; the decision log lives in `gr.State` for the session and
touches disk only through `tempfile.mkdtemp()` to serve a **user-initiated
download** (`app.py:680`) — a transient response file, explicitly covered by
T-NEG-06 and traceability rows F-24 / N-06, not a persistent store.

One known, documented, non-defect: `gr.Blocks(css=...)` emits a Gradio 6
deprecation warning. It is deliberate and owned — registered as
`ENG-CSS-MIGRATION-01` with three named trigger conditions and
`T-DELIV-01b` as its tripwire, because the constructor form is the only one
that survives every launcher, and an unstyled `#pwpm-banner` would scroll the
0→1 accuracy disclaimer out of the viewport. **Left alone deliberately.**

---

## 6. What remains for Hari

**The critical path has been entirely Hari's gates for twenty consecutive
rounds. The agent-checkable board is empty.**

**1. D1–D6 — six pending decisions, SLA expires today (2026-09-01).**
The build proceeds on stated defaults for all six; every one is config rather
than code, with one exception flagged loudly.

- **D1** — prior weight magnitudes, 1→N factor table (`configs/one_to_n.yaml`)
- **D2** — weight of capability-trajectory exposure in 0→1. **The one to read
  first:** two of its three options are config edits, but the *gate* option is
  a structural change to `engine-m0` that requires a spec update before any
  code moves and blocks `space-push`.
- **D3** — does a portfolio/knapsack layer ever enter scope, and on what
  trigger (the Spine's only explicitly-open scope item)
- **D4** — calibration-report cadence and the *n* for the reliability curve
- **D5** — cutover rule from seed distributions to user-log z-scoring.
  Load-bearing: z-scores feed the score, the interval, *and* the path-to-parity
  raw-unit conversion, so a discontinuous cutover can silently flip a near-tie
  between sessions — the exact Tuesday-noise the product exists to remove.
- **D6** — fragility-flag threshold (three leaves shipped three different
  numbers; code ships 0.75σ)

Per the decisions Leaf's own README, whatever Hari does not resolve is
adjudicated same-day, and `resolution_source: hari | ai_adjudication` must be
named **per entry**. Nothing has been resolved early — the clock was respected
for twenty rounds.

**2. D8 and D10 — two pending, SLA 2026-09-02.** D8: does the release claim
Spine metric #1 for both modes or only 1→N? D10: does a skip in the P-14
pre-flight make a run NO RECORD? D10 reaches its SLA with the divergence
**stated rather than silently closed** — three of four demands discharged, one
standing, two seats holding CONTESTED positions on record.

**3. `hf-space-setup`** — Hari's gate, not agent-actionable.

**4. M-UX-02a — one node ends the cycle awaiting a dated line from gtm.**
Its window elapsed unconvened. Sequencing refused to flip it on its own clock
in the final round, correctly: the miss *verdict* is gtm's dated witness line
and nothing else. The node stays RE-OPENABLE by a newly scheduled dated
sitting, and SC-06 reads **"designed so, not yet timed"** until a dated row
says otherwise. Nothing here is a defect anyone can edit away.

---

## 7. One judgment worth recording

This board found the same failure shape three times in three rounds and named
it each time — a **name** wider than its gate (r18, P-14), a **subject** wider
than its file (r19, the no-LLM clause), an **invocation** narrower than its
subject (r20, gate P-1's `-k` form, which read green *through the entire red*).
The general form, in sequencing's words: *a gate whose green depends on how it
was invoked is not a gate.*

That is the cycle's real product, and it is the right one for this repository.
PairwisePM exists because a scorecard that overstates its confidence teaches
PMs to ignore it. A test suite that reports green on the strength of its own
collection order does the same thing to the people who ship it. The leaves
caught it in their own instruments, on the second-to-last round, and closed it
by making the guard harder to weaken rather than easier to pass.
