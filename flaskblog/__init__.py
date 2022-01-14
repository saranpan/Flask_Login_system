from flask import Flask
from flaskblog.SECRET_KEY import SECRET_KEY
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app) 
login_manager = LoginManager(app)

#direct to route 'login'
login_manager.login_view = 'login'
login_manager.login_message = u"Hey!! Please login before access to this page"
#bootstrap based
login_manager.login_message_category = 'danger'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_NOREPLY')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD_NOREPLY')
mail  = Mail(app)


#run routes
from flaskblog import routes
