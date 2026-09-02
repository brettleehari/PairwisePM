# PairwisePM — Technical Specification (derives from spine/SPINE.md)

This document is the locked technical contract every Leaf builds against. It was
settled in the working session of 2026-08-30 against the Noise / clinical-vs-mechanical
research base (Meehl; Grove et al. 2000; Dawes 1979; Goldberg 1970; Bradley-Terry 1952;
Kahneman/Sibony/Sunstein 2021). Where this document and the Spine conflict, the Spine wins.

## 1. Product shape

Two competing GenAI product ideas, A and B, entered on the same questionnaire, on one
screen, in one sitting (occasion-noise cancellation: the pairwise delta cancels only
noise shared by both scores, so both ideas MUST be scored together). A mode toggle
selects the category:

- **0→1 (search)** — searching for product-market fit. Structure and consistency only;
  the UI carries a permanent banner: no predictive-accuracy claim.
- **1→N (allocation)** — roadmap allocation in an established product. The mechanical
  baseline with accuracy claims, earned over time via calibration.

Runtime is purely mechanical: numpy-only, no LLM, no API key, no network calls.

## 2. Factor schemas (editable config, one file per mode)

All factors z-scored against the accumulated log (seed distributions ship in config
until the log grows). Each factor carries: scale, prior weight, sign, a written
rationale, and a **lever|fact** tag (lever = changeable by working; fact = it is what
it is). Evaluative inputs (strategic fit, brand) are captured and displayed but
EXCLUDED from the mechanical score — labeled override inputs.

### 1→N mode
| Factor | Scale | Prior w | Tag |
|---|---|---|---|
| Impact on primary metric | vs. named past feature, −2..+2 | .25 | lever |
| Capability feasibility | eval/prototype pass rate, 0–4 | .20 | lever |
| Reach | users affected/quarter (number) | .15 | fact |
| Unit economics | value per use vs. inference cost, 0–4 | .15 | lever |
| Data flywheel | usage→data→better feature, 0–4 | .10 | fact |
| Risk surface | hallucination/compliance exposure, 0–4 reversed | .05 | lever |
| Effort | person-weeks, reference-class adjusted | −.10 | lever |

### 0→1 mode
| Factor | Scale | Prior w | Tag |
|---|---|---|---|
| Problem severity × frequency | 0–4 | .25 | fact |
| Capability-trajectory exposure | −2..+2 (stronger vs. absorbed as frontier models improve) | .20 | fact |
| Evidence of pull | interviews/waitlist/pre-orders, 0–4 | .20 | lever |
| GenAI-necessity | generative core vs. bolt-on, 0–4 | .15 | fact |
| Data/distribution advantage | 0–4 | .10 | fact |
| Cost to test | weeks to falsifiable prototype | −.10 | lever |
| Ceiling | top-box flag | unweighted | — |

The Ceiling flag never enters the score: when set, the verdict card routes the idea to
human portfolio judgment ("high-ceiling outlier — portfolio decision, not averaged in").

Prior magnitudes for both tables are PENDING HUMAN SIGN-OFF — Decisions Leaf entries
D1 and D2. Build with these defaults; they are config, not code.

## 3. The regression ladder (the model)

| Level | Model | Trains on | Active |
|---|---|---|---|
| M0 | Prior-weight linear score, p = σ(wᵀd), d = z_A − z_B | nothing | always |
| M1 | Ridge logistic Bradley-Terry on factor deltas, **shrinkage centered on M0's prior weights (not zero)** | user's logged picks | ≥ ~10 decisions |
| M2 | Same regression vs. labeled outcomes | outcome labels | ≥ ~45 outcomes (future) |
| M3 | Nonlinear ML | hundreds of outcomes | future, gated |

- Equal-weight ablation toggle (all |w| equal, signs kept) available as scientific control.
- MAP regularization is mandatory from day one (two-fictitious-games / L2): pure MLE
  diverges on small or disconnected comparison graphs.
- Intercept: constrained to zero for scoring (symmetry — swapping A and B must flip p
  exactly). ALSO fit unconstrained as a diagnostic: a significantly nonzero free
  intercept = measured presentation-order bias, surfaced in the audit report.
- M1 vs. M0 weight divergence displayed as "what your revealed policy weighs vs. what
  you say you weigh."

## 4. Uncertainty & honesty rules

- Bootstrap over factors → interval on the win probability. Interval straddling 50% →
  verdict renders as "too close to call — gather evidence", never a forced winner.
- 0→1 mode: permanent structure-not-prediction banner.
- Calibration: Brier score accumulates from decision 1; reliability curve when n permits.
- ζ (Kendall's coefficient of consistency, from circular triads over the log) is the
  live per-judge noise meter; report it in the audit view.

## 5. Leverage panel (the actionable add-on)

For every comparison, on the linear logit L = wᵀd:
1. **Per-factor leverage**: signed contribution w_j·d_j bar chart.
2. **Path to parity**: for the loser, smallest single-factor change reaching 50/50 (and
   60/40), reported in RAW units (required z-shift = L/w_j, converted via factor std).
3. **Lever/fact filter**: parity paths proposed only through levers; if every path runs
   through facts → "loses on fundamentals — no working-harder path flips this."
4. **Fragility flag**: if the winner's margin flips on a small plausible move of one
   factor → "margin rests on the <factor> estimate — re-estimate before committing."

## 6. Decision log

Local JSONL, downloaded/uploaded by the user (Space stores nothing server-side).
Each record: timestamp, mode, both factor vectors (raw + z), evaluative inputs, pick,
model outputs (M0 and M1 p, interval), override rationale if the user overrode,
outcome slot (null until labeled later — schema ready for M2/M3). ζ and Brier are
computed from the log; the log is the training set for M1.

## 7. Deliverable & deployment

- `pairwisepm/` pip-installable package (engine, log, config loader), `app.py` Gradio
  UI, `tests/`, HF Space files (README with YAML header, requirements.txt), pyproject.
- Deployed as a Hugging Face Gradio Space; the same repo clones/installs locally.
- README carries the epistemics: priors are a stated, editable policy, not fitted;
  0→1 makes no accuracy claim; "the LLM's job was at build time — the runtime is
  weights and a bias term."
