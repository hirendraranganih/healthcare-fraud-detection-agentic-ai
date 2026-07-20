import random

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()

PROVIDERS = [
    "Apollo Hospital",
    "Fortis Healthcare",
    "Max Healthcare",
    "Manipal Hospital",
    "AIIMS Delhi",
    "Narayana Health",
    "Medanta",
    "KIMS Hospital",
    "Aster Hospital",
    "Care Hospital",
]

SPECIALITIES = [
    "Cardiology",
    "Orthopedics",
    "Neurology",
    "Oncology",
    "General Medicine",
    "ENT",
    "Pediatrics",
    "Urology",
]

CLAIM_TYPES = [
    "Inpatient",
    "Outpatient",
    "Emergency",
    "Pharmacy",
]

REGIONS = [
    "North",
    "South",
    "East",
    "West",
]

NETWORK = [
    "In-Network",
    "Out-of-Network",
]

DENIAL_REASONS = [
    "None",
    "Duplicate Claim",
    "Missing Documents",
    "Policy Expired",
    "Coding Error",
    "Medical Necessity",
]

DIAGNOSIS = [
    "Hypertension",
    "Diabetes",
    "Heart Disease",
    "Fracture",
    "COVID-19",
    "Cancer",
    "Asthma",
]

PROCEDURES = [
    "MRI",
    "CT Scan",
    "X-Ray",
    "Surgery",
    "Blood Test",
    "ECG",
    "Physiotherapy",
]


def generate_claims(n=10000, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    records = []

    for i in range(n):

        billed = np.random.gamma(5, 8000)

        ratio = np.random.uniform(0.65, 1.00)

        paid = billed * ratio

        denial = np.random.choice(
            [0, 1],
            p=[0.85, 0.15]
        )

        denial_reason = (
            "None"
            if denial == 0
            else random.choice(DENIAL_REASONS[1:])
        )

        turnaround = np.random.randint(1, 30)

        service_date = fake.date_between(
            start_date="-365d",
            end_date="today"
        )

        records.append({

            "claim_id": f"C{i+1:06d}",

            "patient_id": fake.uuid4()[:10],

            "provider_name": random.choice(PROVIDERS),

            "provider_speciality": random.choice(SPECIALITIES),

            "claim_type": random.choice(CLAIM_TYPES),

            "region": random.choice(REGIONS),

            "network_type": random.choice(NETWORK),

            "diagnosis": random.choice(DIAGNOSIS),

            "procedure": random.choice(PROCEDURES),

            "patient_age": np.random.randint(1, 90),

            "service_date": service_date,

            "billed_amount": round(billed, 2),

            "paid_amount": round(paid, 2),

            "paid_to_billed_ratio": round(ratio, 2),

            "claim_status": (
                "Denied"
                if denial
                else random.choice(
                    ["Approved", "Pending"]
                )
            ),

            "denial_flag": denial,

            "denial_reason": denial_reason,

            "turnaround_days": turnaround,

            "over_sla_flag": int(turnaround > 15),

            "true_fraud": 0,

        })

    df = pd.DataFrame(records)

    # =====================================================
    # Inject Fraud Cases (5%)
    # =====================================================

    fraud_count = int(len(df) * 0.05)

    fraud_indices = np.random.choice(
        df.index,
        fraud_count,
        replace=False
    )

    # Mark fraud
    df.loc[fraud_indices, "true_fraud"] = 1

    # Inflate billed amount
    multipliers = np.random.uniform(
        2.5,
        5.0,
        fraud_count
    )

    df.loc[fraud_indices, "billed_amount"] = (
        df.loc[fraud_indices, "billed_amount"] * multipliers
    ).round(2)

    # Almost fully paid suspicious claims
    ratios = np.random.uniform(
        0.95,
        1.00,
        fraud_count
    )

    df.loc[fraud_indices, "paid_to_billed_ratio"] = ratios

    df.loc[fraud_indices, "paid_amount"] = (
        df.loc[fraud_indices, "billed_amount"] * ratios
    ).round(2)

    # Long turnaround
    df.loc[
        fraud_indices,
        "turnaround_days"
    ] = np.random.randint(
        25,
        45,
        fraud_count
    )

    # Assign fraud mostly to selected providers
    high_risk = [
        "Apollo Hospital",
        "Fortis Healthcare"
    ]

    df.loc[
        fraud_indices,
        "provider_name"
    ] = np.random.choice(
        high_risk,
        fraud_count
    )

    # =====================================================
    # Create realistic duplicate claims (~1%)
    # =====================================================

    duplicate_count = int(len(df) * 0.01)

    duplicate_rows = df.loc[
        np.random.choice(
            df.index,
            duplicate_count,
            replace=False
        )
    ].copy()

    duplicate_rows["claim_id"] = [
        f"DUP{i+1:06d}"
        for i in range(duplicate_count)
    ]

    duplicate_rows["true_fraud"] = 1

    df = pd.concat(
        [df, duplicate_rows],
        ignore_index=True
    )

    return df