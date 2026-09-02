"""PairwisePM engine test suite (pytest, engine-only — no Gradio required).

Implements the Compliance leaf's executable specifications
(tests/test_engine_spec.md) against the AS-BUILT API in ``pairwisepm``.
Renames from the spec's provisional §0 shapes are deliberate and declared:

- ``compare(cfg, raw_a, raw_b, *, ...) -> ComparisonResult`` (spec: Verdict);
  probabilities at ``result.m0.p`` / ``result.m1.p`` (spec: p_m0/p_m1),
  verdict strings "A"/"B"/"too_close" (spec: "a"/"b"/"too_close").
- ``fit_m1(delta_rows, picks, cfg, lam=...) -> M1Fit`` with ``.active`` as the
  activation gate (spec: m1_active) and ``.free_intercept`` always fitted as
  the diagnostic (spec: free_intercept=True flag).
- ``DecisionLog`` methods ``kendall_zeta``/``brier`` (spec: zeta/brier free
  functions); JSONL via ``to_jsonl``/``from_jsonl``.
- Engineering's declared choices (per the exchange round): infeasible parity
  paths are KEPT in the list marked ``feasible=False`` (T-PAR-03 option 1);
  fragility epsilon is ``FRAGILITY_Z = 0.75`` z-units pending Decisions D6
  (T-FRAG constants below are derived for 0.75, not the spec's provisional
  0.5); order-bias significance is a Wald z from the penalized Hessian with
  |z| > 2 as the gate.

Every test that pins a numeric constant derived from the D1/D2 default prior
weights says so — regenerate on resolution.
"""

from __future__ import annotations

import inspect
import json
import math
import re
import sys

import numpy as np
import pytest

import pairwisepm
from pairwisepm import (
    FRAGILITY_Z,
    M1_ACTIVATION_N,
    DecisionLog,
    Factor,
    ModeConfig,
    blended_stats,
    compare,
    fit_m1,
    load_default_configs,
    load_mode_config,
    make_record,
    verdict_from,
)
from pairwisepm.strings import (
    PINNED_CEILING,
    PINNED_FRAGILITY_TMPL,
    STRINGS,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

W1N_KEYS = ["impact_primary_metric", "capability_feasibility", "reach",
            "unit_economics", "data_flywheel", "risk_surface", "effort"]
W1N = [0.25, 0.20, 0.15, 0.15, 0.10, 0.05, -0.10]  # D1 defaults (spec §2)
W1N_TAGS = ["lever", "lever", "fact", "lever", "fact", "lever", "lever"]

# D_FIX z-deltas in schema order; L = W1N · d = 0.26 (hand-computed).
D_FIX = [1.0, 0.5, -0.2, 0.0, 0.3, -1.0, 0.4]
L_FIX = 0.26
P_FIX = 0.5646362918030292


def std1_config(stds=None, ranges=None, weights=None) -> ModeConfig:
    """A 1→N-shaped config with seed mean 0 / std 1 (raw values ARE z-values)
    unless overridden — isolates the scorer from the z pipeline (spec §0)."""
    stds = stds or [1.0] * 7
    ranges = ranges or [(-100.0, 100.0)] * 7
    weights = weights or W1N
    factors = [
        Factor(key=k, name=k.replace("_", " "), scale="test",
               prior_weight=abs(w), sign=1 if w >= 0 else -1, tag=t,
               rationale="test fixture", seed_mean=0.0, seed_std=s,
               transform="identity", plausible_range=r)
        for k, w, t, s, r in zip(W1N_KEYS, weights, W1N_TAGS, stds, ranges)
    ]
    return ModeConfig(mode="one_to_n", label="1toN-test", banner=None,
                      factors=factors)


STD1 = std1_config()


def ideas_from_deltas(d):
    """raw_a = d, raw_b = 0 so z_A − z_B = d under STD1."""
    return (dict(zip(W1N_KEYS, [float(x) for x in d])),
            dict(zip(W1N_KEYS, [0.0] * 7)))


@pytest.fixture(scope="module")
def shipped():
    return load_default_configs()


# ---------------------------------------------------------------------------
# T-SYM — swap A/B ⇒ p exactly 1 − p
# ---------------------------------------------------------------------------

def _assert_swap(cfg, raw_a, raw_b, seed=7):
    va = compare(cfg, raw_a, raw_b, seed=seed)
    vb = compare(cfg, raw_b, raw_a, seed=seed)
    assert vb.m0.logit == -va.m0.logit  # bitwise (zero intercept)
    assert abs(va.m0.p + vb.m0.p - 1.0) <= 1e-12
    assert abs(vb.m0.interval[0] - (1 - va.m0.interval[1])) <= 1e-12
    assert abs(vb.m0.interval[1] - (1 - va.m0.interval[0])) <= 1e-12
    if va.m0.verdict == "A":
        assert vb.m0.verdict == "B"
    elif va.m0.verdict == "B":
        assert vb.m0.verdict == "A"
    else:
        assert vb.m0.verdict == "too_close"
    # equal-weight ablation preserves symmetry (T-SYM-02)
    assert vb.m0_equal.logit == -va.m0_equal.logit
    assert abs(va.m0_equal.p + vb.m0_equal.p - 1.0) <= 1e-12


def test_sym_fixture():
    _assert_swap(STD1, *ideas_from_deltas(D_FIX))


def test_sym_property_both_modes(shipped):
    rng = np.random.default_rng(20260830)
    for _ in range(25):
        d = rng.standard_normal(7)
        _assert_swap(STD1, *ideas_from_deltas(d))
    z2o = shipped["zero_to_one"]
    for _ in range(25):
        raw_a, raw_b = {}, {}
        for f in z2o.factors:
            lo, hi = f.plausible_range
            raw_a[f.key] = float(rng.uniform(lo, hi))
            raw_b[f.key] = float(rng.uniform(lo, hi))
        _assert_swap(z2o, raw_a, raw_b)


def test_sym_m1_scoring():
    """Swap symmetry holds for M1 too (zero intercept in the scoring fit)."""
    rng = np.random.default_rng(3)
    rows = [dict(zip(W1N_KEYS, rng.standard_normal(7))) for _ in range(12)]
    picks = [1 if sum(w * r[k] for w, k in zip(W1N, W1N_KEYS)) > 0 else 0
             for r in rows]
    fit = fit_m1(rows, picks, STD1)
    raw_a, raw_b = ideas_from_deltas(D_FIX)
    va = compare(STD1, raw_a, raw_b, m1_fit=fit)
    vb = compare(STD1, raw_b, raw_a, m1_fit=fit)
    assert vb.m1.logit == -va.m1.logit
    assert abs(va.m1.p + vb.m1.p - 1.0) <= 1e-12


# ---------------------------------------------------------------------------
# T-EQ — identical ideas ⇒ exactly 0.5 and too_close
# ---------------------------------------------------------------------------

def test_equal_ideas(shipped):
    for cfg in (STD1, shipped["one_to_n"], shipped["zero_to_one"]):
        raw = {f.key: (f.plausible_range[0] + f.plausible_range[1]) / 2
               for f in cfg.factors}
        v = compare(cfg, dict(raw), dict(raw))
        assert v.m0.logit == 0.0
        assert v.m0.p == 0.5
        assert v.m0.verdict == "too_close"
        assert all(r.contribution == 0.0 for r in v.leverage)


# ---------------------------------------------------------------------------
# T-M0 / T-CFG — hand-computed case; weights are config, not code
# ---------------------------------------------------------------------------

def test_m0_hand_value():
    # Pins the D1 default weights deliberately; regenerate if D1 changes.
    v = compare(STD1, *ideas_from_deltas(D_FIX))
    assert abs(v.m0.logit - L_FIX) <= 1e-12
    assert abs(v.m0.p - P_FIX) <= 1e-9


def test_weights_are_config():
    w = list(W1N)
    w[0] = 0.40  # impact .25 -> .40
    cfg = std1_config(weights=w)
    v = compare(cfg, *ideas_from_deltas(D_FIX))
    assert abs(v.m0.logit - 0.41) <= 1e-12


def test_config_shapes(shipped):
    n2n, z2o = shipped["one_to_n"], shipped["zero_to_one"]
    assert len(n2n.factors) == 7 and len(z2o.factors) == 6
    for cfg in (n2n, z2o):
        for f in cfg.factors:
            assert isinstance(f.prior_weight, float) and f.prior_weight > 0
            assert f.sign in (-1, 1)
            assert f.tag in ("lever", "fact")
            assert f.rationale.strip()
            assert f.scale.strip()
            assert f.seed_std > 0
    # Ceiling: a Flag with NO weight field at all (unweighted by construction)
    ceiling = [g for g in z2o.flags if g.key == "ceiling"]
    assert len(ceiling) == 1
    assert not hasattr(ceiling[0], "prior_weight")
    assert not hasattr(ceiling[0], "tag")
    # |weights| sum to 1.0 in both modes (spec §2 defaults)
    for cfg in (n2n, z2o):
        assert abs(sum(f.prior_weight for f in cfg.factors) - 1.0) <= 1e-9


def test_zero_to_one_banner_mandatory(shipped, tmp_path):
    assert shipped["zero_to_one"].banner == STRINGS["str.banner.01"]
    assert shipped["one_to_n"].banner is None
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "mode: zero_to_one\nlabel: x\nbanner: null\nfactors:\n"
        "  - {key: k, name: n, scale: s, prior_weight: 1.0, sign: 1,\n"
        "     tag: fact, rationale: r, seed_mean: 0, seed_std: 1}\n",
        encoding="utf-8")
    with pytest.raises(ValueError):
        load_mode_config(bad)


