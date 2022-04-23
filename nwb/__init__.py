import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app = Flask(__name__, static_folder=resource_path('static'), template_folder=resource_path('templates'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meetings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)


from nwb import routes