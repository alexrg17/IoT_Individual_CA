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
            session['role'] = user.role  # Store the user's role in the session
            flash('Login successful!', 'success')

            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin.manage_users'))  # Redirect admin to the admin dashboard
            return redirect(url_for('main.home'))  # Redirect normal users to the home page

        flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@login_blueprint.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login.login'))