# ---------------------------------------------------------------------------
# T-MAP — MAP regularization never diverges on degenerate logs
# ---------------------------------------------------------------------------

def _converged(fit):
    w = np.array(list(fit.weights.values()))
    assert np.all(np.isfinite(w)) and np.max(np.abs(w)) <= 10.0


def test_map_empty_log():
    fit = fit_m1([], [], STD1)
    for k, w in zip(W1N_KEYS, W1N):
        assert fit.weights[k] == w  # bitwise: prior returned exactly
    assert fit.active is False


def test_map_one_decision():
    rows = [dict(zip(W1N_KEYS, D_FIX))]
    _converged(fit_m1(rows, [1], STD1))


def test_map_complete_separation():
    rng = np.random.default_rng(1)
    rows, picks = [], []
    for _ in range(12):
        d = rng.standard_normal(7)
        if sum(w * x for w, x in zip(W1N, d)) < 0:
            d = -d
        rows.append(dict(zip(W1N_KEYS, d)))
        picks.append(1)  # pick "A" every time
    fit = fit_m1(rows, picks, STD1)
    _converged(fit)
    assert np.isfinite(fit.free_intercept)


def test_map_rank_deficient_stays_at_prior():
    """A factor with zero observed variation stays AT its prior weight —
    shrinkage centered on the prior, not zero (the classic mistake §3 forbids)."""
    rng = np.random.default_rng(4)
    rows = []
    for _ in range(12):
        d = rng.standard_normal(7)
        d[2] = 0.0  # reach never varies
        rows.append(dict(zip(W1N_KEYS, d)))
    picks = [1 if sum(w * r[k] for w, k in zip(W1N, W1N_KEYS)) > 0 else 0
             for r in rows]
    fit = fit_m1(rows, picks, STD1)
    _converged(fit)
    assert abs(fit.weights["reach"] - W1N[2]) <= 1e-9


# ---------------------------------------------------------------------------
# T-VERDICT — interval straddling 0.5 ⇒ too_close (boundary breaks toward it)
# ---------------------------------------------------------------------------

def test_verdict_rule_units():
    assert verdict_from(0.55, (0.48, 0.61)) == "too_close"
    assert verdict_from(0.56, (0.52, 0.61)) == "A"
    assert verdict_from(0.44, (0.39, 0.48)) == "B"
    assert verdict_from(0.53, (0.50, 0.57)) == "too_close"  # touching counts


