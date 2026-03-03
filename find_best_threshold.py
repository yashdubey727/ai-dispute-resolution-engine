import pandas as pd
import numpy as np

df = pd.read_csv("scored_disputes_test.csv")

MONTHLY_DISPUTES = 8_000_000
MANUAL_REVIEW_COST = 8.0
AVG_FRAUD_LOSS = 110.0
WRONG_REJECT_COST = 5.0

scale_factor = MONTHLY_DISPUTES / len(df)

thresholds = np.arange(0.05, 0.55, 0.01)
t2 = 0.60

best = None

for t1 in thresholds:
    scores = df["fraud_risk_score"].values
    y = df["is_fraud"].values

    auto_approve = scores < t1
    manual_review = (scores >= t1) & (scores < t2)
    auto_reject = scores >= t2

    manual_cases = manual_review.sum()
    reviews_avoided = len(df) - manual_cases
    ops_savings = reviews_avoided * MANUAL_REVIEW_COST * scale_factor

    fraud_leak_cases = ((y == 1) & auto_approve).sum()
    fraud_leak_cost = fraud_leak_cases * AVG_FRAUD_LOSS * scale_factor

    wrong_reject_cases = ((y == 0) & auto_reject).sum()
    wrong_reject_cost = wrong_reject_cases * WRONG_REJECT_COST * scale_factor

    net_value = ops_savings - fraud_leak_cost - wrong_reject_cost
    automation_rate = 1 - manual_review.mean()

    row = (t1, net_value, automation_rate, ops_savings, fraud_leak_cost, wrong_reject_cost)

    if best is None or net_value > best[1]:
        best = row

t1, net_value, automation_rate, ops_savings, fraud_leak_cost, wrong_reject_cost = best

print("Best auto-approve threshold t1:", round(t1, 2))
print("Automation rate:", round(automation_rate, 4))
print("Ops savings monthly USD:", round(ops_savings, 2))
print("Fraud leak cost monthly USD:", round(fraud_leak_cost, 2))
print("Wrong reject cost monthly USD:", round(wrong_reject_cost, 2))
print("Net value monthly USD:", round(net_value, 2))

