from flask import Flask
from flaskblog.SECRET_KEY import SECRET_KEY
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

print('__init__.py checked')

#run routes
from flaskblog import routes
