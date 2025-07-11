import os        #Lets you access environment variables

class Config:
    #Used to secure forms and sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'devkey' 

    #Connects Flask to a PostgreSQL database
    SQLALCHEMY_DATABASE_URI = 'postgresql://intern:intern123@localhost/management_system_db'
    
    #Disables extra (slow) tracking in SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
