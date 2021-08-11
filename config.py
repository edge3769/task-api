import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    PAYSTACK = os.environ.get('PAYSTACK')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SECRET_KEY= os.environ.get('SECRET_KEY') or 'dev'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:love@localhost:5432/task'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp-mail.outlook.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25) or 587
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') or False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['edge3769@gmail.com']
    JWT_HEADER_TYPE = ''
    JWT_ACCESS_TOKEN_EXPIRES = False