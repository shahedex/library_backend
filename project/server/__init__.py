# project/server/__init__.py

import os
import logging

from flask import Flask
from logging.config import dictConfig
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)