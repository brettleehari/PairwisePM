"""PairwisePM — a mechanical pairwise judge for GenAI product decisions.

Two ideas enter on one questionnaire; out comes the winner, a win probability
with an interval, and the levers that would flip the verdict. The runtime is a
traditional offline model — weights and a (zero) bias term. No LLM, no API
key, no network: the LLM's job ended at build time.

Package layout:
- :mod:`pairwisepm.config` — YAML factor-schema loader (the tables are config).
- :mod:`pairwisepm.engine` — z-scoring, M0/M1 regression ladder, bootstrap
  intervals, leverage panel.
- :mod:`pairwisepm.log` — local JSONL decision log, ζ transitivity, Brier.
"""

from .config import (
    EvaluativeInput,
    Factor,
    Flag,
    ModeConfig,
    config_fingerprint,
    default_config_dir,
    load_default_configs,
    load_mode_config,
)
from .engine import (
    FRAGILITY_Z,
    M1_ACTIVATION_N,
    SEED_PSEUDO_WEIGHT,
    ComparisonResult,
    Fragility,
    LeverageRow,
    M1Fit,
    ModelScore,
    ParityPath,
    blended_stats,
    compare,
    effective_weights,
    fit_m1,
    leverage_panel,
    log_derived_stats,
    sigmoid,
    verdict_from,
    zscore_idea,
)
from .log import RELIABILITY_CURVE_MIN_N, SCHEMA_VERSION, DecisionLog, make_record
from .strings import STRINGS, prob_token

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "Factor", "EvaluativeInput", "Flag", "ModeConfig", "config_fingerprint",
    "load_mode_config", "load_default_configs", "default_config_dir",
    "compare", "fit_m1", "zscore_idea", "log_derived_stats", "blended_stats",
    "effective_weights", "leverage_panel", "sigmoid", "verdict_from",
    "ComparisonResult", "ModelScore", "M1Fit", "LeverageRow", "ParityPath",
    "Fragility", "M1_ACTIVATION_N", "FRAGILITY_Z", "SEED_PSEUDO_WEIGHT",
    "DecisionLog", "make_record", "SCHEMA_VERSION", "RELIABILITY_CURVE_MIN_N",
    "STRINGS", "prob_token",
]
