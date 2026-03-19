# formulario de productos

from flask_wtf import Flaskform
from wtforms import StringField, DecimalField, SubmitField,
from wtforms.validators import DataRequired, length, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    cantidad = IntegerField('cantidad', validators=[DataRequired(), NumberRange(min=1)])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Agregar Producto')
