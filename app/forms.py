from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, FileField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class DepartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Save')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    position = StringField('Position', validators=[DataRequired(), Length(max=64)])
    salary = FloatField('Salary', validators=[DataRequired()])
    department_id = SelectField('Department', coerce=int, validators=[DataRequired()])
    
    photo = FileField('Photo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Save')


class ManagerForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    department_id = SelectField('Departmen', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')
        