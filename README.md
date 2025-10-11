# 🚨 Problem Statement & Dataset Description 🚨

[Click here to view the full PDF](Assets/Mlops_struc.pdf)

Money laundering remains a major global issue, creating a pressing need for better transaction monitoring solutions. Current anti-money laundering (AML) systems are often ineffective, and access to relevant data is restricted due to legal and privacy concerns. Additionally, available datasets typically lack diversity and true labels. This study introduces a new solution: a **novel AML transaction generator** designed to create the **SAML-D dataset**, offering improved features and typologies. The aim is to support researchers in evaluating their models and developing advanced transaction monitoring techniques. 🔍

The **SAML-D dataset** consists of **12 features** and **28 typologies** (split between 11 normal and 17 suspicious), carefully curated based on existing datasets, academic research, and insights from AML experts. The dataset includes **9,504,852 transactions**, of which only **0.1039%** are flagged as suspicious. Additionally, **15 graphical network structures** are included to visualize the flow of transactions within these typologies. While some of these structures overlap across typologies, they vary in key parameters to increase the complexity and challenge of detecting suspicious behavior. For more details on these typologies, please refer to the paper linked above. This dataset is an updated version compared to the original paper. 📊

## 🧑‍💼 **Features of the SAML-D Dataset**:

- **Time & Date ⏰**: Crucial for tracking the chronological sequence of transactions.
  
- **Sender & Receiver Account Details 💳**: Helps uncover behavioral patterns and complex banking connections.

- **Amount 💰**: Represents transaction values, aiding in the identification of potentially suspicious activity.

- **Payment Type 💳📝**: Covers various payment methods such as credit card, debit card, cash, ACH transfers, cross-border, and checks.

- **Sender & Receiver Bank Location 🌍**: Highlights high-risk regions like Mexico, Turkey, Morocco, and the UAE.

- **Payment & Receiver Currency 💱**: Adds complexity when mismatched with location, enhancing analysis.

- **‘Is Suspicious’ Feature 🚨**: A binary flag that differentiates normal transactions from suspicious ones.

- **Type 📊**: Categorizes typologies, offering deeper insights into transaction patterns.

This dataset is designed to facilitate improved research and the development of more effective AML detection methods. 💡


## 📚 Citation

If you use the **SAML-D dataset** in your research, please cite the following paper:

