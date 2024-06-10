from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from email_service import send_email_template
from flask_wtf.csrf import CSRFProtect
from forms import ComplaintForm
import re

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

# HTML ve URL linklerini kaldıran fonksiyon
def remove_links_and_tags(input_text):
    clean_text = re.sub(r'http\S+|www\S+|https\S+', '', input_text, flags=re.MULTILINE)
    clean_text = re.sub(r'<.*?>', '', clean_text)
    clean_text = re.sub(r'[<>]', '', clean_text)
    return clean_text

# Ana sayfa
@app.route('/')
def index():
    return "Ana sayfa"

# Kafe form sayfası
@app.route('/form')
def form():
    cafe_id = request.args.get('cafe')
    form = ComplaintForm(cafe_id=cafe_id)
    return render_template(f'form_cafe{cafe_id}.html', form=form, cafe_id=cafe_id)

# Form verilerini işleme
@app.route('/submit', methods=['POST'])
def submit():
    form = ComplaintForm()
    if form.validate_on_submit():
        try:
            name = form.name.data
            phone = form.phone.data
            complaint = form.complaint.data
            
            # Kullanıcı girdilerini temizle
            name = remove_links_and_tags(name)
            phone = remove_links_and_tags(phone)
            complaint = remove_links_and_tags(complaint)
            
            cafe_id = form.cafe_id.data
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
    else:
        cafe_id = form.cafe_id.data
        return render_template(f'form_cafe{cafe_id}.html', form=form, cafe_id=cafe_id)

if __name__ == '__main__':
    app.run(debug=True)
