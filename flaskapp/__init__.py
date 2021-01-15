from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
# from flaskapp.config import Config
from dynaconf import FlaskDynaconf
from config import settings
# create and configure the app

# Instances of extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
# This is structured so that we can use each extension object of multiple apps


def create_app():
    # Creating of main app
    app = Flask(__name__)

    # Manually setting SQLALCHEMY variables to avoid minor errors
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Using Dynaconf extension for configuration management
    FlaskDynaconf(app)
    app.config.from_object(settings)
    app.config.load_extensions()

    # db.init_app(app)
    # bcrypt.init_app(app)
    login_manager.init_app(app)  # For some reason have to keep uncommented ??????????????????
    # mail.init_app(app)

    # Importing blueprints
    from flaskapp.posts.routes import posts
    from flaskapp.users.routes import users
    from flaskapp.main.routes import main
    from flaskapp.auth.routes import auth
    from flaskapp.threads.routes import threads
    from flaskapp.errors.handlers import errors

    # Initializing blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(threads)
    app.register_blueprint(errors)

    return app
