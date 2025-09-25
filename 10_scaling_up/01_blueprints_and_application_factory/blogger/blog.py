from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .models import Post, User
from .forms import AddPostForm
from . import db

# Create blog blueprint
blog = Blueprint('blog', __name__)

@blog.route('/posts')
def show_posts():
    """Display all posts for authenticated users"""
    if session.get('user_available'):
        posts = Post.query.all()
        users = User.query.all()
        return render_template('posts.html', posts=posts, user=users)
    flash('User is not Authenticated')
    return redirect(url_for('main.index'))

@blog.route('/add', methods=['GET', 'POST'])
def add_post():
    if not session.get('user_available'):
        flash('You are not authenticated')
        return redirect(url_for('main.index'))

    form = AddPostForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=session['current_user']).first()
        post = Post(title=form.title.data, description=form.description.data, puid=user.uid)
        db.session.add(post)
        db.session.commit()
        flash('Post added successfully!')
        return redirect(url_for('blog.show_posts'))

    return render_template('add.html', blogpost=form)


@blog.route('/update/<int:pid>/<post_owner>', methods=['GET', 'POST'])
def update_post(pid, post_owner):
    """Update a post if the current user is the owner"""
    if session.get('current_user') == post_owner:
        post = Post.query.get(pid)
        form = AddPostForm(obj=post)
        if request.method == 'POST':
            post.title = form.title.data
            post.description = form.description.data
            db.session.commit()
            return redirect(url_for('blog.show_posts'))
        return render_template('update.html', blogpost=form)
    flash('You are not allowed to edit this post')
    return redirect(url_for('blog.show_posts'))

@blog.route('/delete/<int:pid>/<post_owner>')
def delete_post(pid, post_owner):
    """Delete a post if the current user is the owner"""
    if session.get('current_user') == post_owner:
        post = Post.query.get(pid)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('blog.show_posts'))
    flash('You are not allowed to delete this post')
    return redirect(url_for('blog.show_posts'))