def test_verdict_end_to_end():
    near = [0.05, -0.03, 0.02, 0.0, -0.02, 0.04, 0.01]
    v = compare(STD1, *ideas_from_deltas(near), seed=42, n_boot=1000)
    lo, hi = v.m0.interval
    assert lo <= 0.5 <= hi and v.m0.verdict == "too_close"
    # Clear winner: the canonical seed-comparison deltas (contributions spread
    # across factors). NOTE for compliance: the spec's 3×D_FIX fixture is NOT
    # a clear winner under bootstrap-over-factors — D_FIX's dominant single
    # contribution (+0.75) against a large negative (−0.30) makes the
    # resampled interval straddle 50% even at L = 0.78. Flagged in the
    # exchange round; T-VERDICT-02's clear-winner fixture needs regenerating.
    clear = [0.5, 0.4, -0.4 / 3.0, 0.7, 0.8, -0.5, 0.0]
    v2 = compare(STD1, *ideas_from_deltas(clear))
    assert v2.m0.verdict == "A" and v2.m0.interval[0] > 0.5
    # even on a too-close, lever paths are computed (S4 "cheapest evidence")
    assert v.parity_paths and all(p.tag == "lever" for p in v.parity_paths)


def test_interval_always_present(shipped):
    for d in (D_FIX, [0.0] * 7):
        v = compare(STD1, *ideas_from_deltas(d))
        for sc in (v.m0, v.m0_equal):
            lo, hi = sc.interval
            assert 0.0 <= lo <= sc.p <= hi <= 1.0


# ---------------------------------------------------------------------------
# T-CEIL — ceiling flag never changes the score
# ---------------------------------------------------------------------------

def test_ceiling_never_scores(shipped):
    z2o = shipped["zero_to_one"]
    raw_a = {"problem_severity_frequency": 3.0,
             "capability_trajectory_exposure": 1.0, "evidence_of_pull": 2.0,
             "genai_necessity": 3.0, "data_distribution_advantage": 2.0,
             "cost_to_test": 3.0}
    raw_b = {"problem_severity_frequency": 2.0,
             "capability_trajectory_exposure": -1.0, "evidence_of_pull": 1.0,
             "genai_necessity": 3.0, "data_distribution_advantage": 1.0,
             "cost_to_test": 2.0}
    runs = [compare(z2o, raw_a, raw_b, seed=11, ceiling_a=ca, ceiling_b=cb)
            for ca, cb in ((False, False), (True, False), (True, True))]
    base = runs[0]
    for v in runs[1:]:
        assert v.m0.p == base.m0.p and v.m0.logit == base.m0.logit
        assert v.m0.interval == base.m0.interval
        assert [r.contribution for r in v.leverage] == \
               [r.contribution for r in base.leverage]
        assert [(p.key, p.raw_target, p.feasible) for p in v.parity_paths] == \
               [(p.key, p.raw_target, p.feasible) for p in base.parity_paths]
    assert base.ceiling_notes == []
    assert PINNED_CEILING in runs[1].ceiling_notes[0]
    assert len(runs[2].ceiling_notes) == 2


# ---------------------------------------------------------------------------
# T-EVAL — evaluative inputs are excluded from the score BY CONSTRUCTION
# ---------------------------------------------------------------------------

def test_evaluative_excluded_by_type():
    # The engine's compare() has no evaluative parameter at all: exclusion is
    # by type, not convention. They round-trip through the log record instead.
    assert "evaluative" not in inspect.signature(compare).parameters
    v = compare(STD1, *ideas_from_deltas(D_FIX))
    rec = make_record(
        timestamp="2026-08-30T12:00:00Z", mode="one_to_n",
        name_a="A", name_b="B",
        raw_a=ideas_from_deltas(D_FIX)[0], raw_b=ideas_from_deltas(D_FIX)[1],
        result=v, pick="A",
        evaluative_a={"strategic_fit": "core bet"},
        evaluative_b={"strategic_fit": "adjacent"},
    )
    assert rec["evaluative"]["a"]["strategic_fit"] == "core bet"


# ---------------------------------------------------------------------------
# T-PAR — path to parity: levers only, targets always reported, range flagged
# ---------------------------------------------------------------------------

def test_parity_arithmetic():
    # Impact std 1.2: z-shift = 0.26/0.25 = 1.04; raw = 1.04 × 1.2 = 1.248.
    cfg = std1_config(stds=[1.2, 1.0, 500.0, 1.0, 1.0, 1.0, 2.0],
                      ranges=[(-2, 2), (0, 4), (0, 1e7), (0, 4), (0, 4),
                              (0, 4), (0.5, 52)])
    raw_a = dict(zip(W1N_KEYS, [1.2 * 1.0, 2.5, 900.0, 2.0, 2.3, 1.0, 6.8]))
    raw_b = dict(zip(W1N_KEYS, [0.0, 2.0, 1000.0, 2.0, 2.0, 2.0, 6.0]))
    v = compare(cfg, raw_a, raw_b)
    assert abs(v.m0.logit - L_FIX) <= 1e-9  # deltas reproduce D_FIX
    path = next(p for p in v.parity_paths if p.key == "impact_primary_metric")
    assert path.loser == "B"
    assert abs(path.z_shift - 1.04) <= 1e-9
    assert abs(path.raw_shift - 1.248) <= 1e-9
    assert abs(path.raw_target - (0.0 + 1.248)) <= 1e-9
    assert path.feasible
    # 60/40 for the loser: (0.26 + ln 1.5) / 0.25
    assert abs(path.z_shift_6040 - 2.6618604324326583) <= 1e-9


def test_parity_levers_only():
    v = compare(STD1, *ideas_from_deltas(D_FIX))
    named = {p.key for p in v.parity_paths}
    assert "reach" not in named and "data_flywheel" not in named  # facts
    for p in v.parity_paths:
        assert p.tag == "lever"


def test_parity_infeasible_marked_not_hidden():
    # risk (lever, w=.05): z-shift 0.26/0.05 = 5.2 ⇒ target 2.0+5.2 = 7.2 > 4.
    cfg = std1_config(ranges=[(-2, 2), (0, 4), (0, 1e7), (0, 4), (0, 4),
                              (0, 4), (0.5, 52)])
    raw_a = dict(zip(W1N_KEYS, [1.0, 2.5, 0.0, 2.0, 0.3, 1.0, 6.4]))
    raw_b = dict(zip(W1N_KEYS, [0.0, 2.0, 0.2, 2.0, 0.0, 2.0, 6.0]))
    v = compare(cfg, raw_a, raw_b)
    risk = next(p for p in v.parity_paths if p.key == "risk_surface")
    assert risk.feasible is False  # marked infeasible AND kept in the list
    assert abs(risk.raw_target - 7.2) <= 1e-9  # target reported, not clamped


