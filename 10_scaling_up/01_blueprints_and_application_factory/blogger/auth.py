from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .forms import SignInForm, SignUpForm
from .models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            session['current_user'] = user.username
            session['user_available'] = True
            return redirect(url_for('blog.show_posts'))
    return render_template('signin.html', signinform=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            username=form.username.data,
            password=form.password.data,
            email=form.email.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.signin'))
    return render_template('signup.html', signupform=form)
