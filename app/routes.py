import uuid, os #uuid lets us generate a unique string name to avoid collsions
from flask import Blueprint, render_template, redirect, url_for, flash, request
#Blueprint lets you organize routes into modular groups (ex: route folders)
#render_template returns HTML page from the templates/ folder
from flask import current_app #for photos (?)
from werkzeug.utils import secure_filename #important for files/photos
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, EmployeeForm, DepartmentForm, ManagerForm
from app.models import User, Employee, Department
from app import db


#creates a object named 'main' (identifier of this group of routes)
#__name__ tells Flask where thisblueprint is defined, so it can locate templates and static files realative to this file
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
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()  # Create an instance of the LoginForm(username+password)
    if form.validate_on_submit(): #Checks if the form was submitted(POST) and is valid
        user = User.query.filter_by(username=form.username.data).first()  # Find user by username
        if user and user.password == form.password.data:  # Check if user exists and password matches
            login_user(user)  # Log in the user 
            next_url = request.args.get('next')
            return redirect(next_url or url_for('main.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)

# ------------------------
# Logout
# ------------------------
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# ------------------------
# Dashboard
# ------------------------
@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# ------------------------
# List Employees
# ------------------------
@bp.route('/employees')
@login_required
def list_employees():
    if current_user.role == 'department_manager':
        # Get employees only in the manager's department
        if current_user.department_id:
            employees = Employee.query.filter_by(department_id=current_user.department_id).all()
        else:
            employees = []
            flash('You are not assigned to any department yet.', 'warning')
    else:
        # Admin sees all employees
        employees = Employee.query.all()

    return render_template('employees/list.html', employees=employees)

# ------------------------
# Add Employee
# ------------------------
@bp.route('/employee/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = EmployeeForm()

    # Limit department choices for managers
    if current_user.role == 'department_manager':
        # Manager can only add to their department
        if current_user.department_id:
            form.department_id.choices = [(current_user.department_id, current_user.department.name)]
        else:
            flash('You are not assigned to any department.', 'danger')
            return redirect(url_for('main.list_employees'))
    else:
        # Admin can select any department
        form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]

    if form.validate_on_submit():
        filename = _save_photo(form.photo.data)
        new_employee = Employee(
            name=form.name.data,
            position=form.position.data,
            salary=form.salary.data,
            department_id=form.department_id.data,
            photo=filename    
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
    form = EmployeeForm(obj=employee)

    # Authorization check
    if current_user.role == 'department_manager' and employee.department_id != current_user.department_id:
        flash('You are not authorized to edit this employee.', 'danger')
        return redirect(url_for('main.list_employees'))

    if current_user.role == 'department_manager':
        form.department_id.choices = [(current_user.department_id, current_user.department.name)]
    else:
        form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]

    if form.validate_on_submit():
        employee.name = form.name.data
        employee.position = form.position.data
        employee.salary = form.salary.data
        employee.department_id = form.department_id.data
        new_file = form.photo.data 
        if new_file and new_file.filename:
            filename = _save_photo(new_file)
            if filename:
                if employee.photo:
                    try: os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], employee.photo))
                    except: pass
                employee.photo = filename
        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('main.list_employees'))

    return render_template('employees/edit.html', form=form, employee=employee)

# ------------------------
# Delete Employee
# ------------------------
@bp.route('/employee/delete/<int:id>', methods=['POST'])
@login_required
def delete_employee(id):
    employee = Employee.query.get_or_404(id)

    # Authorization check
    if current_user.role == 'department_manager' and employee.department_id != current_user.department_id:
        flash('You are not authorized to delete this employee.', 'danger')
        return redirect(url_for('main.list_employees'))

    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('main.list_employees'))


def _save_photo(file_storage):
    if not file_storage:
        return None
    
    #makes sure that used file has no dangerous paths
    original = secure_filename(file_storage.filename or '') 
    if not original:
        return None  #if it has dangerous paths or is empty suer inputed invalid file
    
    '''
    # splitext("photo.png") → ("photo", ".png")

    # ext.lower() ensures case insensitivity (.JPG → .jpg).

    # Check if the extension (without .) is in ALLOWED_IMAGE_EXTENSIONS.
    # This is a safety layer, in case the user renames a .exe file to .jpg.

    ext = os.path.splitext(original)[1].lower()  
    if ext.replace('.', '') not in current_app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return None
    '''

    # uuid.uuid4().hex gives a random 32 charachter string and makes it so no two users overwrite each others file
    unique_name = uuid.uuid4().hex
    # if blocked comment is used this line changes into
    # unique_name = f"{uuid.uuid4().hex}{ext}" 
    # ext appends the original file extansion to the unique string (.jpg, .png, .gif)
    
    # joins configured upload folder (uploads) with the unique filename
    dest_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)

    file_storage.save(dest_path)
    return unique_name


# ------------------------
# Departments: List
# ------------------------
@bp.route('/departments')
@login_required
def list_departments():
    if current_user.role == 'department_manager':
        if current_user.department_id:
            departments = Department.query.filter_by(id=current_user.department_id).all()
        else:
            departments = []
            flash('You are not assigned to any department yet.', 'warning')
    else:
        # administrator
        departments = Department.query.all()
    return render_template('departments/list.html', departments=departments)