def test_loses_on_fundamentals(shipped):
    z2o = shipped["zero_to_one"]
    # Gap entirely on facts; both lever paths infeasible (pull at scale top,
    # cost_to_test at its floor for both ideas).
    raw_a = {"problem_severity_frequency": 3.5,
             "capability_trajectory_exposure": 1.0, "evidence_of_pull": 4.0,
             "genai_necessity": 3.0, "data_distribution_advantage": 2.0,
             "cost_to_test": 0.25}
    raw_b = {"problem_severity_frequency": 2.0,
             "capability_trajectory_exposure": 0.0, "evidence_of_pull": 4.0,
             "genai_necessity": 2.0, "data_distribution_advantage": 1.5,
             "cost_to_test": 0.25}
    v = compare(z2o, raw_a, raw_b)
    assert v.m0.verdict == "A"
    assert not any(p.feasible for p in v.parity_paths)
    assert v.loses_on_fundamentals is True


# ---------------------------------------------------------------------------
# T-FRAG — fragility flag (FRAGILITY_Z = 0.75 pending Decisions D6)
# ---------------------------------------------------------------------------

def test_fragility_fragile():
    # d = [0.4, 0...] ⇒ L = 0.10; impact needs 0.4σ ≤ 0.75σ ⇒ fragile.
    v = compare(STD1, *ideas_from_deltas([0.4, 0, 0, 0, 0, 0, 0]))
    assert v.fragility.fragile is True
    assert v.fragility.factor_key == "impact_primary_metric"
    assert PINNED_FRAGILITY_TMPL.format(
        factor=v.fragility.factor_name) in v.fragility.message


def test_fragility_robust():
    # D_FIX: L = 0.26; smallest flip needs 0.26/0.25 = 1.04σ > 0.75σ.
    v = compare(STD1, *ideas_from_deltas(D_FIX))
    assert v.fragility.fragile is False


# ---------------------------------------------------------------------------
# T-ZETA — Kendall's ζ on known cases (most recent pick per pair)
# ---------------------------------------------------------------------------

def _rec(a, b, pick, ts="2026-08-30T12:00:00Z", mode="one_to_n"):
    return {"timestamp": ts, "mode": mode,
            "idea_a": {"name": a, "raw": {}, "z": {}},
            "idea_b": {"name": b, "raw": {}, "z": {}},
            "pick": pick,
            "model": {"active": "M0", "m0_p": 0.6, "verdict": "A"}}


def test_zeta_intransitive_triad():
    log = DecisionLog([_rec("A", "B", "A"), _rec("B", "C", "A"),
                       _rec("C", "A", "A")])
    assert abs(log.kendall_zeta() - 0.0) <= 1e-12


def test_zeta_transitive_sets():
    log3 = DecisionLog([_rec("A", "B", "A"), _rec("B", "C", "A"),
                        _rec("A", "C", "A")])
    assert abs(log3.kendall_zeta() - 1.0) <= 1e-12
    pairs4 = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("B", "D"),
              ("C", "D")]
    log4 = DecisionLog([_rec(a, b, "A") for a, b in pairs4])
    assert abs(log4.kendall_zeta() - 1.0) <= 1e-12


def test_zeta_small_n_returns_none():
    assert DecisionLog([]).kendall_zeta() is None
    assert DecisionLog([_rec("A", "B", "A")]).kendall_zeta() is None
    assert DecisionLog([_rec("A", "B", "A"),
                        _rec("B", "C", "A")]).kendall_zeta() is None


def test_zeta_most_recent_pick_wins():
    # A>B then later B>A: the edge is B beats A (update, not double-count).
    log = DecisionLog([_rec("A", "B", "A"), _rec("B", "C", "A"),
                       _rec("A", "C", "A"), _rec("A", "B", "B")])
    # Now B>A, B>C, A>C: transitive (B > A > C) ⇒ ζ = 1.
    assert abs(log.kendall_zeta() - 1.0) <= 1e-12


# ---------------------------------------------------------------------------
# T-BRIER — hand-computed cases (prediction-of-pick, from decision 1)
# ---------------------------------------------------------------------------

def _rec_p(p, pick):
    r = _rec("A", "B", pick)
    r["model"]["m0_p"] = p
    return r


def test_brier_hand_case():
    log = DecisionLog([_rec_p(0.8, "A"), _rec_p(0.6, "B"), _rec_p(0.5, "A")])
    assert abs(log.brier() - 0.21666666666666667) <= 1e-12


def test_brier_from_decision_one_and_empty():
    assert abs(DecisionLog([_rec_p(0.8, "A")]).brier() - 0.04) <= 1e-12
    assert DecisionLog([]).brier() is None


# ---------------------------------------------------------------------------
# T-SHRINK / T-ACT — shrinkage to prior; activation at exactly 10
# ---------------------------------------------------------------------------

def _small_log(n=3, seed=3):
    rng = np.random.default_rng(seed)
    rows, picks = [], []
    for _ in range(n):
        d = rng.standard_normal(7)
        rows.append(dict(zip(W1N_KEYS, d)))
        picks.append(1 if sum(w * x for w, x in zip(W1N, d)) > 0 else 0)
    return rows, picks


def test_shrink_limit():
    rows, picks = _small_log()
    fit = fit_m1(rows, picks, STD1, lam=1e6)
    assert max(abs(fit.weights[k] - w) for k, w in zip(W1N_KEYS, W1N)) <= 1e-3


def test_shrink_monotone_in_lambda():
    rows, picks = _small_log()

    def dist(lam):
        f = fit_m1(rows, picks, STD1, lam=lam)
        return math.sqrt(sum((f.weights[k] - w) ** 2
                             for k, w in zip(W1N_KEYS, W1N)))

    assert dist(1e3) <= dist(10) + 1e-9 <= dist(0.1) + 2e-9


def test_activation_gate_exactly_10():
    assert M1_ACTIVATION_N == 10  # Decisions convention C1
    rows9, picks9 = _small_log(9, seed=5)
    fit9 = fit_m1(rows9, picks9, STD1)
    assert fit9.active is False
    raw_a, raw_b = ideas_from_deltas(D_FIX)
    v9 = compare(STD1, raw_a, raw_b, m1_fit=fit9)
    assert v9.active_model == "M0"  # inactive fit never drives the verdict
    rows10, picks10 = _small_log(10, seed=5)
    fit10 = fit_m1(rows10, picks10, STD1)
    assert fit10.active is True
    v10 = compare(STD1, raw_a, raw_b, m1_fit=fit10)
    assert v10.active_model == "M1" and v10.m1 is not None
    # divergence payload: per-factor revealed-vs-stated is derivable
    assert set(v10.m1.weights) == set(v10.m0.weights)


