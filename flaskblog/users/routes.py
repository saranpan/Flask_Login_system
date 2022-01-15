from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestPasswordForm, ResetPasswordForm)

from flaskblog.users.utils import save_picture, send_reset_mail


users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
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
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():        
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            #authenticated user (pass in user (User which has mixin so it can pass 'current_user'))
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            
            next_page = request.args.get('next')

            # replace redirect(url_for(next_page)) by redirect(next_page)
            return redirect(next_page) if next_page else redirect(url_for('main.home'))      
        
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account" , methods=['GET', 'POST'])
@login_required  # If validate by current_user.is_authenticated is True, then allow
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

        flash('Your account has been updated!', 'success')
        #current_user.image_file = 
        db.session.commit()
        return redirect(url_for('users.account'))


    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html',title='account',image_file=image_file, form=form)


@users.route("/<string:username>")
@login_required
def user_page(username):
    page= request.args.get('page',1,type=int)

    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=3,page=page)
    return render_template('username_page.html',user=user,posts=posts)
      
# Reset password zone 
@users.route("/request_password", methods=['GET', 'POST'])
def request_password():
    if current_user.is_authenticated:
        return redirect('home')

    form = RequestPasswordForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        send_reset_mail(user)
        flash(f'We have sent the request link to {form.email.data}! check it out !','success')

        # How we can save the token ?

        return redirect(url_for('users.login'))

    return render_template('request_password.html', title='Request Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect('home')

    user = User.verify_reset_token(token)

    if user is None:
        flash('This is expired token or invalid token, please try again','danger')
        return redirect('home')

    
    #user = User.query.filter_by(id=user_id).first()
    form = ResetPasswordForm()

    if form.validate_on_submit():     
        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        flash(f'Your password has been changed !','success')


        return redirect(url_for('users.login'))

    return render_template('reset_password.html', title='Reset Password', form=form)
