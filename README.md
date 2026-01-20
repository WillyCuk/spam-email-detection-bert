# 📧 BERT Phishing Email Detector

A machine learning model based on **BERT** (Bidirectional Encoder Representations from Transformers) designed to classify emails as **Legitimate** or **Phishing**.

---

## CRITICAL: BEFORE YOU CLONE

**This repository uses Git Large File Storage (LFS) to host the model weights (400MB+).**

If you clone this repository without Git LFS, you will only get a tiny pointer file, and the code **will crash** with a "model file too small" or "safetensors" error.

### How to Clone Correctly:

1.  **Install Git LFS** (if you haven't already):
    ```bash
    git lfs install
    ```
2.  **Clone the repository:**
    ```bash
    git clone [https://github.com/WillyCuk/spam-email-detection-bert.git](https://github.com/WillyCuk/spam-email-detection-bert.git)
    cd spam-email-detection-bert
    ```
3.  **Pull the actual model weights:**
    ```bash
    git lfs pull
    ```

---

Research & Training
While app.py is for deployment, the complete research and training pipeline is documented in the Jupyter Notebook file included in this repository (predict_phishing_model.ipynb).

This notebook contains:

Data Preprocessing: The exact cleaning steps applied to the raw dataset.

Model Training: Source code for training BERT, LSTM, and TF-IDF models from scratch.

Comparative Analysis: Graphs and metrics showing the performance comparison between the three models (Proof of Concept).


##  Quick Start For Test Web App

### 1. Install Dependencies
Ensure you have Python 3.8+ installed.
```bash
pip install -r requirements.txt
```

### 2. Run The Web App
```
python app.py
```

or you can visit https://huggingface.co/spaces/WillyCuk/phishing-email-bert-detection