# ---------------------------------------------------------------------------
# T-BIAS — free intercept detects injected order bias, never scores
# ---------------------------------------------------------------------------

def test_order_bias_injected():
    rng = np.random.default_rng(20260830)
    rows = [dict(zip(W1N_KEYS, rng.standard_normal(7))) for _ in range(40)]
    fit = fit_m1(rows, [1] * 40, STD1)  # a judge who always keeps slot A
    assert fit.free_intercept >= 0.75
    assert fit.order_bias_flagged is True
    # the SCORING path is unaffected: swap symmetry still exact under this fit
    raw_a, raw_b = ideas_from_deltas(D_FIX)
    va = compare(STD1, raw_a, raw_b, m1_fit=fit)
    vb = compare(STD1, raw_b, raw_a, m1_fit=fit)
    assert vb.m1.logit == -va.m1.logit


def test_order_bias_mirrored_control():
    rng = np.random.default_rng(20260830)
    rows = [dict(zip(W1N_KEYS, rng.standard_normal(7))) for _ in range(40)]
    mirrored = rows + [{k: -v for k, v in r.items()} for r in rows]
    picks = [1] * 40 + [0] * 40
    fit = fit_m1(mirrored, picks, STD1)
    assert abs(fit.free_intercept) <= 1e-3
    assert fit.order_bias_flagged is False


# ---------------------------------------------------------------------------
# T-LOG — round-trip, schema completeness, log sufficiency
# ---------------------------------------------------------------------------

def test_log_roundtrip_full_precision():
    v = compare(STD1, *ideas_from_deltas(D_FIX))
    rec = make_record(
        timestamp="2026-08-30T14:12:03Z", mode="one_to_n",
        name_a="Idée A", name_b="B",
        raw_a=ideas_from_deltas(D_FIX)[0], raw_b=ideas_from_deltas(D_FIX)[1],
        result=v, pick="B",
        override_rationale="ratée — höher",
    )
    log = DecisionLog([rec])
    back = DecisionLog.from_jsonl(log.to_jsonl())
    assert back.records[0] == rec  # exact, full-precision equality
    assert rec["outcome"] is None and "outcome" in rec  # M2 runway slot
    assert rec["model"]["m1_p"] is None  # null until an M1 fit exists
    for key in ("schema_version", "timestamp", "mode", "idea_a", "idea_b",
                "evaluative", "flags", "pick", "model", "override_rationale",
                "outcome"):
        assert key in rec


def test_log_is_sufficient_training_set():
    """From JSONL text alone: fit_m1, zeta, brier reproduce (SC-07)."""
    cfg = STD1
    rng = np.random.default_rng(9)
    log = DecisionLog()
    names = ["P", "Q", "R", "S"]
    for i in range(12):
        d = rng.standard_normal(7)
        raw_a, raw_b = ideas_from_deltas(d)
        v = compare(cfg, raw_a, raw_b)
        pick = "A" if v.m0.p > 0.5 else "B"
        log.append(make_record(
            timestamp=f"2026-08-30T10:{i:02d}:00Z", mode="one_to_n",
            name_a=names[i % 4], name_b=names[(i + 1) % 4],
            raw_a=raw_a, raw_b=raw_b, result=v, pick=pick))
    before = (log.kendall_zeta(), log.brier())
    rows, picks = log.training_data(cfg)
    w_before = fit_m1(rows, picks, cfg).weights
    reread = DecisionLog.from_jsonl(log.to_jsonl())
    assert reread.kendall_zeta() == before[0]
    assert abs(reread.brier() - before[1]) <= 1e-12
    rows2, picks2 = reread.training_data(cfg)
    w_after = fit_m1(rows2, picks2, cfg).weights
    assert all(abs(w_after[k] - w_before[k]) <= 1e-12 for k in w_before)


def test_log_merge_dedupe_and_order():
    a = DecisionLog([_rec("A", "B", "A", ts="2026-08-30T12:00:00Z"),
                     _rec("B", "C", "A", ts="2026-08-30T13:00:00Z")])
    b = DecisionLog([_rec("A", "B", "A", ts="2026-08-30T12:00:00Z"),  # dup
                     _rec("A", "C", "A", ts="2026-08-30T11:00:00Z")])
    m = a.merged(b)
    assert m.n() == 3  # duplicate (same timestamp + inputs) kept once
    assert [r["timestamp"] for r in m.records] == sorted(
        r["timestamp"] for r in m.records)
    assert a.n() == 2 and b.n() == 2  # inputs not mutated


# ---------------------------------------------------------------------------
# T-FPR — config_fingerprint: policy-version stamp in every log record
# (architecture §4.1 data contract; additive v1.1 key, F-21/DV-10 closed)
# ---------------------------------------------------------------------------

