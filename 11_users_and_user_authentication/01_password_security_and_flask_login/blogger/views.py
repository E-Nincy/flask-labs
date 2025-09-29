from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . models import User, Post, db
from . forms import AddPostForm, SignUpForm, SignInForm, AboutUserForm

from blogger import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts')
@login_required
def show_posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts, user=current_user)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        bp = Post(
            title=form.title.data,
            description=form.description.data,
            puid=current_user.uid
        )
        db.session.add(bp)
        db.session.commit()
        flash('Post added successfully!', 'success')
        return redirect(url_for('show_posts'))
    else:
        print(form.errors) 
    return render_template('add.html', blogpost=form)


@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.uid:
        flash("You can't delete someone else's post!")
        return redirect(url_for('show_posts'))
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully.')
    return redirect(url_for('show_posts'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.uid:
        flash("You can't edit someone else's post!")
        return redirect(url_for('show_posts'))

    form = AddPostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        db.session.commit()
        flash('Post updated successfully.')
        return redirect(url_for('show_posts'))

    return render_template('update.html', blogpost=form, post=post)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signupform = SignUpForm(request.form)
    if request.method == 'POST':
        reg = User(
            signupform.firstname.data,
            signupform.lastname.data,
            signupform.username.data,
            signupform.password.data,
            signupform.email.data
        )
        db.session.add(reg)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('signin'))
    return render_template('signup.html', signupform=signupform)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    signinform = SignInForm()
    if request.method == 'POST':
        em = signinform.email.data
        log = User.query.filter_by(email=em).first()
        if log and log.verify_password(signinform.password.data):
            login_user(log)
            flash("Logged in successfully", "success")
            return redirect(url_for('show_posts'))
        else:
            flash("Invalid username or password", "danger")
    return render_template('signin.html', signinform=signinform)


@app.route('/about_user/<int:user_id>')
@login_required
def about_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('about_user.html', user=user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
