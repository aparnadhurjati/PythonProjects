# Fraud Detection API

A machine learning-powered API for real-time fraud detection using TabNet neural networks. This project provides both single transaction and batch prediction endpoints for detecting fraudulent transactions.

## 🚀 Features

- **Real-time fraud detection** using TabNet deep learning model
- **FastAPI-based REST API** with automatic documentation
- **Single and batch prediction** endpoints
- **Pre-trained on credit card fraud data** from Kaggle
- **Automatic data downloading** and preprocessing
- **TensorBoard integration** for training monitoring
- **Scalable architecture** ready for production deployment

## 📁 Project Structure

```
fraud_api/
├── fraud_api.py           # FastAPI application with prediction endpoints
├── train_tabnet.py        # Model training script with TabNet
├── inference.py           # Model loading and prediction functions
├── requirements.txt       # Python dependencies
├── loaders/
│   └── kaggle_loader.py  # Data loading utilities from Kaggle
├── data/                 # Data directory (ignored in git)
├── models/               # Trained models directory (ignored in git)
└── tabnet_logs/          # Training logs (ignored in git)
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Kaggle API credentials (for data download)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fraud_api
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Kaggle API**
   ```bash
   # Download kaggle.json from your Kaggle account settings
   mkdir ~/.kaggle
   mv kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

## 🏃‍♂️ Quick Start

### 1. Train the Model

Train a TabNet model on credit card fraud data:

```bash
python train_tabnet.py
```

This will:
- Download the Credit Card Fraud dataset from Kaggle
- Preprocess and split the data
- Train a TabNet classifier
- Save the trained model, scaler, and feature names to `models/`
- Log training metrics to TensorBoard

**Monitor training with TensorBoard:**
```bash
tensorboard --logdir=tabnet_logs
```

### 2. Start the API Server

```bash
python fraud_api.py
```

The API will be available at `http://localhost:8000`

### 3. View API Documentation

Navigate to `http://localhost:8000/docs` for interactive API documentation.

## 📡 API Endpoints

### Single Transaction Prediction

**POST** `/predict_one`

Predict fraud probability for a single transaction.

**Request Body:**
```json
{
  "Time": 123456,
  "V1": -0.5,
  "V2": 0.1,
  "V3": 0.05,
  "V4": -0.2,
  "V5": 0.01,
  "V6": 0.03,
  "V7": -0.1,
  "V8": 0.2,
  "V9": 0.0,
  "V10": -0.05,
  "V11": 0.04,
  "V12": 0.02,
  "V13": -0.01,
  "V14": 0.03,
  "V15": -0.02,
  "V16": 0.0,
  "V17": 0.01,
  "V18": -0.03,
  "V19": 0.0,
  "V20": 0.02,
  "V21": 0.01,
  "V22": -0.01,
  "V23": 0.0,
  "V24": 0.01,
  "V25": -0.02,
  "V26": 0.0,
  "V27": 0.03,
  "V28": 0.01,
  "Amount": 120.5
}
```

**Response:**
```json
{
  "fraud_probability": 0.0234
}
```

### Batch Transaction Prediction

**POST** `/predict_batch`

Predict fraud probabilities for multiple transactions.

**Request Body:**
```json
{
  "transactions": [
    {
      "Time": 123456,
      "V1": -0.5,
      // ... other features
      "Amount": 120.5
    },
    {
      "Time": 123457,
      "V1": -0.3,
      // ... other features
      "Amount": 89.2
    }
  ]
}
```

**Response:**
```json
{
  "fraud_probabilities": [0.0234, 0.8901]
}
```

## 🧠 Model Architecture

The project uses **TabNet**, a state-of-the-art deep learning architecture specifically designed for tabular data:

- **Attention-based feature selection**
- **Sequential decision-making process**
- **Interpretable feature importance**
- **Built-in regularization**

### Model Configuration

```python
TabNetClassifier(
    n_d=16,              # Width of decision prediction layer
    n_a=16,              # Width of attention embedding
    n_steps=5,           # Number of successive steps
    gamma=1.5,           # Coefficient for feature reusage
    n_independent=2,     # Number of independent GLU layers
    n_shared=2,          # Number of shared GLU layers
    optimizer_params=dict(lr=2e-2),
    mask_type='entmax'   # Attention mechanism
)
```

## 📊 Dataset

The model is trained on the **Credit Card Fraud Detection** dataset from Kaggle:

- **284,807 transactions** with 492 frauds (0.172% fraud rate)
- **30 features** including:
  - `Time`: Seconds elapsed between transaction and first transaction
  - `V1-V28`: PCA-transformed features (anonymized)
  - `Amount`: Transaction amount
  - `Class`: Target variable (0 = Normal, 1 = Fraud)

## 🔧 Configuration

### Training Parameters

Edit `train_tabnet.py` to modify training configuration:

```python
DATASET = "creditcard"          # Dataset type
MAX_EPOCHS = 50                 # Maximum training epochs
PATIENCE = 10                   # Early stopping patience
BATCH_SIZE = 1024              # Training batch size
VIRTUAL_BATCH_SIZE = 128       # TabNet virtual batch size
```

### Model Artifacts

