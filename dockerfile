# 1. Gunakan Python versi slim (lebih ringan & cepat saat deploy)
FROM python:3.10-slim

# 2. Mencegah Python membuat file cache .pyc & mengaktifkan log agar langsung muncul
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Buat folder kerja di dalam container
WORKDIR /app

# 4. Copy file requirements.txt terlebih dahulu (untuk cache layer)
COPY requirements.txt .

# 5. Install library yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy seluruh sisa kode project kamu ke dalam container
COPY . .

# 7. Buka port 8080 (Port standar yang sering dipakai Back4App/Cloud)
EXPOSE 8080

# 8. PERINTAH MENJALANKAN (PILIH SALAH SATU DI BAWAH):
# Ganti "app.py" dengan nama file utama script python kamu.
CMD ["python", "app.py"]
