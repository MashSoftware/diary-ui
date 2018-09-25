from flask import flash, redirect, render_template, request, url_for
from werkzeug.exceptions import Forbidden
from werkzeug.urls import url_parse

from app import app
from app.forms import (LogInForm, PasswordForm, ProfileForm, RegisterChildForm,
                       UserForm)
from app.models import Child, User
from flask_login import current_user, login_required, login_user, logout_user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('view_diary'))

    form = UserForm()
    if form.validate_on_submit():
        user = User()
        new_user = user.create(form.password.data, form.first_name.data, form.last_name.data, form.email_address.data)
        flash('Thanks for signing up!', 'success')
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
            flash('Invalid email address or password.', 'danger')
            return redirect(url_for('login'))
        login_user(authenticated_user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('view_diary')
        flash('Welcome back {0}!'.format(current_user.first_name), 'success')
        return redirect(next_page)
    return render_template('log_in.html', title='Log in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('index'))


@app.route("/users/<uuid:id>", methods=['GET'])
@login_required
def get_user(id):
    if str(id) != current_user.id:
        raise Forbidden()
    return render_template('user.html', title='My profile')


@app.route("/users/<uuid:id>/edit", methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if str(id) != current_user.id:
        raise Forbidden()

    form = ProfileForm()
    if form.validate_on_submit():
        current_user.update(str(id), form.first_name.data, form.last_name.data, form.email_address.data)
        flash('Your profile has been updated', 'success')
        return redirect(url_for('get_user', id=str(current_user.id)))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email_address.data = current_user.email_address
    return render_template('update_profile.html', title='Update profile', form=form)


@app.route("/users/<uuid:id>/change-password", methods=['GET', 'POST'])
@login_required
def change_password(id):
    if str(id) != current_user.id:
        raise Forbidden()

    form = PasswordForm()
    if form.validate_on_submit():
        current_user.update(id=str(id), password=form.new_password.data)
        flash('Your password has been changed', 'success')
        return redirect(url_for('get_user', id=str(current_user.id)))

    return render_template('change_password.html', title='Change password', form=form)


@app.route("/users/<uuid:id>/delete", methods=['GET'])
@login_required
def delete_user(id):
    if str(id) != current_user.id:
        raise Forbidden()

    user = User()
    logout_user()
    if user.delete(id) is True:
        flash('Your account has been permanently deleted.', 'success')
        return redirect(url_for('index'))


@app.route('/register-child', methods=['GET', 'POST'])
@login_required
def register_child():
    form = RegisterChildForm()
    if form.validate_on_submit():
        child = Child()
        child.create(form.first_name.data, form.last_name.data, str(form.date_of_birth.data), [current_user.id])
        flash('{0} has been registered'.format(form.first_name.data), 'success')
        return redirect(url_for('view_children'))
    return render_template('register_child.html', title='Register a child', form=form)


@app.route('/children', methods=['GET'])
@login_required
def view_children():
    child = Child()
    children = []
    for id in current_user.children:
        children.append(child.get(id))
    return render_template('children.html', title="My children", children=children)


@app.route('/diary', methods=['GET'])
@login_required
def view_diary():
    return render_template('diary.html', title="My diary")
