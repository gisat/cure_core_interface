from flask import Flask
from flaskext.markdown import Markdown
from flask_sqlalchemy import SQLAlchemy
from ccsi.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


#extension
db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'forms.login'

def create_app(config_class=Config):
    # initialize app
    app = Flask(__name__)
    Markdown(app)
    app.config.from_object(Config)

    #database
    db.init_app(app)
    #bcrypt
    bcrypt.init_app(app)
    #login
    login_manager.init_app(app)
    # blueprints
    from ccsi.main.routes import main
    from ccsi.errors.handlers import errors
    from ccsi.forms.routes import forms
    from ccsi.search.routes import search

    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(forms)
    app.register_blueprint(search)

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app
