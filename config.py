import os        # Lets you access environment variables and build file paths on any os

class Config:
    # Used to secure forms and sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'devkey' 

    # Connects Flask to a PostgreSQL database
    SQLALCHEMY_DATABASE_URI = 'postgresql://intern:intern123@localhost/management_system_db'
    
    # Disables extra (slow) tracking in SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Absolute path to where the uploaded images are stored
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  #@MB per request
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}