import numpy as np
import pandas as pd

from scipy.stats import zscore
from sklearn.ensemble import IsolationForest


def run_isolation_forest(df):

    features = [
        "billed_amount",
        "paid_amount",
        "paid_to_billed_ratio",
        "turnaround_days",
        "patient_age",
    ]

    X = df[features]

    model = IsolationForest(
        n_estimators=200,
        contamination=0.03,
        random_state=42,
    )

    preds = model.fit_predict(X)

    scores = model.decision_function(X)

    df["iforest_prediction"] = preds
    df["iforest_score"] = scores

    df["iforest_anomaly"] = (
        df["iforest_prediction"] == -1
    )

    return df


def detect_zscore(df):

    z = np.abs(zscore(df["billed_amount"]))

    df["zscore"] = z

    df["zscore_anomaly"] = z > 3

    return df


def detect_iqr(df):

    q1 = df["billed_amount"].quantile(0.25)

    q3 = df["billed_amount"].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr

    upper = q3 + 1.5 * iqr

    df["iqr_anomaly"] = (
        (df["billed_amount"] < lower)
        |
        (df["billed_amount"] > upper)
    )

    return df


def detect_duplicate_claims(df):

    duplicate_cols = [
        "patient_id",
        "procedure",
        "service_date",
        "billed_amount",
    ]

    df["duplicate_claim"] = (
        df.duplicated(
            subset=duplicate_cols,
            keep=False,
        )
    )

    return df


def calculate_provider_risk(df):

    provider = (
        df.groupby("provider_name")
        .agg(
            total_claims=("claim_id", "count"),
            denied=("denial_flag", "sum"),
            avg_bill=("billed_amount", "mean"),
            anomalies=("iforest_anomaly", "sum"),
        )
        .reset_index()
    )

    provider["risk_score"] = (
        provider["denied"] * 0.35
        + provider["anomalies"] * 0.45
        + provider["avg_bill"] / 50000
    )

    provider["risk_score"] = (
        provider["risk_score"]
        - provider["risk_score"].min()
    ) / (
        provider["risk_score"].max()
        - provider["risk_score"].min()
    )

    return provider


def apply_all_models(df):

    df = run_isolation_forest(df)

    df = detect_zscore(df)

    df = detect_iqr(df)

    df = detect_duplicate_claims(df)

    provider_risk = calculate_provider_risk(df)

    return df, provider_risk