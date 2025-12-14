from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from datetime import datetime
import pytz
import os

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_sangat_aman'

# --- Konfigurasi ---
DATABASE_FILE = 'database.txt'
USERNAME_VALID = 'nase'
PASSWORD_VALID = 'sukasari1'
# Lokasi folder templates untuk mengambil logo
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

def get_wib_time():
    tz = pytz.timezone('Asia/Jakarta')
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S WIB")

def ensure_https(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        return 'https://' + url
    return url

# --- Routes Khusus ---

# Route untuk menampilkan LOGO dari folder templates
@app.route('/logo_image')
def logo_image():
    return send_from_directory(TEMPLATE_DIR, 'logo.png')

# --- Routes Utama ---

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME_VALID and password == PASSWORD_VALID:
            session['logged_in'] = True
            return redirect(url_for('input_data'))
        else:
            error = "Username atau Password salah!"
            
    return render_template('index.html', error=error)

@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        waktu = get_wib_time()
        nomor = request.form['nomor']
        nama = request.form['nama']
        website = ensure_https(request.form['website'])
        keterangan = request.form['keterangan']
        
        with open(DATABASE_FILE, 'a') as f:
            f.write(f"{waktu}|{nomor}|{nama}|{website}|{keterangan}\n")
            
        return redirect(url_for('output_data'))
        
    return render_template('input.html', wib=get_wib_time())

@app.route('/list')
def output_data():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    data_list = []
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    data_list.append({
                        'waktu': parts[0],
                        'nomor': parts[1],
                        'nama': parts[2],
                        'website': parts[3],
                        'ket': parts[4]
                    })
    
    return render_template('output.html', data=reversed(data_list))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
