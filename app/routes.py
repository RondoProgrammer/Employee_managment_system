from flask import Blueprint, render_template, redirect, url_for, flash, request
#Blueprint lets you organize routes into modular groups (ex: route folders)
#render_template returns HTML page from the templates/ folder
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, EmployeeForm
from app.models import Administrator, Employee, DepartmentManager, Department
from app import db


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
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
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

@bp.route('/employees')
@login_required
def list_employees():
    if hasattr(current_user, 'department'):  # Department Manager
        employees = Employee.query.filter_by(department_id=current_user.department.id).all()
    else:  # Admin
        employees = Employee.query.all()
    return render_template('employees/list.html', employees=employees)

@bp.route('/employee/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = EmployeeForm()
    
    # Limit department choices based on role
    if hasattr(current_user, 'department'):
        form.department_id.choices = [(current_user.department.id, current_user.department.name)]
    else:
        form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]

    if form.validate_on_submit():
        new_employee = Employee(
            name=form.name.data,
            position=form.position.data,
            salary=form.salary.data,
            department_id=form.department_id.data
        )
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('main.list_employees'))
    
    return render_template('employees/add.html', form=form)

# ------------------------
# Edit Employee
# ------------------------
@bp.route('/employee/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    
    # Authorization check
    if hasattr(current_user, 'department') and employee.department_id != current_user.department.id:
        flash('You are not authorized to edit this employee.', 'danger')
        return redirect(url_for('main.list_employees'))

    form = EmployeeForm(obj=employee)
    if hasattr(current_user, 'department'):
        form.department_id.choices = [(current_user.department.id, current_user.department.name)]
    else:
        form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]

    if form.validate_on_submit():
        employee.name = form.name.data
        employee.position = form.position.data
        employee.salary = form.salary.data
        employee.department_id = form.department_id.data
        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('main.list_employees'))

    return render_template('employees/edit.html', form=form)

# ------------------------
# Delete Employee
# ------------------------
@bp.route('/employee/delete/<int:id>', methods=['POST'])
@login_required
def delete_employee(id):
    employee = Employee.query.get_or_404(id)

    # Authorization check
    if hasattr(current_user, 'department') and employee.department_id != current_user.department.id:
        flash('You are not authorized to delete this employee.', 'danger')
        return redirect(url_for('main.list_employees'))

    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('main.list_employees'))