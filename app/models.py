from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db

# Administrator model: represents users with full system access
class Administrator(UserMixin, db.Model):
    __tablename__ = 'administrator'



class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False )

    #creates a string of the aove, helpful when debugging
    def __repr__(self):
        return '<Name %r>' % self.name 
