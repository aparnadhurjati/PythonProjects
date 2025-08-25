# Credit Card Fraud Detection with Deep Learning

A PyTorch-based deep learning project for detecting fraudulent credit card transactions using neural networks.

## 🎯 Project Overview

This project implements a deep neural network (`FraudNet`) to classify credit card transactions as legitimate or fraudulent. The model uses a feedforward architecture with dropout regularization to prevent overfitting.

## 🏗️ Architecture

**FraudNet** - A 3-layer feedforward neural network:
- Input layer: Variable dimensions (based on dataset features)
- Hidden layer 1: 64 units with ReLU activation + Dropout(0.5)
- Hidden layer 2: 32 units with ReLU activation + Dropout(0.5)
- Output layer: 1 unit with Sigmoid activation (binary classification)

## 📁 Project Structure

```
DeepLearning/
├── data/
│   └── creditcard.csv          # Credit card transaction dataset
├── logs/                       # TensorBoard log files
├── plots/                      # Generated plots and visualizations
├── venv/                       # Python virtual environment
├── data_loader.py              # Data loading and preprocessing
├── model.py                    # Neural network architecture definition
├── train.py                    # Training script with TensorBoard logging
├── inference.py                # Inference utilities
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create required directories
mkdir -p logs plots data
```

### 2. Download Dataset

The project requires the Credit Card Fraud dataset. You have two options:

**Option A: Manual Download (Recommended)**
1. Go to [Kaggle Credit Card Fraud Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
2. Download `creditcard.csv`
3. Place it in the `data/` directory

**Option B: Using Kaggle CLI (requires Kaggle account)**
```bash
pip install kaggle
# Download kaggle.json from your Kaggle account settings
# Place it in ~/.kaggle/kaggle.json
kaggle datasets download -d mlg-ulb/creditcardfraud -p data --unzip
```

### 3. Training

```bash
# Start training
python train.py
```

The training script will:
- Load and preprocess the credit card dataset
- Train the FraudNet model for 10 epochs
- Log metrics to TensorBoard (loss, AUC)
- Generate confusion matrix visualization
- Save the trained model

### 4. Monitor Training

```bash
# Start TensorBoard
tensorboard --logdir logs --port 6006
```

Open `http://localhost:6006` in your browser to view:
- Training/validation loss curves
- AUC metrics over time
- Model architecture

### 5. Inference

```python
from inference import load_model_for_inference, infer_proba

# Load trained model
model = load_model_for_inference("FraudNet.pth", input_dim=30)

# Make predictions
probabilities = infer_proba(model, features)
```

## 📊 Model Performance

The model is evaluated using:
- **Binary Cross-Entropy Loss**: Training objective
- **AUC (Area Under ROC Curve)**: Primary metric for imbalanced datasets
- **Confusion Matrix**: Detailed classification performance

## 🔧 Configuration

### Training Parameters
- **Epochs**: 10 (configurable in `train.py`)
- **Learning Rate**: 1e-3 (Adam optimizer)
- **Batch Size**: 512
- **Loss Function**: Binary Cross-Entropy

### Model Hyperparameters
- **Dropout Rate**: 0.5 (both hidden layers)
- **Hidden Layer Sizes**: [64, 32]
- **Activation**: ReLU (hidden), Sigmoid (output)

## 📈 Key Features

- **TensorBoard Integration**: Real-time training monitoring
- **Automatic Model Saving**: Checkpoint management
- **Confusion Matrix Visualization**: Performance analysis
- **GPU Support**: Automatic CUDA detection and usage
- **Modular Design**: Separate data loading, model, and training components

## 🛠️ Dependencies

- **PyTorch**: Deep learning framework
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation
- **Scikit-learn**: Metrics and evaluation
- **Matplotlib/Seaborn**: Visualization
- **TensorBoard**: Training monitoring

## 📝 Usage Examples

### Custom Training

```python
from train import train_model
from data_loader import load_data
from model import FraudNet

# Load data
train_ds, test_ds, input_dim, y_test = load_data()

# Create model and train
model = FraudNet(input_dim)
train_model(model, train_loader, test_loader, y_test, epochs=20, lr=1e-4)
```

### Model Evaluation

```python
from sklearn.metrics import classification_report

# Get predictions
y_pred = (probabilities >= 0.5).astype(int)

# Detailed classification report
print(classification_report(y_test, y_pred))
```

## 🔍 Data Format

The model expects input features as:
- **Shape**: `(batch_size, input_dim)`
- **Type**: `torch.float32`
- **Preprocessing**: Same scaling/normalization as training data

## 📊 Output

- **Probabilities**: Raw sigmoid outputs in [0, 1] range
- **Predictions**: Binary labels (0: legitimate, 1: fraud) using 0.5 threshold
- **Confidence**: Higher probability indicates stronger fraud prediction

## 🚨 Important Notes

- **Class Imbalance**: Credit card fraud datasets are typically highly imbalanced
- **Threshold Tuning**: Default 0.5 threshold may not be optimal for your use case
- **Data Preprocessing**: Ensure test data uses same preprocessing as training
- **Model Persistence**: Models are saved as `.pth` files (PyTorch state_dict format)



## 📄 License

This project is for educational purposes. Please ensure compliance with your dataset's license terms.


### Getting Help

- Check the logs in the `logs/` directory
- Verify all dependencies are installed correctly
- Ensure your dataset format matches expectations

---

**Happy Training! 🚀**
