
from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

def validar_moneda_to(formulario, campo):
    moneda_from = formulario.moneda_from.data

    if moneda_from == campo:
        raise ValidationError("La moneda destino debe ser diferente a la moneda origen")


class PurchaseForm(FlaskForm):

    moneda_from = SelectField("From:", validators = [DataRequired(message= "Falta la moneda origen")], 
    choices= ['EUR','ETH','BNB','LUNA','SOL','BTC','BCH','LINK','ATOM','USDT' ])

    moneda_to = SelectField("To:", validators = [DataRequired(message= "Falta la moneda origen"), validar_moneda_to], 
    choices= ['EUR','ETH','BNB','LUNA','SOL','BTC','BCH','LINK','ATOM','USDT' ])

    cantidad_from = FloatField("Q:", validators=[DataRequired(message= "Falta la cantidad"), NumberRange(message= "Debe ser una cantidad positiva", min=0.00000001)])

    calcular= SubmitField("calcular")
    
    cantidad_to = HiddenField()
    campos = HiddenField()
    from_hidden = HiddenField()
    to_hidden = HiddenField()
    cant_hidden= HiddenField()
    aceptar = SubmitField("aceptar")

    

    

    
