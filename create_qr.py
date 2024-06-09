import qrcode

# Kafelerin ID'leri ve URL'leri
cafes = {
    1: "http://localhost:5000/form?cafe=1",
    2: "http://localhost:5000/form?cafe=2",
    3: "http://localhost:5000/form?cafe=3",
    4: "http://localhost:5000/form?cafe=4",
    5: "http://localhost:5000/form?cafe=5"
}

# QR kodlarını oluşturma fonksiyonu
def create_qr(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)

# Her kafe için QR kodlarını oluştur
for cafe_id, url in cafes.items():
    filename = f"qr_cafe{cafe_id}.png"
    create_qr(url, filename)
    print(f"QR kodu oluşturuldu: {filename}")
