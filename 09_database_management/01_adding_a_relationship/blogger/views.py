from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify

from . models import User, Post, db
from . forms import AddPostForm, SignUpForm, SignInForm, AboutUserForm

from blogger import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts')
def show_posts():
    if session['user_available']:
        posts = Post.query.all()
        user = User.query.all()
        return render_template('posts.html', posts=posts, user=user)
    flash('User is not Authenticated')
    return redirect(url_for('index'))


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if session['user_available']:
        blogpost = AddPostForm(request.form)
        us = User.query.filter_by(username=session['current_user']).first()
        if request.method == 'POST':
            bp = Post(blogpost.title.data, blogpost.description.data, us)
            db.session.add(bp)
            db.session.commit()
            return redirect(url_for('show_posts'))
        return render_template('add.html', blogpost=blogpost)
    flash('User is not Authenticated')
    return redirect(url_for('index'))


@app.route('/delete/<int:pid>/<post_owner>', methods=('GET', 'POST'))
def delete_post(pid, post_owner):
    if session['current_user'] == post_owner:
        me = Post.query.get(pid)
        db.session.delete(me)
        db.session.commit()
        return redirect(url_for('show_posts'))
    flash('You are not a valid user to Delete this Post')
    return redirect(url_for('show_posts'))


@app.route('/update/<pid>/<post_owner>', methods=('GET', 'POST'))
def update_post(pid, post_owner):
    if session['current_user'] == post_owner:
        me = Post.query.get(pid)
        blogpost = AddPostForm(obj=me)
        if request.method == 'POST':
            bpost = Post.query.get(pid)
            bpost.title = blogpost.title.data
            bpost.description = blogpost.description.data
            db.session.commit()
            return redirect(url_for('show_posts'))
        return render_template('update.html', blogpost=blogpost)
    flash('You are not a valid user to Edit this Post')
    return redirect(url_for('show_posts'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        if existing_user:
            flash('Username or Email already exists. Please choose another.')
            return redirect(url_for('signup'))

        user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            username=form.username.data,
            password=form.password.data,
            email=form.email.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please sign in.')
        return redirect(url_for('signin'))
    return render_template('signup.html', signupform=form)



@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('Email not found. Please sign up first.')
            return redirect(url_for('signin'))

        if user.password != form.password.data:
            flash('Incorrect password.')
            return redirect(url_for('signin'))

        session['current_user'] = user.username
        session['user_available'] = True
        flash('Signed in successfully!')
        return redirect(url_for('show_posts'))

    return render_template('signin.html', signinform=form)

@app.route('/about_user')
def about_user():
    aboutuserform = AboutUserForm()
    if session['user_available']:
        user = User.query.filter_by(username=session['current_user']).first()
        return render_template('about_user.html', user=user, aboutuserform=aboutuserform)
    flash('You are not a Authenticated User')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    session['user_available'] = False
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
