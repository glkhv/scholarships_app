from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SECRET_KEY'] = 'sajdkq37432878fjjlla324fvcx'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'static/sert'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.jinja_env.add_extension('jinja2.ext.loopcontrols')

db = SQLAlchemy(app)
ma = Marshmallow(app)
