import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load scored test data
df = pd.read_csv("scored_disputes_test.csv")

# Stripe-scale assumptions
MONTHLY_DISPUTES = 8_000_000
MANUAL_REVIEW_COST = 8.0
AVG_FRAUD_LOSS = 110.0
WRONG_REJECT_COST = 5.0

sample_size = len(df)
scale_factor = MONTHLY_DISPUTES / sample_size

thresholds = np.arange(0.05, 0.55, 0.02)
t2 = 0.60  # reject threshold

net_values = []
automation_rates = []

for t1 in thresholds:
    scores = df["fraud_risk_score"].values
    y = df["is_fraud"].values

    auto_approve = scores < t1
    manual_review = (scores >= t1) & (scores < t2)
    auto_reject = scores >= t2

    manual_rate = manual_review.mean()
    automation_rate = 1 - manual_rate

    manual_cases = manual_review.sum()
    baseline_manual = sample_size
    reviews_avoided = baseline_manual - manual_cases
    ops_savings = reviews_avoided * MANUAL_REVIEW_COST * scale_factor

    fraud_leak_cases = ((y == 1) & auto_approve).sum()
    fraud_leak_cost = fraud_leak_cases * AVG_FRAUD_LOSS * scale_factor

    wrong_reject_cases = ((y == 0) & auto_reject).sum()
    wrong_reject_cost = wrong_reject_cases * WRONG_REJECT_COST * scale_factor

    net_value = ops_savings - fraud_leak_cost - wrong_reject_cost

    net_values.append(net_value)
    automation_rates.append(automation_rate)

# Plot Net Value
plt.figure()
plt.plot(thresholds, net_values)
plt.xlabel("Auto-Approve Threshold")
plt.ylabel("Net Monthly Value (USD)")
plt.title("Threshold vs Net Monthly Value")
plt.savefig("threshold_vs_net_value.png")
plt.close()

# Plot Automation Rate
plt.figure()
plt.plot(thresholds, automation_rates)
plt.xlabel("Auto-Approve Threshold")
plt.ylabel("Automation Rate")
plt.title("Threshold vs Automation Rate")
plt.savefig("threshold_vs_automation.png")
plt.close()

print("Charts saved:")
print("threshold_vs_net_value.png")
print("threshold_vs_automation.png")