# ------------------------
# Departments: Add (Admin only)
# ------------------------
@bp.route('/department/add', methods=['GET', 'POST'])
@login_required
def add_department():
    if current_user.role != 'administrator':
        flash('Only administrators can add departments.', 'danger')
        return redirect(url_for('main.list_departments'))

    form = DepartmentForm()
    if form.validate_on_submit():
        d = Department(name=form.name.data.strip())
        db.session.add(d)
        db.session.commit()
        flash('Department added.', 'success')
        return redirect(url_for('main.list_departments'))
    return render_template('departments/add.html', form=form)


# ------------------------
# Departments: Edit (Admin only)
'''
@bp.route('/department/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    if current_user.role != 'administrator':
        flash('Only administrators can edit departments.', 'danger')
        return redirect(url_for('main.list_departments'))

    dept = Department.query.get_or_404(id)
    form = DepartmentForm(obj=dept)
    if form.validate_on_submit():
        dept.name = form.name.data.strip()
        db.session.commit()
        flash('Department updated.', 'success')
        return redirect(url_for('main.list_departments'))
    return render_template('departments/edit.html', form=form)
'''

# ------------------------
# Departments: Delete (Admin only)
# ------------------------
@bp.route('/department/delete/<int:id>', methods=['POST'])
@login_required
def delete_department(id):
    if current_user.role != 'administrator':
        flash('Only administrators can delete departments.', 'danger')
        return redirect(url_for('main.list_departments'))

    dept = Department.query.get_or_404(id)
    if dept.employees:
        flash('Cannot delete a department that still has employees.', 'warning')
        return redirect(url_for('main.list_departments'))

    db.session.delete(dept)
    db.session.commit()
    flash('Department deleted.', 'success')
    return redirect(url_for('main.list_departments'))


@bp.route('/managers')
@login_required
def list_managers():
    if current_user.role != 'administrator':
        flash('Access denied. Only Admins can view this page.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    managers = User.query.filter_by(role='department_manager').all()

    # Render the department manager dashboard template
    return render_template('managers/list.html',managers=managers)

@bp.route('/managers/add', methods=['GET' , 'POST'])
@login_required
def add_managers():
    if current_user.role != 'administrator':
        flash('Access denied. Only Admins can add department managers.', 'danger')
        return redirect(url_for('main.dashboard'))
    form = ManagerForm()

    free_departments = Department.query.filter(~Department.manager.any()).all()
    form.department_id.choices = [(dept.id, dept.name) for dept in free_departments]

    if not free_departments:
        flash('No available departments without a manager.', 'warning')
        return redirect(url_for('main.dashboard'))

    if form.validate_on_submit():
        new_manager = User(
            username=form.username.data.strip(),
            password=form.password.data.strip(),  
            role='department_manager',
            department_id=form.department_id.data
        )
        db.session.add(new_manager)
        db.session.commit()
        flash('Department Manager added successfully!', 'success')
        return redirect(url_for('main.list_managers'))

    return render_template('managers/add.html', form=form)


@bp.route('/managers/delete/<int:id>', methods=['POST'])
def delete_managers(id):
    manager = User.query.get_or_404(id)

    # Only allow deleting department managers
    if manager.role != 'department_manager':
        flash('You can only delete department managers.', 'danger')
        return redirect(url_for('main.list_managers'))

    db.session.delete(manager)
    db.session.commit()
    flash(f'Manager "{manager.username}" deleted successfully.', 'success')
    return redirect(url_for('main.list_managers'))


@bp.route('/managers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_managers(id):
    manager = User.query.get_or_404(id)

    # Only department managers can be edited here
    if manager.role != 'department_manager':
        flash('You can only edit department managers.', 'danger')
        return redirect(url_for('main.list_managers'))

    form = ManagerForm(obj=manager)  # Make sure you have a ManagerForm similar to EmployeeForm

    # Authorization check — managers can only edit themselves
    if current_user.role == 'department_manager' and manager.id != current_user.id:
        flash('You are not authorized to edit this manager.', 'danger')
        return redirect(url_for('main.list_managers'))

    if current_user.role == 'department_manager':
        # Department managers can only stay in their current department
        form.department_id.choices = [
            (current_user.department_id, current_user.department.name)
        ]
    else:
        # Admin: show all free departments + current one
        free_departments = Department.query.filter(~Department.manager.any()).all()
        if manager.department and manager.department not in free_departments:
            free_departments.append(manager.department)
        form.department_id.choices = [(d.id, d.name) for d in free_departments]

    if form.validate_on_submit():
        manager.username = form.username.data
        if hasattr(manager, 'email'):
            manager.email = form.email.data
        manager.department_id = form.department_id.data
        db.session.commit()
        flash('Manager updated successfully!', 'success')
        return redirect(url_for('main.list_managers'))

    return render_template('managers/edit.html', form=form, manager=manager)

