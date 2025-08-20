import pandas as pd
import joblib
from pytorch_tabnet.tab_model import TabNetClassifier

# -----------------------------
# Load artifacts once at import
# -----------------------------
MODEL_PATH = "models/best_tabnet_model.zip"
SCALER_PATH = "models/scaler.pkl"
FEATURE_NAMES_PATH = "models/feature_names.pkl"

clf = TabNetClassifier()
clf.load_model(MODEL_PATH)

scaler = joblib.load(SCALER_PATH)
feature_names = joblib.load(FEATURE_NAMES_PATH)


def predict_single(transaction: dict) -> float:
    """
    Predict fraud probability for a single transaction (dict input).
    """
    df = pd.DataFrame([transaction])
    df = df[feature_names]  # enforce correct column order
    X_scaled = scaler.transform(df.values)
    prob = clf.predict_proba(X_scaled)[:, 1][0]
    return float(prob)


def predict_batch(transactions: list[dict]) -> list[float]:
    """
    Predict fraud probability for multiple transactions (list of dicts).
    """
    df = pd.DataFrame(transactions)
    df = df[feature_names]  # enforce correct column order
    X_scaled = scaler.transform(df.values)
    probs = clf.predict_proba(X_scaled)[:, 1]
    return probs.tolist()
