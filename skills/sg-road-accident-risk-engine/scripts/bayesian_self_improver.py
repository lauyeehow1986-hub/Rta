#!/usr/bin/env python3
"""
Online Bayesian Gamma-Poisson & Logistic SGD Self-Improving Loop for Singapore Road Accident Engine.
Ingests new accident records (from LTA DataMall TrafficIncidents or SPF casualty logs),
updates subzone conjugate priors, recalculates YoY trend velocity (EWMA), and tunes feature weights.
"""
import json
import math
import sys
from datetime import datetime

DEFAULT_PRIORS = {
    "TPE_PUNGGOL_CORRIDOR": {"alpha": 84.0, "beta": 1000.0, "ewma_trend": 0.142, "brier_history": [0.082]},
    "BKE_WOODLANDS_EXIT10A": {"alpha": 79.0, "beta": 1000.0, "ewma_trend": 0.118, "brier_history": [0.079]},
    "PIE_JURONG_WEST_TUAS": {"alpha": 76.0, "beta": 1000.0, "ewma_trend": 0.129, "brier_history": [0.081]},
    "CTE_BRADDELL_ANG_MO_KIO": {"alpha": 74.0, "beta": 1000.0, "ewma_trend": 0.065, "brier_history": [0.075]},
    "CLARKE_QUAY_RIVER_VALLEY": {"alpha": 68.0, "beta": 1000.0, "ewma_trend": 0.088, "brier_history": [0.077]},
    "GEYLANG_KALLANG_SIMS": {"alpha": 71.0, "beta": 1000.0, "ewma_trend": 0.094, "brier_history": [0.078]},
    "TAMPINES_AVE10_CENTRAL": {"alpha": 66.0, "beta": 1000.0, "ewma_trend": 0.112, "brier_history": [0.074]},
    "TOA_PAYOH_BISHAN_OLD_ESTATE": {"alpha": 58.0, "beta": 1000.0, "ewma_trend": 0.135, "brier_history": [0.071]}
}

FEATURE_WEIGHTS = {
    "w_rain_hydroplane": 0.615,
    "w_speed_shear": 0.854,
    "w_bar_nightlife": 0.742,
    "w_motorcycle_exposure": 1.295,
    "w_elderly_jaywalk": 0.912,
    "w_driver_youth_peers": 0.588
}


def update_engine(subzone_id: str, observed_accidents: int, exposure_windows: int, features: dict, learning_rate: float = 0.035) -> dict:
    state = DEFAULT_PRIORS.get(subzone_id, {"alpha": 50.0, "beta": 1000.0, "ewma_trend": 0.05, "brier_history": [0.080]}).copy()
    prior_mean = state["alpha"] / state["beta"]

    # 1. Conjugate Gamma-Poisson Posterior Update
    state["alpha"] += observed_accidents
    state["beta"] += exposure_windows
    posterior_mean = state["alpha"] / state["beta"]

    # 2. EWMA Trend Velocity Update
    observed_rate = observed_accidents / max(1, exposure_windows)
    relative_delta = (observed_rate - prior_mean) / max(1e-4, prior_mean)
    state["ewma_trend"] = round(0.85 * state["ewma_trend"] + 0.15 * relative_delta, 4)

    # 3. Online Logistic SGD Weight Refinement & Brier Score Audit
    linear_z = sum(FEATURE_WEIGHTS.get(k, 0.5) * v for k, v in features.items())
    pred_prob = 1.0 / (1.0 + math.exp(-linear_z + 2.5))
    y_actual = 1.0 if observed_accidents > 0 else 0.0
    error = y_actual - pred_prob
    brier = round((pred_prob - y_actual) ** 2, 5)
    state["brier_history"].append(brier)

    updated_weights = {}
    for k, w in FEATURE_WEIGHTS.items():
        x_val = features.get(k, 0.0)
        updated_weights[k] = round(w + learning_rate * error * x_val, 4)

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "subzone_id": subzone_id,
        "prior_rate_per_1k": round(prior_mean * 1000, 2),
        "posterior_rate_per_1k": round(posterior_mean * 1000, 2),
        "updated_ewma_yoy_trend": state["ewma_trend"],
        "brier_calibration_loss": brier,
        "updated_feature_weights": updated_weights
    }


if __name__ == "__main__":
    sample_result = update_engine(
        subzone_id="TPE_PUNGGOL_CORRIDOR",
        observed_accidents=3,
        exposure_windows=20,
        features={"w_rain_hydroplane": 1.0, "w_speed_shear": 1.0, "w_motorcycle_exposure": 1.0}
    )
    print(json.dumps(sample_result, indent=2))
