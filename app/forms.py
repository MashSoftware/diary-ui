from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, DateTimeField, DecimalField,
                     PasswordField, RadioField, SelectField, StringField,
                     TextAreaField)
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional


class UserForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(message="First name is required")])
    last_name = StringField('Last name', validators=[InputRequired(message="Last name is required")])
    email_address = StringField('Email address', validators=[InputRequired(message="Email address is required"), Email()],
                                description="We'll never share your email with anyone else.")
    password = PasswordField('Password', validators=[InputRequired(message="Password is required"), Length(min=8, max=72)],
                             description="Must be between 8 and 72 characters long.")
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(
        message="Please confirm your password"), EqualTo('password', message="Passwords must match.")])


class LogInForm(FlaskForm):
    email_address = StringField('Email address', validators=[
                                InputRequired(message="Email address is required"), Email()])
    password = PasswordField('Password', validators=[InputRequired(message="Password is required")])
    remember_me = BooleanField('Remember me')


class ProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(message="First name is required")])
    last_name = StringField('Last name', validators=[InputRequired(message="Last name is required")])
    email_address = StringField('Email address', validators=[InputRequired(message="Email address is required"), Email()],
                                description="We'll never share your email with anyone else.")


class PasswordForm(FlaskForm):
    current_password = PasswordField('Current password', validators=[
                                     InputRequired(message="Current password is required")])
    new_password = PasswordField('New password', validators=[InputRequired(message="New password is required"), Length(min=8, max=72)],
                                 description="Must be between 8 and 72 characters long.")
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(
        message="Please confirm your password"), EqualTo('new_password', message="Passwords must match.")])


class ChildForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(message="First name is required")])
    last_name = StringField('Last name', validators=[InputRequired(message="Last name is required")])
    date_of_birth = DateField('Date of birth', validators=[InputRequired(message="Date of birth is required")])


class UserSearchForm(FlaskForm):
    email_address = StringField('Email address', validators=[InputRequired(message="Email address is required"), Email()])


class EventForm(FlaskForm):
    type = SelectField('Type', choices=[('sleep', 'Sleep'), ('feed', 'Feed'), ('change', 'Change')])
    started_at = DateTimeField('Started at', format='%d/%m/%Y %H:%M:%S', default=datetime.utcnow)
    ended_at = DateTimeField('Ended at', format='%d/%m/%Y %H:%M:%S')
    amount = DecimalField('Amount', validators=[Optional()])
    unit = StringField('Unit', validators=[Optional()])
    side = RadioField('Side', choices=[('left', 'Left'), ('right', 'Right')])
    description = TextAreaField('Description', validators=[Optional()])
