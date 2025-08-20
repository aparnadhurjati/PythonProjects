import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.model_selection import train_test_split

def load_fraud_data(
    dataset="creditcard",
    data_dir="data",
    test_size=0.2,
    random_state=42,
    balance_data=True
):
    """
    Downloads a fraud detection dataset from Kaggle, splits into train/test,
    and optionally balances the dataset using undersampling.
    
    Returns:
        X_train, X_test, y_train, y_test, feature_names
    """
    api = KaggleApi()
    api.authenticate()

    os.makedirs(data_dir, exist_ok=True)

    # -----------------------------
    # Download datasets
    # -----------------------------
    if dataset == "creditcard":
        print("Downloading Credit Card Fraud dataset...")
        api.dataset_download_files("mlg-ulb/creditcardfraud", path=data_dir, unzip=True)
        file_path = os.path.join(data_dir, "creditcard.csv")
        target_col = "Class"
    elif dataset == "paysim":
        print("Downloading PaySim dataset...")
        api.dataset_download_files("ealaxi/paysim1", path=data_dir, unzip=True)
        file_path = os.path.join(data_dir, "PS_20174392719_1491204439457_log.csv")
        target_col = "isFraud"
    else:
        raise ValueError("Dataset not supported. Choose 'creditcard' or 'paysim'.")

    print(f"Loading data from {file_path} ...")
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()  # remove spaces from column names

    # -----------------------------
    # Features / target
    # -----------------------------
    X = df.drop(target_col, axis=1)
    y = df[target_col]

    feature_names = X.columns.tolist()

    # -----------------------------
    # Optional balancing via undersampling
    # -----------------------------
    if balance_data:
        print("Balancing dataset using undersampling...")
        fraud_idx = y[y == 1].index
        nonfraud_idx = y[y == 0].index
        n_fraud = len(fraud_idx)
        nonfraud_sample_idx = nonfraud_idx.to_series().sample(n=n_fraud, random_state=random_state)
        selected_idx = fraud_idx.union(nonfraud_sample_idx)
        X = X.loc[selected_idx]
        y = y.loc[selected_idx]

    # -----------------------------
    # Train/test split
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    print(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")
    return X_train, X_test, y_train, y_test, feature_names
