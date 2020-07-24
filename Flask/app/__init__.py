from flask import Flask
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
cors = CORS(app)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
ma = Marshmallow(app)

from app.controllers import default,login,api
