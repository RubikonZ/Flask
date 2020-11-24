import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# create and configure the app
app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

from flaskapp import routes