from flask import render_template

from app import app


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', title='Not found'), 404


@app.errorhandler(500)
def internal_server(error):
    return render_template('error.html', title='Internal Server Error'), 500
