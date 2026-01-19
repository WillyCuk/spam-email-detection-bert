# File: app.py

from flask import Flask, request, render_template_string
from predictor import load_model, predict_phishing

app = Flask(__name__)
load_model()

# MODIFIKASI TEMPLATE HTML
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Phishing Email Detector</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background: #f4f4f9; color: #333; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
        .container { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 700px; } /* Diperlebar */
        h1 { color: #4a4a4a; text-align: center; }
        textarea { width: 100%; height: 150px; padding: 10px; border-radius: 4px; border: 1px solid #ccc; font-size: 16px; box-sizing: border-box; }
        button { background-color: #007bff; color: white; padding: 12px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; width: 100%; }
        button:hover { background-color: #0056b3; }
        .result { margin-top: 20px; padding: 15px; border-radius: 4px; text-align: center; font-weight: bold; }
        .phishing { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .legitimate { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .explanation { text-align: left; margin-top: 15px; font-size: 0.9em; font-weight: normal; }
        .explanation ul { list-style-type: none; padding-left: 0; }
        .explanation li { background: rgba(0,0,0,0.05); padding: 8px; border-radius: 4px; margin-bottom: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Phishing Email Detector</h1>
        <form method="post">
            <textarea name="email_text" placeholder="Paste the full email content here..."></textarea><br><br>
            <button type="submit">Detect Phishing</button>
        </form>
        {% if result %}
        <div class="result {{ 'phishing' if 'Phishing' in result.prediction else 'legitimate' }}">
            <h3>Prediction: {{ result.prediction }}</h3>
            <p>Confidence: {{ result.confidence }}</p>
            
            <!-- TAMBAHKAN BAGIAN INI UNTUK MENAMPILKAN ALASAN -->
            {% if result.explanation %}
            <div class="explanation">
                <h4>Alasan Deteksi:</h4>
                <ul>
                {% for reason in result.explanation %}
                    <li>{{ reason }}</li>
                {% endfor %}
                </ul>
            </div>
            {% endif %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        email_text = request.form['email_text']
        if email_text.strip():
            result = predict_phishing(email_text)
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(debug=True)