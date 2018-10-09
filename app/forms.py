from datetime import date, datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, DateTimeField, DecimalField,
                     PasswordField, RadioField, SelectField, StringField,
                     TextAreaField)
from wtforms.validators import (Email, EqualTo, InputRequired, Length,
                                Optional, ValidationError)

from app.models import User


class UserForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(message="First name is required")])
    last_name = StringField('Last name', validators=[InputRequired(message="Last name is required")])
    email_address = StringField('Email address', validators=[InputRequired(message="Email address is required"), Email()],
                                description="We'll never share your email with anyone else.")
    password = PasswordField('Password', validators=[InputRequired(message="Password is required"), Length(min=8, max=72, message="Password must be between 8 and 72 characters long")],
                             description="Must be between 8 and 72 characters long.")
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(
        message="Please confirm your password"), EqualTo('password', message="Passwords must match.")])

    def validate_email_address(self, email_address):
        if User().search(email_address.data):
            raise ValidationError('Email address is already in use')


class LogInForm(FlaskForm):
    email_address = StringField('Email address', validators=[
                                InputRequired(message="Email address is required"), Email()])
    password = PasswordField('Password', validators=[InputRequired(message="Password is required"), Length(min=8, max=72, message="Password must be between 8 and 72 characters long")],
                             description="Must be between 8 and 72 characters long.")
    remember_me = BooleanField('Remember me')


class ProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(message="First name is required")])
    last_name = StringField('Last name', validators=[InputRequired(message="Last name is required")])
    email_address = StringField('Email address', validators=[InputRequired(message="Email address is required"), Email()],
                                description="We'll never share your email with anyone else.")

    def validate_email_address(self, email_address):
        if User().search(email_address.data):
            raise ValidationError('Email address is already in use')


class PasswordForm(FlaskForm):
    current_password = PasswordField('Current password', validators=[
                                     InputRequired(message="Current password is required"), Length(min=8, max=72, message="Current password must be between 8 and 72 characters long")])
    new_password = PasswordField('New password', validators=[InputRequired(message="New password is required"), Length(min=8, max=72, message="New password must be between 8 and 72 characters long")],
                                 description="Must be between 8 and 72 characters long.")
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(
        message="Please confirm your password"), EqualTo('new_password', message="Passwords must match.")])

    def validate_new_password(self, new_password):
        if new_password.data == self.current_password.data:
            raise ValidationError('New password must be different to current password')


class ChildForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(message="First name is required")])
    middle_name = StringField('Middle name', validators=[Optional()])
    last_name = StringField('Last name', validators=[InputRequired(message="Last name is required")])
    date_of_birth = DateField('Date of birth', validators=[InputRequired(message="Date of birth is required")])

    def validate_date_of_birth(self, date_of_birth):
        if date_of_birth.data > date.today():
            raise ValidationError('Date of birth must be in the past')


class UserSearchForm(FlaskForm):
    email_address = StringField('Email address', validators=[
                                InputRequired(message="Email address is required"), Email()])


class EventForm(FlaskForm):
    type = SelectField('Type', choices=[('sleep', 'Sleep'), ('feed', 'Feed'),
                                        ('change', 'Change')], validators=[InputRequired(message="Type is required")])
    started_at = DateTimeField('Started at', format='%d/%m/%Y %H:%M:%S',
                               validators=[InputRequired(message="Started at is required")], default=datetime.utcnow)
    ended_at = DateTimeField('Ended at', format='%d/%m/%Y %H:%M:%S',
                             validators=[Optional()], description="Leave blank if ongoing")
    amount = DecimalField('Amount', validators=[Optional()])
    unit = StringField('Unit', validators=[Optional()])
    side = RadioField('Side', choices=[('left', 'Left'), ('right', 'Right')], validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
