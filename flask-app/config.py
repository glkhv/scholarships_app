from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SECRET_KEY'] = 
app.config['SQLALCHEMY_DATABASE_URI'] = 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']

UPLOAD_FOLDER = 'static/sert'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.jinja_env.add_extension('jinja2.ext.loopcontrols')

db = SQLAlchemy(app)
ma = Marshmallow(app)
