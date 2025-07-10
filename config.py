import os        #Lets you access environment variables

class Config:
    #Used to secure forms and sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'devkey' 

    #Connects Flask to a PostgreSQL database
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/employee_db'
    
    #Disables extra (slow) tracking in SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
