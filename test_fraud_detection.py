from src.data_generator import generate_claims
from src.fraud_detection import apply_all_models

# Generate synthetic claims
df = generate_claims(10000)

# Run fraud detection
df, provider = apply_all_models(df)

print("=" * 50)
print("Claims Data")
print("=" * 50)
print(df.head())

print("\n" + "=" * 50)
print("Provider Risk Scores")
print("=" * 50)
print(provider.head())

print("\n" + "=" * 50)
print("Summary")
print("=" * 50)
print(f"Total Claims: {len(df)}")
print(f"Isolation Forest Anomalies: {df['iforest_anomaly'].sum()}")
print(f"Z-Score Anomalies: {df['zscore_anomaly'].sum()}")
print(f"IQR Anomalies: {df['iqr_anomaly'].sum()}")
print(f"Duplicate Claims: {df['duplicate_claim'].sum()}")
print(f"Injected Fraud Cases : {df['true_fraud'].sum()}")