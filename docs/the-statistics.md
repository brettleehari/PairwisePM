# The Statistics Behind PairwisePM

A scorecard that hides its error bars is not a measurement. It is a decoration.

This document explains every statistical and machine-learning idea used in this project, one by one, and points at the line of code where each one lives. No idea here is new. Almost all of it is 40 to 70 years old. If we cut through the hype, the interesting part of this project is not the model, it is the discipline of refusing to claim more than the model can carry.

I have spent twenty years around product delivery, and the same scene repeats. Two ideas on a slide. Two RICE scores, 47.3 and 44.1. A room that treats the 3.2 point gap as information. It is not information. It is rounding error wearing a suit.

---

## 1. Bias & Noise : the decomposition everything rests on

Take any judgement that has a true answer. Your error splits in two.

**Bias** is the average error. Everybody in the room reads high.
**Noise** is the scatter. The same PM gives different answers to the same question on different days.

In squared error terms they add:

```
MSE = Bias² + Noise²
```

That equation is the whole reason this project exists. The two terms contribute equally. Most organizations spend all their improvement effort on bias — better frameworks, better training, better templates — and none on noise, because noise is invisible in any single decision. You cannot see scatter in one shot. You need a set of judgements of like cases to see it at all.

Reduce noise and you reduce error even when you have no idea which direction your bias runs. That is a free lunch, and it is rare.

**Important caveat, and this one is load-bearing :** the decomposition needs a true value to exist. "Which feature will move retention more" has one. "Which feature is more on-brand" does not. So the mechanical core of this tool only accepts predictive factors. Evaluative inputs — strategy fit, brand, taste — are captured in the app, displayed next to the verdict, and never enter the score. See section 22.

---

## 2. Three kinds of noise, and which one a model can actually kill

Noise decomposes further:

```
System Noise² = Level Noise² + Pattern Noise²
Pattern Noise² = Stable Pattern² + Occasion²
```

**Level noise** is the easy one. One PM is systematically bullish, marks everything a point high. Another is stingy.

**Stable pattern noise** is the PM's own idiosyncratic reaction to particular cases. She always over-values developer tooling. Consistently. Every time. This is usually the largest component, and it is *stable* — it is arguably not error at all, it is her policy.

**Occasion noise** is the same judge, same case, different Tuesday. Mood, sleep, order of presentation, what happened in the meeting before. In one software estimation study developers re-estimating identical tasks differed by an average of 71 percent. Occasion noise is typically the smallest of the three, and it is the one a model of the judge removes completely.

Be honest about the size of the prize. A model of your own policy does not make you smarter. It has no information you did not have. It just does not have Tuesdays.

---

## 3. Why pairwise & not a 1 to 10 score

This is the single most consequential design decision in the tool, and the argument is one line of algebra.

Score idea A absolutely and you get:

```
score_A = true_A + level_bias + occasion_noise
```

Score both A and B in the same sitting and subtract:

```
delta = score_A − score_B = (true_A − true_B) + (level_bias − level_bias) + ...
                          = (true_A − true_B)
```

The level bias **cancels by subtraction**. A PM who marks everything two points high marks both options two points high. Pairwise comparison is not a gentler form of scoring, it deletes a whole noise term.

Two conditions attach and both are enforced in the app :

1. **Both ideas must be scored in the same sitting.** The cancellation only removes noise that is *shared* by the two scores. Score A on Tuesday and B on Thursday and the occasion noise is no longer shared — it re-enters as delta noise, worse than before because now it is uncorrelated. This is why the UI is one screen, two columns, and refuses partial input.
2. **It does not touch stable pattern noise.** Your durable idiosyncrasies survive the subtraction untouched. Pairwise is not a cure, it is one specific deletion.

Frameworks like RICE do the opposite. They multiply and divide four soft estimates, so the errors compound instead of cancelling, and then present the product to one decimal place.

---

## 4. Putting different factors on one scale : z-scoring

Reach is a count of users. Effort is person-weeks. Impact is a −2 to +2 judgement against a named past feature. You cannot add these until they share a scale.

Each raw value becomes a z-score:

```
z = (raw − μ) / σ
```

The μ and σ come from **seed distributions** shipped in `configs/one_to_n.yaml` and `configs/zero_to_one.yaml`, because a brand new user has no history to standardize against.

