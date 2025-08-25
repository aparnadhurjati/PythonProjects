import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import TensorDataset
import torch
import os
import matplotlib.pyplot as plt
import seaborn as sns

data_dir = "data"

def load_data():
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, "creditcard.csv")
    
    # Check if dataset exists, if not provide instructions
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Dataset not found at {file_path}. "
            "Please download the Credit Card Fraud dataset from Kaggle "
            "and place 'creditcard.csv' in the 'data/' directory. "
            "Dataset: mlg-ulb/creditcardfraud"
        )

    df = pd.read_csv(file_path)
    classDistVisual(df)
    featureDistVisual(df)
    X = df.drop("Class", axis=1)
    y = df["Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    train_ds = TensorDataset(
        torch.tensor(X_train, dtype=torch.float32),
        torch.tensor(y_train.values, dtype=torch.float32)
    )
    test_ds = TensorDataset(
        torch.tensor(X_test, dtype=torch.float32),
        torch.tensor(y_test.values, dtype=torch.float32)
    )

    return train_ds, test_ds, X_train.shape[1], y_test

def classDistVisual(df: pd.DataFrame):


    sns.countplot(x='Class', data=df)
    plt.title("Fraud vs Non-Fraud Transactions")
    plt.savefig("plots/classdist.png", bbox_inches="tight"); plt.close()

def featureDistVisual(df: pd.DataFrame):
    plt.figure(figsize=(10,8))
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, cmap="coolwarm", center=0)
    plt.title("Feature correlation"); 
    plt.savefig("plots/featuredist.png", bbox_inches="tight"); plt.close()
