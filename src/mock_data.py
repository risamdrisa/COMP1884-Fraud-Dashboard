import random
import pandas as pd
from datetime import datetime, timedelta

# --- Weights for composite score ---
WEIGHTS = {
    "transaction_risk": 0.40,
    "account_risk":     0.25,
    "merchant_risk":    0.20,
    "credit_risk":      0.15,
}

def classify_risk(score):
    """Turn a number into a risk label."""
    if score >= 0.75:
        return "high"
    elif score >= 0.40:
        return "medium"
    else:
        return "low"

def mock_score(component, transaction_id):
    """Generate a realistic fake score for a given component."""
    random.seed(hash(transaction_id + component))
    return round(random.uniform(0, 1), 4)

def generate_mock_dataset(n=500):
    """Generate n fake transactions with risk scores."""
    rows = []
    start_time = datetime.utcnow() - timedelta(days=30)

    for i in range(n):
        txn_id = f"TXN-{i:05d}"

        # Get a score for each component
        scores = {k: mock_score(k, txn_id) for k in WEIGHTS}

        # Calculate composite score using weights
        composite = sum(WEIGHTS[k] * scores[k] for k in WEIGHTS)

        # Spread timestamps over last 30 days
        timestamp = start_time + timedelta(minutes=i * 86)

        rows.append({
            "transaction_id":   txn_id,
            "timestamp":        timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_risk": scores["transaction_risk"],
            "account_risk":     scores["account_risk"],
            "merchant_risk":    scores["merchant_risk"],
            "credit_risk":      scores["credit_risk"],
            "composite_risk_score": round(composite, 4),
            "risk_label":       classify_risk(composite),
        })

    return pd.DataFrame(rows)

# Run this file to generate the data
if __name__ == "__main__":
    df = generate_mock_dataset(500)
    df.to_csv("data/processed/risk_scores.csv", index=False)
    print("✅ Done! 500 transactions generated.")
    print(df["risk_label"].value_counts())
    print(f"\nSample data:")
    print(df.head(3))