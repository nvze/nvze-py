# 1. Gunakan image Python resmi sebagai dasar
FROM python:3.8

# 2. Set direktori kerja di dalam container
WORKDIR /app

# 3. Salin semua file aplikasi ke direktori kerja
COPY . /app

# 4. Install dependensi aplikasi
RUN pip install -r requirements.txt

# 5. Tentukan perintah untuk menjalankan aplikasi

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