As your log grows, your own data should take over. The transition is the subtle part. A hard cutover at some threshold changes every subsequent z-score, and therefore changes the verdict, silently, between sessions — the exact Tuesday-noise this tool exists to remove. So the shipped default is a **Bayesian blend**: the seed acts as a pseudo-sample of weight 10 (`SEED_PSEUDO_WEIGHT` in `engine.py`) that your real data gradually swamps. No discontinuity, converges to pure-log. `blended_stats()` implements it.

---

## 5. The model : Bradley-Terry, which is just logistic regression on differences

The Bradley-Terry model (1952) gives each item a strength and says the probability one beats the other depends only on the *difference* of strengths:

```
P(A beats B) = π_A / (π_A + π_B) = σ(β_A − β_B)
```

where σ is the logistic function, σ(x) = 1/(1+e⁻ˣ).

The version we need is the **feature** version. Instead of fitting a strength per idea (useless — every idea is new), we express strength as a weighted sum of factors. Then:

```
P(A beats B) = σ(wᵀd)      where d = z_A − z_B
```

That is the entire model. One dot product. Every past decision "we picked A over B" becomes one training row: features are the factor deltas, label is 1.

Thurstone's Case V is the same model with a probit link instead of logistic. The choice between them changes nothing that matters here.

---

## 6. The intercept : zero for scoring, free for diagnosis

A symmetric pairwise model must have **no intercept**. If it had one, the model would believe the option entered in the left column wins more often, which is a statement about your form layout, not about your ideas. So the scoring fit constrains it to zero by simply not including an intercept column. This gives us an exact guarantee, tested to 1e-12: swapping A and B returns exactly 1 − p.

But that same intercept is interesting. So the code fits it a **second** time, unconstrained, lightly penalized (`lam_intercept=0.05`), purely as a diagnostic. Its z-statistic is a *measurement of your presentation-order bias* — do you favour whatever you typed first? That number is surfaced in the audit view and never, ever used for scoring.

Same parameter. Forbidden in one role, informative in another.

---

## 7. Why the default weights are not fitted

The instinct is to fit weights from data. Resist it, and the reason is Robyn Dawes, "The Robust Beauty of Improper Linear Models" (1979).

A *proper* model optimizes its weights by regression. An *improper* model uses non-optimal weights — equal weights, or in our case documented prior weights. Dawes showed improper models frequently **match or beat** properly fitted regression out of sample, and both beat human intuition.

The mechanism is plain. With small n and correlated predictors, fitted weights chase noise in the training set. Equal weights cannot overfit, because they were never fit. Dawes & Corrigan add the sharper point: nearly all the power of a linear model comes from knowing *which* variables matter and their *sign*, not from their precise magnitudes.

So `M0`, the default model, uses the prior weights in the config, and the app carries an equal-weight toggle as a scientific control.

A trap worth naming, because it is easy to walk into: choosing which factors to include *is itself fitting*. Screen your factors on the same data you evaluate on and your improper model has quietly become a proper one.

---

## 8. The flat maximum : why arguing about decimals is a waste of an afternoon

Related result, from Einhorn & Hogarth. When predictors are correlated, the prediction surface is **flat** across a wide range of weightings. Moving a weight from 0.25 to 0.22 usually does not change the ranking at all.

This is genuinely liberating. It means the two open weight questions in this project (`leaves/decisions/decisions.yml`, entries D1 and D2) matter far less than the *ordering* of the factors. Get the ranking right and defensible. The decimals are config, not code, and you can tune them later without touching a line.

---

## 9. Model of the judge : Goldberg's bootstrapping

Now the interesting one, and it needs **no outcome data at all**.

Lewis Goldberg, "Man versus model of man" (1970). Build a linear model that predicts *the judge's own past judgements*. Then throw away the judge and use the model. It beats the judge.

Why? Because it applies the judge's own policy with perfect consistency. Referring back to section 2 — it sets occasion noise to zero. In Goldberg's study judges correlated 0.84 with truth while their own bootstrapped models hit 0.89.

This is exactly what `fit_m1()` does. It trains on your logged picks. It needs no outcomes, no ground truth, no waiting a year to see whether the feature worked. It just needs a record of what you chose. It activates at 10 logged picks (`M1_ACTIVATION_N`).

The honest framing : the expected gain is small but free. It is not a smarter judge. It is you, on your best day, every day.

