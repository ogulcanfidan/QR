from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from email_service import send_email_template
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'tektekeryasar'
csrf = CSRFProtect(app)

# Veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Kafe e-posta adresleri
cafes = {
    "1": "ogulcanfidannn@gmail.com",
    "2": "ogulcan@24yemek.com.tr",
    "3": "cukadar.mertkaan@gmail.com",
    "4": "mertkaancukadar@posta.mu.edu.tr",
    "5": "cafe5@example.com"
}

# Ana sayfa
@app.route('/')
def index():
    return "Ana sayfa"

# Kafe form sayfası
@app.route('/form')
def form():
    cafe_id = request.args.get('cafe')
    return render_template(f'form_cafe{cafe_id}.html', cafe_id=cafe_id)

# Form verilerini işleme
@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        phone = request.form['phone']
        complaint = request.form['complaint']
        cafe_id = request.form['cafe_id']
        
        to_email = cafes.get(cafe_id, "default@example.com")

        conn = get_db_connection()
        conn.execute('INSERT INTO complaints (name, phone, complaint, cafe_id) VALUES (?, ?, ?, ?)',
                     (name, phone, complaint, cafe_id))
        conn.commit()
        conn.close()

        send_email_template(name, phone, complaint, to_email)
        
        flash('Şikayetiniz gönderildi!', 'success')
    except Exception as e:
        print(e)
        flash('Şikayetiniz gönderilemedi!', 'error')
    
    return redirect(url_for('form', cafe=cafe_id))

if __name__ == '__main__':
    app.run(debug=True)