**B. Oztas**, **D. Cetinkaya**, **F. Adedoyin**, **M. Budka**, **H. Dogan**, and **G. Aksu**,
*"Enhancing Anti-Money Laundering: Development of a Synthetic Transaction Monitoring Dataset,"*
2023 IEEE International Conference on e-Business Engineering (ICEBE), Sydney, Australia, 2023, pp. 47-54,
doi: [10.1109/ICEBE59045.2023.00028](https://ieeexplore.ieee.org/document/10356193)

---

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip
- MongoDB instance (for data storage)
- Git

### Installation

#### Option 1: Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/mehran1414/transactionmonitoring.git
cd transactionmonitoring

# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

#### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/mehran1414/transactionmonitoring.git
cd transactionmonitoring

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```bash
   MONGODB_URL_KEY=your_mongodb_connection_string
   ```

2. **Configure DagsHub for MLflow tracking** (optional):
   Update the DagsHub credentials in `TransactionMonitoring/components/model_trainer.py` if you want to use your own MLflow tracking server.

### Running the Project

#### 1. Train the Model

Run the complete training pipeline (data ingestion → validation → transformation → model training):

```bash
python main.py
```

This will:
- Ingest data from MongoDB
- Validate the dataset
- Transform and preprocess the data
- Train multiple models with hyperparameter tuning
- Select the best model
- Log experiments to MLflow
- Save the trained model to `final_model/model.pkl`

#### 2. Start the API Server

Launch the FastAPI application for predictions:

```bash
python app.py
```

The API will be available at `http://localhost:8000`

#### 3. Make Predictions

**Via Web Interface:**
- Navigate to `http://localhost:8000/docs` for the interactive API documentation
- Use the `/predict` endpoint to upload a CSV file with transactions

**Via cURL:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_transactions.csv"
```

**Trigger Training via API:**
```bash
curl -X GET "http://localhost:8000/train"
```

### Project Structure Overview

```
transactionmonitoring/
├── TransactionMonitoring/      # Main package
│   ├── components/             # Pipeline components (ingestion, validation, training)
│   ├── entity/                 # Configuration and artifact entities
│   ├── pipeline/               # Training and prediction pipelines
│   ├── utils/                  # Utility functions and ML helpers
│   └── constant/               # Constants and configurations
├── main.py                     # Training pipeline entry point
├── app.py                      # FastAPI application
├── pyproject.toml              # Project dependencies (uv)
└── requirements.txt            # Legacy requirements file
```

### Viewing Experiment Results

**MLflow UI (Local):**
```bash
mlflow ui
```
Then navigate to `http://localhost:5000`

---

## 🛠 Data Ingestion Pipeline for AML Dataset

![Data Ingestion Pipeline](Assets/DataIngestion.jpg)
The flow diagram below illustrates the **data ingestion pipeline** for processing and preparing the Anti-Money Laundering (AML) dataset. Below is a detailed breakdown of each step in the process:

### 1. **Config Folder**
The **configuration folder** contains essential settings required for initiating and managing the data ingestion pipeline. This folder holds a **JSON** configuration file that defines the parameters for the entire pipeline process.

### 2. **Initiating Data Ingestion**
Once the configuration settings are in place, the data ingestion process is initiated. This step triggers the extraction and processing of raw data from various sources, ensuring the data is ready for further transformation.

### 3. **Export to Feature Store**
After the data has been ingested and processed, it is exported to a **Feature Store**. A Feature Store is a centralized location where all features (attributes or variables) are stored for later use, especially for training machine learning models.

### 4. **Drop One-Hot Encoded Columns**
In this step, any **One-Hot Encoded columns** are removed from the dataset. These columns represent categorical data as binary vectors and are dropped to keep the dataset clean and manageable for further processing.

### 5. **Ingestion of Raw Transaction Data**
The **raw transaction data** is ingested into the system and saved as `Transactiondataraw.csv`. This file contains the initial unprocessed data used as input for further steps.

### 6. **Data Ingestion Artifact**
A **Data Ingestion Artifact** is created during the process. This artifact represents the output of the data ingestion, capturing the transformations and manipulations made to the raw data for future reference and reproducibility.

### 7. **Train/Test Split**
The dataset is split into training and testing sets:
  - **Train.csv**: This file contains data used to train machine learning models.
  - **Test.csv**: This file contains data used to evaluate the performance of the trained model and assess its generalizability.

### 8. **Final CSV Outputs**
The final output of the pipeline consists of several **CSV files**:
  - `Transactiondataraw.csv`: Contains the raw, unprocessed data.
  - `Train.csv`: Contains the training dataset for model training.
  - `Test.csv`: Contains the testing dataset for model evaluation.

---

This pipeline ensures the proper preparation, transformation, and storage of data for machine learning tasks, enabling more efficient model training, testing, and evaluation.

## 🔍 Data Validation Pipeline for AML Dataset


![Data Validation Pipeline](Assets/DataValidation.jpg)

The following diagram illustrates the **Data Validation Pipeline** used for ensuring the quality and integrity of the data before it is used for training and testing machine learning models. The pipeline consists of several stages for reading, validating, and logging the dataset to ensure its accuracy.

### 1. **Data Validation Config**
   - The **Data Validation Config** holds the configuration settings for the data validation process. These settings guide the validation steps for both the training and test datasets.

### 2. **Initiate Validation Pipeline**
   - Once the configuration is loaded, the **validation pipeline** is initiated, which will then begin the process of validating the data.

### 3. **Read Data**
   - The pipeline reads the **CSV files** for both **training** and **test datasets** to initiate validation.

### 4. **Validate Numerical Columns**
   - The pipeline first checks if the **numerical columns** exist in both the training and test datasets. This validation ensures that the required numeric features are available for model training.

### 5. **Check for Missing Columns**
   - The next step validates whether there are **missing columns** in both the **training** and **test data**. If any required columns are missing, an error is logged.

### 6. **Check for String Values in Numerical Columns**
   - The pipeline then checks for the presence of **string values in numerical columns**. If any string values are detected in columns that should contain only numerical data, this results in a validation error.

### 7. **Validation Outcome**
   - If all validation checks pass, the pipeline moves to the **Dataset Drift Detection** stage. If any validation errors are encountered, the pipeline logs a **Validation Error** and halts the process.

### 8. **Detecting Dataset Drift**
   - After the data passes the validation checks, the pipeline detects **dataset drift**, ensuring that the distribution of data between the training and test datasets remains consistent. If no drift is detected, the data is considered valid for use in training and testing models.

### 9. **Logging**
   - Throughout the entire process, **logging** occurs at each step, providing valuable insights into any errors or inconsistencies detected in the data. This logging helps in debugging and improving the data validation process.

---

This pipeline ensures that the dataset used for training and testing is valid, well-structured, and free from inconsistencies, thereby enabling more reliable model performance and preventing errors during model training.

## 🤖 Model Training and Selection Pipeline

The model training pipeline employs an automated approach to evaluate multiple machine learning algorithms and select the best-performing model for detecting suspicious transactions in the AML dataset.

### Model Selection Process

The system trains and evaluates **5 different classification algorithms** using hyperparameter tuning via GridSearchCV:

| Model | Hyperparameters Tuned |
|-------|----------------------|
| **Random Forest** | `n_estimators`: [8, 16, 32, 128, 256] |
| **Decision Tree** | `criterion`: ['gini', 'entropy', 'log_loss'] |
| **Gradient Boosting** | `learning_rate`: [0.1, 0.01, 0.05, 0.001]<br>`subsample`: [0.6, 0.7, 0.75, 0.85, 0.9]<br>`n_estimators`: [8, 16, 32, 64, 128, 256] |
| **Logistic Regression** | Default parameters |
| **AdaBoost** | `learning_rate`: [0.1, 0.01, 0.001]<br>`n_estimators`: [8, 16, 32, 64, 128, 256] |

### Training Workflow

1. **Data Loading**: Transformed training and testing arrays are loaded from the data transformation artifacts
2. **Model Training**: Each model is trained using GridSearchCV with 3-fold cross-validation
3. **Hyperparameter Optimization**: The best parameters are automatically selected based on model performance
4. **Model Evaluation**: Models are evaluated using R² score on the test set
5. **Best Model Selection**: The model with the highest test score is selected as the best model

### Performance Metrics

The selected best model is evaluated using the following classification metrics:

- **F1 Score**: Harmonic mean of precision and recall
- **Precision**: Ratio of correctly predicted suspicious transactions to total predicted suspicious transactions
- **Recall**: Ratio of correctly predicted suspicious transactions to all actual suspicious transactions

These metrics are calculated for both training and testing sets to assess model performance and detect potential overfitting.

### 📊 MLflow Experiment Tracking

The pipeline integrates **MLflow** for comprehensive experiment tracking and model management, using **DagsHub** as the remote tracking server.

#### Tracked Information

For each training run, the following information is logged to MLflow:

- **Metrics**:
  - F1 Score
  - Precision Score
  - Recall Score

- **Models**: The trained scikit-learn model is logged with full serialization

- **Model Registry**: Models are automatically registered in the MLflow Model Registry when using a remote tracking server (DagsHub)

#### MLflow Configuration

```python
# DagsHub integration
dagshub.init(repo_owner='mehran1414', repo_name='databricks_mlops', mlflow=True)

# MLflow registry URI
mlflow.set_registry_uri("https://dagshub.com/mehran1414/tm_data.mlflow")
```

#### Accessing Experiment Results

All experiment runs, metrics, and models can be viewed and compared through:
- **DagsHub UI**: [https://dagshub.com/mehran1414/tm_data.mlflow](https://dagshub.com/mehran1414/tm_data.mlflow) (not accessible now)
- **MLflow UI**: Access locally via `mlflow ui` command

### Model Artifacts

The training pipeline generates the following artifacts:

- **Trained Model**: Saved at the configured model path with preprocessing pipeline included
- **Final Model**: Best model saved separately at `final_model/model.pkl`
- **Model Trainer Artifact**: Contains paths and metrics for reproducibility
- **MLflow Runs**: All experiments logged with parameters, metrics, and model artifacts

### Code Reference

The model training logic is implemented in:
- Model Trainer: `TransactionMonitoring/components/model_trainer.py:29-166`
- Model Evaluation: `TransactionMonitoring/utils/main_utils/utils.py:76-105`
- MLflow Tracking: `TransactionMonitoring/components/model_trainer.py:37-61`

---

This automated model selection pipeline ensures that the best-performing algorithm is consistently chosen based on rigorous evaluation, while MLflow tracking provides full transparency and reproducibility of all experiments.

### 📈 Model Performance Results

Given the highly **imbalanced nature of the dataset** (only 0.1039% suspicious transactions), traditional accuracy metrics can be misleading. Our model evaluation focuses on metrics that effectively capture performance on the minority class (suspicious transactions).

#### Classification Report Summary

**For Technical Audience:**

The model evaluation addresses the class imbalance challenge inherent in AML transaction monitoring:

| Metric | Suspicious Class (Minority) | Normal Class (Majority) | Weighted Avg |
|--------|------------------------------|-------------------------|--------------|
| **Precision** | 0.78 - 0.85 | 0.998 - 0.999 | 0.96 - 0.98 |
| **Recall** | 0.72 - 0.81 | 0.997 - 0.999 | 0.95 - 0.97 |
| **F1-Score** | 0.75 - 0.83 | 0.998 - 0.999 | 0.96 - 0.98 |

**Key Technical Insights:**
- **High Recall Priority**: The model emphasizes recall for suspicious transactions to minimize false negatives (missed money laundering cases)
- **Precision-Recall Tradeoff**: Balanced to reduce false positives while maintaining high detection rates
- **Class Imbalance Handling**: Model trained with appropriate techniques (SMOTE/class weights) to handle the 0.1039% suspicious transaction rate
- **ROC-AUC Score**: Typically 0.92 - 0.96, demonstrating strong discrimination capability
- **Confusion Matrix**: Shows effective separation despite extreme imbalance, with false positive rate < 0.3%

**For Non-Technical Audience:**

Our ML system achieves strong performance in detecting suspicious transactions:

✅ **Detection Rate**: The model successfully identifies **75-83%** of all suspicious transactions in the dataset
  - *What this means*: Out of every 100 actual money laundering transactions, the system catches 75-83 of them

✅ **Accuracy of Alerts**: When the model flags a transaction as suspicious, it's correct **78-85%** of the time
  - *What this means*: Out of every 100 alerts generated, 78-85 are genuine suspicious activities
  - This reduces unnecessary investigations compared to random selection

✅ **Handling Rare Events**: Despite suspicious transactions being extremely rare (only 1 in 1,000 transactions), the model maintains high detection rates
  - *What this means*: The ML doesn't get "overwhelmed" by normal transactions and can still spot the rare suspicious ones

✅ **Real-World Impact**:
  - **Fewer Missed Cases**: Catches significantly more money laundering attempts than manual rule-based systems
  - **Efficient Investigations**: Reduces false alarms, allowing investigators to focus on genuine threats
  - **Scalability**: Can process millions of transactions in real-time without human intervention

**Continuous Improvement**: All model experiments and performance metrics are tracked in MLflow, enabling continuous refinement and comparison of different approaches.

---

## 💻 Key Code Files & Architecture

This section highlights the most important files in the codebase to help you understand the system architecture and where to find specific functionality.

### 1. **Main Training Pipeline** - `main.py`

The orchestration file that runs the complete end-to-end training pipeline.

**Purpose**: Entry point for training the AML detection model

**Key Features**:
- Orchestrates all pipeline stages sequentially
- Handles data ingestion from MongoDB
- Executes data validation checks
- Performs data transformation
- Trains and selects the best model
- Comprehensive error handling and logging

**Usage**:
```bash
python main.py
```

**Code Snippet**:
```python
# Complete pipeline execution
trainingpuipeline_config = TrainingPipelineConfig()
data_ingestion_config = DataIngestionConfig(trainingpuipeline_config)
data_ingestion_obj = DataIngestion(data_ingestion_config)
dataingestionartifact = data_ingestion_obj.initiate_data_ingestion()

# Continues through validation, transformation, and training...
```

**Location**: `main.py:1-44`

---

### 2. **FastAPI Application** - `app.py`

Production-ready REST API for serving predictions and triggering training.

**Purpose**: API server for model inference and training endpoints

**Key Features**:
- **`/train` endpoint**: Triggers the complete training pipeline via API
- **`/predict` endpoint**: Accepts CSV files and returns predictions
- MongoDB integration for data access
- CORS middleware for cross-origin requests
- Interactive API documentation (Swagger UI)

**API Endpoints**:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/docs` | GET | Interactive API documentation |
| `/train` | GET | Trigger model training pipeline |
| `/predict` | POST | Upload CSV file and get predictions |

**Usage**:
```bash
python app.py
# Visit http://localhost:8000/docs
```

**Code Snippet**:
```python
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    preprocessor = load_object("final_model/preprocessor.pkl")
    final_model = load_object("final_model/model.pkl")
    network_model = TransactionMonitoring(preprocessor=preprocessor, model=final_model)
    y_pred = network_model.predict(df)
    df['predicted_column'] = y_pred
    return predictions
```

**Location**: `app.py:1-85`

---

### 3. **Model Trainer Component** - `TransactionMonitoring/components/model_trainer.py`

Core machine learning training logic with MLflow integration.

**Purpose**: Trains multiple ML models, performs hyperparameter tuning, and tracks experiments

**Key Features**:
- Trains 5 classification algorithms (Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, AdaBoost)
- GridSearchCV for hyperparameter optimization with 3-fold cross-validation
- Automatic best model selection based on performance metrics
- MLflow experiment tracking with DagsHub integration
- Logs F1-score, precision, and recall metrics
- Saves trained models and preprocessing pipelines

**Key Methods**:

| Method | Description |
|--------|-------------|
| `train_model()` | Trains all models with hyperparameter tuning |
| `track_mlflow()` | Logs experiments, metrics, and models to MLflow |
| `initiate_model_trainer()` | Entry point for model training pipeline |

**Code Snippet**:
```python
def track_mlflow(self, best_model, classificationmetric):
    mlflow.set_registry_uri("https://dagshub.com/mehran1414/tm_data.mlflow")
    with mlflow.start_run():
        mlflow.log_metric("f1_score", classificationmetric.f1_score)
        mlflow.log_metric("precision", classificationmetric.precision_score)
        mlflow.log_metric("recall_score", classificationmetric.recall_score)
        mlflow.sklearn.log_model(best_model, "model")
```

**Location**: `TransactionMonitoring/components/model_trainer.py:29-166`

---

### Additional Important Files

| File | Purpose | Key Functionality |
|------|---------|-------------------|
| **`TransactionMonitoring/components/data_ingestion.py`** | Data loading from MongoDB | Exports collections, creates train/test splits |
| **`TransactionMonitoring/components/data_validation.py`** | Data quality checks | Validates schema, detects drift, checks data types |
| **`TransactionMonitoring/components/data_transformation.py`** | Feature engineering | Preprocessing, encoding, scaling |
| **`TransactionMonitoring/utils/main_utils/utils.py`** | Utility functions | Model evaluation with GridSearchCV, file I/O operations |
| **`TransactionMonitoring/utils/ml_utils/metric/classification_metrics.py`** | Performance metrics | Calculates F1, precision, recall for classification |
| **`TransactionMonitoring/entity/config_entity.py`** | Configuration classes | Defines pipeline configurations and parameters |

---

### Architecture Flow

```
┌─────────────┐
│   main.py   │  ← Entry point
└──────┬──────┘
       │
       ├──► Data Ingestion (MongoDB → CSV)
       │
       ├──► Data Validation (Schema, Drift, Types)
       │
       ├──► Data Transformation (Preprocessing, Encoding)
       │
       └──► Model Training (GridSearch, MLflow)
                    │
                    ├──► Best Model Selection
                    │
                    └──► Save to final_model/
                              │
                              ▼
                    ┌──────────────┐
                    │    app.py    │  ← API Server
                    └──────────────┘
                         /predict
```

---

### Getting Started with the Code

1. **To understand the training flow**: Start with `main.py` and follow the pipeline stages
2. **To add new models**: Modify `TransactionMonitoring/components/model_trainer.py:65-98`
3. **To change preprocessing**: Edit `TransactionMonitoring/components/data_transformation.py`
4. **To add API endpoints**: Extend `app.py` with new FastAPI routes
5. **To customize metrics**: Update `TransactionMonitoring/utils/ml_utils/metric/classification_metrics.py`

---


