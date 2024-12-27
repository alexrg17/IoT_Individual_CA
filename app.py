from flask import Flask, session, redirect, url_for
from database.init_db import db, init_db
from controllers.login_controller import login_blueprint
from controllers.register_controller import register_blueprint
from controllers.main_controller import main_blueprint
from controllers.admin_controller import admin_blueprint  # Import the admin blueprint
import config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Initialize the database
init_db(app)

# Register blueprints
app.register_blueprint(login_blueprint)  # Register the login blueprint
app.register_blueprint(register_blueprint)  # Register the register blueprint
app.register_blueprint(main_blueprint, url_prefix='/')  # Register the main blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')  # Register the admin blueprint

# Redirect root to the appropriate endpoint based on user role
@app.route('/')
def home_redirect():
    if 'user_id' in session:
        # Check if the logged-in user is an admin
        if session.get('role') == 'admin':
            return redirect(url_for('admin.manage_users'))  # Redirect to the admin dashboard
        return redirect(url_for('main.home'))  # Redirect to the user home page
    return redirect(url_for('login.login'))  # Redirect to login if not logged in

if __name__ == "__main__":
    app.run(debug=True)