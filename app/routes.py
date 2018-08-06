from flask import flash, redirect, render_template, url_for

from app import app
from app.forms import ChildForm, UserForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Matt'}
    return render_template('index.html', title='Home', user=user)


@app.route('/users', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        flash('Success!')
        return redirect(url_for('index'))
    return render_template('user.html', title='Create user', form=form)


@app.route('/children', methods=['GET', 'POST'])
def create_child():
    form = ChildForm()
    if form.validate_on_submit():
        flash('Success!')
        return redirect(url_for('index'))
    return render_template('child.html', title='Register child', form=form)
