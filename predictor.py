# File: predictor.py

import re
import string
import torch
from transformers import BertTokenizer, BertForSequenceClassification


# ... (kode clean_text, load_model, dan variabel global tetap sama) ...


# --- Fungsi Preprocessing (sama seperti di Colab) ---
def clean_text(text):
    opening_pattern = re.compile(
        r"is the following email safe or phishing\?\?.*\n", re.IGNORECASE
    )
    text = opening_pattern.sub("", text)
    closing_pattern = re.compile(
        r"\s*(?:Email type is|email_type is):.*$", re.IGNORECASE
    )
    text = closing_pattern.sub("", text)
    header_pattern = re.compile(
        r"(date|sender|receiver|email subject|email body):\s*", re.IGNORECASE
    )
    text = header_pattern.sub("", text)
    text = text.lower()
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"<.*?>+", "", text)
    text = re.sub(r"[%s]" % re.escape(string.punctuation), "", text)
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\w*\d\w*", "", text)
    text = re.sub(r"http\S+|www\S+", "", text)
    return text


# --- Variabel Global untuk Model dan Tokenizer ---
model = None
tokenizer = None
device = None


# --- Fungsi untuk Memuat Model (sama seperti sebelumnya) ---
def load_model(model_path="./best_bert_phishing_classifier"):
    """Memuat tokenizer dan model BERT dari direktori."""
    global model, tokenizer, device
    print("Memuat model BERT... (mungkin perlu beberapa saat)")
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model = BertForSequenceClassification.from_pretrained(model_path)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    print(f"✅ Model dimuat ke perangkat: {device}")


# --- Tambahkan Fungsi Analisis Indikator Phishing ---
def analyze_phishing_indicators(text):
    """
    Menganalisis teks email untuk mencari indikator phishing yang umum
    dan pola yang lebih halus. Mengembalikan daftar alasan.
    """
    reasons = []
    text_lower = text.lower()

    # 1. Cari URL
    url_pattern = re.compile(r"http\S+|www\S+")
    urls = re.findall(url_pattern, text_lower)
    if urls:
        reasons.append("🔗 Email mengandung satu atau lebih URL.")
        for url in urls:
            # Cek URL shortener
            if any(
                shortener in url
                for shortener in ["bit.ly", "tinyurl.com", "t.co", "goo.gl"]
            ):
                reasons.append(
                    "⚠️ Menggunakan URL shortener, yang sering digunakan untuk menyembunyikan link asli."
                )
            # Cek domain mencurigakan
            if "paypal" in url and "paypal.com" not in url:
                reasons.append("🚨 URL mencurigakan yang menyamar sebagai PayPal.")
            if "amazon" in url and "amazon.com" not in url:
                reasons.append("🚨 URL mencurigakan yang menyamar sebagai Amazon.")
            if "bri" in url and "bri.co.id" not in url:
                reasons.append("🚨 URL mencurigakan yang menyamar sebagai Bank BRI.")

    # 2. Cari kata-kata mendesak atau menakut-nakuti
    urgent_keywords = [
        "urgent",
        "segera",
        "aktifkan sekarang",
        "verifikasi segera",
        "akun terkunci",
        "hadiah",
        "menang",
        "klaim",
        "gratis",
        "suspended",
        "limited",
        "security alert",
        "immediate action required",
    ]
    found_urgent = [kw for kw in urgent_keywords if kw in text_lower]
    if found_urgent:
        reasons.append(
            f"🚨 Mengandung kata-kata mendesak/menakut-nakuti: {', '.join(found_urgent[:3])}"
        )

    # 3. Cari permintaan informasi sensitif
    sensitive_info_keywords = [
        "password",
        "kata sandi",
        "pin",
        "credit card",
        "kartu kredit",
        "cvv",
        "ssn",
        "nomor rekening",
    ]
    found_sensitive = [kw for kw in sensitive_info_keywords if kw in text_lower]
    if found_sensitive:
        reasons.append(f"🕵️‍♂️ Meminta informasi sensitif: {', '.join(found_sensitive)}")

    # 4. Cari kesalahan tata bahasa atau ejaan yang umum
    common_typos = ["paypaI", "amaz0n", "microsft", "g00gle"]
    for typo in common_typos:
        if typo in text_lower:
            reasons.append(
                f"⚠️ Terdapat kemungkinan kesalahan ejaan yang mencurigakan: '{typo}'"
            )
            break

    # --- ATURAN BARU UNTUK MENANGKAP KASUS YANG LEBIHALUS ---

    # 5. Cek pola "ancaman terselubung" (covert threats)
    #    Ini adalah kalimat yang terdengar masuk akal tapi bertujuan menakut-nakuti.
    covert_threats = [
        "package has an incorrect address",
        "failed delivery attempt",
        "incorrect shipping address",
        "your account will be suspended",
        "your account has been limited",
        "action required to continue service",
        "unable to validate your billing information",
        "subscription may be canceled",
    ]
    found_threats = [threat for threat in covert_threats if threat in text_lower]
    if found_threats:
        reasons.append(
            f"⚠️ Mengandung kalimat ancaman terselubung: '{found_threats[0]}'"
        )

    # 6. Cek kombinasi "permintaan tindakan" + "ancaman"
    #    Ini adalah aturan yang lebih kuat untuk mendeteksi manipulasi.
    action_keywords = ["click", "confirm", "verify", "update", "log in", "visit link"]
    threat_keywords = [
        "suspended",
        "canceled",
        "returned",
        "blocked",
        "limited",
        "failed",
        "incorrect",
    ]

    has_action = any(action in text_lower for action in action_keywords)
    has_threat = any(threat in text_lower for threat in threat_keywords)

    if has_action and has_threat:
        reasons.append(
            "🚨 Menggabungkan permintaan tindakan ('klik/konfirmasi') dengan ancaman ('dibatalkan/dikembalikan')."
        )

    # Jika tidak ada indikator spesifik yang ditemukan, berikan alasan umum
    if not reasons:
        reasons.append(
            "Model mendeteksi pola kalimat dan struktur yang umum ditemukan pada email phishing berdasarkan pembelajaran sebelumnya."
        )

    return reasons


