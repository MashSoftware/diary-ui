from flask import flash, redirect, render_template, url_for

from app import app
from app.forms import LogInForm, RegisterChildForm, SignUpForm
from app.models import User


@app.route('/')
def index():
    user = {'username': 'Matt'}
    return render_template('index.html', title='Home', user=user)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User()
        new_user = user.create(form.password.data, form.first_name.data, form.last_name.data, form.email_address.data)
        flash('{0} {1} signed up!'.format(new_user["first_name"], new_user["last_name"]))
        return redirect(url_for('get_user', user_id=str(new_user["user_id"])))
    return render_template('sign_up.html', title='Sign up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        flash('{} logged in'.format(form.email_address.data))
        return redirect(url_for('index'))
    return render_template('log_in.html', title='Sign in', form=form)


@app.route("/users/<uuid:user_id>", methods=['GET'])
def get_user(user_id):
    user = User()
    result = user.get(user_id)
    return render_template('user.html', title='User profile', user=result)


@app.route('/register-child', methods=['GET', 'POST'])
def create_child():
    form = RegisterChildForm()
    if form.validate_on_submit():
        flash('Registered child!')
        return redirect(url_for('index'))
    return render_template('child.html', title='Register child', form=form)
