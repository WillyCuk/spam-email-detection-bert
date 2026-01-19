# Gunakan image Python resmi yang ringan
FROM python:3.12-slim

# Set working directory
WORKDIR /code

# Salin requirements dan install
# (Kita pakai --no-cache-dir agar image tetap kecil)
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Salin semua file proyek ke dalam image
COPY . .

# Perintah untuk menjalankan aplikasi saat container nyala
# Hugging Face mengharapkan aplikasi berjalan di port 7860
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]