from flask import Flask
from flaskext.markdown import Markdown
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from ccsi.config import config
from ccsi.app.routes import SearchEndpointsFactory



#extension
db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'forms.login'

def create_endpoints():
    SearchEndpointsFactory.create(config.ENDPOINTS)


def create_app(config_class=config):
    # initialize app
    app = Flask(__name__)

    Markdown(app)
    app.config.from_object(config)

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

    # blueprint registering
    # app modules
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(forms)

    # search api
    from ccsi.app.routes import docs, search_api

    # swagger
    from ccsi.app.api_spec import spec
    app.config.update({
        'APISPEC_SPEC': spec,
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
    })

    with app.app_context():
        search_api.init_app(app)
        docs.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()


    return app
