
from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

class PurchaseForm(FlaskForm):

    moneda_from = SelectField("From", validators = [DataRequired(message= "Falta la moneda origen")], 
    choices= [(0,'EUR'),(1,'ETH'), (2,'BNB'), (3,'LUNA'),(4,'SOL'),
    (5,'BTC'),(6,'BCH'),(7,'LINK'),(8,'ATOM'),(9,'USDT') ])

    moneda_to = SelectField("To", validators = [DataRequired(message= "Falta la moneda origen")], 
    choices= [(0,'EUR'),(1,'ETH'), (2,'BNB'), (3,'LUNA'),(4,'SOL'),
    (5,'BTC'),(6,'BCH'),(7,'LINK'),(8,'ATOM'),(9,'USDT') ])

    cantidad_from = FloatField("Q", validators=[DataRequired(), NumberRange(message= "Debe ser una cantidad positiva", min=0.01)])


    aceptar = SubmitField("Aceptar")
    cancelar = SubmitField("Cancelar")