import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI Dispute Resolution Engine", layout="wide")

df = pd.read_csv("scored_disputes_test.csv")

MONTHLY_DISPUTES = 8_000_000
MANUAL_REVIEW_COST = 8.0
AVG_FRAUD_LOSS = 110.0
WRONG_REJECT_COST = 5.0
scale_factor = MONTHLY_DISPUTES / len(df)

st.title("AI Dispute Resolution Engine")
st.markdown("### Executive Threshold Simulator")

st.markdown(
"""
Adjust the auto-approve threshold to balance automation, fraud containment, and economic impact.
"""
)

st.markdown("---")

t1 = st.slider("Auto-Approve Threshold (t1)", 0.01, 0.20, 0.055, 0.005)
t2 = 0.60

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

annual_value = net_value * 12

col1, col2, col3, col4 = st.columns(4)

col1.metric("Automation Rate", f"{automation_rate*100:.2f}%")
col2.metric("Operational Savings (Monthly)", f"${ops_savings:,.0f}")
col3.metric("Fraud Leakage (Monthly)", f"${fraud_leak_cost:,.0f}")
col4.metric("Net Value (Monthly)", f"${net_value:,.0f}")

st.markdown("---")

st.subheader("Annualized Impact")

st.metric("Net Value (Annualized)", f"${annual_value:,.0f}")

st.markdown("---")

st.caption(
"Assumptions: 8M monthly disputes | $8 manual review cost | $110 average fraud loss | $5 wrong reject proxy."
)