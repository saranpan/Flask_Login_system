
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new" , methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('You have created a new post!', 'success')

        return redirect(url_for('main.home')) 

    return render_template('create_post.html',title='New Post', form=form, legend='Create New Post')

@posts.route("/post/<int:post_id>" , methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()

    if request.method == "GET":        
        form.title.data = post.title
        form.content.data = post.content

    return render_template('post.html',title=post.title, post=post,form=form)

@posts.route("/post/<int:post_id>/update" , methods=['POST'])
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
        return redirect(url_for('posts.post',post_id=post.id))
        #Not a blank space form
    else:
        flash('Update Failed! Make sure the letter in content is higher than 3','danger')
        return redirect(url_for('posts.post',post_id=post.id))

@posts.route("/post/<int:post_id>/delete" , methods=['POST'])
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
    return redirect(url_for('main.home'))

