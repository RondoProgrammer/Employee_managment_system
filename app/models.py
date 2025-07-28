from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db


class Administrator(UserMixin, db.Model):
    __tablename__ = 'administrators'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Administrator {self.name}>'
    

class DepartmentManager(UserMixin, db.Model):
    __tablename__ = 'department_managers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    
    #db.relationship sets up a relationship between two model classes in your code — not directly in the database.
    #unique=True ensures each manager can be assigned to only one department
    #uselist=False makes the relationship one-to-one from Department side
    department = db.relationship('Department', backref=db.backref('manager',uselist=False))

    def __repr__(self):
        return f'<DepartmentManager {self.name}>'


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    # Foreign key to link each manager to a department
    manager_id = db.Column(db.Integer, db.ForeignKey('department_managers.id'), nullable=False)

    #lazy=True 
    #Added relationship with employee here (not necessary in employee anymore bc its handled from backref)
    employees = db.relationship('Employee', backref='department', lazy=True)

    def __repr__(self):
        return f'<Department {self.name}>'


class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True, )
    name = db.Column(db.String(64), nullable=False)
    position = db.Column(db.String(64), nullable=False)
    salary = db.Column(db.Float, nullable=False)

    # Foreign key to link each employee to a department
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)


    #creates a string of the above, helpful when debugging
    def __repr__(self):
        return f'<Employee {self.name}>'
