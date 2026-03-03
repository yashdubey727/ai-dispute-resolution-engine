import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("scored_disputes_test.csv")

MONTHLY_DISPUTES = 8_000_000
MANUAL_REVIEW_COST = 8.0
AVG_FRAUD_LOSS = 110.0
WRONG_REJECT_COST = 5.0

scale_factor = MONTHLY_DISPUTES / len(df)

thresholds = np.arange(0.02, 0.30, 0.005)
t2 = 0.60

rows = []
for t1 in thresholds:
    scores = df["fraud_risk_score"].values
    y = df["is_fraud"].values

    auto_approve = scores < t1
    manual_review = (scores >= t1) & (scores < t2)
    auto_reject = scores >= t2

    automation_rate = 1 - manual_review.mean()

    reviews_avoided = len(df) - manual_review.sum()
    ops_savings = reviews_avoided * MANUAL_REVIEW_COST * scale_factor

    fraud_leak_cost = ((y == 1) & auto_approve).sum() * AVG_FRAUD_LOSS * scale_factor
    wrong_reject_cost = ((y == 0) & auto_reject).sum() * WRONG_REJECT_COST * scale_factor

    net_value = ops_savings - fraud_leak_cost - wrong_reject_cost

    rows.append((t1, automation_rate, ops_savings, fraud_leak_cost, wrong_reject_cost, net_value))

res = pd.DataFrame(rows, columns=[
    "t1", "automation_rate", "ops_savings", "fraud_leak_cost", "wrong_reject_cost", "net_value"
])

best_row = res.loc[res["net_value"].idxmax()]
best_t1 = float(best_row["t1"])
best_net = float(best_row["net_value"])
best_auto = float(best_row["automation_rate"])

# Chart 1: Net value
plt.figure()
plt.plot(res["t1"], res["net_value"])
plt.axvline(best_t1, linestyle="--")
plt.scatter([best_t1], [best_net])
plt.xlabel("Auto-Approve Threshold (t1)")
plt.ylabel("Net Monthly Value (USD)")
plt.title("Net Value vs Auto-Approve Threshold")
plt.savefig("portfolio_net_value.png")
plt.close()

# Chart 2: Automation
plt.figure()
plt.plot(res["t1"], res["automation_rate"])
plt.axvline(best_t1, linestyle="--")
plt.scatter([best_t1], [best_auto])
plt.xlabel("Auto-Approve Threshold (t1)")
plt.ylabel("Automation Rate")
plt.title("Automation Rate vs Auto-Approve Threshold")
plt.savefig("portfolio_automation_rate.png")
plt.close()

print("Saved portfolio_net_value.png and portfolio_automation_rate.png")
print("Best t1:", round(best_t1, 3), "Net:", round(best_net, 2), "Automation:", round(best_auto, 4))