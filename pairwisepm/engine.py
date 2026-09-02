"""PairwisePM scoring engine — the regression ladder, uncertainty, and leverage.

Runtime is purely mechanical (Spine): numpy only, no LLM, no API key, no
network. The LLM's job ended at build time; this file is weights and a bias
term — and the bias term is constrained to zero.

Honesty rules implemented here (each is enforced in code, not prose):

1. Symmetry — the scoring intercept is constrained to zero, so swapping A and B
   yields exactly 1 − p. A separately fitted FREE intercept is exposed only as
   an order-bias diagnostic and never used for scoring (spec §3).
2. Intervals always — every probability ships with a bootstrap-over-factors
   interval; when the interval straddles 50% the verdict is ``too_close``,
   never a forced winner (spec §4).
3. Prior-centered shrinkage — M1 ridge shrinks toward the PM's *stated* prior
   weights, not toward zero: with little data the model IS the stated policy,
   and it drifts to the revealed policy only as evidence accumulates (spec §3).
4. Two-fictitious-games regularization — pseudo-comparisons anchored at the
   prior keep the MLE from diverging on small or disconnected comparison
   graphs (spec §3, mandatory from day one).
5. Lever/fact discipline — path-to-parity is only ever proposed through
   ``lever`` factors and only within each factor's plausible raw range; when
   no lever path exists the answer is ``loses_on_fundamentals``, not a
   fantasy instruction to change a fact (spec §5).
6. Ceiling never scores — a set Ceiling flag routes to human portfolio
   judgment; it does not touch the logit (spec §2).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .config import Factor, ModeConfig
from .strings import PINNED_CEILING, PINNED_FRAGILITY_TMPL

M1_ACTIVATION_N = 10  # decisions logged (per mode) before M1 activates
# (Decisions convention C1: exactly 10, per mode, override picks count.)
FRAGILITY_Z = 0.75  # a "small plausible move" of one factor, in z units.
# Decisions D6 (pending): 0.75σ is the build-meanwhile default; compliance's
# provisional spec used 0.5σ. Whichever option wins, this becomes config and
# compliance regenerates the T-FRAG fixtures — the RULE (fragile ⇔ a plausible
# ≤ε move of one factor flips the margin) is unchanged.
SEED_PSEUDO_WEIGHT = 10.0  # Decisions D5 build-meanwhile default (Bayesian blend)
_LOGIT_60 = math.log(0.6 / 0.4)  # ≈ 0.4055


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x)) if x >= 0 else math.exp(x) / (1.0 + math.exp(x))


def _sigmoid_vec(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -35, 35)))


# ---------------------------------------------------------------------------
# z-scoring
# ---------------------------------------------------------------------------

def zscore_idea(raw: Dict[str, float], cfg: ModeConfig) -> Dict[str, float]:
    """z-score one idea's raw factor values against the seed (or log-derived)
    distributions carried by ``cfg`` (transform applied first)."""
    return {f.key: f.zscore(float(raw[f.key])) for f in cfg.factors}


def log_derived_stats(
    raw_vectors: Sequence[Dict[str, float]], cfg: ModeConfig, min_n: int = 10
) -> Dict[str, Tuple[float, float]]:
    """(mean, std) per factor in transform space from logged raw vectors.

    Returns stats only when at least ``min_n`` values exist and the spread is
    non-degenerate; callers feed the result to
    ``ModeConfig.with_updated_distributions``.

    WARNING (Decisions D5, pending): this helper is a HARD replacement of the
    seed distributions. Wiring it directly into the app would be a hard
    seed-to-log cutover, which can silently flip a near-tie verdict between
    sessions — the exact occasion noise the product removes. The D5
    build-meanwhile default is the Bayesian blend in :func:`blended_stats`;
    v1 ships seeds-only (nothing wired). Do not wire this function as the
    z-basis unless D5 resolves to the hard-cutover option.
    """
    out: Dict[str, Tuple[float, float]] = {}
    for f in cfg.factors:
        vals = [f.to_transform_space(v[f.key]) for v in raw_vectors if f.key in v]
        if len(vals) >= min_n:
            arr = np.asarray(vals, dtype=float)
            std = float(arr.std(ddof=1))
            if std > 1e-9:
                out[f.key] = (float(arr.mean()), std)
    return out


def blended_stats(
    raw_vectors: Sequence[Dict[str, float]],
    cfg: ModeConfig,
    pseudo_weight: float = SEED_PSEUDO_WEIGHT,
) -> Dict[str, Tuple[float, float]]:
    """Seed-as-pseudo-sample Bayesian blend of z-scoring distributions
    (Decisions D5 build-meanwhile default; ``pseudo_weight`` is config).

    The shipped seed distribution for each factor acts as a pseudo-sample of
    ``pseudo_weight`` observations (mean ``seed_mean``, variance ``seed_std²``)
    that the user's log gradually swamps. There is no discontinuity: with an
    empty log the result IS the seed distribution; as n grows it converges to
    the pure log statistics. Returns (mean, std) in transform space for every
    factor — feed to ``ModeConfig.with_updated_distributions``.

    NOT wired into app.py in v1 (seeds-only ships); this is the implementation
    D5 requires to exist before any switchover ships.
    """
    w0 = float(pseudo_weight)
    out: Dict[str, Tuple[float, float]] = {}
    for f in cfg.factors:
        vals = np.asarray(
            [f.to_transform_space(v[f.key]) for v in raw_vectors if f.key in v],
            dtype=float,
        )
        n = float(vals.size)
        m0, s0 = f.seed_mean, f.seed_std
        if n == 0:
            out[f.key] = (m0, s0)
            continue
        total_w = w0 + n
        mean = (w0 * m0 + float(vals.sum())) / total_w
        # Pooled second moment: seed contributes w0·(s0² + m0²).
        ss = w0 * (s0 * s0 + m0 * m0) + float((vals * vals).sum())
        var = max(ss / total_w - mean * mean, 1e-12)
        out[f.key] = (mean, math.sqrt(var))
    return out


# ---------------------------------------------------------------------------
# result containers
# ---------------------------------------------------------------------------

@dataclass
class ModelScore:
    model: str  # "M0" | "M0-equal" | "M1"
    p: float  # P(A beats B); by symmetry, swapping inputs gives exactly 1 - p
    logit: float
    interval: Tuple[float, float]  # 90% bootstrap-over-factors interval on p
    verdict: str  # "A" | "B" | "too_close"
    weights: Dict[str, float]  # effective weights used


@dataclass
class LeverageRow:
    key: str
    name: str
    tag: str
    weight: float
    delta: float  # z_A - z_B
    contribution: float  # weight * delta, signed toward A


@dataclass
class ParityPath:
    """One lever factor's path to 50/50 (and 60/40) for the losing idea.

    Targets are ALWAYS reported, even when they fall outside the plausible
    range — an off-scale target is flagged (``feasible=False``), never
    silently clamped or hidden (GTM contract; compliance T-PAR-03: the chosen
    representation is marked-infeasible-and-kept, not excluded). ``z_shift`` is
    the required z move (spec §5: gap / w_j); ``raw_shift``/``raw_target`` are
    in raw units via the factor's std and inverse transform.
    """

    key: str
    name: str
    tag: str
    loser: str  # "A" | "B"
    current_raw: float
    z_shift: float  # required z move for 50/50 (signed)
    raw_shift: float  # raw-unit move for 50/50 (raw_target - current_raw)
    raw_target: float  # raw value the loser's factor must reach for 50/50
    feasible: bool  # 50/50 target inside the plausible range
    z_shift_6040: float  # required z move for the loser to reach 60/40
    raw_shift_6040: float
    raw_target_6040: float
    feasible_6040: bool
    note: str

    # Backward-compat accessors (round-1 shape): None ⇔ infeasible.
    @property
    def target_raw_parity(self) -> Optional[float]:
        return self.raw_target if self.feasible else None

    @property
    def target_raw_6040(self) -> Optional[float]:
        return self.raw_target_6040 if self.feasible_6040 else None


@dataclass
class Fragility:
    fragile: bool
    factor_name: Optional[str] = None
    factor_key: Optional[str] = None
    required_z_shift: Optional[float] = None
    message: str = ""


@dataclass
class M1Fit:
    weights: Dict[str, float]  # scoring weights (intercept constrained to 0)
    n_train: int
    free_intercept: float  # diagnostic-only fit
    free_intercept_se: float
    order_bias_z: float  # free_intercept / se; |z| > 2 => measured order bias
    active: bool

    @property
    def order_bias_flagged(self) -> bool:
        return abs(self.order_bias_z) > 2.0


@dataclass
class ComparisonResult:
    mode: str
    banner: Optional[str]
    z_a: Dict[str, float]
    z_b: Dict[str, float]
    deltas: Dict[str, float]
    m0: ModelScore
    m0_equal: ModelScore  # equal-weight ablation (scientific control)
    m1: Optional[ModelScore]
    active_model: str  # "M0" until M1 activates, then "M1"
    leverage: List[LeverageRow]
    parity_paths: List[ParityPath]
    loses_on_fundamentals: bool
    fragility: Fragility
    ceiling_notes: List[str] = field(default_factory=list)

    @property
    def active(self) -> ModelScore:
        return self.m1 if (self.active_model == "M1" and self.m1) else self.m0


# ---------------------------------------------------------------------------
# M0: prior-weight linear score
# ---------------------------------------------------------------------------

def effective_weights(cfg: ModeConfig, equal: bool = False) -> Dict[str, float]:
    """Effective weight vector. ``equal=True`` is the equal-weight ablation:
    all magnitudes set to the mean |w|, signs kept (Dawes 1979 control)."""
    if not equal:
        return {f.key: f.effective_weight for f in cfg.factors}
    mag = float(np.mean([abs(f.effective_weight) for f in cfg.factors]))
    return {f.key: f.sign * mag for f in cfg.factors}


def verdict_from(p: float, interval: Tuple[float, float]) -> str:
    """The honesty gate as a pure function (spec §4, Decisions C2): the verdict
    is "too_close" exactly when the interval straddles 50%, BOUNDARY TOUCHING
    INCLUDED — an endpoint exactly at 0.5 breaks toward too_close, never toward
    a forced winner."""
    lo, hi = interval
    if lo <= 0.5 <= hi or p == 0.5:
        return "too_close"
    return "A" if p > 0.5 else "B"


def _score(
    deltas: Dict[str, float],
    weights: Dict[str, float],
    model: str,
    n_boot: int,
    seed: int,
) -> ModelScore:
    """p = σ(wᵀd) with a zero intercept (symmetry rule #1) and a
    bootstrap-over-factors interval (honesty rule #2)."""
    keys = list(weights.keys())
    contrib = np.array([weights[k] * deltas[k] for k in keys], dtype=float)
    L = float(contrib.sum())
    p = sigmoid(L)
    lo, hi = _bootstrap_interval(contrib, n_boot=n_boot, seed=seed)
    return ModelScore(model=model, p=p, logit=L, interval=(lo, hi),
                      verdict=verdict_from(p, (lo, hi)), weights=dict(weights))


def _bootstrap_interval(
    contrib: np.ndarray, n_boot: int = 2000, seed: int = 0, level: float = 0.90
) -> Tuple[float, float]:
    """90% percentile interval on p by resampling the per-factor contributions
    with replacement. With ~7 factors this is deliberately coarse — a coarse
    honest interval beats a precise false one. Deterministic given ``seed``."""
    k = contrib.size
    if k == 0:
        return (0.5, 0.5)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, k, size=(n_boot, k))
    logits = contrib[idx].sum(axis=1)
    ps = _sigmoid_vec(logits)
    a = (1.0 - level) / 2.0
    return (float(np.quantile(ps, a)), float(np.quantile(ps, 1.0 - a)))


# ---------------------------------------------------------------------------
# M1: ridge logistic Bradley-Terry on factor deltas
# ---------------------------------------------------------------------------

def _newton_logistic(
    X: np.ndarray,
    y: np.ndarray,
    center: np.ndarray,
    penalty: np.ndarray,
    max_iter: int = 200,
    tol: float = 1e-9,
) -> Tuple[np.ndarray, np.ndarray]:
    """Penalized logistic regression by Newton-Raphson.

    Minimizes  -loglik(w) + 1/2 (w-center)ᵀ P (w-center),  P = diag(penalty).
    ``y`` may contain soft labels in [0, 1] (used by the fictitious games).
    Returns (w_hat, Hessian at w_hat).
    """
    w = center.copy()
    P = np.diag(penalty)
    for _ in range(max_iter):
        mu = _sigmoid_vec(X @ w)
        grad = X.T @ (mu - y) + P @ (w - center)
        s = np.clip(mu * (1.0 - mu), 1e-9, None)
        H = X.T @ (X * s[:, None]) + P
        step = np.linalg.solve(H + 1e-10 * np.eye(H.shape[0]), grad)
        w = w - step
        if float(np.max(np.abs(step))) < tol:
            break
    mu = _sigmoid_vec(X @ w)
    s = np.clip(mu * (1.0 - mu), 1e-9, None)
    H = X.T @ (X * s[:, None]) + P
    return w, H


def _fictitious_games(cfg: ModeConfig) -> Tuple[np.ndarray, np.ndarray]:
    """Two fictitious games per factor (honesty rule #4): unit-delta
    pseudo-comparisons in both presentation orders, with soft outcomes equal to
    the PRIOR model's prediction. They anchor the fit at the stated policy when
    real data is thin and prevent MLE divergence on disconnected graphs,
    without biasing the intercept (the pair is order-symmetric)."""
    k = len(cfg.factors)
    w0 = np.array([f.effective_weight for f in cfg.factors], dtype=float)
    X = np.vstack([np.eye(k), -np.eye(k)])
    y = np.concatenate([_sigmoid_vec(w0), _sigmoid_vec(-w0)])
    return X, y


def fit_m1(
    delta_rows: Sequence[Dict[str, float]],
    picks: Sequence[int],
    cfg: ModeConfig,
    lam: float = 1.0,
    lam_intercept: float = 0.05,
) -> M1Fit:
    """Fit M1 from logged picks (pick = 1 when the user chose A).

    Ridge logistic Bradley-Terry on factor deltas with shrinkage CENTERED ON
    THE PRIOR WEIGHTS, not zero (honesty rule #3), plus two fictitious games
    per factor (rule #4). Two fits are performed:

    - scoring fit: intercept constrained to zero, so swap(A,B) => exactly 1-p
      (rule #1). These are the weights the product uses.
    - diagnostic fit: free intercept, shrunk only lightly toward zero. Its
      z-statistic is the measured presentation-order bias, surfaced in the
      audit view and NEVER used for scoring.

    ``active`` is True only at >= M1_ACTIVATION_N real picks; below that the
    fit is still returned (for display) but M0 remains the verdict model.
    """
    keys = cfg.factor_keys
    k = len(keys)
    w0 = np.array([f.effective_weight for f in cfg.factors], dtype=float)
    n = len(picks)

    Xr = (np.array([[r[k_] for k_ in keys] for r in delta_rows], dtype=float)
          if n else np.zeros((0, k)))
    yr = np.asarray(picks, dtype=float)
    Xf, yf = _fictitious_games(cfg)
    X = np.vstack([Xr, Xf])
    y = np.concatenate([yr, yf])

    # Scoring fit: no intercept column => intercept identically zero.
    w_hat, _ = _newton_logistic(X, y, center=w0, penalty=np.full(k, lam))

    # Diagnostic fit: free intercept in column 0, centered at 0, light penalty.
    Xb = np.hstack([np.ones((X.shape[0], 1)), X])
    center_b = np.concatenate([[0.0], w0])
    pen_b = np.concatenate([[lam_intercept], np.full(k, lam)])
    wb, Hb = _newton_logistic(Xb, y, center=center_b, penalty=pen_b)
    cov = np.linalg.inv(Hb + 1e-10 * np.eye(k + 1))
    b = float(wb[0])
    se = float(math.sqrt(max(cov[0, 0], 1e-18)))
    z = b / se if se > 0 else 0.0

    return M1Fit(
        weights={k_: float(w) for k_, w in zip(keys, w_hat)},
        n_train=n,
        free_intercept=b,
        free_intercept_se=se,
        order_bias_z=z,
        active=n >= M1_ACTIVATION_N,
    )


# ---------------------------------------------------------------------------
# Leverage panel
# ---------------------------------------------------------------------------

def _parity_target(
    factor: Factor,
    weight: float,
    L: float,
    loser: str,
    z_loser: float,
    target_logit_for_A: float,
) -> Optional[Tuple[float, float, float, bool]]:
    """(z_shift, raw_shift, raw_target, feasible) so the logit hits the target.

    Required z-shift = logit-gap / w_j (spec §5), converted to raw units via
    the factor's std and inverse transform. The target is always computed and
    returned; ``feasible`` marks whether it stays inside the plausible range
    (off-scale targets are flagged, never clamped). Returns None only for a
    zero-weight factor (no finite move exists)."""
    if abs(weight) < 1e-12:
        return None
    delta_z = ((L - target_logit_for_A) / weight if loser == "B"
               else (target_logit_for_A - L) / weight)
    current_raw = factor.raw_from_z(z_loser)
    raw = factor.raw_from_z(z_loser + delta_z)
    return (delta_z, raw - current_raw, raw, factor.in_plausible_range(raw))


def leverage_panel(
    cfg: ModeConfig,
    weights: Dict[str, float],
    z_a: Dict[str, float],
    z_b: Dict[str, float],
    raw_a: Dict[str, float],
    raw_b: Dict[str, float],
    score: ModelScore,
) -> Tuple[List[LeverageRow], List[ParityPath], bool, Fragility]:
    """Per-factor contributions, path-to-parity, and the fragility flag.

    Honesty rule #5 lives here: parity paths are proposed ONLY through lever
    factors and only within the plausible raw range. When every closing path
    runs through facts (or out of range), the return says the loser
    loses_on_fundamentals — the tool refuses to recommend changing reality.
    """
    L = score.logit
    deltas = {k: z_a[k] - z_b[k] for k in cfg.factor_keys}
    rows = [
        LeverageRow(key=f.key, name=f.name, tag=f.tag, weight=weights[f.key],
                    delta=deltas[f.key],
                    contribution=weights[f.key] * deltas[f.key])
        for f in cfg.factors
    ]
    rows.sort(key=lambda r: -abs(r.contribution))

    paths: List[ParityPath] = []
    loses_on_fundamentals = False
    fragility = Fragility(fragile=False, message="")

    if score.p == 0.5:
        # Exact tie: there is no runner-up to route a parity path to.
        return rows, paths, False, fragility

    # Parity paths are computed for the lower-p side even when the VERDICT is
    # too_close: design S4 reframes them as "cheapest evidence" — the honesty
    # gate withholds the winner, never the levers.
    loser = "B" if score.p > 0.5 else "A"
    z_l = z_a if loser == "A" else z_b
    raw_l = raw_a if loser == "A" else raw_b
    t6040 = -_LOGIT_60 if loser == "B" else _LOGIT_60

    any_lever_path = False
    for f in cfg.factors:
        w = weights[f.key]
        if f.tag != "lever":
            continue  # parity is never proposed through a fact
        tp = _parity_target(f, w, L, loser, z_l[f.key], 0.0)
        t6 = _parity_target(f, w, L, loser, z_l[f.key], t6040)
        if tp is None or t6 is None:
            continue  # zero-weight lever: no finite move exists
        zp, rsp, rtp, feas_p = tp
        z6, rs6, rt6, feas_6 = t6
        any_lever_path = any_lever_path or feas_p
        note = ("smallest single-factor move reaching 50/50"
                if feas_p else
                "target falls outside the plausible range — shown, not proposed")
        paths.append(ParityPath(
            key=f.key, name=f.name, tag=f.tag, loser=loser,
            current_raw=float(raw_l[f.key]),
            z_shift=zp, raw_shift=rsp, raw_target=rtp, feasible=feas_p,
            z_shift_6040=z6, raw_shift_6040=rs6, raw_target_6040=rt6,
            feasible_6040=feas_6, note=note,
        ))
    # Feasible paths first, smallest required z-shift first.
    paths.sort(key=lambda p: (not p.feasible, abs(p.z_shift)))
    loses_on_fundamentals = not any_lever_path

    # Fragility (spec §5.4): does the winner's margin flip on a small plausible
    # move (<= FRAGILITY_Z z-units) of ANY single factor, on either side?
    best: Optional[Tuple[float, Factor]] = None
    for f in cfg.factors:
        w = weights[f.key]
        if abs(w) < 1e-12:
            continue
        need = abs(L) / abs(w)  # z-shift magnitude that lands the logit on 0
        if need > FRAGILITY_Z:
            continue
        # Exact signed shifts that flip the verdict: changing z_A[j] by δ moves
        # L by +w·δ; changing z_B[j] by δ moves L by −w·δ.
        gap = L + math.copysign(1e-6, L)
        for side, z_s, delta_z in (("A", z_a, -gap / w), ("B", z_b, gap / w)):
            raw_target = f.raw_from_z(z_s[f.key] + delta_z)
            if f.in_plausible_range(raw_target):
                if best is None or need < best[0]:
                    best = (need, f)
                break
    if best is not None:
        need, f = best
        fragility = Fragility(
            fragile=True, factor_name=f.name, factor_key=f.key,
            required_z_shift=need,
            # Compliance-pinned copy (T-FRAG), factor name interpolated.
            message=PINNED_FRAGILITY_TMPL.format(factor=f.name)
            + f" (a {need:.2f}σ move flips it)",
        )
    return rows, paths, loses_on_fundamentals, fragility


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def compare(
    cfg: ModeConfig,
    raw_a: Dict[str, float],
    raw_b: Dict[str, float],
    *,
    m1_fit: Optional[M1Fit] = None,
    ceiling_a: bool = False,
    ceiling_b: bool = False,
    n_boot: int = 2000,
    seed: int = 7,
) -> ComparisonResult:
    """Run one full A-vs-B comparison.

    v1 is strictly two ideas (Spine refusal R-02): the parameters after
    ``raw_b`` are keyword-only, so a third positional "idea" raises TypeError,
    and no public callable in this package accepts a list of ideas.

    Both ideas are z-scored against the same distributions in the same call —
    the pairwise delta cancels only noise shared by both scores, which is why
    the product insists on one questionnaire, one screen, one sitting.

    ``m1_fit`` (from :func:`fit_m1` over the user's log) drives the verdict
    only when ``m1_fit.active`` — below ~10 logged picks the verdict model is
    M0, the user's stated policy. The equal-weight ablation is always computed
    as a scientific control. Ceiling flags never touch any logit (rule #6);
    they add routing notes for human portfolio judgment.
    """
    if m1_fit is not None and not isinstance(m1_fit, M1Fit):
        # Fail-fast half of refusal R-02 (compliance DV-4): a third idea dict
        # smuggled into the keyword slot dies here with a clean TypeError,
        # never deep inside the fit.
        raise TypeError(
            "compare() takes exactly two ideas (raw_a, raw_b); m1_fit must be "
            f"an M1Fit from fit_m1(), not {type(m1_fit).__name__}"
        )
    z_a = zscore_idea(raw_a, cfg)
    z_b = zscore_idea(raw_b, cfg)
    deltas = {k: z_a[k] - z_b[k] for k in cfg.factor_keys}

    m0 = _score(deltas, effective_weights(cfg), "M0", n_boot, seed)
    m0_eq = _score(deltas, effective_weights(cfg, equal=True), "M0-equal",
                   n_boot, seed + 1)

    m1_score: Optional[ModelScore] = None
    active_model = "M0"
    if m1_fit is not None:
        m1_score = _score(deltas, m1_fit.weights, "M1", n_boot, seed + 2)
        if m1_fit.active:
            active_model = "M1"

    active = m1_score if active_model == "M1" else m0
    weights = active.weights
    rows, paths, lof, frag = leverage_panel(
        cfg, weights, z_a, z_b, raw_a, raw_b, active
    )

    ceiling_notes = []
    for name, flag in (("A", ceiling_a), ("B", ceiling_b)):
        if flag:
            # Compliance-pinned routing copy (T-CEIL-02).
            ceiling_notes.append(
                f"Idea {name} carries the Ceiling flag: {PINNED_CEILING}. "
                "The flag is unweighted and did not enter the score."
            )

    return ComparisonResult(
        mode=cfg.mode, banner=cfg.banner, z_a=z_a, z_b=z_b, deltas=deltas,
        m0=m0, m0_equal=m0_eq, m1=m1_score, active_model=active_model,
        leverage=rows, parity_paths=paths, loses_on_fundamentals=lof,
        fragility=frag, ceiling_notes=ceiling_notes,
    )
