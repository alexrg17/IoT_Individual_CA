from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
import datetime
from models.user import User
from database.init_db import db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()
# Initialize Fernet cipher using a secret key
cipher = Fernet(os.getenv("Cipher_Key").encode())

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the user from the database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Generate JWT token
            jwttoken = create_access_token(
                identity={"username": username, "role": user.role},
                expires_delta=datetime.timedelta(minutes=15)
            )

            # Encrypt the JWT token
            encrypted_jwt = cipher.encrypt(jwttoken.encode())

            # Debug: Print encrypted token
            print("Encrypted JWT Token:", encrypted_jwt.decode())

            # Set session data
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role  # Store the user's role in the session

            # Set encrypted JWT in cookie and redirect
            response = redirect(url_for('main.home'))
            response.set_cookie('jwttoken', encrypted_jwt.decode(), httponly=True)
            return response

        # Handle invalid credentials
        flash('Invalid username or password.', 'danger')
        return render_template('login.html')

    return render_template('login.html')

@login_blueprint.route('/logout')
def logout():
    # Clear session data
    session.clear()
    
    # Clear the JWT cookie
    response = redirect(url_for('login.login'))
    response.delete_cookie('jwttoken')
    flash('You have been logged out.', 'info')
    return response