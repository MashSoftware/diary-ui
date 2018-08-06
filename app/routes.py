from flask import flash, redirect, render_template, url_for

from app import app
from app.forms import RegisterChildForm, SignUpForm, LogInForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Matt'}
    return render_template('index.html', title='Home', user=user)


@app.route('/signup', methods=['GET', 'POST'])
def create_user():
    form = SignUpForm()
    if form.validate_on_submit():
        flash('{} {} signed up!'.format(form.first_name.data, form.last_name.data))
        return redirect(url_for('index'))
    return render_template('sign_up.html', title='Sign up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        flash('{} logged in'.format(form.email_address.data))
        return redirect(url_for('index'))
    return render_template('log_in.html', title='Sign in', form=form)


@app.route('/register-child', methods=['GET', 'POST'])
def create_child():
    form = RegisterChildForm()
    if form.validate_on_submit():
        flash('Registered child!')
        return redirect(url_for('index'))
    return render_template('child.html', title='Register child', form=form)