One design decision here I would defend in a room. **Override picks count toward the gate and are included in the training data.** When you overrule the tool, that is the strongest possible signal of your revealed policy. Filtering overrides out would train the model to agree with itself, which is circular.

---

## 10. Shrinkage centered on the prior, not on zero

This is the piece I am most pleased with, and it is a small idea.

Standard ridge regression penalizes weights for being far from **zero**:

```
minimize  −loglik(w) + λ‖w‖²
```

With almost no data, that pulls every weight toward zero — toward a model that believes nothing at all. Which is not our belief. Our belief, before seeing any of your decisions, is the stated prior policy in the config.

So the penalty is centered on the prior instead (`_newton_logistic`, `engine.py`):

```
minimize  −loglik(w) + ½ (w − w₀)ᵀ P (w − w₀)
```

The behaviour this buys is continuous & correct at both ends. With 0 decisions, M1 returns exactly the prior — verified to 1e-6 in the tests. With 200 decisions, the likelihood dominates and you get essentially a free fit. There is no threshold, no switch, no cliff. The model earns the right to disagree with the stated policy, gradually, in proportion to evidence.

Optimization is Newton-Raphson, which converges in a handful of iterations on a problem this small.

---

## 11. Two fictitious games : why plain maximum likelihood blows up

A practical failure mode that bites everyone who implements Bradley-Terry for the first time.

If your comparison graph is not strongly connected, or one option wins every single time it appears, the maximum likelihood estimate **diverges**. The weight runs off to infinity, because infinity fits the data best. With five logged decisions this is not an edge case, it is Tuesday.

The classical fix is to add pseudo-observations — "two fictitious games". `_fictitious_games()` adds, for each factor, a pair of unit-delta pseudo-comparisons in **both presentation orders**, with soft outcomes equal to the prior model's own prediction.

Two properties fall out. The fit is anchored at the stated policy when real data is thin, and because the pair is order-symmetric it adds **no** bias to the intercept — so the order-bias diagnostic in section 6 stays clean.

---

## 12. The interval : bootstrap, and it is never optional

A single probability is a lie of precision. Every verdict carries a 90 percent interval, produced by bootstrapping over the per-factor contributions (`_bootstrap_interval`).

The interface rule that follows is enforced in the code and in the tests : the probability is **never rendered without its interval**. There is no code path in the app that can print "A wins, 59%" on its own. It prints "59% (52–64%)" or it prints nothing.

---

## 13. Too close to call

If the interval straddles 50 percent, the tool declines to name a winner.

```
if lo ≤ 0.5 ≤ hi:  verdict = "too close to call"
```

Boundary touching counts as straddling — the tie breaks toward humility (`verdict_from`, and convention C2 in the decisions queue).

This is the most valuable output the tool produces and the one users like least. "Gather more evidence" is a real answer. A tool that always names a winner is not more decisive, it is just less honest — it is the RICE 47.3-vs-44.1 problem with better arithmetic.

Note that there is deliberately **no second dead-band**. The interval already widens when the evidence is thin. Adding a fixed margin on top would double-count the same uncertainty.

---

## 14. Leverage : decomposing a verdict into who caused it

Because the model is linear in the log-odds, the verdict pulls apart exactly:

```
L = wᵀd = Σⱼ wⱼ · dⱼ
```

Each term `wⱼ · dⱼ` is factor j's signed contribution to the decision. No approximation, no attribution heuristic, no SHAP required — the model is linear, so the decomposition is the model.

`leverage_panel()` returns these as a sorted bar chart. It answers "why did it say that", and it frequently reveals that a verdict you liked rests entirely on a number you guessed.

---

## 15. Path to parity : the actionable half

Given a verdict, what is the smallest single change that would flip it?

Solve for the shift in factor j that drives the log-odds to zero:

```
required z-shift  = L / wⱼ
required raw shift = (L / wⱼ) × σⱼ
```

Then convert back through that factor's standard deviation so the answer arrives in **units a human can act on** — not "raise z by 1.04" but "raise the eval pass rate from 62% to 78%", or "cut three person-weeks of scope".

The panel computes this for parity (50/50) and for a 60/40 margin, and checks the target against the factor's plausible range. A path that requires a reach of forty million users is arithmetic, not advice, and gets marked infeasible.

---