def test_config_fingerprint_stamped_and_canonical(shipped, tmp_path):
    n2n = shipped["one_to_n"]
    # Shipped configs carry a sha256 hex fingerprint, distinct per mode.
    for cfg in shipped.values():
        assert re.fullmatch(r"[0-9a-f]{64}", cfg.fingerprint)
    assert shipped["one_to_n"].fingerprint != shipped["zero_to_one"].fingerprint
    # Stable across loads; insensitive to YAML formatting; sensitive to policy.
    import yaml as _yaml
    src = (pairwisepm.default_config_dir() / "one_to_n.yaml").read_text(
        encoding="utf-8")
    reloaded = load_mode_config(pairwisepm.default_config_dir() / "one_to_n.yaml")
    assert reloaded.fingerprint == n2n.fingerprint
    reformatted = tmp_path / "reformatted.yaml"
    reformatted.write_text(
        _yaml.safe_dump(_yaml.safe_load(src), sort_keys=True), encoding="utf-8")
    assert load_mode_config(reformatted).fingerprint == n2n.fingerprint
    edited_data = _yaml.safe_load(src)
    edited_data["factors"][0]["prior_weight"] = 0.40  # a policy change
    edited = tmp_path / "edited.yaml"
    edited.write_text(_yaml.safe_dump(edited_data), encoding="utf-8")
    assert load_mode_config(edited).fingerprint != n2n.fingerprint
    # Stamped into records; null (not absent) when the caller has none; and
    # pre-v1.1 records without the key still parse (ignore-unknown/missing).
    raw = {f.key: f.raw_from_z(0.5 if f.sign > 0 else -0.5) for f in n2n.factors}
    raw_b = {f.key: f.raw_from_z(0.0) for f in n2n.factors}
    v = compare(n2n, raw, raw_b)
    rec = make_record(timestamp="2026-08-30T12:00:00Z", mode="one_to_n",
                      name_a="A", name_b="B", raw_a=raw, raw_b=raw_b,
                      result=v, pick="A", config_fingerprint=n2n.fingerprint)
    assert rec["config_fingerprint"] == n2n.fingerprint
    rec_old = make_record(timestamp="2026-08-30T12:00:00Z", mode="one_to_n",
                          name_a="A", name_b="B", raw_a=raw, raw_b=raw_b,
                          result=v, pick="A")
    assert rec_old["config_fingerprint"] is None
    del rec_old["config_fingerprint"]  # a pre-v1.1 record
    back = DecisionLog.from_jsonl(DecisionLog([rec, rec_old]).to_jsonl())
    assert back.n() == 2 and back.brier() is not None


# ---------------------------------------------------------------------------
# D5 — blended z-basis (seed as pseudo-sample; no discontinuity)
# ---------------------------------------------------------------------------

def test_blended_stats_continuity():
    cfg = STD1
    empty = blended_stats([], cfg)
    for f in cfg.factors:
        assert empty[f.key] == (f.seed_mean, f.seed_std)  # no log ⇒ seed
    one = blended_stats([{k: 2.0 for k in W1N_KEYS}], cfg)
    for f in cfg.factors:
        m, s = one[f.key]
        # one observation nudges, never jumps: mean moves toward 2 by 1/11
        assert abs(m - 2.0 / 11.0) <= 1e-12
    big = [{k: float(x) for k in W1N_KEYS}
           for x in np.random.default_rng(0).normal(5.0, 2.0, size=500)]
    blended = blended_stats(big, cfg, pseudo_weight=10)
    for f in cfg.factors:
        m, s = blended[f.key]
        assert abs(m - 5.0) < 0.4 and abs(s - 2.0) < 0.5  # converges to log


# ---------------------------------------------------------------------------
# T-NEG — negative tests for Spine refusals
# ---------------------------------------------------------------------------

FORBIDDEN_IMPORTS = ("openai", "anthropic", "transformers", "litellm",
                     "langchain", "httpx", "requests", "aiohttp")


def test_no_llm_or_network_imports():
    """T-NEG-01 — the Spine's first refusal: no LLM, no network, at runtime.

    ROUND-19 SUBJECT CORRECTION (compliance, spec §27i), and it is a
    STRENGTHENING of the clause rather than a relaxation of it. The import half
    of this test used to read ``sys.modules`` **of the pytest process**, which
    is not the product: it is whatever every previously-collected test file
    happened to import. That made the assertion ORDER-DEPENDENT and it was
    green only by collection accident — ``tests/test_packaging.py`` execs
    ``app.py``, which imports gradio, which imports ``httpx``, and gradio's
    UI dependency is legitimate (T-PKG-02 keeps it OUT of the engine and
    ``test_no_network_calls_at_runtime`` below kills the socket). Demonstrated
    rather than argued, on the unmutated repo::

        pytest tests/test_packaging.py tests/test_engine.py
        → FAILED test_no_llm_or_network_imports - AssertionError: httpx

    The same file passes alone and passed in the full suite only because
    ``test_engine`` sorts before ``test_packaging``. A guard on the Spine's
    hardest refusal that reds on the order its own suite is invoked in is a
    guard nobody can act on: the honest reading of that red is "some other test
    imported gradio", and the fix a hurried reader reaches for is to delete the
    line. So the claim is now asserted where it is actually true and actually
    load-bearing — **importing the ENGINE, in a fresh interpreter, pulls in no
    LLM and no network client** — which is order-independent, is the property
    the shipped package must have, and is the property a `pip install` of this
    project can break.

    ROUND-20 SCOPE WORD ON THE SENTENCE THAT USED TO END THIS DOCSTRING
    (decisions' demand, accepted; the struck text is kept legible, because a
    correction that deletes what it corrects teaches nobody). It read: *"The
    source scan is unchanged and still covers ``app.py``."* That is true of the
    TEXT and false of the GRAPH, and the difference is the whole of what a
    later reader needs. The source scan is a REGEX over direct
    ``import``/``from`` lines in ``pairwisepm/*.py`` plus ``app.py``; the
    child-process probe's subject is the ENGINE only (``pairwisepm`` and its
    four modules). So ``app.py``'s TRANSITIVE import graph is asserted by
    nothing in this clause, and that is deliberate rather than a hole: app.py
    imports gradio, gradio imports ``httpx``, that UI dependency is legitimate
    (T-PKG-02 keeps it out of the engine), and nothing should red on it. What
    holds the runtime claim on the UI surface is a DIFFERENT instrument —
    ``test_no_network_calls_at_runtime`` below, whose socket kill-switch runs a
    full cycle in both modes. Verified rather than reasoned (decisions' run,
    re-derived here): a fresh interpreter importing the engine loads ~217
    modules with ``httpx`` and ``gradio`` both absent, while one that execs
    ``app.py`` has ``httpx`` in ``sys.modules``. Whoever asks whether a NEW
    app-side dependency is covered by this clause must read **no** — direct
    import lines only, never the transitive graph.

    THIS CLAUSE HAS A FLOOR (design's round-20 demand):
    ``test_the_no_llm_guard_cannot_be_quietly_weakened`` below asserts, by AST
    over this file, that ``FORBIDDEN_IMPORTS`` still names the network and LLM
    modules, that this clause carries no skip marker, and that BOTH halves
    survive. The fifteen-second fix visible from a red here is to delete a name
    from the tuple, and that single edit retires the Spine's offline promise
    with the whole suite green behind it.
    """
    import json
    import pathlib
    import subprocess

    pkg = pathlib.Path(pairwisepm.__file__).parent
    probe = (
        "import json, sys, importlib\n"
        "for m in ('pairwisepm', 'pairwisepm.engine', 'pairwisepm.config',\n"
        "          'pairwisepm.log', 'pairwisepm.strings'):\n"
        "    importlib.import_module(m)\n"
        "sys.stdout.write(json.dumps(sorted(sys.modules)))\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", probe],
        capture_output=True, text=True, cwd=str(pkg.parent),
    )
    assert proc.returncode == 0, (
        "the engine package could not be imported in a fresh interpreter:\n"
        + proc.stderr
    )
    loaded = json.loads(proc.stdout)
    pulled = sorted(
        name for name in FORBIDDEN_IMPORTS
        if any(m == name or m.startswith(name + ".") for m in loaded)
    )
    assert not pulled, (
        f"importing the engine pulls in {pulled} — the Spine refuses any LLM "
        "in the runtime loop and any network call (SPINE.md, Solution "
        "Direction + Scope Boundaries Out). This is asserted in a CHILD "
        "PROCESS on purpose: read from the pytest process it is a statement "
        "about the test session, not about the product."
    )

    sources = list(pkg.glob("*.py")) + [pkg.parent / "app.py"]
    pat = re.compile(
        r"^\s*(import|from)\s+(" + "|".join(FORBIDDEN_IMPORTS) + r")\b",
        re.MULTILINE)
    for src in sources:
        assert not pat.search(src.read_text(encoding="utf-8")), src


