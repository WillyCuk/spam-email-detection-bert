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

##  Quick Start

### 1. Install Dependencies
Ensure you have Python 3.8+ installed.
```bash
pip install -r requirements.txt
```

### 2. Run The Detector
```
python predict.py
```


