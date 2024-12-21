from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from database.init_db import db

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Validate that all fields are provided
        if not name or not email or not username or not password:
            flash('All fields are required!', 'danger')
            return render_template('register.html')

        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists!', 'danger')
            return render_template('register.html')

        # Create a new user
        new_user = User(name=name, email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login.login'))  # Redirect to login page

    return render_template('register.html')