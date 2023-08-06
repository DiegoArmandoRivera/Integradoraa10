import os

class Config(object):
    SECRET_KEY = 'equiporeest'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = '20203tn144@utez.edu.mx'
    MAIL_PASSWORD = os.environ.get('PASSWORD_EMAIL_CF')

class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:Masterxbox19@reest.ciicou1qy8x0.us-east-1.rds.amazonaws.com/prueba'    
    SQLALCHEMY_TRACK_MODIFICATIONS = False