# The names T-NEG-01's tuple may never stop containing. The tuple may GROW —
# a new hosted-inference client belongs in it — and may never SHRINK, because
# the cheapest exit from a red on the clause above is to delete the offending
# name, which buys a green suite by retiring the Spine's loudest refusal.
_NO_LLM_FLOOR = frozenset({
    "openai", "anthropic", "transformers", "litellm", "langchain",
    "httpx", "requests", "aiohttp",
})


def test_the_no_llm_guard_cannot_be_quietly_weakened():
    """T-NEG-01d — the floor under the Spine's first refusal.

    Registered round 20 on design's demand, in the T-COPY-03 / T-VEND-07
    pattern and for their reason: an instrument that two other seats cite, and
    that a hurried reader can silence with a one-token edit, needs its own
    shape asserted or the silencing happens with the suite green.

    The exposure is specific and it was created by the round-19 repair, not by
    an accident. T-NEG-01's red now reads ``importing the engine pulls in
    ['httpx']``, and the fastest edit that clears it is to delete ``"httpx"``
    from ``FORBIDDEN_IMPORTS`` — one token, no test deleted, no docstring
    touched, whole suite green, and the Spine's *"runs entirely offline after
    download"* (Success Metrics) plus *"Out: any LLM in the runtime loop"*
    (Scope Boundaries) unwatched from that minute on. Three other edits are the
    same shape: adding ``@pytest.mark.skip``, deleting the source-scan half so
    only the engine probe remains, or deleting the child-process half so only
    the regex remains.

    So four properties, all read off THIS file's AST rather than off memory:

    1. ``FORBIDDEN_IMPORTS`` still names every module in ``_NO_LLM_FLOOR``.
       Growing the tuple is free; shrinking it reds here, in the same change,
       naming what was removed.
    2. T-NEG-01 carries NO skip marker and calls no ``pytest.skip``. Its
       subject is the shipped package, which exists in every tree that can run
       this file, so a skip here could only ever be an excuse.
    3. BOTH HALVES SURVIVE — the child-process probe (``subprocess.run`` on
       ``sys.executable``) and the source scan (a regex built from
       ``FORBIDDEN_IMPORTS``, run over the package plus ``app.py``). Either
       half alone still passes and still reads like a guard: the probe alone
       stops watching app.py's import lines, the regex alone stops watching
       what a transitive dependency drags in.
    4. ``test_no_network_calls_at_runtime`` is still present and unskipped. It
       is the only instrument holding the runtime claim on the UI surface,
       which T-NEG-01's round-20 scope word says out loud it does not cover.

    This clause asserts SHAPE, never behaviour: it stays green when someone
    strengthens the guard, adds a name, or replaces the probe with a stricter
    one — the T-COPY-03 property that keeps a floor from becoming a freeze.
    """
    import ast
    import pathlib

    source = pathlib.Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}

    # (1) The tuple may grow, never shrink.
    declared = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "FORBIDDEN_IMPORTS"
            for t in node.targets
        ):
            declared = node.value
    assert declared is not None, (
        "FORBIDDEN_IMPORTS is no longer assigned at module level in this "
        "file. T-NEG-01 builds both of its halves out of that tuple; without "
        "it the clause asserts whatever is left."
    )
    names = {
        e.value for e in getattr(declared, "elts", [])
        if isinstance(e, ast.Constant) and isinstance(e.value, str)
    }
    dropped = sorted(_NO_LLM_FLOOR - names)
    assert not dropped, (
        "FORBIDDEN_IMPORTS has stopped naming " + ", ".join(dropped)
        + " — that is the fifteen-second exit from a T-NEG-01 red and it "
        "retires the Spine's offline promise (Success Metrics: 'runs "
        "entirely offline after download'; Out: 'any LLM in the runtime "
        "loop') with the whole suite green. The tuple may GROW freely. It "
        "shrinks only by a deliberate change that edits _NO_LLM_FLOOR here, "
        "in the same commit, with the reason written down."
    )

    # (2) + (4) No skips on either refusal clause.
    for name in ("test_no_llm_or_network_imports",
                 "test_no_network_calls_at_runtime"):
        node = functions.get(name)
        assert node is not None, (
            f"{name} has gone missing from this file. The Spine's refusal of "
            "any LLM in the runtime loop has exactly two instruments and this "
            "is one of them."
        )
        markers = [
            ast.unparse(dec) for dec in node.decorator_list
            if "skip" in ast.unparse(dec) or "xfail" in ast.unparse(dec)
        ]
        assert not markers, (
            f"{name} carries {markers[0]}. A skipped refusal guard reports as "
            "a green run in which nothing was refused."
        )
        skips = [
            sub for sub in ast.walk(node)
            if isinstance(sub, ast.Call)
            and isinstance(sub.func, ast.Attribute)
            and sub.func.attr in ("skip", "xfail")
            and isinstance(sub.func.value, ast.Name)
            and sub.func.value.id == "pytest"
        ]
        assert not skips, (
            f"{name} can now skip itself. Its subject is the shipped package, "
            "which is present in every tree that can run this file at all."
        )

    # (3) Both halves of T-NEG-01 survive.
    neg01 = functions["test_no_llm_or_network_imports"]
    calls = list(ast.walk(neg01))
    subprocess_run = any(
        isinstance(sub, ast.Call)
        and isinstance(sub.func, ast.Attribute)
        and sub.func.attr == "run"
        and isinstance(sub.func.value, ast.Name)
        and sub.func.value.id == "subprocess"
        for sub in calls
    )
    assert subprocess_run, (
        "T-NEG-01 no longer runs its forbidden-module census in a CHILD "
        "PROCESS. Read from the pytest process, that half is a statement "
        "about the test session's collection order, not about the product — "
        "which is the round-19 defect it was rewritten to remove."
    )
    assert any(
        isinstance(sub, ast.Attribute) and sub.attr == "executable"
        for sub in calls
    ), "T-NEG-01's probe no longer launches a fresh `sys.executable`."
    assert any(
        isinstance(sub, ast.Call)
        and isinstance(sub.func, ast.Attribute)
        and sub.func.attr == "compile"
        and isinstance(sub.func.value, ast.Name)
        and sub.func.value.id == "re"
        for sub in calls
    ), (
        "T-NEG-01's SOURCE-SCAN half is gone. The child-process probe covers "
        "the engine's import graph; the regex is what watches app.py's own "
        "import lines, and each half passes and reads like a guard without "
        "the other."
    )
    literals = {
        sub.value for sub in calls
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str)
    }
    assert "app.py" in literals, (
        "T-NEG-01's source scan no longer names app.py. The UI module is the "
        "one file in this repository that a network client could enter "
        "through a direct import without the engine probe noticing."
    )
    assert sum(
        1 for sub in calls
        if isinstance(sub, ast.Name) and sub.id == "FORBIDDEN_IMPORTS"
    ) >= 2, (
        "T-NEG-01 references FORBIDDEN_IMPORTS fewer than twice: one of its "
        "two halves has stopped being built from the shared tuple, so the "
        "tuple floor asserted above no longer reaches both."
    )


