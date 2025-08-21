from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users' # This table will store both Administrators and Department Managers

    id = db.Column(db.Integer, primary_key=True) # Primary Key
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(32), nullable=False)  # administrator or department_manager 
 
    # Foreign key to the Department table (for DepartmentManager) 
    # Nullable because admins might not belong to any department
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True) 

    # Relationship to Department table
    # - Allows access to the department object via user.department
    # - backref='manager' creates a reverse relationship from Department to User
    # - uselist=False indicates a one-to-one relationship (one manager per department)
    department = db.relationship('Department', backref='manager', uselist=False) 
    
    # String representation of the object, useful for debugging
    def __repr__(self):
        return f'<User {self.username}>'
    
    
class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

class Employee(db.Model):
    __tablename__ = 'employees'
    

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    position = db.Column(db.String(64), nullable=False)
    salary = db.Column(db.Float, nullable=False)

    photo = db.Column(db.String(256), nullable=True)
    
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    department = db.relationship('Department', backref='employees')