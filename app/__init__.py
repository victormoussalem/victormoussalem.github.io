from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

#TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '/static')
#print TEMPLATE_DIR

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
