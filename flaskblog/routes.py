from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt 
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
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
    #/home?page=1 as default
    page= request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3,page=page)
    return render_template('home.html',posts=posts)

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

# Create new picture file 
def split_file_name(file_name):
    return file_name.split('.')[0]

def check_duplicate_file(check_file,all_file):
    name_list = list(map(split_file_name,all_file))
    if check_file in name_list:
        random_hex = secrets.token_hex(8)
        return check_duplicate_file(random_hex, all_file)
    else: 
        return check_file

def save_picture(form_picture):

    all_picture = os.listdir('flaskblog\static\profile_pics')
    
    # Prevent duplicated profile picture file name
    random_hex = check_duplicate_file(secrets.token_hex(8),all_picture)

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
        return redirect(url_for('account'))


    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html',title='account',image_file=image_file, form=form)

@app.route("/post/new" , methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('You have created a new post!', 'success')

        return redirect(url_for('home')) 

    return render_template('create_post.html',title='New Post', form=form, legend='Create New Post')

@app.route("/post/<int:post_id>" , methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()

    if request.method == "GET":        
        form.title.data = post.title
        form.content.data = post.content

    return render_template('post.html',title=post.title, post=post,form=form)

@app.route("/post/<int:post_id>/update" , methods=['POST'])
@login_required
def update_post(post_id):

    post = Post.query.get_or_404(post_id)
    form = PostForm()

    # prevent /update directly
    if current_user != post.author:
        abort(403)

    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        flash('The post is updated!', 'success')
        db.session.commit()
        return redirect(url_for('post',post_id=post.id))
        #Not a blank space form
    else:
        flash('Update Failed! Make sure the letter in content is higher than 3','danger')
        return redirect(url_for('post',post_id=post.id))

@app.route("/post/<int:post_id>/delete" , methods=['POST'])
@login_required
def delete_post(post_id):

    #no form required (just input button)
    # So, No get method, cuz we don't get any input as form type
    post =  Post.query.get_or_404(post_id)

    if current_user != post.author:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post is deleted!','success')
    return redirect(url_for('home'))


@app.route("/<string:username>")
@login_required
def user_page(username):
    page= request.args.get('page',1,type=int)

    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=3,page=page)
    print(f'Saran said {posts}')
    return render_template('username_page.html',user=user,posts=posts)
        