After training, the following files are saved to `models/`:

- `best_tabnet_model.zip` - Trained TabNet model
- `scaler.pkl` - StandardScaler for feature normalization
- `feature_names.pkl` - Feature names for correct ordering

## 🧪 Testing

Test the API using the provided sample input:

### Option 1: Interactive Swagger UI (Recommended for beginners)

1. **Start the API server**
   ```bash
   python fraud_api.py
   ```

2. **Open your browser and navigate to** `http://localhost:8000/docs`

3. **Test the endpoints interactively:**
   - Expand the `/predict_one` endpoint
   - Click "Try it out"
   - Use the sample JSON data below
   - Click "Execute"

   **Sample JSON for single prediction:**
   ```json
   {
     "Time": 123456,
     "V1": -0.5,
     "V2": 0.1,
     "V3": 0.05,
     "V4": -0.2,
     "V5": 0.01,
     "V6": 0.03,
     "V7": -0.1,
     "V8": 0.2,
     "V9": 0.0,
     "V10": -0.05,
     "V11": 0.04,
     "V12": 0.02,
     "V13": -0.01,
     "V14": 0.03,
     "V15": -0.02,
     "V16": 0.0,
     "V17": 0.01,
     "V18": -0.03,
     "V19": 0.0,
     "V20": 0.02,
     "V21": 0.01,
     "V22": -0.01,
     "V23": 0.0,
     "V24": 0.01,
     "V25": -0.02,
     "V26": 0.0,
     "V27": 0.03,
     "V28": 0.01,
     "Amount": 120.5
   }
   ```

### Option 2: Command Line (curl)

1. **Start the API server**
   ```bash
   python fraud_api.py
   ```

2. **In another terminal, test with curl**

   **Batch prediction:**
   ```bash
   curl -X POST "http://localhost:8000/predict_batch" \
        -H "Content-Type: application/json" \
        -d '{
          "transactions": [
            {
              "Time": 123456,
              "V1": -0.5,
              "V2": 0.1,
              "V3": 0.05,
              "V4": -0.2,
              "V5": 0.01,
              "V6": 0.03,
              "V7": -0.1,
              "V8": 0.2,
              "V9": 0.0,
              "V10": -0.05,
              "V11": 0.04,
              "V12": 0.02,
              "V13": -0.01,
              "V14": 0.03,
              "V15": -0.02,
              "V16": 0.0,
              "V17": 0.01,
              "V18": -0.03,
              "V19": 0.0,
              "V20": 0.02,
              "V21": 0.01,
              "V22": -0.01,
              "V23": 0.0,
              "V24": 0.01,
              "V25": -0.02,
              "V26": 0.0,
              "V27": 0.03,
              "V28": 0.01,
              "Amount": 120.5
            }
          ]
        }'
   ```

   **Single prediction:**
   ```bash
   curl -X POST "http://localhost:8000/predict_one" \
        -H "Content-Type: application/json" \
        -d '{
          "Time": 123456,
          "V1": -0.5,
          "V2": 0.1,
          "V3": 0.05,
          "V4": -0.2,
          "V5": 0.01,
          "V6": 0.03,
          "V7": -0.1,
          "V8": 0.2,
          "V9": 0.0,
          "V10": -0.05,
          "V11": 0.04,
          "V12": 0.02,
          "V13": -0.01,
          "V14": 0.03,
          "V15": -0.02,
          "V16": 0.0,
          "V17": 0.01,
          "V18": -0.03,
          "V19": 0.0,
          "V20": 0.02,
          "V21": 0.01,
          "V22": -0.01,
          "V23": 0.0,
          "V24": 0.01,
          "V25": -0.02,
          "V26": 0.0,
          "V27": 0.03,
          "V28": 0.01,
          "Amount": 120.5
        }'
   ```

## 📈 Performance Monitoring

The training script logs metrics to TensorBoard:

- **AUC** (Area Under Curve)
- **Log Loss**
- **Accuracy**

View training progress:
```bash
tensorboard --logdir=tabnet_logs --port=6006
```

## 🚀 Deployment

### Local Development

For development and testing, simply run:

```bash
python fraud_api.py
```

The API will be available at `http://localhost:8000`

### Production Deployment

For production use, consider these improvements:

- **WSGI Server**: Use a production server like **Gunicorn** instead of the built-in uvicorn
- **Security**: Implement **rate limiting**, **authentication**, and **input validation**
- **Monitoring**: Set up **logging**, **error handling**, and **performance monitoring**
- **Scalability**: Consider **load balancing** and **containerization** (Docker)

### Docker (Optional)

Advanced users can containerize the application:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "fraud_api.py"]
```

Build and run:
```bash
docker build -t fraud-api .
docker run -p 8000:8000 fraud-api
```


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TabNet**: [TabNet: Attentive Interpretable Tabular Learning](https://arxiv.org/abs/1908.07442)
- **Dataset**: [Credit Card Fraud Detection](https://www.kaggle.com/mlg-ulb/creditcardfraud) on Kaggle
- **FastAPI**: Modern, fast web framework for building APIs



---

**Note**: This project is for educational and research purposes. For production fraud detection systems, additional security measures, compliance checks, and thorough testing are required.
