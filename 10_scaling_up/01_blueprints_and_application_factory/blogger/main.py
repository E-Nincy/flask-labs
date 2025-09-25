from flask import Blueprint, render_template, session, flash, redirect, url_for
from .forms import AboutUserForm
from .models import User

# Create main blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main.route('/about_user')
def about_user():
    """Display the current user's profile"""
    if session.get('user_available'):
        user = User.query.filter_by(username=session['current_user']).first()
        form = AboutUserForm()
        return render_template('about_user.html', user=user, aboutuserform=form)
    flash('You are not Authenticated')
    return redirect(url_for('main.index'))
