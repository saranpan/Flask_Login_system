from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt 
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import secrets,os


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


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=post)

@app.route("/about")
def about():
    return render_template('about.html',title='about')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('home')

    form = RegistrationForm()
    if form.validate_on_submit():
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect('home')

    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            #authenticated user (pass in user (User which has mixin so it can pass 'current_user'))
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            
            next_page = request.args.get('next')

            return redirect(url_for(next_page)) if next_page else redirect(url_for('home'))
      
        
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/home')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    #f_ext as file name (eg. JPG, PNG)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\profile_pics', picture_fn)
    
    

    #To save the memory of our database
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account" , methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            image_file_name = save_picture(form.picture.data)
            current_user.image_file = image_file_name

        if form.username.data:
            current_user.username = form.username.data

        if form.email.data:
            current_user.email = form.email.data
            
        
        #current_user.image_file = 
        db.session.commit()


    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='account',image_file=image_file, form=form)

