# PairwisePM — Engine Test Specifications

leaf: compliance (owns this spec); engineering owns the engine the suite runs against
status: IMPLEMENTED — the executable suite is `/tests/test_engine.py` (engine,
45 tests) plus `/tests/test_packaging.py` (T-PKG + T-NEG-06 + T-CUST-01,
7 tests) plus `/tests/test_vendoring.py` (T-VEND-01, 1 test); 53 tests,
all green against the real `pairwisepm` package with no engine mocks
(integration run 2026-08-30, clean venv, gradio 6.26.0 installed — no skips).
This document remains the normative spec: every test in the suite carries its
T-XXX ID from here. §0 below is the REAL engineering API the suite binds to
(updated in the exchange round from the pre-build assumptions, as agreed —
shapes were binding, names were negotiable). §0.1 records every deviation
between the pre-build spec and the shipped engine, each marked ratified or
flagged.
traces_to: /leaves/compliance/traceability.md (test IDs referenced there are defined here)

---

## 0. Binding API (the shipped surface the suite binds to)

```python
# pairwisepm.config
load_default_configs() -> {"one_to_n": ModeConfig, "zero_to_one": ModeConfig}
load_mode_config(path) -> ModeConfig    # refuses bannerless zero_to_one (ValueError)
# Factor: key, name, scale, prior_weight (magnitude), sign (+1|-1), tag lever|fact,
#   rationale, seed_mean/seed_std (transform space), transform identity|log10p,
#   plausible_range (raw units). effective_weight = sign * prior_weight.
# Ceiling lives in ModeConfig.flags as Flag (NO weight/tag attribute exists).
# EvaluativeInput is a separate typed list the engine never scores.

# pairwisepm.engine
compare(cfg, raw_a: dict, raw_b: dict, m1_fit=None, ceiling_a=False,
        ceiling_b=False, n_boot=2000, seed=7) -> ComparisonResult
# ComparisonResult: mode, banner (cfg.banner, always set for 0→1), z_a, z_b,
#   deltas, m0/m0_equal/m1: ModelScore{model, p, logit, interval, verdict, weights},
#   active_model "M0"|"M1", leverage: [LeverageRow{key,name,tag,weight,delta,
#   contribution}], parity_paths: [ParityPath{key,name,tag,loser,current_raw,
#   target_raw_parity|None, target_raw_6040|None, feasible, note}],
#   loses_on_fundamentals: bool, fragility: Fragility{fragile, factor_key,
#   required_z_shift, message}, ceiling_notes: [str]. .active -> verdict model.
# verdict in {"A", "B", "too_close"}; interval = 90% bootstrap-over-factors.
fit_m1(delta_rows: [dict], picks: [int 1=A], cfg, lam=1.0, lam_intercept=0.05)
    -> M1Fit{weights, n_train, free_intercept, free_intercept_se, order_bias_z,
             active (n >= M1_ACTIVATION_N == 10), order_bias_flagged (|z| > 2)}
leverage_panel(cfg, weights, z_a, z_b, raw_a, raw_b, score) -> (rows, paths,
    loses_on_fundamentals, fragility)     # public; T-PAR/T-FRAG bind here
effective_weights(cfg, equal=False)       # equal=True: sign(w) * mean(|w|) ablation
M1_ACTIVATION_N = 10;  FRAGILITY_Z = 0.75

# pairwisepm.log
make_record(timestamp, mode, name_a, name_b, raw_a, raw_b, result, pick "A"|"B",
            evaluative_a/b, flags_a/b, override_rationale) -> dict  # caller clock
DecisionLog: append, to_jsonl, from_jsonl, for_mode, n, training_data(cfg),
    raw_vectors, kendall_zeta(mode) -> float|None, brier(mode) -> float|None,
    outcome_brier(mode) -> float|None, override_rate(mode) -> float|None
```

## 0.1 Deviations between pre-build spec and shipped engine

| # | Pre-build spec said | Shipped engine does | Disposition |
|---|---|---|---|
| DV-1 | Verdict boundary: interval TOUCHING 0.5 counts as straddling (breaks toward too_close) | Inclusive straddle `lo <= 0.5 <= hi`, plus `p == 0.5` → too_close (engineering adopted the architecture ruling in the exchange round) | RESOLVED — spec position shipped; `test_verdict_rule_units` pins the touching case `(0.53, (0.50, 0.57)) ⇒ too_close` |
| DV-2 | ζ preference relation = most recent pick per unordered pair | Most recent pick per unordered pair (later records overwrite the edge — repeat comparisons update, never double-count); exact Kendall c_max on a complete tournament, ĉ_max = T·(n+1)/(4(n−2)) fallback on incomplete graphs | NO DEVIATION — shipped matches the spec; T-ZETA pins endpoints (intransitive ⇒ 0, transitive ⇒ 1), small-n ⇒ None, and the most-recent-pick-wins update rule |
| DV-3 | Runtime dependency whitelist {numpy, gradio} | {numpy, PyYAML, gradio} — PyYAML reads the factor configs (weights-as-config is itself a Spine-serving mechanism) | RATIFIED; T-NEG-01c whitelist updated |
| DV-4 | `compare` with a 3rd idea raises TypeError | 3rd positional lands in `m1_fit` and fails later with AttributeError, not a clean TypeError | RESOLVED at integration: `compare` type-checks `m1_fit` (isinstance M1Fit) and raises a clean TypeError; `test_strictly_two_ideas` covers both the positional and keyword smuggling paths, plus the structural R-02 assertions |
| DV-5 | Fragility ε default 0.5 z-units (compliance-proposed) | `FRAGILITY_Z = 0.75`, single-factor plausible-range-checked flip | OPEN as decision **D6** (decisions.yml, status pending — a real three-way divergence: engine 0.75σ, compliance 0.5σ, GTM one-rung). Build-meanwhile default is the shipped 0.75; T-FRAG constants regenerated for 0.75 (fixtures chosen so both values give the same pass/fail) and regenerate again on D6 resolution |
| DV-6 | Infeasible parity path: marked or excluded (engineering to pick one) | Kept in list with `feasible: False` and `target_raw_parity: None`; feasible paths sort first, smallest z-shift first | RATIFIED — T-PAR-03 pins this representation |
| DV-7 | Order-bias significance mechanic unspecified (Wald vs bootstrap) | Wald z on the lightly-penalized free intercept; flag at `|z| > 2` | RATIFIED — T-BIAS-01/02 pin it |
| DV-8 | M1 fit returns None / p_m1 None below gate | `fit_m1` always returns an M1Fit (display), `active=False` below 10 picks; `compare` keeps `active_model="M0"` and the verdict comes from M0 | RATIFIED — display-but-never-verdict is Spine-compatible; T-ACT-01 pins `result.active is result.m0` below the gate |
| DV-9 | Free-standing `write_record(path)`/`read_log(path)` file API | In-memory `DecisionLog` + `to_jsonl`/`from_jsonl`; file custody is the UI layer's (download/upload, gr.State) | RATIFIED — matches the no-server-storage enforcement (log moves only through the user's hands); T-LOG binds to the text round-trip |
| DV-10 | Log record carries `config_fingerprint` (architecture §4.1) | IMPLEMENTED at integration 2026-08-30: `ModeConfig.fingerprint` = sha256 of the canonical parsed YAML (format-insensitive, policy-sensitive); `make_record(..., config_fingerprint=)` stamps it (null for pre-v1.1 callers); `app.py` passes it on every logged decision | RESOLVED — T-FPR (`test_config_fingerprint_stamped_and_canonical`) pins shape, stability, sensitivity, stamping, and pre-v1.1 tolerance; traceability F-21 closed |

Conventions used throughout:

- `W1N` = 1→N prior weights in schema order: `[.25, .20, .15, .15, .10, .05, -.10]`
  for (impact, feasibility, reach, unit_econ, flywheel, risk, effort). Config defaults
  per technical-spec §2 (pending D1/D2; tests read weights FROM config, never hardcode
  except where a hand-computed expectation requires the default — those tests must be
  regenerated if D1/D2 changes the defaults, and say so inline).
- `sigma(x) = 1/(1+exp(-x))`.
- "bitwise identical" = `==` on floats (not approx). "≈ t" = absolute tolerance t.
- Any stochastic step (bootstrap) takes an explicit `seed`; tests always pass one.
- Z-scoring: for unit tests of engine arithmetic, tests construct ideas whose z-deltas
  are forced by supplying a config with seed distributions mean 0 / std 1 so that
  raw values ARE z-values (`STD1_CONFIG`). This isolates the scorer from the
  z-scoring pipeline; T-LOG and T-CFG cover the pipeline itself.

Shared fixture `D_FIX` (z-deltas, 1→N schema order):
`d = [1.0, 0.5, -0.2, 0.0, 0.3, -1.0, 0.4]`
Hand-computed: `L = W1N · d = 0.26`, `p = sigma(0.26) = 0.5646362918030292`.

---

## 1. T-SYM — Symmetry: swap A/B ⇒ p exactly 1 − p

Traces: SC-01, SC-03; technical-spec §3 (intercept constrained to zero for scoring).

**T-SYM-01.** Build ideas A, B with `STD1_CONFIG` such that `z_A − z_B = D_FIX`.
1. `va = compare(A, B, "1toN", seed=7)`; `vb = compare(B, A, "1toN", seed=7)`.
2. Assert `vb.logit == -va.logit` **bitwise** (d negates exactly; a zero intercept
   adds nothing; any nonzero intercept in the scoring path breaks this assertion —
   that is the point of the test).
3. Assert `abs(va.p_m0 + vb.p_m0 - 1.0) <= 1e-12`.
4. Assert verdict consistency: if `va.verdict == "a"` then `vb.verdict == "b"`
   (and `too_close` maps to `too_close`).
5. Assert `vb.interval == (1 - va.interval[1], 1 - va.interval[0])` each end ≈ 1e-12
   (bootstrap must be seeded on the unordered pair or re-derived by reflection so the
   interval is swap-consistent; an interval that materially changes when the user
   swaps columns is a presentation-order artifact — exactly what the Spine refuses).
6. Repeat 1–5 in `"0to1"` mode with that schema's factor count.
7. Property extension (same assertions): 50 pseudorandom d vectors from
   `numpy.random.default_rng(20260830)`, standard normal, both modes.

**T-SYM-02 (ablation preserves symmetry).** With equal-weight ablation toggled on
(all |w| equal, signs kept — technical-spec §3), repeat T-SYM-01 steps 1–4.
Covers matrix row F-14 (T-ABL-01 is an alias of this test plus: assert ablation
weight vector is `sign(w) * mean(|w|)` of the config weights).

## 2. T-EQ — All-equal factors ⇒ p = 0.5

Traces: SC-01, SC-09.

**T-EQ-01.** Ideas A and B with identical raw factor values (every factor, both
modes). Assert `logit == 0.0` bitwise, `p_m0 == 0.5` bitwise (`sigma(0.0)` is exactly
0.5 in IEEE double), and `verdict == "too_close"` (the interval necessarily straddles
0.5 — a tie must never render a forced winner). Assert `contributions[j] == 0.0`
for every factor.

## 3. T-M0 — Hand-computed M0 case

