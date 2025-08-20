import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from pytorch_tabnet.tab_model import TabNetClassifier
from torch.utils.tensorboard import SummaryWriter
from loaders.kaggle_loader import load_fraud_data
from pytorch_tabnet.tab_model import TabNetClassifier
from torch.utils.tensorboard import SummaryWriter
from loaders.kaggle_loader import load_fraud_data
import joblib
import os
import datetime
import torch

# -----------------------------
# Load dataset
# -----------------------------
# df = pd.read_csv("creditcard.csv")
# df.columns = df.columns.str.strip()  # remove stray spaces

# target_col = "Class"
# X = df.drop(target_col, axis=1).values
# y = df[target_col].values

# # Train/test split
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, stratify=y, random_state=42
# )

# -----------------------------
    # Config
    # -----------------------------
DATASET = "creditcard"      # or "paysim"
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_DIR = f"./tabnet_logs/run_{timestamp}"
MODELS_DIR = "./models"
MAX_EPOCHS = 50
PATIENCE = 10
BATCH_SIZE = 1024
VIRTUAL_BATCH_SIZE = 128

os.makedirs(MODELS_DIR, exist_ok=True)

# Load dataset (Credit Card Fraud or PaySim)
# X_train, X_test, y_train, y_test, feature_names = load_fraud_data(
#     dataset=DATASET,    
#     balance_data=True
# )
X_train, X_test, y_train, y_test, feature_names = load_fraud_data(
        dataset=DATASET, data_dir="data", test_size=0.2, random_state=42, balance_data=False
    )

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save scaler for inference
scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")
joblib.dump(scaler, scaler_path)
# -----------------------------
# TensorBoard setup
# -----------------------------
writer = SummaryWriter(log_dir=LOG_DIR)

if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Using GPU: {torch.cuda.get_device_name()}")
else:
    device = torch.device("cpu")
    print("CUDA not available, using CPU")
# -----------------------------
# TabNet model
# -----------------------------
clf = TabNetClassifier(
    n_d=16, n_a=16, n_steps=5,
    gamma=1.5, n_independent=2, n_shared=2,
    optimizer_params=dict(lr=2e-2),
    mask_type='entmax'
)

# -----------------------------
# Train in ONE call
# -----------------------------
clf.fit(
    X_train, y_train,
    eval_set=[(X_train, y_train), (X_test, y_test)],
    eval_name=['train', 'val'],
    eval_metric=['auc', 'logloss', 'accuracy'],
    max_epochs=MAX_EPOCHS,              # train multiple epochs in one call
    patience=PATIENCE,                # early stopping patience
    batch_size=BATCH_SIZE,
    virtual_batch_size=VIRTUAL_BATCH_SIZE 
)

# -----------------------------
# Log metrics per epoch
# -----------------------------
history = clf.history.history
metrics = ['auc', 'logloss', 'accuracy']

# -----------------------------
# Log metrics per epoch (robust)
# -----------------------------
hist = clf.history.history
metrics = ['auc', 'logloss', 'accuracy']

# Some keys might not exist depending on eval_metric choices; guard with .get
num_epochs = len(hist.get('train_auc', []))
for epoch in range(num_epochs):
    for m in metrics:
        tr_key, va_key = f"train_{m}", f"val_{m}"
        if tr_key in hist:
            writer.add_scalar(f"{m.upper()}/train", hist[tr_key][epoch], epoch)
        if va_key in hist:
            writer.add_scalar(f"{m.UPPER() if hasattr(str, 'UPPER') else m.upper()}/val", hist[va_key][epoch], epoch)
    # Optional: concise console log when AUC is available
    if 'train_auc' in hist and 'val_auc' in hist:
        print(f"Epoch {epoch+1}: AUC train={hist['train_auc'][epoch]:.4f}, val={hist['val_auc'][epoch]:.4f}")

writer.close()

# -----------------------------
# Save best model
# -----------------------------
clf.save_model(f"{MODELS_DIR}/best_tabnet_model")
print("✅ Training complete. Best model saved as 'best_tabnet_model.zip'")

# Save feature names for inference-time ordering checks
joblib.dump(feature_names, os.path.join(MODELS_DIR, "feature_names.pkl"))
