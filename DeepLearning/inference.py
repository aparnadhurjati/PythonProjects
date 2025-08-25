import torch
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from model import FraudNet  # ensure this matches your model class

def load_model_for_inference(pth_path: str, input_dim: int, device: str = "cpu") -> torch.nn.Module:
    model = FraudNet(input_dim)
    state = torch.load(pth_path, map_location=device)
    model.load_state_dict(state)
    model.to(device)
    model.eval()
    return model

def infer_proba(model: torch.nn.Module, features, device: str = "cpu", batch_size: int = 1024) -> np.ndarray:
    if isinstance(features, np.ndarray):
        X = torch.from_numpy(features).float()
    elif torch.is_tensor(features):
        X = features.float()
    else:
        raise TypeError("features must be a NumPy array or a torch.Tensor")

    dl = DataLoader(TensorDataset(X), batch_size=batch_size, shuffle=False)
    probs = []
    with torch.no_grad():
        for (xb,) in dl:
            xb = xb.to(device)
            p = model(xb).squeeze(1)  # model outputs sigmoid probs
            probs.append(p.cpu())
    return torch.cat(probs).numpy()

def infer_label(model: torch.nn.Module, features, threshold: float = 0.5, **kwargs) -> np.ndarray:
    probs = infer_proba(model, features, **kwargs)
    return (probs >= threshold).astype(np.int64)



def main():


    X = np.array([
        [ 0.12, -1.45,  0.33,  0.08, -0.57,  0.14,  0.72, -0.21,  0.05, -0.11,
        -0.36,  0.49,  0.27, -0.09,  0.63, -0.44,  0.18,  0.07, -0.52,  0.31,
        0.22, -0.28,  0.16,  0.04, -0.19,  0.12, -0.06,  0.25,  0.10,  0.15],
        [ -0.05,  0.22, -0.91,  0.41,  0.18, -0.34,  0.09,  0.56, -0.27,  0.12,
        0.38, -0.14,  0.21,  0.47, -0.08,  0.30, -0.17,  0.52,  0.11, -0.33,
        0.29,  0.06, -0.25,  0.19,  0.03, -0.22,  0.44, -0.10,  0.20,  0.05]
    ], dtype=np.float32)
    model = load_model_for_inference("FraudNet.pth", input_dim=X.shape[1], device="cpu")
    probs = infer_proba(model, X)            # returns probabilities in [0,1]
    preds = infer_label(model, X, 0.5)       # returns 0/1 labels
    print(probs, preds)


if __name__ == "__main__":
    main()