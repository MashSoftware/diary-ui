from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class UserForm(FlaskForm):
    email_address = StringField('Email address', validators=[DataRequired(), Email()], description="We'll never share your email with anyone else.")
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], description="Must be at least 8 characters long.")
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    submit = SubmitField('Create')