## 16. Lever & fact : the tag that keeps the advice honest

Every factor in the config carries a tag.

A **lever** is something you can change by working: eval pass rate, effort, evidence of pull, unit economics.
A **fact** is what it is: problem severity, segment size, capability-trajectory exposure.

Parity paths are only proposed through levers. If every route to parity runs through a fact, the tool says so plainly — *this loses on fundamentals, no amount of working harder flips it*. That sentence is itself a decision-grade output, and it is the one a spreadsheet will never give you.

---

## 17. Fragility : the mirror image

The same math, pointed the other way. If the **winner's** margin would flip under a small plausible move of one factor — currently 0.75 z-units, `FRAGILITY_Z` — the card says so:

*"A wins, but the margin rests entirely on the effort estimate. Re-estimate before committing."*

A win that survives only if your guess was exactly right is not a win, it is a coin flip with a narrative attached.

---

## 18. Kendall's ζ : a noise meter that needs no outcomes and no second person

My favourite instrument in the whole project, because it measures your own incoherence from your own data, today.

If you prefer A over B, and B over C, and then C over A, you have a **circular triad**. That is not a mistake about the world, it is an internal contradiction — no ranking of A, B, C is consistent with all three of your own choices.

Kendall & Babington Smith (1940) count them:

```
T = n(n²−1)/24 − ½ Σᵢ (pᵢ − (n−1)/2)²
```

where pᵢ is item i's win count. Then the coefficient of consistency:

```
ζ = 1 − T / T_max
```

ζ = 1 is perfectly transitive. ζ = 0 is maximally cyclic. It needs no ground truth, no outcomes, and no second rater — which makes it the one honesty instrument that works for a PM sitting alone. `kendall_zeta()` in `log.py` computes it, and returns `None` honestly when there is not yet a complete triad to judge, rather than inventing a number.

---

## 19. Brier score : being right vs knowing how right you are

Discrimination and calibration are different virtues.

**Discrimination** is ranking: does the tool put better ideas above worse ones?
**Calibration** is honesty about confidence: of all the times it said 70 percent, did the thing happen about 70 percent of the time?

The Brier score is the mean squared error of a probability forecast:

```
Brier = (1/N) Σ (pᵢ − oᵢ)²
```

Lower is better, 0 is perfect. It accumulates from decision one. A reliability curve — predicted probability binned against observed frequency — unlocks at 30 decisions (`RELIABILITY_CURVE_MIN_N`), and not before, because a calibration plot drawn from eight points is itself overconfident. An uncalibrated calibration report would be a fine joke at this product's expense.

---

## 20. The c-statistic : the scoreboard we have not earned yet

For a choice model, the c-statistic equals the AUC, and it has a beautifully direct reading: **the probability the model ranks a randomly chosen better idea above a worse one.** 0.5 is a coin flip. Related quantities: Somers' D = 2c − 1, and c = percent concordant + ½ percent tied.

Here is why it is not in the product yet, and this is the part most tools quietly skip.

To distinguish c = 0.80 from chance you need roughly 45 outcome-labeled decisions. For c = 0.70, about 109. If you have 5 decisions and post "c = 1.000", you have not measured discrimination, you have measured your sample size. So the tool ships the metrics that are honest at small n — pick agreement, ζ, Brier — and leaves the outcome scoreboard locked until the data exists to support it.

---

## 21. The ladder : four models, each earning its place

| Level | Model | Trains on | Active at |
|---|---|---|---|
| M0 | Prior-weight linear, σ(w₀ᵀd) | nothing | day one |
| M1 | Ridge logistic BT, shrunk to prior | your logged picks | ~10 picks |
| M2 | Same regression vs. outcomes | labeled outcomes | ~45 outcomes |
| M3 | Nonlinear ML, interactions | hundreds | far future |

Each rung replaces the one below **only** by beating it out of sample on c-statistic and Brier. The equal-weight version stays available throughout as the control.

The direction of travel is the opposite of the industry instinct. More sophistication is not generally better here. With small, noisy, non-stationary data — which is exactly what product decisions are — the simple end of the ladder usually wins out of sample. The ceiling for a real PM tool is low, and that is a feature.

---

## 22. Predictive & evaluative : the line the mechanical core will not cross

Back to section 1. MSE = Bias² + Noise² requires a true value to exist.

