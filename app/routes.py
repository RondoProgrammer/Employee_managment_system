from flask import Blueprint, render_template
#Blueprint lets you organize routes into modular groups (ex: route folders)
#render_template returns HTML page from the templates/ folder


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