Traces: SC-04, SC-05; technical-spec §3.

**T-M0-01.** With `STD1_CONFIG` and `D_FIX`: assert `abs(logit - 0.26) <= 1e-12` and
`abs(p_m0 - 0.5646362918030292) <= 1e-9`. (Regenerate constants if D1 changes
defaults — this test pins config defaults deliberately, as the traceability check
that shipped config matches technical-spec §2.)

**T-CFG-01.** Load both mode schemas from config. For every factor assert presence
and type of: `scale`, `prior_weight` (float), `sign` (implied by weight sign),
`rationale` (non-empty str), `tag in {"lever", "fact"}` — except 0→1 `ceiling`,
which must have `tag` absent/`None` and NO `prior_weight` (unweighted, §2).
Assert 1→N has 7 weighted factors, 0→1 has 6 weighted factors + ceiling flag.

**T-CFG-02.** Copy the 1→N config, change impact weight .25 → .40, pass via
`config=`. Assert the logit on `D_FIX` becomes `0.26 + 0.15·1.0 = 0.41` ≈ 1e-12.
Weights are config, not code.

## 4. T-MAP — MAP regularization never diverges on degenerate logs

Traces: SC-08; technical-spec §3 ("MAP regularization is mandatory from day one:
pure MLE diverges on small or disconnected comparison graphs").

Fixture builder `mk_record(d, pick)` produces a minimal valid log record with
z-delta `d` and `pick in {"a","b"}`. All fits use default `lam` unless stated.
"Converges" means: returns without exception, every weight finite
(`numpy.isfinite` all), and `max(|w_j|) <= 10.0`.

**T-MAP-01 (empty log).** `fit_m1([], W1N)` returns the prior weights exactly
(bitwise) with intercept 0.0 — defined fallback, no exception. Also
`m1_active([]) is False`.

**T-MAP-02 (one decision).** Single record `mk_record(D_FIX, "a")`. Fit converges.
(Pure MLE is separable here — weights would run to ±∞; MAP must not.)

**T-MAP-03 (all-one-winner / complete separation).** 12 records, d vectors drawn
`default_rng(1)` standard normal but each scaled so `W1N·d > 0`, pick `"a"` every
time. Fit converges. Additionally fit with `free_intercept=True`: also converges.

**T-MAP-04 (disconnected / degenerate design).**
(a) Idea-graph disconnection: 12 records forming two clusters — ideas {P,Q}
compared only with each other (6 records), ideas {R,S} only with each other
(6 records). Fit converges (factor-delta regression must not care that the idea
graph is disconnected).
(b) Rank-deficient design: 12 records where factor index 2 (reach) has `d_2 = 0.0`
in every record. Fit converges AND `abs(w_2 - W1N[2]) <= 1e-9`: a factor with no
observed variation must stay AT its prior weight (shrinkage center, not zero —
this assertion fails if ridge is centered on zero, which is the classic
implementation mistake technical-spec §3 forbids).

## 5. T-VERDICT — Interval straddling 0.5 ⇒ too_close

Traces: SC-09; technical-spec §4.

**T-VERDICT-01 (rule unit test).** The verdict rule as a pure function of
`(p, interval)`: `(0.55, (0.48, 0.61))` ⇒ `too_close`; `(0.56, (0.52, 0.61))` ⇒
`"A"`; `(0.44, (0.39, 0.48))` ⇒ `"B"`. Boundary `(0.53, (0.50, 0.57))`:
spec position is `too_close` (touching 0.5 counts as straddling — honesty rule
breaks toward "too close", never toward a forced winner); the shipped engine
now implements exactly this (DV-1 RESOLVED — `verdict_from` uses `lo <= 0.5 <= hi`).
Implemented as T-VERDICT rule-consistency property in `test_engine.py`
(verdict must equal the rule on every observed compare) plus the `p == 0.5`
tie case.

**T-VERDICT-02 (end-to-end).** Near-tie fixture: `d = [0.05, -0.03, 0.02, 0.0,
-0.02, 0.04, 0.01]` (L = 0.00915), `seed=42`, bootstrap n=1000. Assert interval
straddles 0.5 and `verdict == "too_close"`; assert the rendered recommendation
string contains "gather evidence" and does NOT name a winner. Clear-winner fixture
REGENERATED (exchange-round finding, confirmed at integration): `3 × D_FIX` is NOT
a clear winner under bootstrap-over-factors — D_FIX's dominant +0.75 contribution
against a −0.30 makes the resampled interval straddle 50% even at L = 0.78. The
suite uses spread-contribution deltas
`d = [0.5, 0.4, −0.4/3, 0.7, 0.8, −0.5, 0.0]` ⇒ verdict `"A"` with the interval
entirely above 0.5 (`test_verdict_end_to_end`).

**T-VERDICT-03 (interval always present).** For every compare in this suite's
fixtures (both modes, tie and non-tie): `interval` is a 2-tuple with
`0 <= lo <= p_active <= hi <= 1`. "Intervals shown always" is Spine SC-09.

## 6. T-CEIL — Ceiling flag never changes the score

Traces: R-03, F-12; technical-spec §2.

**T-CEIL-01.** 0→1 fixture pair, `seed=11`. Run once with `ceiling=False` on both
ideas, once with `ceiling=True` on idea A, once with it on both. Assert `p_m0`,
`logit`, `interval`, `contributions`, and `parity_paths` are **bitwise identical**
across all three runs. Any drift means the flag leaked into the score.

**T-CEIL-02.** With `ceiling=True` on A: `ceiling_routed is True` and the verdict
card payload contains the routing text "high-ceiling outlier — portfolio decision,
not averaged in". With no flags: `ceiling_routed is False` and text absent.

## 7. T-EVAL / T-NEG-05 — Evaluative inputs never affect the score

Traces: R-05; technical-spec §2.

**T-EVAL-01.** Fixture pair with `seed=11`. Sweep evaluative inputs (strategic
fit, brand) over their full range on both ideas — at minimum the 4 corner
combinations (min/min, min/max, max/min, max/max). Assert all score outputs
(`p_m0`, `p_m1`, `logit`, `interval`, `contributions`, `parity_paths`,
`fragility`) **bitwise identical** across the sweep. THEN assert the evaluative
values DO round-trip: they appear in `verdict.evaluative` and in the written log
record (they are captured and displayed as labeled overrides — excluded means
excluded from the score, not from the record).

## 8. T-PAR — Path to parity: levers only, plausible range only

Traces: SC-04, SC-13; technical-spec §5.2–5.3. Required z-shift for factor j is
`L / w_j` in the direction that closes the loser's gap; raw shift = z-shift ×
factor std (§5.2: "reported in RAW units").

Fixture: `STD1_CONFIG` variant `PAR_CONFIG` with per-factor stds
`[1.2, 1.0, 500.0, 1.0, 1.0, 1.0, 2.0]` (reach in users, effort in person-weeks)
and declared raw scale bounds per technical-spec §2 (impact −2..+2, feasibility
0–4, unit_econ 0–4, risk 0–4, effort ≥ 0). Ideas built so `d = D_FIX`
(`L = 0.26`, A wins, B is the loser). B's current raw values:
`[0.0 (impact), 2.0 (feas), 1000, 2.0 (unit_econ), 2.0 (fly), 2.0 (risk), 6.0 (effort)]`.

**T-PAR-01 (arithmetic).** The parity path for `impact` (lever, w=.25):
z-shift `= 0.26/0.25 = 1.04` ≈ 1e-9; raw shift `= 1.04 × 1.2 = 1.248` ≈ 1e-9;
target raw value `0.0 + 1.248 = 1.248`, inside −2..+2 ⇒ feasible. The 60/40 path
(loser reaching p = 0.6): z-shift `= (0.26 + ln(1.5))/0.25 = 2.6618604324326583`
⇒ raw target `3.194…`, OUTSIDE −2..+2 ⇒ `target_raw_6040 is None` (the range
check applies to the 60/40 target too). Shipped ParityPath fields: `key`,
`name`, `tag`, `loser`, `current_raw`, `target_raw_parity | None`,
`target_raw_6040 | None`, `feasible`, `note`. Feasible checks also asserted for
`feas` (target 3.3) and `effort` (sign −1: target 0.8 = 6 − 2.6×2). The suite
binds these via the public `leverage_panel` with a constructed winning
ModelScore — isolating parity math from bootstrap noise — plus an end-to-end
compare on an all-positive-contribution fixture.

**T-PAR-02 (levers only).** No ParityPath may name a `fact`-tagged factor. In this
1→N fixture: `reach`, `flywheel` never appear. Assert by exhaustive check of
`parity_paths`. (Technical-spec §5.3: "parity paths proposed only through levers.")

**T-PAR-03 (plausible range).** `risk` (lever, w=.05) needs z-shift
`0.26/0.05 = 5.2` ⇒ raw target `2.0 + 5.2 = 7.2`, outside 0–4 ⇒ the path is marked
`feasible: False` (or excluded from the proposed list — engineering picks one
representation and states it; the assertion is that it is NEVER presented as an
actionable path). Same check for `effort` if its target goes below 0.

**T-PAR-04 (loses on fundamentals).** Fixture where the entire gap sits on facts:
0→1 mode, `d = [1.5 (severity: fact), 1.0 (trajectory: fact), 0.0 (pull: lever),
1.0 (necessity: fact), 0.5 (advantage: fact), 0.0 (cost_to_test: lever)]` with a
config whose lever stds/bounds make both lever paths infeasible (pull already at
top-box 4 for B; cost_to_test already at its floor). Assert `parity_paths` contains
no feasible path and the verdict payload carries "loses on fundamentals — no
working-harder path flips this" (§5.3 exact copy: design leaf owns final string;
test pins a payload flag `fundamentals: True` plus the copy via a constant).

## 9. T-FRAG — Fragility flag

Traces: SC-09, F-11; technical-spec §5.4. Shipped "small plausible move"
ε = `FRAGILITY_Z = 0.75` z-units on a single factor (DV-5 → decision **D6**,
status pending: engineering's shipped constant is the build-meanwhile default
over compliance's proposed 0.5; the T-FRAG fixtures below regenerate against
whatever epsilon D6 resolves to). The RULE under test
is unchanged: fragile ⇔ ∃ factor j with `|L| / |w_j| <= ε` AND the flipping
move stays inside the factor's plausible raw range.

**T-FRAG-01 (fragile).** `L = 0.10` on the PAR fixture. Impact: required shift
`0.10/0.25 = 0.4σ <= 0.75` and in-range ⇒ `fragility.fragile is True`,
`factor_key == "impact"`, `required_z_shift == 0.4`, message contains
"re-estimate before committing".

**T-FRAG-02 (robust).** `L = 0.26`; smallest flip needs `0.26/0.25 = 1.04σ >
0.75` ⇒ `fragility.fragile is False`, empty message.

## 10. T-ZETA — Kendall's ζ on known cases

Traces: SC-08; technical-spec §4. Formula under test: with n ideas and win counts
`a_i` from the pairwise preference relation, circular triads
`c = n(n−1)(2n−1)/12 − ½·Σ a_i²`; `ζ = 1 − c/c_max`. The shipped engine counts
circular triads directly over complete triads and normalizes by
`ĉ_max = T·(n+1)/(4(n−2))` — verified to agree with the classical formula at
the endpoints tested below. Preference relation from the log: **majority
direction per unordered idea pair** (tied pairs drop the edge) — DV-2 in §0.1,
ratified (pre-build spec said most-recent-pick; majority is a defensible
aggregation and is now the pinned behavior).

