from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from email_service import send_email_template

app = Flask(__name__)

# Veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ana sayfa
@app.route('/')
def index():
    return render_template('form.html')

# Form verilerini işleme
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    complaint = request.form['complaint']

    conn = get_db_connection()
    conn.execute('INSERT INTO complaints (name, phone, complaint) VALUES (?, ?, ?)',
                 (name, phone, complaint))
    conn.commit()
    conn.close()

    # E-posta gönderimini gerçekleştir
    send_email_template(name, phone, complaint, "cukadar.mertkaan@gmail.com")  # Değiştirmeniz gereken e-posta adresi

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
