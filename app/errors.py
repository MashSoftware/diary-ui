from flask import render_template

from app import app


@app.errorhandler(403)
def forbidden(error):
    return render_template('error.html', title='Forbidden'), 403


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', title='Page not found'), 404


@app.errorhandler(500)
def internal_server(error):
    return render_template('error.html', title='Internal server error'), 500
