from flask import Blueprint, render_template, redirect, url_for, flash, request
#Blueprint lets you organize routes into modular groups (ex: route folders)
#render_template returns HTML page from the templates/ folder
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm
from app.models import Administrator
from werkzeug.security import check_password_hash

#creates a object named 'main' (identifier of this group of routes)
#__name__ tells Flask where thisblueprint is defined, so it can locate 
# templates and static files realative to this file
bp = Blueprint('main', __name__)

#The route decorator for bp, defines the URl path / 
# (which is the homepage) as http://localhost:5000/
@bp.route('/')

#the view function for the / route
#when someone visits /, Flask will call this function to generate a response
def index():   
    
    #This tells Flask to render and return an HTML file called index.html
    return render_template('index.html')



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Administrator.query.filter_by(name=form.username.data).first()
        if user and user.password == form.password.data:  # Use hash check in production!
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')