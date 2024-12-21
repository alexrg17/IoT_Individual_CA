from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from database.init_db import db
from werkzeug.security import check_password_hash

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the user from the database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Login successful
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))

        flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@login_blueprint.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login.login'))