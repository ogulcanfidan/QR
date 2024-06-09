from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp

class ComplaintForm(FlaskForm):
    cafe_id = HiddenField('Cafe ID', validators=[DataRequired()])
    name = StringField('Adınız', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Telefon Numaranız', validators=[DataRequired(), Length(max=15)])
    complaint = TextAreaField('Şikayetiniz', validators=[
        DataRequired(),
        Length(max=500),
        Regexp(r'^[^\<\>\&]*$', message="Şikayet metninde geçersiz karakterler var.")
    ])
    submit = SubmitField('Gönder')