"Will this raise 30-day retention" is predictive. It has an answer, eventually.
"Is this on-brand" is evaluative. There is no fact of the matter to be wrong about.

So evaluative inputs are captured in the app, shown beside the verdict, and structurally excluded from the score — they are not even in `compare()`'s signature, and a test asserts they cannot influence it. The tool has an opinion about reach. It has no opinion about your brand, and it says so.

---

## 23. Two modes, two different honesty settings

**1→N (allocation)** — choosing what goes in the release. Repeated similar decisions, stable-ish environment, measurable outcomes, reference classes that accumulate. This is the regime the whole clinical-vs-mechanical literature was built for. The tool makes a mechanical claim here.

**0→1 (search)** — looking for product-market fit. Non-stationary, tiny n, low environmental predictability, broken-leg cues everywhere. Also the regime where payoffs are convex: one hit funds everything, so a false negative is the expensive error.

In 0→1 the tool provides structure and consistency and **makes no predictive-accuracy claim**. That banner is permanent, it is asserted by a test, and the config loader refuses to load the mode without it.

The ceiling flag follows from the same reasoning. A high-ceiling outlier is routed to human portfolio judgement rather than being averaged into a score, because tail-hunting is a portfolio question wearing a ranking question's clothes. Convexity belongs at selection, never inside the probability.

---

## 24. Broken legs : when to overrule the model

Meehl's example. A formula predicts whether someone attends the cinema tonight, and it is a good formula — but she broke her leg this morning. The formula cannot see that. Overruling it is correct.

This is the legitimate case for human override, and the app always allows it. Pick against the verdict, or against a too-close-to-call, and it is logged with one sentence of rationale. No friction, no nagging.

The catch, and the literature is blunt about it : humans **drastically overuse** the broken-leg exception. Ordinary cues get treated as decisive, and the override quietly reintroduces the noise the model removed. So overrides are recorded, they carry your stated reason, and they can later be audited against outcomes. If your overrides underperform the model — which is the usual finding — that is worth knowing, and you will only know it if you wrote them down.

---

## What the evidence base actually says

Since every section above leans on it, the summary in one place.

Meehl (1954) reviewed the comparative studies available then; in all but one, actuarial prediction equalled or beat the clinician. Grove et al. (2000) meta-analyzed 136 studies: mechanical prediction about 10 percent more accurate on average, substantially better in 33 to 47 percent of studies, humans substantially better in only 6 to 16 percent.

Read that carefully, because the popular version of it is wrong. The claim is **not** that any model beats any human. Models degrade badly with broken-leg cues, tiny samples, and non-stationary environments — which describes a great deal of product strategy. The defensible claim is narrower and still worth building on : *a simple, consistent mechanical rule is a golden baseline that beats most humans most of the time, mostly by removing noise rather than by being clever.*

That is what this is. A baseline that does not have Tuesdays, that shows its interval, and that says "too close to call" when it means it.

---

## References

1. Kahneman, Sibony & Sunstein — *Noise: A Flaw in Human Judgment* (2021)
2. Meehl — *Clinical versus Statistical Prediction* (1954)
3. Grove, Zald, Lebow, Snitz & Nelson — "Clinical versus mechanical prediction: a meta-analysis", *Psychological Assessment* 12(1) (2000)
4. Dawes — "The Robust Beauty of Improper Linear Models in Decision Making", *American Psychologist* 34(7) (1979)
5. Dawes & Corrigan — "Linear models in decision making", *Psychological Bulletin* 81(2) (1974)
6. Goldberg — "Man versus model of man", *Psychological Bulletin* 73(6) (1970)
7. Bradley & Terry — "Rank analysis of incomplete block designs", *Biometrika* 39 (1952)
8. Thurstone — "A law of comparative judgment", *Psychological Review* 34 (1927)
9. Kendall & Babington Smith — "On the method of paired comparisons", *Biometrika* 31 (1940)
10. Brier — "Verification of forecasts expressed in terms of probability", *Monthly Weather Review* 78 (1950)
11. Einhorn & Hogarth — "Unit weighting schemes for decision making", *Organizational Behavior and Human Performance* 13 (1975)
12. Grimstad & Jørgensen — "Inconsistency of expert judgment-based estimates of software development effort", *Journal of Systems and Software* 80(11) (2007)

Do let me know where you think the reasoning is wrong, there is always room for improvement.
