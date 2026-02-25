from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, EmailField, validators

class UserForm(FlaskForm): 
    id = IntegerField('ID') 
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El nombre es requerido')
    ])
    apellidos = StringField('Apellidos', [
        validators.DataRequired(message='Los apellidos son requeridos')
    ])
    email = EmailField('Correo Electrónico', [
        validators.DataRequired(message='El email es requerido'),
        validators.Email(message='Ingrese un correo válido')
    ])
    telefono = StringField('Teléfono')