def test_no_network_calls_at_runtime(monkeypatch, tmp_path):
    """Socket kill-switch: a full cycle in both modes touches no network."""
    import socket

    def _boom(*a, **k):
        raise AssertionError("network call in runtime")

    monkeypatch.setattr(socket, "socket", _boom)
    monkeypatch.setattr(socket, "create_connection", _boom)
    shipped = load_default_configs()
    log = DecisionLog()
    rng = np.random.default_rng(2)
    for i in range(12):
        d = rng.standard_normal(7)
        raw_a, raw_b = ideas_from_deltas(d)
        v = compare(STD1, raw_a, raw_b)
        log.append(make_record(
            timestamp=f"2026-08-30T10:{i:02d}:00Z", mode="one_to_n",
            name_a=f"I{i % 3}", name_b=f"I{(i + 1) % 3}",
            raw_a=raw_a, raw_b=raw_b, result=v,
            pick="A" if v.m0.p >= 0.5 else "B"))
    (tmp_path / "log.jsonl").write_text(log.to_jsonl(), encoding="utf-8")
    reread = DecisionLog.from_jsonl(
        (tmp_path / "log.jsonl").read_text(encoding="utf-8"))
    reread.kendall_zeta(); reread.brier()
    rows, picks = reread.training_data(STD1)
    fit_m1(rows, picks, STD1)
    z2o = shipped["zero_to_one"]
    raw = {f.key: (f.plausible_range[0] + f.plausible_range[1]) / 2
           for f in z2o.factors}
    compare(z2o, dict(raw), dict(raw), ceiling_a=True)


def test_strictly_two_ideas():
    raw_a, raw_b = ideas_from_deltas(D_FIX)
    with pytest.raises(TypeError):
        compare(STD1, raw_a, raw_b, dict(raw_a))  # a third idea
    with pytest.raises(TypeError):
        # DV-4: even smuggled into the keyword slot, a third idea dict fails
        # fast with a clean TypeError, not an AttributeError mid-fit.
        compare(STD1, raw_a, raw_b, m1_fit=dict(raw_a))
    public = [n for n in dir(pairwisepm) if not n.startswith("_")]
    for n in public:
        assert not re.search(r"rank|sort|tournament|round_robin|portfolio"
                             r"|knapsack|optimi[sz]e|allocat", n, re.I), n


def test_banner_attached_and_wording(shipped):
    z2o, n2n = shipped["zero_to_one"], shipped["one_to_n"]
    raw = {f.key: (f.plausible_range[0] + f.plausible_range[1]) / 2
           for f in z2o.factors}
    v = compare(z2o, dict(raw), dict(raw))
    assert v.banner == STRINGS["str.banner.01"]  # every 0→1 result carries it
    raw_n = {f.key: f.raw_from_z(0.0) for f in n2n.factors}
    assert compare(n2n, dict(raw_n), dict(raw_n)).banner is None
    for word in ("accuracy", "predictive"):
        assert word not in v.banner.lower()


def test_engine_determinism():
    raw_a, raw_b = ideas_from_deltas(D_FIX)
    v1 = compare(STD1, raw_a, raw_b, seed=7)
    v2 = compare(STD1, raw_a, raw_b, seed=7)
    assert v1.m0.p == v2.m0.p and v1.m0.interval == v2.m0.interval
    assert [r.contribution for r in v1.leverage] == \
           [r.contribution for r in v2.leverage]


def test_requirements_whitelist():
    """Runtime deps: numpy + PyYAML (engine/config) + gradio (UI only).
    PyYAML is on the whitelist per architecture (spec §2: editable YAML
    config) — flagged to compliance to amend T-NEG-01c's {numpy, gradio}."""
    import pathlib
    req = (pathlib.Path(pairwisepm.__file__).parent.parent
           / "requirements.txt").read_text(encoding="utf-8")
    deps = {re.split(r"[<>=!~\[]", ln.strip())[0].lower()
            for ln in req.splitlines()
            if ln.strip() and not ln.strip().startswith("#")}
    assert deps <= {"numpy", "pyyaml", "gradio"}, deps
