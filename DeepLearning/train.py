from pandas._libs.tslibs.offsets import YearBegin
from scipy import test
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import  DataLoader
from data_loader import load_data
from sklearn.metrics import roc_auc_score
from model import FraudNet
import torch.utils.tensorboard as tb
import datetime
from model import save_model
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np

def plotLossCurve(train_losses, val_losses):
    plt.figure()
    plt.plot(train_losses, label="train")
    plt.plot(val_losses, label="val")
    plt.xlabel("Epoch"); plt.ylabel("Loss"); plt.legend(); plt.title("Loss")
    plt.savefig("plots/losscurve.png", bbox_inches="tight"); plt.close()

def confusion_matrix_visual(y_pred_probs, y_test):
    y_pred_probs = np.asarray(y_pred_probs, dtype=np.float32)
    y_test = np.asarray(y_test)
    y_pred_labels = (y_pred_probs >= 0.5).astype(int)  # Convert probabilities to class labels
    cm = confusion_matrix(y_test, y_pred_labels)

    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.savefig("plots/confusionmatrix.png", bbox_inches="tight"); plt.close()

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_DIR = f"./logs/run_{timestamp}"

# ------------------------
# Training function
# ------------------------
def train_model(model, train_loader, test_loader, y_test, epochs=10, lr=1e-3):
    from os import path
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model = model.to(device)

    train_logger = tb.SummaryWriter(path.join(LOG_DIR, 'train'), flush_secs=1)
    test_logger = tb.SummaryWriter(path.join(LOG_DIR, 'test'), flush_secs=1)

    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    train_loss = []
    test_loss = []

    for epoch in range(epochs):
        model.train()
        train_preds = []
        train_labels = []
        for xb, yb in train_loader:
            preds = model(xb).squeeze()
            loss = criterion(preds, yb)
            train_loss.append(loss.item())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_preds.extend(preds.detach().numpy())
            train_labels.extend(yb.numpy())
        train_logger.add_scalar("loss", sum(train_loss)/len(train_loss), global_step=epoch)
        train_auc = roc_auc_score(train_labels, train_preds)
        train_logger.add_scalar("auc", train_auc, global_step=epoch)  
        # Validation AUC
        model.eval()
        with torch.no_grad():
            y_pred = []
            for xb, yb in test_loader:
                preds=model(xb).squeeze()
                y_pred.extend(model(xb).squeeze().numpy())
                loss = criterion(preds, yb)
                test_loss.append(loss.item())
                
        auc = roc_auc_score(y_test, y_pred)
        if epoch==8:
            confusion_matrix_visual(y_pred, y_test)
        test_logger.add_scalar("auc", auc, global_step=epoch)
        test_logger.add_scalar("loss", sum(test_loss)/len(test_loss), global_step=epoch)
        
        print(f"Epoch {epoch+1}/{epochs} - Test AUC: {auc:.4f}")
    

def main():
    train_ds, test_ds, input_dim, y_test = load_data()
    train_loader = DataLoader(train_ds, batch_size=512, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=512, shuffle=False)

    model = FraudNet(input_dim)
    train_model(model, train_loader, test_loader, y_test, epochs=10, lr=1e-3)
    save_model(model)


if __name__ == "__main__":
    main()

