from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt 
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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

        flash(f'Account created for {form.username.data}!')
        return redirect(url_for('home'))
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

@app.route("/account")
@login_required
def account():
    return render_template('account.html',title='account')
    """
    #similar to these below commands (but also flash & has query next to the next request webpage)

    if current_user.is_authenticated:
        return render_template('account.html',title='account')
    else:
        return redirect('login') 
        # This return (/login) instead of (/login?next=%2Faccount)  
    """

