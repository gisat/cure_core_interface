from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(400)
def error_400(error):
    return render_template('errors/error.xml', error=error), 400

@errors.app_errorhandler(501)
def error_501(error):
    return render_template('errors/error.xml', error=error), 501

