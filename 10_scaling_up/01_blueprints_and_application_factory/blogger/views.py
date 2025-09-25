from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .models import User, Post
from .forms import AddPostForm, SignUpForm, SignInForm, AboutUserForm
from . import db

# Create blueprints
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
blog = Blueprint('blog', __name__)

# ===== Main routes =====
@main.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main.route('/about_user')
def about_user():
    """Show logged-in user info"""
    if session.get('user_available'):
        user = User.query.filter_by(username=session['current_user']).first()
        form = AboutUserForm()
        return render_template('about_user.html', user=user, aboutuserform=form)
    flash('You are not authenticated')
    return redirect(url_for('main.index'))

# ===== Auth routes =====
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            username=form.username.data,
            password=form.password.data,
            email=form.email.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now sign in.')
        return redirect(url_for('auth.signin'))
    return render_template('signup.html', signupform=form)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            session['current_user'] = user.username
            session['user_available'] = True
            flash(f'Welcome {user.username}!')
            return redirect(url_for('blog.show_posts'))
        flash('Invalid email or password')
    return render_template('signin.html', signinform=form)

@auth.route('/logout')
def logout():
    session.clear()
    session['user_available'] = False
    flash('Logged out successfully')
    return redirect(url_for('main.index'))

# ===== Blog routes =====
@blog.route('/posts')
def show_posts():
    """Show all posts"""
    if not session.get('user_available'):
        flash('You are not authenticated')
        return redirect(url_for('main.index'))

    posts = Post.query.all()
    users = User.query.all()
    return render_template('posts.html', posts=posts, user=users)

@blog.route('/add', methods=['GET', 'POST'])
def add_post():
    """Add a new post"""
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
    """Update an existing post"""
    if session.get('current_user') != post_owner:
        flash('You are not allowed to edit this post')
        return redirect(url_for('blog.show_posts'))

    post = Post.query.get(pid)
    form = AddPostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        db.session.commit()
        flash('Post updated successfully!')
        return redirect(url_for('blog.show_posts'))

    return render_template('update.html', blogpost=form)

@blog.route('/delete/<int:pid>/<post_owner>')
def delete_post(pid, post_owner):
    """Delete a post"""
    if session.get('current_user') != post_owner:
        flash('You are not allowed to delete this post')
        return redirect(url_for('blog.show_posts'))

    post = Post.query.get(pid)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!')
    return redirect(url_for('blog.show_posts'))
