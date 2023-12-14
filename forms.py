from wtforms import Form
from wtforms import StringField, TextAreaField, IntegerField,TelField
from wtforms.fields import EmailField
from wtforms import PasswordField
from wtforms import HiddenField
from wtforms import validators
from models import User
from models import Estacionamiento

def lenght_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('El campo debe estar vacio')



class CommentForm(Form):
    comment = TextAreaField('Comentario')
    honeypot = HiddenField('',[lenght_honeypot])




class LoginForm(Form):
    username = StringField(
        "Usuario",
        [validators.length(min=4, max=30), validators.DataRequired()]
    )
    password = PasswordField('Password',[validators.DataRequired()])





class CreateForm(Form):
    estacionamiento = StringField(
        "Estacionamiento",
        [validators.length(min=4, max=50), validators.DataRequired()],
    )
    capacidad = IntegerField(
        "Capacidad"
        , [validators.NumberRange(min=1, max=9999), validators.DataRequired()]
    )
    cp=IntegerField(
        "Coodigo Postal", 
        [validators.NumberRange(min=1000, max=999998), validators.data_required()]
    )
    telefono = StringField(
        "Telefono", 
        [validators.length(min=10, max=10), validators.data_required()]
    )
    username = StringField(
        "Username",
        [validators.length(min=4, max=30), validators.DataRequired()],
    )
    password = PasswordField(
        "Password"
        ,[validators.length(min=8, max=50),validators.Regexp(r'^(?=.*[a-z])(?=.*[A-Z]).+$', message='La contraseña debe contener al menos una letra mayúscula y una letra minúscula.'),validators.DataRequired()]
    )
    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('El usuario ya se encuentra registrado')
    
    def validate_estacionamiento(form,field):
        estacionamiento = field.data
        est = Estacionamiento.query.filter_by(estacionamiento = estacionamiento).first()
        if est is not None:
            raise validators.ValidationError('Ya se ecnuentra existente el estacionamiento')   
        
    def validate_telefono(form, field):
        if not field.data.isdigit():
            raise validators.ValidationError('Este campo solo debe contener números.')




class CreateUser(Form):
    username = StringField(
        "Username",
        [validators.length(min=4, max=30), validators.DataRequired()],
    )
    password = PasswordField(
        "Password"
        ,[validators.length(min=8, max=50),validators.Regexp(r'^(?=.*[a-z])(?=.*[A-Z]).+$', message='La contraseña debe contener al menos una letra mayúscula y una letra minúscula.'),validators.DataRequired()]
    )
    rol = StringField(
        "Rol",
        [validators.length(min=4, max=30), validators.DataRequired()]
    )
    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('El usuario ya se encuentra registrado')
        



class CreateTari(Form):
    tolerancia = IntegerField(
        "Tolerancia"
        , [validators.NumberRange(min=1, max=9999), validators.DataRequired()]
    )
    primerasDos = IntegerField(
        "Primeras dos horas"
        , [validators.NumberRange(min=1, max=9999), validators.DataRequired()]
    )
    extra = IntegerField(
        "Hora extra"
        , [validators.NumberRange(min=1, max=9999), validators.DataRequired()]
    )
    pension_dia = IntegerField(
        "Día"
        , [validators.NumberRange(min=1, max=9999), validators.DataRequired()]
    )
    pension_semana = IntegerField(
        "Semana"
        , [validators.NumberRange(min=1, max=9999), validators.DataRequired()]
    )
    pension_mes = IntegerField(
        "Mes"
        , [validators.NumberRange(min=1, max=9999), validators.DataRequired()]
    )

    
class todoesta(Form):
    estacionamiento = StringField(
        "Estacionamiento"
        ,[validators.length(min=4, max=30), validators.DataRequired()]
    )


class CreateUserTodo(Form):
    username = StringField(
        "Username",
        [validators.length(min=4, max=30), validators.DataRequired()],
    )
    password = PasswordField(
        "Password"
        ,[validators.length(min=8, max=50),validators.Regexp(r'^(?=.*[a-z])(?=.*[A-Z]).+$', message='La contraseña debe contener al menos una letra mayúscula y una letra minúscula.'),validators.DataRequired()]
    )
    rol = StringField(
        "Rol",
        [validators.length(min=4, max=30), validators.DataRequired()]
    )
    estacionamiento = StringField(
        "Estacionamiento"
        ,[validators.length(min=4, max=30), validators.DataRequired()]
    )
    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('El usuario ya se encuentra registrado')

class ModificarRol(Form):
    username = StringField(
        "Username",
        [validators.length(min=4, max=30), validators.DataRequired()],
    )
    rol = StringField(
        "Rol",
        [validators.length(min=4, max=30), validators.DataRequired()]
    )