**T-ZETA-01 (intransitive triad).** Log: A beats B, B beats C, C beats A (three
records, distinct idea names, any d vectors consistent with picks). n=3, wins
(1,1,1): `c = 2.5 − 1.5 = 1`, `c_max = 1` ⇒ `zeta == 0.0` ≈ 1e-12. Perfectly
inconsistent judge reads 0.

**T-ZETA-02 (transitive sets).** (a) A>B, B>C, A>C: wins (2,1,0), `c = 0` ⇒
`zeta == 1.0` ≈ 1e-12. (b) Four ideas, all 6 pairs, wins (3,2,1,0):
`c = 7 − 7 = 0` ⇒ `zeta == 1.0`. Perfectly consistent judge reads 1, independent
of n.

**T-ZETA-03 (small-n behavior).** Logs with 1 and 2 decisions (< 3 distinct ideas
or no closed triple): `zeta(records)` returns `None` (rendered as "accumulating —
needs 3 ideas") — never an exception, never a fake number. Accumulates "from
decision 1" (SC-08) means computed on every log state without crashing, not that
a value is invented before one is defined.

## 11. T-BRIER — Brier on a hand-computed case

Traces: SC-08; technical-spec §4. v1 Brier is prediction-of-the-pick (outcome
labels don't exist until M2): `y = 1` if pick == "a", scored against the p shown
at decision time (the active model's p, as stored in the record).

**T-BRIER-01.** Log of three records with stored `(p, pick)`:
`(0.8, "a"), (0.6, "b"), (0.5, "a")` ⇒
`((0.8−1)² + (0.6−0)² + (0.5−1)²)/3 = (0.04 + 0.36 + 0.25)/3 =
0.21666666666666667` ≈ 1e-12.

**T-BRIER-02.** Single record `(0.8, "a")` ⇒ `0.04` ≈ 1e-12 (defined from
decision 1); empty log ⇒ `None`, no exception.

## 12. T-SHRINK — M1 shrinks to M0 weights at tiny n

Traces: SC-08; technical-spec §3 ("shrinkage centered on M0's prior weights, not
zero"). Fixture log `SMALL_LOG`: 3 records, d from `default_rng(3)` standard
normal, picks set to whichever side `W1N·d` favors.

**T-SHRINK-01 (limit).** `fit_m1(SMALL_LOG, W1N, lam=1e6)` ⇒
`max_j |w_j − W1N_j| <= 1e-3` and `intercept == 0` (constrained). If shrinkage
were centered on zero this fit returns ≈ 0 everywhere and the assertion fails —
this is the canonical guard for the §3 requirement.

**T-SHRINK-02 (monotone shrinkage).** On `SMALL_LOG`, let
`dist(lam) = ‖w(lam) − W1N‖₂`. Assert `dist(1e3) <= dist(10) + 1e-9 <= dist(0.1)
+ 2e-9`: distance from the prior is non-increasing in λ.

**T-ACT-01 (activation).** 9 records ⇒ `m1_active` False and `compare(...).p_m1 is
None`, M0 verdict still fully rendered; 10 records ⇒ `m1_active` True, `p_m1`
present, and the audit payload exposes per-factor `w_M1 − w_M0` divergence
(T-DIV-01: "what your revealed policy weighs vs. what you say you weigh").

## 13. T-BIAS — Free intercept detects injected order bias

Traces: SC-01, SC-09; technical-spec §3 (free intercept as diagnostic only).

**T-BIAS-01 (injected bias).** 40 records: d vectors `default_rng(20260830)`
standard normal (7 factors), pick `"a"` on every record regardless of d — a judge
who always keeps the first-presented idea. `fit_m1(..., free_intercept=True)`:
assert `intercept >= 0.75` and the audit report flags presentation-order bias
(payload key `order_bias_flag: True` when the intercept's bootstrap/Wald interval
excludes 0 — engineering picks the significance mechanic; the fixture is
constructed to be unambiguous under any reasonable one). Assert also that the
SCORING path in `compare` is unaffected: T-SYM-01 assertions still hold on this
log's model (diagnostic never contaminates the score).

**T-BIAS-02 (control).** Mirror-balanced log: the same 40 records PLUS their 40
reflections (`d → −d`, pick `"a" → "b"`). The likelihood is exactly symmetric ⇒
assert `|intercept| <= 1e-3` and `order_bias_flag: False`.

## 14. T-LOG — Log round-trip and schema

Traces: SC-07, SC-12; technical-spec §6.

**T-LOG-01 (round-trip).** Build a full record R: timestamp (ISO-8601), mode,
both factor vectors raw AND z (floats at full precision, include an irrational-ish
value like `0.5646362918030292` and a negative), evaluative inputs, pick, model
outputs (`p_m0`, `p_m1` (null when inactive), interval), override rationale string
containing unicode ("ratée — höher"), `outcome: null`. `write_record` to a temp
path, `read_log`, assert `read[0] == R` exactly (JSON round-trips IEEE doubles
losslessly via repr — full-precision equality is required, not approx). Append a
second record; assert order and both intact. Re-read file written by a previous
run of the suite (bytes fixed in a fixture file) to pin format stability.

**T-LOG-02 (schema completeness).** Every record produced by an end-to-end
`compare`+confirm cycle contains ALL §6 fields — including the `outcome` slot
present-and-null (schema ready for M2/M3) and `override_rationale` present
whenever pick contradicts the verdict.

**T-LOG-03 (log is the training set).** From a written 12-record log alone
(fresh process, no in-memory state): `fit_m1`, `zeta`, `brier` all run and match
the values computed before the write ≈ 1e-12. The downloaded log is sufficient to
reconstruct the model — "log fully in the user's hands" (SC-07).

## 15. T-NEG — Negative tests for Spine refusals

Traces: SC-15 / R-01..R-06; matrix §3. Regression guards, run every release.

**T-NEG-01a (no LLM imports).** Import `pairwisepm` in a fresh interpreter; assert
`sys.modules` contains none of: `openai`, `anthropic`, `transformers`, `litellm`,
`langchain` (any prefix), `httpx`, `requests`, `aiohttp`. Also statically scan
`pairwisepm/` and `app.py` sources for those import names.

**T-NEG-01b (socket kill-switch).** Monkeypatch `socket.socket` (and
`socket.create_connection`) to raise `AssertionError("network call in runtime")`.
Run a full cycle in both modes: compare → verdict → parity → write_record →
read_log → zeta/brier → fit_m1 on 12 records. Must complete untouched. This is
the executable form of "runs entirely offline" (SC-07) and "no LLM in the runtime
loop" (R-01).

**T-NEG-01c (dependency set).** Parse requirements: runtime deps ⊆
{numpy, PyYAML, gradio} (+ stdlib) — PyYAML added per DV-3 (it reads the
factor configs; weights-as-config is Spine-serving). Anything else fails the
test until this spec is amended with a Spine-consistent justification.

**T-NEG-02 (strictly two ideas).** `compare` with a third positional idea ⇒
`TypeError`. Public API surface (`dir(pairwisepm)` minus underscored) contains no
name matching `rank|sort|tournament|round_robin`; an `ideas: list` parameter on
any public callable fails the test. v1 is A-vs-B, period (R-02).

**T-NEG-03 (no portfolio automation).** Package namespace contains no module or
public callable matching `portfolio|knapsack|optimi[sz]e|allocat`. Ceiling routing
is a message, not a computation (T-CEIL-01 already pins score-invariance).

**T-NEG-04 (no 0→1 accuracy claims).** (a) Every 0→1 `compare` result has
`banner` set to the structure-not-prediction text; 1→N has `banner is None`.
(b) The 0→1 audit payload labels Brier/ζ with the word "consistency" and never
the words "accuracy" or "predictive" in 0→1-mode user-facing strings (assert on
the payload constants module shared with design).

**T-NEG-05.** = T-EVAL-01 (evaluative inputs never affect the score; captured in
log and display only).

**T-NEG-06 (no server-side storage).** (a) Static: `app.py` contains no database
client, no writes outside `tempfile`-scoped session paths, no HF persistent
storage / Datasets push. (b) Behavioral: after a simulated session (compare +
log download + log upload), assert no file created by the app persists outside
the session temp directory; uploaded log content is not written anywhere except
the in-session working copy handed back to the user.

## 16. T-PKG — Deliverable shape (smoke)

Traces: SC-14; technical-spec §7. **T-PKG-01:** `import pairwisepm` works and
`__version__ == "0.1.0"` (the clean-venv `pip install .` check remains a
release-gate step in the audit protocol, not an in-suite test — it needs
network for build deps). **T-PKG-02:** repo root contains `app.py`,
`requirements.txt`, both `configs/*.yaml`; `pyproject.toml` and README checks
run when those files exist and SKIP with a release-gate warning otherwise — a
release candidate cannot ship while they skip (matrix F-16/F-18). README must
contain the three §7 epistemics statements as substrings ("editable policy",
"no accuracy claim", "the LLM's job was at build time"). **T-PKG-03:** with
gradio installed, `app.py` imports and exposes module-level `demo` as
`gr.Blocks` (HF Spaces contract); skips via importorskip where gradio is
absent.

## 17. T-VEND — One-way string vendoring is byte-identical

Traces: architecture.md §4.2 (copy authority: design's leaf file is the single
source; `pairwisepm/strings.py` is a verbatim vendored mirror), serving the
SC-09 honesty-copy chain (states.md → config → tests). **T-VEND-01** (in
`/tests/test_vendoring.py`): `pairwisepm/strings.py` byte-equals
`leaves/design/strings.py`; any drift, either direction, is a red suite until
re-vendored design → package (never the reverse). Skips ONLY in a stripped
deployment where the design leaf is absent (the vendored module is then the
sole copy by construction); in the repo/CI context a skip here is an
unexpected skip under checklist P-8. History: the boundary held by discipline
alone until round 2, and drifted within one round of being "verified
identical" (design's additive keys, 2026-08-30 22:08, re-vendored 22:11) —
this guard exists because the drift was observed, not hypothesized.

## 18. T-CUST — Custody nudge counts session appends only

Traces: SC-07 ("log fully in the user's hands") / SC-15 (overconfidence
refusal applied to custody claims); design S10b (binding `{n_session}`
semantics); states.md §6.4 R-1. **T-CUST-01** (in `/tests/test_packaging.py`,
gradio-gated): `str.log.unsaved_nudge`'s `{n_session}` slot receives the count
of records APPENDED THIS SESSION only, never the total log size. Asserts:
(a) a log of uploaded-only records with `n_session=0` renders no nudge at all;
(b) with `n_session=1` the nudge says 1 and the total-count rendering is
absent; (c) end-to-end `do_upload` of a multi-record file into a fresh session
yields an audit view with no "exists only in this browser tab" claim.
Regression guard for the round-2 honesty defect where `render_audit` was fed
the total log count — a false custody claim about records already in the
user's own file.

## 19. T-CEIL-03 — S5 ceiling routing strip renders in the UI

Traces: SC-09 (honest by construction — the user must SEE that flagging did
not move the number), SC-13 (leverage panel / routing surfaces), R-03
legibility half (the routing note stays a message to a human, and that message
must actually reach the human); design states.md S5 + §6.4 R-3 (landed
round 2). **T-CEIL-03** (in `/tests/test_packaging.py`, gradio-gated —
`render_verdict` lives in app.py): with the shipped `zero_to_one` config and
the T-CEIL-01 fixture ideas, the verdict card renders per flag state:
(a) no flag ⇒ none of `str.ceiling.strip`/`.both`/`.mech_label` appears;
(b) A flagged ⇒ `str.ceiling.strip` formatted with A's name (and never B's),
plus the engine's pinned note with `str.ceiling.mech_label`; (c) B flagged ⇒
the name tracks the flagged idea; (d) both flagged ⇒ `str.ceiling.both`.
Complements T-CEIL-01/02: those prove the flag never enters the score (engine
half); this pins that the exclusion is asserted AND explained on the card
(UI half). Guards against the strip silently vanishing in a future app.py
refactor — which every engine test would miss.

## 20. T-SER — Untouched inputs never reach the handler as values (R-8 guard)

Traces: SC-09 / SC-15 ("a judge that overstates its confidence is worse than
no judge" — a verdict computed from 12 silently-imputed scores is fabricated
confidence), SC-03 / spec §1 (both ideas scored together — void when 12 of 14
scores are imputed zeros), design S2 ("the tool never guesses") and states.md
§6.4 R-8. **STATUS: IMPLEMENTED —
`tests/test_packaging.py::test_untouched_factor_never_scores`, green
2026-08-31 (56/56), landed round 4 in the SAME change as the fix per the
pairing requirement below. Red-first satisfied twice over: engineering
demonstrated the test FAILING against the pre-fix `gr.Number` build
(round 4, on the record), and the red is verifiable BY CONSTRUCTION —
clause (a) asserts no factor input `isinstance gr.Number`, which
necessarily fails on the pre-fix build whose factor inputs were
`gr.Number(value=None)`. The shipped mechanism is Textbox factor inputs
(untouched payload `""`) screened by `_coerce_raw`/`_screen_factors`;
the test drives the handlers with exactly those frontend payloads and
pins that an explicit 0 stays a score.** Historical contract text
follows unchanged. The defect lived in Gradio 6.26's
serialization layer: `gr.Number(value=None)` renders and submits a literal
`0`, so `_missing_factors` never sees `None` and the no-imputation blocking
rule is void in a real browser. The existing suite is STRUCTURALLY BLIND to
this class — every handler test passes Python `None` directly, which is how a
green 54-test suite coexisted with a void blocking rule.

**T-SER-01** (mechanism engineering's choice; level is the requirement): the
check must exercise the serialization boundary, not the handler signature —
via `gradio_client` against the instantiated demo, or a schema/payload-level
assertion that an untouched Number component neither carries nor submits a
default `0` (e.g. the component's `postprocess(None)`/config default must not
yield `0`, and a submit with untouched fields must reach the handler as
missing, rendering `str.partial.verdict_placeholder`). Two acceptance clauses,
both behavioral: (a) an untouched factor NEVER reaches the handler as a value;
(b) Compare on an incomplete form renders the S2 missing-factor list, never a
raw Gradio error toast or a computed verdict.

**Red-first requirement:** before the fix merges, T-SER-01 must be
demonstrated to FAIL against the current app.py under gradio 6.26.0 — a guard
that passes on the broken build is not a guard. **Pairing requirement
(T-VEND-01 discipline):** the fix and T-SER-01 land in the same change, never
the fix alone; F-28 in the traceability matrix stays GAP and pre-push gate
P-10 stays red until both land together.

## 21. T-THEME — Forced-background blocks force their text color (R-9 guard)

Traces: SC-09 via design MP-1 (the interval-welded probability token "must
survive a squint"); states.md §6.4 R-9 (verdict headline and runner-up chip
near-invisible in Gradio's dark theme; amber `#fef3c7` strips share the root
cause). **STATUS: IMPLEMENTED —
`tests/test_packaging.py::test_forced_light_backgrounds_force_text_color`,
green 2026-08-31 (56/56), landed round 4 in the same change as the R-9 CSS
fix per the pairing requirement. Broadened round 5 by compliance to the
full contract below: the pin matches ANY forced hex background
(`background:`/`background-color:`, any color — not just the two hexes
shipped today) and requires an adjacent forced `color:`; verified green
on the as-built app.py before landing. Dark-theme legibility as a human
judgment stays under the manual audit (render session 2).** Historical
contract text follows unchanged. **T-THEME-01** (static, automatable, not
gradio-gated): scan
every inline-styled HTML block emitted by app.py's render functions; any block
that forces a `background`/`background-color` MUST also set an explicit
`color` (on the block or on every text-bearing descendant). This is a
regex/parse-level pin over the rendered strings — cheap, deterministic, and it
reds on the exact regression class (a future block added with a forced light
background and inherited theme text). Pairing requirement as §20: lands in the
same change as the R-9 CSS fix, never fix-alone. Dark-theme LEGIBILITY as a
human judgment stays under the manual audit (M-UX re-check after the fix);
this test pins the mechanism so the defect class cannot silently return.

### §21b — T-THEME-01b strengthening (round 6, R-9b): descendant coverage

**Why (browser-disproved guard, third instance):** render session 2
(states.md §6.7, 2026-08-31) shows T-THEME-01 GREEN while the S3/S4 verdict
headline, its `<b>` MP-1 token, the runner-up chip span, and the S1/S2
placeholder inner divs compute `rgb(244,244,245)` on `rgb(250,250,249)` in
the served dark theme. Root cause: gradio 6.26's
`.gradio-container-6-26-0 .prose * { color: var(--body-text-color) }` beats
INHERITANCE from the block's forced inline color — so a pin that asserts
background-implies-color on the same element cannot see a stylesheet rule
that re-colors the element's children. The as-implemented test satisfied
§21's letter via the "(on the block …)" branch; §6.7 proves that branch
insufficient in the served UI. The honor-system gap moved down a layer
again: serialization (§20) → CSS specificity (this section).

**T-THEME-01b contract** (strengthens, never replaces, T-THEME-01; the
block-level pin stays): every TEXT-BEARING ELEMENT nested inside a
forced-background block must carry its own forced `color` — satisfied either
by (i) an inline `color:` on every nested text-bearing element (`div`, `b`,
`span`, `li`, …) inside any forced-background block, or (ii) a scoped style
rule shipped by app.py whose specificity beats `.prose *` for those
descendants, in which case the test pins that rule's presence and coverage.
Mechanism is engineering's choice; the LEVEL is the requirement: the check
must red on a nested text-bearing element that would inherit — rather than
carry — its color inside a forced-background block. Concretely, against the
as-built app.py the current `<div style='font-size:1.25em'><b>` headline
(app.py ~lines 176, 192) and the runner-up chip span must red the
strengthened pin until the R-9b fix lands.

**Red-first requirement:** T-THEME-01b must be demonstrated to FAIL against
the pre-fix app.py (trivially satisfiable by construction: the headline div
carries no `color:`). **Pairing requirement (same as §20):** the R-9b fix
and the strengthened test land in the SAME change, never the fix alone.
F-29 in the traceability matrix stands at partial (R-9b residual) and
pre-push gate P-11 stays red until both land together, followed by a
browser legibility re-check (render session 3) per §6.7's method.
The M-UX-03 sticky-banner residue is a SEPARATE obligation (F-19/P-5) and
neither clears nor is cleared by this section.

**STATUS — IMPLEMENTED (round 7, 2026-08-31):**
`tests/test_packaging.py::test_forced_light_blocks_color_every_nested_element`.
Contract met at the required LEVEL: an HTML-parser audit
(`_NestedColorAudit`) walks the REAL rendered S1/S2/S3/S4/stale/banner
surfaces and reds on any text-bearing element inside a forced-background
block that lacks its own `color:`. Red-first honored by construction via an
in-test sensitivity self-test asserting the audit flags the exact pre-fix
headline shape (`<b>` with no own color inside a forced-light wrapper) that
browser session 2 caught — so the guard's sensitivity is re-proved on every
run, not once at landing. Landed in the SAME change as the R-9b fix
(inline color on every nested element; mechanism (i) of the contract).
Verified independently by compliance: own code read + own suite run,
58/58 green. Gradio-gated via `importorskip` per P-8's skip discipline.
P-11's fix+guard half clears; its render-session-3 half remains open.

---

## 22. T-BANNER — 0→1 banner scroll-persistence mechanism (M-UX-03 static pin)

**Matrix hook:** F-19 / P-5. **Registered round 7 (2026-08-31).**

**T-BANNER-01** = `tests/test_packaging.py::test_banner_scroll_persistent_static`
(static, never skips). Pins the MECHANISM of the M-UX-03 fix so it cannot
silently regress:

- app.py ships a `#pwpm-banner { ... }` CSS rule containing
  `position: sticky`, `top: 0`, and a `z-index` (the banner must layer above
  the cards it scrolls over);
- the rule targets the gr.HTML COMPONENT WRAPPER via `elem_id="pwpm-banner"`
  — sticky on the inner div would stick only within its own wrapper's height,
  i.e. be a no-op, which is the defect class that shipped;
- the css is actually wired into the Blocks the Space serves
  (`gr.Blocks(... css=_CSS)`). Engineering's recorded note: gradio 6.26
  deprecation-warns on constructor `css=` but honors it via the
  `_deprecated_css` fallback (verified in the installed package source);
  deliberate — the constructor path survives any launcher. If a future
  pinned sdk_version drops the fallback, this assertion is the tripwire.
- The banner's inner background is opaque by construction
  (`background:#0b7285` inline in `BANNER_HTML`), and its text color is
  covered by the §21/§21b audits like every other forced-background block.

**Scope limit, stated to keep the claim honest:** this is the STATIC half
only. Scroll-persistence as experienced is behavioral and belongs to the
manual M-UX-03 browser re-run (render session 3, recorded per-check-ID
append-only). F-19 flips off manual-FAILED, and P-5 clears, ONLY on that
re-run's PASS — never on this pin alone. A static pin over a surface the
browser has twice disproved is a regression guard, not an acceptance.

### §22b — T-BANNER-01 strengthening (round 8, M-UX-03 third FAIL): the fixed fallback contract

**Written BEFORE the fallback lands** (the house discipline: acceptance
contract precedes fix — T-VEND-01/T-SER-01/T-THEME-01b pattern, fourth
application). **Matrix hook:** F-19 / P-5.

**Founding evidence (states.md §6.9, render session 3, 2026-08-31):** the
FOURTH green-guard/browser-false instance, one layer below §21b. T-BANNER-01
was green AND the browser itself confirmed computed `position: sticky; top:
0px; z-index: 100` on the wrapper — yet the banner scrolled fully out of the
viewport (rect top −1255 at scrollY 1500), because the single clipping
ancestor `div.gradio-container.gradio-container-6-26-0` computes
`overflow: hidden` while the DOCUMENT is the scroller: the sticky's nearest
scrollport never scrolls, so the rule is applied but structurally inert.
**The blindness ladder this registers:** serialization (T-SER-01) →
specificity (T-THEME-01b) → structural context (T-BANNER-01). A static pin
can verify a rule is APPLIED; only the browser can verify it takes EFFECT.
The next guard on any surface class must be written at the layer that can
see the defect — and where no automatable layer can (structural context),
the pin's docstring must SAY so and name the browser check that owns
acceptance.

**Contract for the fallback landing (engineering's own pre-committed
`position: fixed`, owed on §6.9's delivered evidence):**

- (a) the `#pwpm-banner` rule becomes `position: fixed` (top 0, z-index
  kept), still targeting the COMPONENT WRAPPER via `elem_id` — §6.9
  confirmed viability: zero fixed-position breakers between banner and root;
- (b) fixed removes the banner from flow, so the change MUST reserve its
  height (spacer element or container `padding-top`) — a banner that
  overlaps the mode toggle trades an M-UX-03 FAIL for an M-UX-01 regression;
- (c) T-BANNER-01 is updated IN THE SAME CHANGE to pin the new mechanism
  (fixed + height reservation + wiring), **red-first against the current
  sticky build**: the updated pin must FAIL on today's app.py before the
  fallback lands — verifiable by construction, since asserting
  `position: fixed` cannot pass against the shipped `position: sticky` rule;
- (d) the updated docstring records the §6.9 lesson verbatim: the pin
  verifies rule-applied; rule-effective belongs to the browser.

**Acceptance:** F-19 flips off manual-FAILED, and P-5 clears, ONLY on render
session 4's single behavioral check — banner rect within the viewport at
scrollY 1500 in the served 0→1 dark-theme page — recorded per-check-ID,
append-only (§6.10 when recorded). Third time stating it because it has now
been demonstrated four times: a green static pin never accepts a browser
surface.

**STATUS (round 8, 2026-08-31): fallback LANDED, all four clauses.**
(a) `_CSS` now pins `#pwpm-banner { position: fixed; top: 0; left: 0;
right: 0; z-index: 100; }` — wrapper-targeted, left/right anchored against a
fixed box's shrink-to-fit width. (b) Height reserved by `BANNER_SPACER_HTML`:
an in-flow, `visibility:hidden`, content-exact duplicate of the banner,
placed FIRST in the Blocks layout — a top:0 fixed box covers the top of the
VIEWPORT, so the reservation sits at the top of the PAGE and nothing (header,
mode toggle) hides beneath the banner at any scroll position; a duplicate
rather than a magic pixel height tracks the real copy through edits and text
wrapping by construction. The spacer toggles WITH the banner in
`on_mode_change` (pinned). (c) T-BANNER-01 updated in the same change,
red-first by construction: the `position: fixed` assertion cannot pass
against the shipped sticky rule. (d) Docstring carries the §6.9 lesson:
the pin verifies rule-applied; rule-effective belongs to the browser.
Acceptance unchanged — session 4's viewport check only.

---

## 23. T-STR — count-template singular selection (design §6.8 R-10 wiring)

**Landed round 8 (2026-08-31), same change as the R-10 canonical re-vendor.**

Design promoted the R-10 mint into canonical `leaves/design/strings.py` this
round; T-VEND-01 went red mid-flow (the guard catching the open window —
working as designed) and the byte-identical re-vendor into
`pairwisepm/strings.py` landed in this same change, per the round-7
commitment and architecture's §5.12 routing pins: canonical edit first,
mirror rides the same change, package copy never edited directly. The
`str.verdict.stale` tail fix (R-10(ii)) needed zero wiring — as-built flow
is already manual-Compare, so copy and behavior converged on design's
revised text.

**T-STR-01** = `tests/test_packaging.py::test_count_templates_select_singular_variant`
(gradio-gated via importorskip, P-8). Pins the R-10(i) wiring:

- catalogue shape — every `*_one` ID is the singular of an existing plural;
- selection rule — `_S_n(base, 1)` returns the `_one` template, `_S_n(base,
  2)` the plural, for all four wired IDs (`str.partial.verdict_placeholder`,
  `str.m1.progress`, `str.log.unsaved_nudge`, `str.log.uploaded_ok`);
- render-level — the S2 placeholder says "1 factor score to go" at one
  missing and "2 factor scores to go" at two;
- R-10(ii) — the stale card says "Press Compare" and never "Recomputing":
  copy states the as-built behavior, no phantom auto-recompute.

`str.empty.example_cta` is wired as the example button's label (the
previously hardcoded literal now routes through the catalogue).
`str.log.loaded`/`str.log.loaded_one` and `str.m1.progress_zero` remain
catalogued-but-unwired — no rendering call site exists; wiring them without
one would be surface area with no spec backing. T-CUST-01(b) and
T-SER-01(c) updated in this change: both previously pinned the plural-with-1
shape ("1 decisions", "1 factor scores") that R-10(i) exists to kill; they
now assert the singular variant AND the absence of the defect shape.

Suite: 59/59.

---

## 24. T-VEND-02/03 — the vendoring guard must assert on the BOUND module

Traces: architecture.md §4.2/§4.3 (copy authority and declared copy count),
SC-09 via the honesty-copy chain. Registered round 14 on architecture's
A-13-01, independently reproduced from the compliance seat before acceptance.

**The defect being closed.** §17's T-VEND-01 compares two *paths it constructs
itself* from `__file__` and never imports the package it guards. An undeclared
third copy — a NON-editable install in the project venv
(`.venv/lib/python3.11/site-packages/pairwisepm/`, `direct_url.json` =
`{"dir_info": {}}`) — had drifted from the authority at line 79: no
`str.empty.example_cta` (read unconditionally by `app.py:848` at layout
construction, so an off-root launch raises `KeyError` before first paint) and
still carrying the pre-R-10 `"Recomputing…"` tail that F-30 exists to keep out
of served copy. Which copy `import pairwisepm` bound was decided by the
interpreter's working directory, and **T-VEND-01 reported PASS from either
directory**. Reproduced from this seat round 14: from `/tmp` the session bound
site-packages and the full suite still returned all-green.

This is the guard-blindness ladder (§20 → §21b → §22b) landing on the
vendoring boundary: a path comparison verifies the mirror is WRITTEN; only an
import verifies the mirror is what RUNS.

**Contract.**
- **T-VEND-02** — `importlib.import_module("pairwisepm.strings").__file__` MUST
  resolve to the in-repo `pairwisepm/strings.py`, and *those* bytes MUST equal
  the design authority's. Asserting on the imported module is the whole point:
  a version that rebuilds the path from `__file__` does not discharge this.
- **T-VEND-03** — the same invariant for the config authority: the directory
  `pairwisepm.config.default_config_dir()` actually loads MUST be the repo's
  `configs/`. The wheel force-includes `configs/`, so a non-editable install
  leaves a second frozen copy of the mode schemas; D1/D2 resolve into those
  YAML files, and a shadowed copy would serve stale prior weights with no error
  and no failing engine test.
- **T-VEND-04** — the invariant is the COUNT, not the binding: a repo checkout
  MUST expose exactly one importable `pairwisepm/__init__.py` across `sys.path`.
  T-VEND-02/03 assert this session bound the right copy and are silent about a
  duplicate that merely exists — from the repo root `sys.path[0]` wins and they
  stay green while a stale install waits for the first off-root launch. A plain
  `pip install .` into the working venv recreates the A-13-01 condition in one
  command with no other symptom, which is why this is a test rather than a
  checklist habit.
- All skip only in a stripped deployment (design leaf absent), per §17; a skip
  in the repo/CI context is an unexpected skip under P-8.
- T-VEND-01 is **retained unchanged** as the disk-level pin. It is not
  superseded — it claims rule-APPLIED and is honest about that; T-VEND-02/03
  claim rule-EFFECTIVE for the running interpreter.

**Red-first, demonstrated at the predicate level** (round 14, compliance's own
run — the T-NEG-07 method: shown by construction rather than by mutating files
this leaf does not own). A stale shadow copy was placed on `sys.path` in a
scratchpad and the package imported from it: T-VEND-02 clause (a) RED, clause
(b) RED, T-VEND-03 RED — **and T-VEND-01 GREEN in the same run**, which is the
blindness reproduced on demand rather than argued. T-VEND-04 separately: GREEN
against the current `sys.path`, RED with the shadow directory added.

**Environment half — A-13-01 — verified closed round 14** from this seat, not
taken on report: `direct_url.json` now reads `{"dir_info": {"editable": true}}`,
`site-packages/pairwisepm/` is gone, an off-root interpreter binds the in-repo
module, and the full suite from `/tmp` is green *against the right module*.
Per the standing method the guard and the fix are both required; both are in.

**Collateral, priced rather than quietly dropped:** every "own run, N/N"
certification in the record from rounds 9–13 — this leaf's included — was
cwd-conditional evidence, not the unconditional evidence its wording implied.
The runs were real and the numbers were real; what was missing is that nothing
in the suite established *which module* produced them. From round 14 forward
T-VEND-02 establishes it, so the certification means what it says.

## 25. T-DELIV-01 — the banner rule is DELIVERED, not merely written

Traces: SC-09 / R-04 via F-19 and §22b. Registered round 14 on engineering's
demand, after this seat verified the mechanism in the installed tree.

**The gap.** Every other M-UX-03 instrument is a static assertion over app.py's
source; `position:fixed live at app.py:769` evidences that the rule is WRITTEN.
The delivery path is thinner than that pin suggests: app.py passes the rule via
`gr.Blocks(css=...)`, which gradio 6 deprecated. On the constructed object
**`demo.css` is `None`** (verified this round) — the rule survives only in the
private `demo._deprecated_css`, which `launch()` reads at
`gradio/blocks.py:2785`. A gradio major dropping that fallback serves the
banner **unstyled**, with no exception and every static pin green: §22b's
browser-confirmed acceptance silently voided.

**Contract.**
- **T-DELIV-01a** (static, never skips) — both dependency declarations
  (`requirements.txt`, `pyproject.toml` `[app]`) MUST carry a *major upper
  bound* on gradio. A bare `>=X` is not a bound; a `!=` exclusion is not a
  bound either (it excludes a known-bad release, not the unknown future major
  that is the risk). README's pinned Space `sdk_version` major MUST match the
  declared floor, or the bound guards a runtime the Space does not run.
- **T-DELIV-01b** (gradio-gated) — the CSS MUST be present on the object that
  gets served (`css` or `_deprecated_css`) and MUST carry the `#pwpm-banner`
  `position:fixed` rule; and while app.py uses the deprecated constructor path,
  the installed gradio MUST still expose `_deprecated_css`. This is the
  automatable analogue of a browser row: not "the CSS is in app.py" but "the
  CSS is in the attribute `launch()` reads, and `launch()` still reads it".

**Red-first, predicate level** (round 14, own run): `>=6.0,<7` GREEN;
`>=4.0` (the pre-round-14 shipped state) RED; bare `gradio` RED;
`>=6.0,!=6.1` RED; `>=6.0,<=6.99` GREEN. For (b): a Blocks-alike with
`css=None` and no `_deprecated_css` (the gradio-7 scenario) RED; the shipped
gradio-6 object GREEN.

**Standing effect:** widening the bound now reads as **evidence loss** — it
reds T-DELIV-01a and routes to a new render session — rather than passing as
dependency housekeeping. This does not make T-BANNER-01 redundant: the pin
still owns rule-APPLIED, and the browser still owns final rule-EFFECTIVE
(§6.11). T-DELIV-01 closes the middle rung that neither was watching.

---

## 26. T-VEND-05/06 — the copy DELIVERED, and policy values that cannot go stale unseen

Traces: SC-09 (honest by construction) via F-25/F-30, and SC-06/D1-D2 policy
values via the new F-31 row. Registered round 15 on design's CX-14-01 demand
and decisions' verified note about the second `configs/` copy.

**The gap §24 left.** T-VEND-02 asserts the bound module's bytes equal the
design authority's — strictly stronger than any value assertion — but it
**skips when the design leaf is absent**, and that is precisely the stripped
install a user gets. So on a shipped install, no instrument asserted anything
about the copy that reaches the user. The round-14 defect (a bindable module
missing `str.empty.example_cta` and still carrying the pre-R-10 `"Recomputing…"`
tail) was invisible there by construction. **File-identical is not
copy-delivered, and copy-delivered-in-a-checkout is not copy-delivered-on-an-
install.**

- **T-VEND-05** (value level, **never skips**) — on the module `import
  pairwisepm.strings` actually binds: `str.empty.example_cta` MUST exist
  (`app.py` reads it at layout construction; absent ⇒ KeyError before first
  paint), and `str.verdict.stale` MUST end `"Press Compare to recompute."` and
  MUST NOT contain `"Recomputing"`. The second clause is not cosmetic: a stale
  card promising an automatic recompute is a judge asserting work it is not
  doing — the Spine's forbidden confidence overstatement, aimed at the tool's
  own behavior (design §6.8 R-10(ii) / F-30).
- **T-VEND-06** (repo-checkout gated) — the invariant on `configs/` is NOT
  "no second copy" (the wheel force-includes one, and that is what makes
  `default_config_dir()` resolve on a non-editable install) but **"no STALE
  second copy"**: any `configs/*.yaml` found under another `sys.path` entry
  MUST be byte-identical to the repo authority. Zero duplicates is a passing
  state; a drifted duplicate is not.

**Why (06) is the more consequential half.** A stale strings copy crashes
loudly at `app.py:848`. A stale configs copy serves old prior weights with no
error and no failing engine test — a plausible wrong verdict, arriving as a
number nobody would question. D1/D2 resolve into these files; the failure mode
is: repo YAML edited with `resolution_source` per value, suite green,
provenance lines citing values the engine never loaded.

**Red-first, demonstrated not asserted** (round 15, own run, synthetic shadow
on `PYTHONPATH` built in scratchpad — no repo file mutated): against a shadow
package carrying the pre-R-10 tail with the CTA key removed, and a shadow
`configs/one_to_n.yaml` with one edited line, **T-VEND-02, 03, 04, 05 and 06
all FAIL and T-VEND-01 PASSES in the same run**. With the shadow removed:
67/67 from the repo root and 67/67 from an off-root working directory.
T-VEND-06 is not vacuous today — it compares two real duplicates on this
machine (`site-packages/configs/{one_to_n,zero_to_one}.yaml`, currently
byte-identical, install-time frozen).

**Standing effect.** After the D1-D6 resolution round edits the repo YAML, a
surviving install-time snapshot goes stale in that instant and T-VEND-06 reds
— which is the alarm firing at the moment the hazard becomes live, not a
month later. Remedy is reinstall or uninstall; never edit the copy.

---

## 27. Round 16 — a guard's ACTIVATION, and the rendered text outside the catalogue

Two corrections, both of the same species and both reported by another seat
against instruments this leaf owns.

### §27a — the skip predicate: activation narrower than subject (T-VEND-03/04/06)

Engineering reproduced it rather than argued it, and this seat reproduced the
reproduction. All four round-14/15 vendoring guards gated on
`_in_repo_checkout()` — the presence of `leaves/design/strings.py`. That is
the right precondition for **T-VEND-01/02 only**, whose subject IS the design
authority file. It is the wrong one for:

* **T-VEND-03** — which config directory the engine LOADS;
* **T-VEND-04** — how many importable copies of the package exist on `sys.path`;
* **T-VEND-06** — whether a duplicate schema has gone stale.

None of those has anything to do with the design leaf, and the gate was
narrowest exactly where the hazard is widest: `pyproject.toml`'s
`[tool.hatch.build.targets.sdist] include` ships `tests` **without** `leaves`,
so in an installed or sdist tree the guards were present and inert — while a
repo checkout, the only place they ran, is the case where `sys.path[0]`
already wins and a shadow is least likely.

**Measured, own run, in an sdist-shaped tree** (`pairwisepm/`, `configs/`,
`tests/`, `app.py`, `pyproject.toml`; no `leaves/`), built in scratchpad and
removed after — no repo file mutated:

| | T-VEND-01 | 02 | 03 | 04 | 05 | 06 | result |
|---|---|---|---|---|---|---|---|
| round-15 predicate | skip | skip | skip | skip | **pass** | skip | `1 passed, 5 skipped` |
| round-16 predicate | skip | skip | **pass** | **RED** | **pass** | **pass** | `1 failed, 3 passed, 2 skipped` |

The two remaining skips are T-VEND-01/02 and they are honest: with no
authority file there is nothing to compare against. The RED is a **true
positive** — that tree genuinely exposed two importable `pairwisepm` copies
(its own and the repo's, via the editable `.pth`), which is precisely the
condition T-VEND-04 exists to name and which the old predicate hid.

Corrected predicates, each naming its own subject:

* T-VEND-03/06 → `_repo_config_authority()` (`<root>/configs` is a directory).
* T-VEND-04 → **no skip at all.** Its subject is `sys.path`, which exists in
  every tree. Where the tree carries a package authority, identity is asserted
  as before; where it does not, the COUNT invariant is still the whole claim
  and is asserted alone (`len(found) <= 1`).

**The lesson, stated as the mirror of A-13-01:** that was a guard whose SCOPE
was narrower than its claim. This was a guard whose ACTIVATION was narrower
than its subject. The two are indistinguishable in a green suite — `65
passed`, `67 passed`, and four of them never ran.

**Census asymmetry, carried into the guards themselves** (architecture's
round-16 demand, accepted): T-VEND-04 is a **COUNT invariant whose scope is
the PACKAGE authority only**. T-VEND-03 is a **RESOLUTION invariant** — a
second `configs/` tree is *permitted by design*, because the wheel's
`force-include` is what makes `default_config_dir()` resolve identically from
a clone and from a non-editable install. Both docstrings now say so, so the
pair cannot be compressed into "exactly one copy of everything" — a reading
that would either demote the package count to a preference or invite deleting
the force-include, which would break `pip install pairwisepm`'s ability to
find its schemas at all. T-VEND-06 covers the config side's real invariant:
not *no second copy* but *no STALE second copy*.

### §27b — T-COPY-01/01b and T-NEG-08 — `tests/test_copy_surfaces.py`

Design's §6.15 census found the copy chain certifying one population of
three. Every copy-integrity instrument on this board — T-VEND-01 (files on
disk), T-VEND-02 (the bound module's bytes), T-VEND-05 (the bound module's
values), and design's mirror checks — is scope-limited to
`leaves/design/strings.py`. Two other populations render to the browser and
nothing watched either.

**T-COPY-01 — configs rendered text is written, not stubbed.** The mode
schemas carry `label`, `factors[].name/.scale/.rationale`,
`flags[].name/.description` and `evaluative_inputs[].name/.note` — all
rendered. The only prior coverage was `test_engine.py::test_config_shapes`,
which asserts `rationale.strip()` and `scale.strip()`: non-empty, not
correct. Reds on empty or placeholder text (`TBD`, `TODO`, `FIXME`, `XXX`,
`WIP`, `lorem ipsum`, `placeholder`, `???`).

**T-COPY-01b — a rendered label is prose, not the machine key.** Catches a
schema edit that fills a text field from `key` (`impact_primary_metric`)
instead of writing the label (`Impact on primary metric`): non-empty,
renders, reads to a user as a leaked internal identifier.

**T-NEG-08 — the Spine's excluded-from-score refusal is VISIBLE.** Spine,
Scope Boundaries (Out): evaluative factors are *"captured and displayed as
labeled override inputs only"*. The engine honors that structurally; what
tells a **user** is the `(not scored)` marker on each of four `gr.Textbox`
labels in `app.py`. Those four literals are not in the catalogue, so no
instrument watched the sentence a presenter points at when they say the model
refuses to score strategic fit. Censused **by AST**, not regex, so a moved
line or reflowed call cannot silently empty it; the count is pinned at four
so a restructured panel is a deliberate diff rather than a vacuous pass.

**T-NEG-08a** — the same refusal at the config authority (`note` contains
"not scored", in both modes; the log record's copy of it).
**T-NEG-08b** — the refusal is *structural*: `EvaluativeInput` must never
gain `prior_weight`/`sign`/`tag`/`seed_mean`/`seed_std`, and no key may be
both a scored factor and an evaluative input.

**Red-first, demonstrated not asserted** (own run, mutated copies in
scratchpad; no repo file touched). Three mutations — a rationale replaced with
`TBD`, one `(not scored)` deleted from a label, one schema `note` reduced to
`"captured"` — produce **3 failed, 2 passed** here, each with the offending
field named. The **same three mutations leave `tests/test_engine.py` entirely
green** (44 passed; its one failure in the scratchpad tree was a missing
`requirements.txt`, unrelated). That is design's finding measured rather than
restated: until this file, the Spine's most quotable refusal could be deleted
from the screen with the suite green.

**Scope, stated so this file is not read wider than it checks.** These are
NEGATIVE tests. They do **not** invent a copy authority for either population
— that is design's ruling to make, not this seat's. They pin the properties
checkable without one, so the two open rows rest on an instrument rather than
on prose while the authority question is settled.

**Suite after this round: 72/72 from the repo root and 72/72 off-root**, own
run (67 + 5).

---

## 28. Round 17 — a gate's green must entail that assertions ran

### §27c — T-VEND-07 — `tests/test_vendoring.py` cannot return an all-skipped green

**Registered on sequencing's round-16 demand.** Gate P-14 makes
`pytest tests/test_vendoring.py` the pre-flight deciding whether the M-UX-02a
sitting produces a RECORD at all. The defect they named is in the file, not in
the gate: **pytest exits 0 on an all-skipped file.** Until §27a, all four
original guards gated on the design leaf's presence and `pyproject.toml`'s
sdist include ships `tests` without `leaves`, so engineering measured
`4 skipped in 0.00s` in an sdist-shaped tree — a green with zero assertions
behind it. A witness would have recorded a pass, and F-17 would have flipped a
Spine metric on a run that measured nothing.

§27a fixed the predicates. §27c makes the fix un-undoable, because a predicate
is one line and the pressure to add a skip arrives exactly when a guard is
inconvenient. The instrument reads `tests/test_vendoring.py`'s own AST — not a
regex, so a reflowed call or a moved line cannot silently empty it — and
asserts three properties:

1. **The floor.** `test_exactly_one_importable_copy_of_the_package` (T-VEND-04,
   the count invariant) and `test_bound_module_carries_the_r10_corrected_copy`
   (T-VEND-05, the served-value pin) carry no `pytest.skip` call and no
   skip/skipif marker. In any tree, in any install, a green in that file means
   at least these two asserted.
2. **Activation names its own subject.** Every clause that does skip skips on
   `_in_repo_checkout` (the design-authority pair, whose subject IS
   `leaves/design/strings.py`) or `_repo_config_authority` (the config pair,
   whose subject IS `<root>/configs`). A third predicate is permitted but must
   red here first — which is where activation-vs-subject gets examined rather
   than assumed. This is the round-16 defect class turned into a tripwire: a
   guard whose ACTIVATION is narrower than its SUBJECT reads identically to a
   passing suite.
3. **Counted, not just named.** At least two clauses are unskippable, asserted
   as a count, so deleting a floor clause cannot be masked by renaming another.

**Red-first, demonstrated on scratch copies with no repo file mutated:**

| mutation | result |
| --- | --- |
| `pytest.skip` added to T-VEND-05 | RED — "one of gate P-14's floor clauses and it has acquired a skip predicate" |
| T-VEND-06's predicate swapped for an unsanctioned `_some_new_gate` | RED — "skips on a predicate this file does not sanction" |
| unmodified file | GREEN, `7 passed in 0.04s` |

**What it does NOT claim.** It does not make T-VEND-01/02/03/06 run everywhere,
and it does not pretend to: those skip honestly where their own subject is
absent. It removes exactly one state — a green with nothing behind it. P-14's
matrix row carries the operative reading (`exit 0` **and** `0 skipped`, skip
count recorded beside the result); this guard is why that clause is enforced
rather than trusted to a presenter counting skips at the hour.

### §27d — premise correction inside T-VEND-03/04/06 (round 17)

The guards said the second `configs/` tree is left by "any non-editable
install". **It is left by every install of this project, editable included** —
hatchling's editable target derives from the wheel target and inherits
`[tool.hatch.build.targets.wheel.force-include]`. Verified from this seat:
`direct_url.json` = `{"dir_info": {"editable": true}}`, no
`site-packages/pairwisepm/` directory (only the `.pth`), and the same
dist-info's RECORD listing both YAML files at sha256 values recomputed here
from the repo's `configs/` and matching. Two `configs/` trees are on `sys.path`
in a normal pytest session.

Consequence, stated in the docstrings because it changes what a red MEANS:
T-VEND-06 does not wait for a future reinstall — it reds on the next suite run
after the D1/D2 write, on the install this repo has today. That red is the
guard working. Remedy is refresh-or-remove (`pip install -e .` again, or
`pip uninstall pairwisepm`); never a hand-edit of the site-packages copy, and
never deleting the `force-include`, which is what lets an installed package
find its schemas at all. Demonstrated: a divergent duplicate on `sys.path`
reds T-VEND-06 (`1 failed, 5 passed`), scratch only.

**Suite after this round: 73/73 from the repo root and 73/73 off-root**, own
run (72 + 1).

### §27e — T-COPY-02/02b/02c/02d — the AUTHORITY half of F-32/F-33 (round 18)

§27b pinned everything about `configs/*.yaml` text that is checkable WITHOUT a
copy authority: it exists, it is not a placeholder, it is not a leaked machine
key. What no instrument could assert was whether the text is the text design
approved — and this seat deliberately refused to invent that authority, because
a test encoding an unratified expectation makes a preference look like a
requirement. Design ruled it in round 17 (states.md §6.17, F-32 answer (a)) by
creating `leaves/design/copy-authority.yaml`: generated from live bytes,
ratified by the seat that owns the copy, carrying **no** policy/numeric field
so the D1-D6 resolution round cannot red it.

**T-COPY-02 — config text == design's ratified fixture.** Diffs `label`,
`factors[].name/.scale/.rationale`, `flags[].name/.description` and
`evaluative_inputs[].name/.scale/.note` against the fixture, **both
directions**: a key ratified but absent from the schema, a key present but
unratified, and any value mismatch all red. A one-way diff is how a copy guard
goes quietly empty. Reds on exactly one event — rendered text moving without
design ratification — which converts design's §6.12(b6) per-line notification
from a promise five seats accepted into an instrument.

**T-COPY-02b — the four `app.py` evaluative labels == the ratified four.**
T-NEG-08 pins the MARKER and the count; it is silent about the rest of the
string, so `A · Strategic fit (not scored)` → `A · Strategic Fit (not scored)`
passes it. That wording is what gtm's tour stop 483 narrates and what design's
§6.17 names as the sole on-screen carrier of the refusal, so it is pinned
against the ratified set. This also makes gtm's byte-identical-move demand
machine-checkable: when ENG-COPY-EVALLABELS-01 fires, a move that also tidies
the phrasing reds in the push that does it.

**T-COPY-02c — an exemption must cite a guard that EXISTS.** Round-18 finding,
and a correction to this seat's first draft of it. Writing T-COPY-02 exposed a
rendered config field that **no census on this board carries**: `banner`.
Design's §6.15 seven-field census, their round-17 four-field correction, F-32's
row and the fixture's own `render_map` all enumerate this population and none
lists it — yet it is the permanent 0→1 claim-limiting banner, the most
Spine-load-bearing string in either schema. The clause was first drafted to
assert it against `str.banner.01` on the premise that nothing asserted the
quotation. **That premise was false.** Demonstrating the red first (§27f)
reddened three clauses, two already shipped: `test_zero_to_one_banner_mandatory`
and `test_banner_attached_and_wording` both pin the banner against
`STRINGS["str.banner.01"]`. The field was covered; only the CENSUS was wrong.
So the clause became what was actually missing: `_RATIFIED_ELSEWHERE` maps an
exempted field to its authority key, file and clause names, and T-COPY-02c
CHECKS the citation — file present, clauses present by AST, each still
referencing the key. Delete or rename one of the banner's two guards and this
reds, naming the field that just lost its authority.

**T-COPY-02d — the census cannot go stale by someone adding a field.** Every
copy census on this board has been a hand-written list and every one has been
wrong at least once inside three rounds. This derives the population from the
dataclasses: every `str`/`Optional[str]` field on
`ModeConfig`/`Factor`/`Flag`/`EvaluativeInput` that is not a declared machine
identifier must be covered by the fixture diff or by a named alternative
authority. It never skips. It found `ModeConfig.fingerprint` on its first run
(correctly classified as an identifier) and it is what makes the `banner` gap
above impossible to reintroduce.

### §27f — T-COPY-03 and the RED-FIRST ADMISSION STANDARD (round 18)

**T-COPY-03 — the copy guards cannot be quietly weakened.** gtm deleted a
presenter eyes-on check from the witness pre-flight on the strength of
T-NEG-08 and asked for a notification if that test is ever weakened, renamed,
made skippable or removed. Accepted — and executed as an instrument, because a
promise about an instrument that two other seats have retired checks against
should not rest on memory. Reads this file's own AST and asserts: (1) every
required clause present by name; (2) T-NEG-08 still censuses by `ast.parse`
and still pins the count at four (the two weakenings gtm named by hand: a
regex form empties on a reflow, a dropped count pin passes vacuously on zero
labels); (3) no clause carries a skip marker and every `pytest.skip` lives in a
sanctioned helper that names its own subject — spec §27a applied prospectively
to the newer file, not only retrospectively to the older one; (4) a counted
floor of clauses that never skip, so gate P-15 cannot go green on a run in
which nothing asserted.

**ADMISSION STANDARD, registered against the D1-D6 resolution-round procedure
(engineering's demand, accepted whole).** No further gate, command or check
enters that procedure without a **demonstrated red**: the mutation that makes
it fail, run and reported by the proposing seat, in scratch, with no repo file
mutated. A check nobody can red is indistinguishable at 11pm from a check that
already passed, and a procedure long enough to skim is a procedure that gets
skimmed on the one day it matters. This seat owes it first and paid it this
round — seven mutations, scratch tree, no repo file touched:

| # | Mutation | Red |
|---|---|---|
| 1 | a factor rationale reworded in `configs/one_to_n.yaml` | T-COPY-02 |
| 2 | `Strategic fit` → `Strat. fit` in an `app.py` label | T-COPY-02b + T-NEG-08 |
| 3 | `Strategic fit` → `Strategic Fit` (marker and count intact) | T-COPY-02b alone |
| 4 | `rationale` dropped from `_FACTOR_TEXT_FIELDS` | T-COPY-02d |
| 5 | T-NEG-08's AST census swapped for an empty tree (regex form) | T-COPY-03 (+2) |
| 6 | T-NEG-08's `== 4` count pin softened to `== len(evaluative)` | T-COPY-03 |
| 7 | T-NEG-08 deleted outright / a floor clause given a skip path | T-COPY-03 |
| 8 | `test_banner_attached_and_wording` renamed in `test_engine.py` | T-COPY-02c |

Skip behavior measured rather than asserted: in an sdist-shaped tree (`leaves/`
absent) the file reports **8 passed, 2 skipped** — exactly the two
fixture-dependent clauses, on their own subject.

**Suite after this round: 78/78 from the repo root and 78/78 off-root**, own
run (73 + 5).

---

## 29. Round 19 — the audit view's honesty, the guard that is not a test, and a green that depended on collection order

### §27g — T-NEG-09 / T-NEG-09b — `tests/test_audit_honesty.py` (rows F-34 / F-35)

Design's §6.18 finding: `app.py` has TWO rendering surfaces and every copy
census on this board measured one. The `gr.*` CONSTRUCTION surface is censused
(21 literals, partitioned in design's §6.17(ii)); the RUNTIME-HTML surface —
six `render_*` builders whose output reaches the browser through `gr.HTML(...)`
— contributes ZERO literals to that predicate and paints at least thirteen
uncatalogued strings in the audit view alone.

**T-NEG-09 — the 0→1 no-prediction caption ARRIVES on the screen.** Three
instruments already guard `str.audit.01_caption`'s bytes (T-VEND-01/02/05) and
one sweeps it for banned words (T-NEG-04b); all four are guards on the STRING,
and none of them asserts that a user ever sees it. Deleting the
`if log.n("zero_to_one")` gate in `render_audit` leaves the whole suite green
with the Spine's `Out: accuracy claims in 0→1 mode` refusal gone from the
surface it was minted for — the F-33 defect one view over. Asserted in BOTH
directions, because a caption pasted unconditionally is a different defect that
passes a one-way check: absent on a pure 1→N log, present once a 0→1 record
exists. Skips only where gradio is absent (its own subject, gated exactly as
`test_packaging.py::_load_app` is).

**T-NEG-09b — the pooled statistics are censused and classified.** A CENSUS,
not a requirement, and the distinction is the design of the clause: `n` is
POOLED-DISCLOSED (it prints the per-mode split beside the total), while
`kendall_zeta`, `brier`, `outcome_brier` and `override_rate` are POOLED-F-35 —
computed over the whole log, under a caption that scopes itself to 0→1, with no
denominator on screen. Passing a mode through (THE FIX, owner engineering) drops
a call out of the census and leaves the clause GREEN; adding a fifth undisclosed
pooled statistic reds it in the change that adds it. Never skips: its subject is
`app.py`'s AST, so this file cannot return an all-skipped green either.

**Reproduction, with the finding narrowed by the reproduction.** A≻B, B≻C, A≻C
in 1→N displays ζ = 1.00. One 0→1 comparison reversing the **A–C** pair drops
the displayed row to 0.00 while `kendall_zeta("one_to_n")` stays 1.00.
Reversing the **A–B** pair instead does NOT move it (B≻A, B≻C, A≻C is still
transitive). So the condition is a cross-mode re-comparison that both overwrites
an edge AND closes a circular triad — the mechanism design named
(`log.py:198-206`: unordered-pair keys, most-recent-write-wins) is exactly
right, and the wider sentence a reader would quote off it is not.

### §27h — T-COPY-02e — an exemption's guard, when the guard is not a test

Design ruled `banner` in §6.19 by option (b): exempt from
`leaves/design/copy-authority.yaml` by AUTHORITY — the catalogue's
`str.banner.01` owns those bytes — with the render_map row naming `app.py`'s
module-level `assert Z2O.banner == S["str.banner.01"]` as the guard. Architecture
demanded the row name that assert, on the ground that it is stronger than the
diff: it runs at import, cannot acquire a skip, cannot be deselected by `-k`,
and reds as *the app does not start*. Both are right, and together they are the
reason the assert needed a guard of its own: **an instrument nothing watches is
one keystroke from being an instrument nothing has**, and this one is a bare
`assert` in a UI file — the easiest line in the repository to delete while
chasing an unrelated import error.

T-COPY-02e reads `app.py`'s AST and requires a MODULE-LEVEL assert whose test
names both the banner and `str.banner.01` (nested inside a function it would
fire on nobody's launch). It deliberately does NOT assert the banner's words —
`test_zero_to_one_banner_mandatory` and `test_banner_attached_and_wording` do,
and T-COPY-02c checks that those two still exist — nor that the banner reaches
the screen (F-19/P-5's browser record owns that).

**Scope word on T-COPY-02, architecture's demand, now answerable as four-of-five
rather than as a hole:** the fixture's `render_map` carries TEN names, five
RENDERING; T-COPY-02 diffs the nine design ratified, which on the rendering half
is four of five. The fifth is `banner`, exempt by authority with its instruments
named. A green T-COPY-02 means *the ratified config copy matches design's
ratified text*, never *all rendered config copy is verified*.

### §27i — N-01's guard was ORDER-DEPENDENT (gate P-1)

`pytest tests/` opened round 19 at **1 failed, 79 passed** — the failure being
`test_no_llm_or_network_imports`, the negative test on the Spine's first
refusal — and the same clause passed when run alone. The import half asserted
that no forbidden module appears in `sys.modules` **of the pytest process**,
which is not the product: it is whatever every previously-collected test file
happened to import. `tests/test_packaging.py` execs `app.py` → gradio → `httpx`,
a legitimate UI dependency, and the clause was green only because `test_engine`
sorts before `test_packaging`. Demonstrated on the unmutated repo:

    pytest tests/test_packaging.py tests/test_engine.py
    → FAILED test_no_llm_or_network_imports - AssertionError: httpx

The trigger was this seat's own new file (`test_audit_honesty.py` renders the
audit view for real, sorts first, imports gradio one file earlier); the defect
predates it and reproduces with that file deleted.

Corrected in the strengthening direction: the claim is asserted **in a child
process** — importing `pairwisepm` and every submodule in a fresh interpreter
pulls in no LLM and no network client. Order-independent, a property a
`pip install` of this project can actually break, and strictly wider than the
regex source scan, which stays unchanged.

| # | Mutation | Red |
|---|---|---|
| 1 | none — the shipped repo, run as `pytest tests/test_packaging.py tests/test_engine.py` | old form of T-NEG-01 (the defect) |
| 2 | `_il.import_module("httpx")` appended to `pairwisepm/engine.py` (no `import httpx` line for the regex to find) | new form of T-NEG-01 |
| 3 | `assert Z2O.banner == S["str.banner.01"]` deleted from `app.py` | T-COPY-02e **alone** — control run beside it, nothing else moved |

**Standing lesson, and it belongs with §27a and §27c rather than beside them:** a
suite lies about itself in more than one way. §27a was activation narrower than
subject; §27c was a green in which nothing asserted; **§27i is a green that
depends on the order the suite was invoked in.** All three read identically to a
passing run. A count is evidence only if the same clauses assert in any
invocation order, and no clause may assert on the state of the test process
when it means to assert on the product.

**Suite after this round: 81/81 from the repo root and 81/81 off-root**, own
run (78 + 3); 61/61 on the two-file ordering that was red when the round began;
sdist-shaped tree, both copy files: 11 passed, 2 skipped.

### §27j — the round-19 repair's own residue: a floor, a scope word, an owner (round 20)

§27i strengthened N-01's guard and, in doing so, created a one-token exit that
did not exist before. The clause's red now reads `importing the engine pulls in
['httpx']`, and the fastest edit that clears it is deleting `"httpx"` from
`FORBIDDEN_IMPORTS`: no test removed, no docstring touched, suite green, and the
Spine's *"runs entirely offline after download"* (Success Metrics) plus
*"Out: any LLM in the runtime loop"* unwatched from that minute. **T-NEG-01d**
(`test_the_no_llm_guard_cannot_be_quietly_weakened`, design's demand) is the
floor, in the T-COPY-03 / T-VEND-07 pattern: read off `test_engine.py`'s own
AST, it asserts (1) `FORBIDDEN_IMPORTS` still names every module in
`_NO_LLM_FLOOR` — the tuple may GROW freely and shrinks only by an edit that
moves the floor in the same change; (2) neither refusal clause carries a skip
marker or calls `pytest.skip`; (3) **both halves survive** — the child-process
probe (`subprocess.run` on `sys.executable`) and the source scan (a regex built
from the same tuple, naming `app.py`); (4) `test_no_network_calls_at_runtime` is
still present and unskipped. It asserts SHAPE, never behaviour, so strengthening
the guard keeps it green — a floor that a legitimate improvement reds is a
freeze, and this board has refused that shape twice.

**Scope word on N-01, decisions' demand, and it corrects a sentence this seat
wrote one round ago.** The docstring ended *"The source scan is unchanged and
still covers `app.py`"* — true of the TEXT, false of the GRAPH. The source scan
is a regex over DIRECT `import`/`from` lines; the child-process probe's subject
is the ENGINE only. So `app.py`'s TRANSITIVE import graph is asserted by nothing
in N-01, deliberately: app.py imports gradio, gradio imports `httpx`, that UI
dependency is legitimate, and the runtime claim on that surface is held by a
different instrument — `test_no_network_calls_at_runtime`'s socket kill-switch,
which runs a full cycle in both modes. The false sentence is struck in place with
its text legible; a reader asking whether a new app-side dependency is covered by
N-01 must read **no**.

**T-NEG-08c** (`test_the_pick_question_asks_for_the_users_own_pick`, design's
§6.19(iii) demand) closes the residue design declared rather than papered over:
`"Which do you actually pick?"` was recorded as "covered in the interim by the
eyes-on five", gtm correctly retired that ritual in round 17 on the strength of
executed censuses, and between those rounds the literal had ZERO instruments. It
is its OWN clause, never a fifth member of T-NEG-08's set, because T-NEG-08's
`== 4` count pin is what makes a restructured panel rendering zero labels fail
and because widening that census would silently widen engineering's bounded
ENG-COPY-EVALLABELS-01 trigger. Byte-exact, count-pinned at one, plus the widget
kind (`gr.Radio` — a two-choice carrier is what makes the logged pick one of
exactly the two ideas compared).

**The unparseable-fixture clause** (engineering's demand) is the third
observable state of `leaves/design/copy-authority.yaml`: absent → honest skip on
the pair's own subject; present → diffed; **present and unreadable → RED, with
an owner**. It stays a red — "design's ratified text is unreadable" is not the
claim "this tree has no design leaf" — and only the sentence changes: whose file
it is, that the first action is to re-run, and that blanking it to obtain a skip
converts a loud red into a quiet green. Engineering OBSERVED the state (mid-save,
their own edits confined to two docstrings) and priced the class without mutating
a repo file: 855 of the fixture's 8593 single-byte prefixes fail to parse.
`UnicodeDecodeError` is caught beside `yaml.YAMLError` because demonstrating the
red found what reasoning had not — a truncated save can cut a multi-byte
character and raise out of `read_text` before pyyaml is reached.

Red-first, as the standard requires. Four mutants for the floor (scratch copies
of `test_engine.py`, no repo file mutated) and four scratch trees for the copy
clauses (symlinked `configs`/`pairwisepm`, copied `app.py` and fixture):

| # | Mutation | Red | Note |
|---|---|---|---|
| 1 | `"httpx"` deleted from `FORBIDDEN_IMPORTS` | T-NEG-01d alone | **T-NEG-01 itself stayed GREEN** — the whole point |
| 2 | `@pytest.mark.skip` on T-NEG-01 | T-NEG-01d alone | the clause reports as skipped, the floor reds |
| 3 | source-scan half deleted from T-NEG-01 | T-NEG-01d alone | probe-only still reads like a guard |
| 4 | child-process probe half deleted | T-NEG-01d alone | regex-only still reads like a guard |
| 5 | `actually` dropped from the pick question in `app.py` | T-NEG-08c alone | control run beside it, one pre-existing scratch-tree red in both |
| 6 | `gr.Radio` → `gr.Dropdown` on the same widget | T-NEG-08c alone | wording green, carrier changed |
| 7 | fixture truncated mid multi-byte character | T-COPY-02 + 02b | message owned, not a bare `UnicodeDecodeError` |
| 8 | fixture given an unterminated quoted scalar | T-COPY-02 + 02b | message owned, `ScannerError` quoted inside it |

**Suite after this round: 83/83 from the repo root and 83/83 off-root**, own run
(81 + 2); `pytest tests/test_audit_honesty.py tests/test_engine.py` 48/48 — the
ordering pair that was red two rounds ago; gate P-15's file 12 passed / 0 skipped
in a checkout and **10 passed / 2 skipped** in an sdist-shaped tree (T-NEG-08c
runs there: the sdist ships `app.py`, so its activation follows the
cross-reference clauses rather than the fixture-governed pair).

---

## Manual checks referenced by the traceability matrix (not automatable)

- **M-UX-01** — both ideas visibly on one screen, single sitting; no wizard split.
- **M-UX-02** — timed blank-to-verdict walkthrough ≤ 5:00, fresh user. **Round-13
  scope split:** M-UX-02a (1→N) is the half both registered instruments measure;
  M-UX-02b (0→1) has no instrument and no scheduled sitting. A 1→N record
  converts SC-06 for 1→N only.
- **M-UX-03** — 0→1 banner visible in every UI state (entry, verdict, audit).
- **M-DOC-01** — README epistemics checklist (priors = stated editable policy;
  no 0→1 accuracy claim; "the LLM's job was at build time").

Owners per the matrix. A release candidate ships only with all automated specs
green and the four manual checks signed off.
