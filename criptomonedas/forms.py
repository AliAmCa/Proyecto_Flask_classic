
from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField, FormField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

def validar_moneda_to(formulario, campo):
    moneda_from = formulario.moneda_from.data

    if moneda_from == campo:
        raise ValidationError("La moneda destino debe ser diferente a la moneda origen")


class PurchaseForm(FlaskForm):

    moneda_from = SelectField("From", validators = [DataRequired(message= "Falta la moneda origen")], 
    choices= [(0,'EUR'),(1,'ETH'), (2,'BNB'), (3,'LUNA'),(4,'SOL'),
    (5,'BTC'),(6,'BCH'),(7,'LINK'),(8,'ATOM'),(9,'USDT') ])

    moneda_to = SelectField("To", validators = [DataRequired(message= "Falta la moneda origen"), validar_moneda_to], 
    choices= [(0,'EUR'),(1,'ETH'), (2,'BNB'), (3,'LUNA'),(4,'SOL'),
    (5,'BTC'),(6,'BCH'),(7,'LINK'),(8,'ATOM'),(9,'USDT') ])

    cantidad_from = FloatField("Q:", validators=[DataRequired(message= "Falta la cantidad"), NumberRange(message= "Debe ser una cantidad positiva", min=0.000001)])

    calcular= SubmitField("")

    #cantidad_to = FloatField("Q:")

    aceptar = SubmitField("")

    

    

    