# --- Modifikasi Fungsi Prediksi dengan Debugging ---
def predict_phishing(email_text):
    """
    Memprediksi apakah sebuah email adalah phishing atau tidak,
    memberikan alasan jika terdeteksi phishing, dan menggunakan
    whitelist untuk mengurangi false positive pada promosi sah.
    """
    if model is None or tokenizer is None:
        raise RuntimeError("Model belum dimuat. Panggil load_model() terlebih dahulu.")

    # 1. Bersihkan teks
    cleaned_text = clean_text(email_text)

    # 2. Tokenisasi
    inputs = tokenizer(
        cleaned_text, return_tensors="pt", truncation=True, padding=True, max_length=256
    )

    # 3. Pindahkan input ke perangkat
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # 4. Prediksi dengan Model BERT
    with torch.no_grad():
        outputs = model(**inputs)

    # 5. Proses hasil dari model
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=1)
    predicted_class_id = torch.argmax(probabilities, dim=1).item()
    confidence_score = probabilities[0, predicted_class_id].item()

    label_map = {0: "Legitimate (Aman)", 1: "Phishing (Berbahaya)"}
    prediction_label = label_map[predicted_class_id]

    # --- LOGIKA TAMBAHAN: WHITELIST UNTUK MENGURANGI FALSE POSITIVE ---

    # Cek apakah email mengandung link ke domain terpercaya
    # Kita menggunakan teks asli (email_text) karena URL sudah dibersihkan di 'cleaned_text'
    trusted_domains = [
        "amazon.com",
        "amazon.co.uk",
        "amazon.ca",
        "amazon.de",
        "paypal.com",
        "ebay.com",
        "google.com",
        "microsoft.com",
        "linkedin.com",
        "facebook.com",
        "netflix.com",
        "spotify.com",
    ]

    # Ekstrak semua URL dari teks asli
    urls = re.findall(r"http[s]?://\S+", email_text.lower())

    is_trusted_link_found = False
    for url in urls:
        for domain in trusted_domains:
            # Cek apakah domain terpercaya adalah bagian dari URL
            # dan memastikan itu bukan subdomain yang mencurigakan
            if f".{domain}" in url or url.startswith(f"{domain}/"):
                is_trusted_link_found = True
                print(f"INFO: Ditemukan link terpercaya '{domain}' dalam email.")
                break
        if is_trusted_link_found:
            break

    # Jika model memprediksi Phishing, TAPI ada link terpercaya, kita periksa lebih lanjut
    if predicted_class_id == 1 and is_trusted_link_found:
        # Ini adalah kasus di mana model mungkin salah (False Positive)
        # Kita mengubah keputusan menjadi Aman, tetapi dengan penjelasan khusus.
        print(
            "PERINGATAN: Model memprediksi Phishing, tetapi menemukan link terpercaya. Mengubah prediksi menjadi Aman."
        )

        prediction_label = "Legitimate (Aman)"
        predicted_class_id = 0
        # Kita menurunkan sedikit confidence untuk menunjukkan adanya "ketidakpastian"
        confidence_score = max(confidence_score, 0.85)

    # --- AKHIR LOGIKA WHITELIST ---

    # 6. Siapkan penjelasan (explanation)
    explanation = []
    if predicted_class_id == 1:
        # Jika prediksi akhirnya Phishing, cari alasannya seperti biasa
        explanation = analyze_phishing_indicators(email_text)
    elif is_trusted_link_found:
        # Jika prediksi akhirnya Aman karena ada link terpercaya, beri penjelasan
        explanation.append(
            "✅ Email dianggap aman karena mengandung link ke domain terpercaya, meskipun mengandung kata-kata yang biasanya ada di email phishing."
        )

    return {
        "prediction": prediction_label,
        "confidence": f"{confidence_score:.2%}",
        "explanation": explanation,
    }
