import numpy as np
import pandas as pd

np.random.seed(42)

N = 1_000_000

customer_tenure_days = np.random.gamma(shape=2.5, scale=180, size=N)
prior_disputes_90d = np.random.poisson(lam=0.3, size=N)
customer_dispute_rate = np.clip(np.random.beta(2, 20, size=N), 0, 1)
transaction_amount = np.random.lognormal(mean=3.5, sigma=1.0, size=N)

merchant_risk_tier = np.random.choice([0, 1, 2], size=N, p=[0.6, 0.3, 0.1])
merchant_dispute_rate = np.clip(np.random.beta(2, 15, size=N), 0, 1)

tx_count_24h = np.random.poisson(lam=1.2, size=N)
time_since_tx_days = np.random.exponential(scale=15, size=N)
is_cross_border = np.random.binomial(1, 0.18, size=N)

fraud_prob = (
    0.15 * (prior_disputes_90d > 1) +
    0.10 * customer_dispute_rate +
    0.20 * (merchant_risk_tier == 2) +
    0.10 * (tx_count_24h > 3) +
    0.15 * is_cross_border +
    0.10 * (transaction_amount > np.percentile(transaction_amount, 80))
)

fraud_prob = np.clip(fraud_prob, 0, 0.9)
is_fraud = np.random.binomial(1, fraud_prob)

df = pd.DataFrame({
    "customer_tenure_days": customer_tenure_days,
    "prior_disputes_90d": prior_disputes_90d,
    "customer_dispute_rate": customer_dispute_rate,
    "transaction_amount": transaction_amount,
    "merchant_risk_tier": merchant_risk_tier,
    "merchant_dispute_rate": merchant_dispute_rate,
    "tx_count_24h": tx_count_24h,
    "time_since_tx_days": time_since_tx_days,
    "is_cross_border": is_cross_border,
    "is_fraud": is_fraud
})

print("Dataset shape:", df.shape)
print("Fraud rate:", df["is_fraud"].mean())

df.to_csv("stripe_disputes_simulated.csv", index=False)
print("CSV saved successfully.")