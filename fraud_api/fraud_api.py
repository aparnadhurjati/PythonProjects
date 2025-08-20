from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from inference import predict_single, predict_batch

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(title="Fraud Detection API")

# -----------------------------
# Request schemas
# -----------------------------
class Transaction(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float

class TransactionsBatch(BaseModel):
    transactions: List[Transaction]

# -----------------------------
# Endpoints
# -----------------------------
@app.post("/predict_one")
def predict_one(tx: Transaction):
    prob = predict_single(tx.dict())
    return {"fraud_probability": prob}


@app.post("/predict_batch")
def predict_many(batch: TransactionsBatch):
    probs = predict_batch([t.dict() for t in batch.transactions])
    return {"fraud_probabilities": probs}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
