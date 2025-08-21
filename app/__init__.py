import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


#creates objects that handle databases, migrations, login state
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

#Defines application factory pattern (can create multiple app insances with different configs)
def create_app():

    #initializes new Flask app instance
    #__name__ is a built in python variable which represents the name of the curr module
    #This is the main application module. Use this module’s location to find things like templates, static files, etc.
    app = Flask(__name__)
    app.config.from_object('config.Config') #Loads config settings from congfig.py

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    #binds all objects created above to the flask app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  #@login_required knows where to send unauth’d users

    #imports all the routs (URLs) from app/routes.py
    #Registers the blueprint (bp) with the main app, so all your routes are included.
    from . import routes
    app.register_blueprint(routes.bp)

    # Import models so Alembic sees them for migrations
    from app import models

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
         return User.query.get(int(user_id))

    #returns the fully configured app instance
    return app 