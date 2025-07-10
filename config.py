import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'devkey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/employee_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
