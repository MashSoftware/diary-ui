from datetime import date

from flask import flash, redirect, render_template, request, url_for
from werkzeug.exceptions import Forbidden
from werkzeug.urls import url_parse

from app import app
from app.forms import (BreastfeedForm, ChangeForm, ChildForm, FormulaForm,
                       LogInForm, PasswordForm, ProfileForm, SleepForm,
                       UserForm, UserSearchForm)
from app.models import Child, Event, User
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
        user = User().create(form.password.data, form.first_name.data.title(),
                             form.last_name.data.title(), form.email_address.data)
        flash('Thanks for signing up!', 'success')
        return redirect(url_for('get_user', id=str(user.id)))

    return render_template('sign_up.html', title='Create an account', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LogInForm()
    if form.validate_on_submit():
        user = User().login(form.email_address.data, form.password.data)
        if user is None:
            flash('Invalid email address or password.', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
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


@app.route("/users/<uuid:id>/update-profile", methods=['GET', 'POST'])
@login_required
def update_profile(id):
    if str(id) != current_user.id:
        raise Forbidden()

    form = ProfileForm()
    if form.validate_on_submit():
        current_user.update_profile(str(id), form.first_name.data.title(),
                                    form.last_name.data.title(), form.email_address.data)
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
        user = User().change_password(str(id), form.current_password.data, form.new_password.data)
        if user is None:
            flash('Invalid password.', 'danger')
            return redirect(url_for('change_password', id=id))
        flash('Your password has been changed', 'success')
        return redirect(url_for('get_user', id=str(current_user.id)))

    return render_template('change_password.html', title='Change password', form=form)


@app.route("/users/<uuid:id>/delete", methods=['GET'])
@login_required
def delete_user(id):
    if str(id) != current_user.id:
        raise Forbidden()

    logout_user()
    if User().delete(id) is True:
        flash('Your account has been permanently deleted.', 'success')
        return redirect(url_for('index'))


@app.route('/register-child', methods=['GET', 'POST'])
@login_required
def register_child():
    form = ChildForm()
    if form.validate_on_submit():
        child = Child().create(form.first_name.data.title(), form.last_name.data.title(),
                               str(form.date_of_birth.data), [current_user.id])
        flash('{0} {1} has been registered'.format(child["first_name"], child["last_name"]), 'success')
        return redirect(url_for('view_children'))
    return render_template('register_child.html', title='Register a child', form=form)


@app.route('/children', methods=['GET'])
@login_required
def view_children():
    children = []
    for id in current_user.children:
        # Should have API route to get array of children for a user ID
        # One API call rather than X many
        children.append(Child().get(id))
    return render_template('children.html', title="My children", children=children)


@app.route('/children/<uuid:id>', methods=['GET'])
@login_required
def get_child(id):
    if str(id) not in current_user.children:
        raise Forbidden()

    child = Child().get(id)
    return render_template('child.html', title='{0} {1}'.format(child["first_name"], child["last_name"]), child=child)


@app.route('/children/<uuid:id>/update', methods=['GET', 'POST'])
@login_required
def update_child(id):
    if str(id) not in current_user.children:
        raise Forbidden()

    child = Child().get(id)
    form = ChildForm()

    if form.validate_on_submit():
        Child().update(str(id), form.first_name.data.title(), form.last_name.data.title(), str(form.date_of_birth.data), child["users"])
        flash('Child has been updated', 'success')
        return redirect(url_for('get_child', id=str(id)))
    elif request.method == 'GET':
        form.first_name.data = child["first_name"]
        form.last_name.data = child["last_name"]
        form.date_of_birth.data = date.fromisoformat(child["date_of_birth"])
    return render_template('update_child.html', title='Update child', form=form)


@app.route('/children/<uuid:id>/delete', methods=['GET'])
@login_required
def delete_child(id):
    if str(id) not in current_user.children:
        raise Forbidden()

    if Child().delete(id) is True:
        flash('Child has been permanently deleted.', 'success')
        return redirect(url_for('view_children'))


@app.route('/children/<uuid:id>/add', methods=['GET', 'POST'])
@login_required
def search_user(id):
    form = UserSearchForm()
    child = Child().get(id)

    if form.validate_on_submit():
        user = User().search(form.email_address.data)
        return render_template('user_search.html', title="Add a care giver to {0} {1}".format(child["first_name"], child["last_name"]), form=form, child=child, user=user)

    return render_template('user_search.html', title="Add a care giver to {0} {1}".format(child["first_name"], child["last_name"]), form=form, child=child)


@app.route('/diary', methods=['GET'])
@login_required
def view_diary():
    events = Event().get(current_user.children[0])
    return render_template('diary.html', title="My diary", events=events)


@app.route('/diary/add-sleep', methods=['GET', 'POST'])
@login_required
def add_sleep():
    form = SleepForm()
    if form.validate_on_submit():
        Event().create(
            user_id=current_user.id,
            child_id=current_user.children[0],
            type='sleep',
            started_at=str(form.started_at.data),
            ended_at=str(form.ended_at.data) if form.ended_at.data else None,
            feed_type=None,
            change_type=None,
            amount=None,
            unit=None,
            side=None,
            notes=form.notes.data)
        flash('Sleep has been added', 'success')
        return redirect(url_for('view_diary'))

    return render_template('sleep.html', title='Add sleep', form=form)


@app.route('/diary/add-breastfeed', methods=['GET', 'POST'])
@login_required
def add_breastfeed():
    form = BreastfeedForm()

    if form.validate_on_submit():
        pass

    return render_template('breastfeed.html', title='Add breastfeed', form=form)


@app.route('/diary/add-formula', methods=['GET', 'POST'])
@login_required
def add_formula():
    form = FormulaForm()
    if form.validate_on_submit():
        Event().create(
            user_id=current_user.id,
            child_id=current_user.children[0],
            type='feed',
            started_at=str(form.started_at.data),
            ended_at=str(form.ended_at.data) if form.ended_at.data else None,
            feed_type='formula',
            change_type=None,
            amount=float(form.amount.data),
            unit=form.unit.data,
            side=None,
            notes=form.notes.data)
        flash('Formula has been added', 'success')
        return redirect(url_for('view_diary'))
    return render_template('formula.html', title='Add formula', form=form)


@app.route('/diary/add-change', methods=['GET', 'POST'])
@login_required
def add_change():
    form = ChangeForm()

    if form.validate_on_submit():
        pass

    return render_template('change.html', title='Add change', form=form)
