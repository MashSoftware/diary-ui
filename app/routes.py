from flask import flash, redirect, render_template, request, url_for
from werkzeug.urls import url_parse
from werkzeug.exceptions import Forbidden

from app import app
from app.forms import LogInForm, RegisterChildForm, SignUpForm
from app.models import User
from flask_login import current_user, login_required, login_user, logout_user


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignUpForm()
    if form.validate_on_submit():
        user = User()
        new_user = user.create(form.password.data, form.first_name.data, form.last_name.data, form.email_address.data)
        flash('{0} {1} signed up!'.format(new_user.first_name, new_user.last_name))
        return redirect(url_for('get_user', id=str(new_user.id)))

    return render_template('sign_up.html', title='Create a new account', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LogInForm()
    if form.validate_on_submit():
        user = User()
        authenticated_user = user.login(form.email_address.data, form.password.data)
        if authenticated_user is None:
            flash('Invalid email address or password.')
            return redirect(url_for('login'))
        login_user(authenticated_user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash('Welcome back!')
        return redirect(next_page)
    return render_template('log_in.html', title='Log in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have Logged out.')
    return redirect(url_for('index'))


@app.route("/users/<uuid:id>", methods=['GET'])
@login_required
def get_user(id):
    if str(id) != current_user.id:
        raise Forbidden()
    return render_template('user.html', title='My profile')


@app.route('/register-child', methods=['GET', 'POST'])
@login_required
def create_child():
    form = RegisterChildForm()
    if form.validate_on_submit():
        flash('Registered child!')
        return redirect(url_for('index'))
    return render_template('child.html', title='Register a child', form=form)
