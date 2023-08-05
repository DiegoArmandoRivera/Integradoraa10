from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime

db = SQLAlchemy()

#clase que crea automaticamente la tabla estaconamientos en la base de datos
class Estacionamiento(db.Model):
    __tablename__ = 'estacionamientos'


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estacionamiento = db.Column(db.String(50), unique=True, nullable=False)
    capacidad = db.Column(db.Integer())
    cp = db.Column(db.Integer())
    telefono =  db.Column(db.String(11))

    user = db.relationship('User')
    ticket = db.relationship('Ticket')
    tarifa = db.relationship('Tarifa')

    # create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, estacionamiento, capacidad, cp, telefono):
        self.estacionamiento = estacionamiento
        self.capacidad = capacidad
        self.cp = cp
        self.telefono = telefono




class User(db.Model):
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(200))
    rol = db.Column(db.String(30))
    estacionamiento = db.Column(db.ForeignKey('estacionamientos.estacionamiento'))


    def __init__(self, username, password, rol, estacionamiento):
        self.username = username
        self.password = self.create_password(password)
        self.rol = rol
        self.estacionamiento = estacionamiento

    def create_password(self, password):
        return generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)
    




class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    encargado = db.Column(db.String(50))
    entrada = db.Column(db.DateTime)
    salida = db.Column(db.DateTime)
    costo = db.Column(db.Integer())
    estacionamiento = db.Column(db.ForeignKey('estacionamientos.estacionamiento'))

    def __init__(self, entrada,salida,costo,encargado,estacionamiento):
        self.entrada = entrada
        self.salida = salida
        self.costo = costo
        self.encargado = encargado
        self.estacionamiento = estacionamiento




class Tarifa(db.Model):

    __tablename__ = 'tarifas'



    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tolerancia = db.Column(db.Integer)
    primerasDos = db.Column(db.Integer)
    extra = db.Column(db.Integer)
    estacionamiento = db.Column(db.ForeignKey('estacionamientos.estacionamiento'))
    
    def __init__(self,primerasDos,extra,tolerancia,estacionamiento):
        self.extra = extra
        self.primerasDos = primerasDos
        self.tolerancia = tolerancia
        self.estacionamiento = estacionamiento

