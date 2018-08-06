from flask_wtf import FlaskForm
from wtforms import (DateField, PasswordField, RadioField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired, Email, EqualTo, Length


class UserForm(FlaskForm):
    email_address = StringField('Email address', validators=[DataRequired(), Email()], description="We'll never share your email with anyone else.")
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=72)], description="Must be between 8 and 72 characters long.")
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    submit = SubmitField('Create')


class ChildForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    date_of_birth = DateField('Date of birth', validators=[DataRequired()])
    gender = RadioField('Gender', validators=[DataRequired()], choices=[('male', 'Male'), ('female', 'Female')])
    submit = SubmitField('Create')