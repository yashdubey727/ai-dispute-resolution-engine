import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.linear_model import LogisticRegression

DATA_PATH = "stripe_disputes_simulated.csv"

df = pd.read_csv(DATA_PATH)

target = "is_fraud"
X = df.drop(columns=[target])
y = df[target]

numeric_features = [
    "customer_tenure_days",
    "prior_disputes_90d",
    "customer_dispute_rate",
    "transaction_amount",
    "merchant_dispute_rate",
    "tx_count_24h",
    "time_since_tx_days",
    "is_cross_border",
]

categorical_features = ["merchant_risk_tier"]

preprocess = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

clf = Pipeline(
    steps=[
        ("preprocess", preprocess),
        ("model", LogisticRegression(max_iter=200)),
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

clf.fit(X_train, y_train)

probs = clf.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, probs)

print("ROC AUC:", round(auc, 4))

preds = (probs >= 0.5).astype(int)
print("\nClassification report at threshold 0.5:\n")
print(classification_report(y_test, preds, digits=4))

out = X_test.copy()
out["is_fraud"] = y_test.values
out["fraud_risk_score"] = probs
out.to_csv("scored_disputes_test.csv", index=False)

print("\nSaved scored_disputes_test.csv")   

import pandas as pd

df1 = pd.read_csv("stripe_disputes_simulated.csv")
df1.to_excel("stripe_disputes_simulated.xlsx", index=False)

df2 = pd.read_csv("scored_disputes_test.csv")
df2.to_excel("scored_disputes_test.xlsx", index=False)
print("hello")