from datetime import datetime

from flask import Flask, render_template, url_for, flash , redirect  
from forms import RegistrationForm, LoginForm
from SECRET_KEY import SECRET_KEY
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# prevent CSRF 
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

# nullable = FALSE : cannot be null

# Create table 'USER', 'POST'
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # Instead of print __main__ object, but as this instead
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"




# Variable
post = [
    {'author': 'Saran Pannasuriyaporn',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Dec 31, 2021'
        },
    {'author': 'Nuchpol Arpassompob',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Jan 1, 2022'
        }]        
            



#Treat "/" and "/about" as the same routes
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=post)

@app.route("/about")
def about():
    return render_template('about.html',title='about')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)







# debug = True : automatically update without rerun
if __name__ == "__main__":
    app.run(debug=False)

