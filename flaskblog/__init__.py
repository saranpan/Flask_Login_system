from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from flaskblog.config import Config

#Utilities
db = SQLAlchemy()
bcrypt = Bcrypt() 

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = u"Please login before access to this page"
login_manager.login_message_category = 'danger'

mail  = Mail()


#Main App
def create_app(config_class=Config):
    app = Flask(__name__)
    print(Config.SECRET_KEY)

    #Load all config
    app.config.from_object(Config)

    # Initialize our utilities on app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Load all Blueprints
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
