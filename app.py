from flask import Flask, render_template, session, redirect, url_for
from database.init_db import db, init_db
from controllers.login_controller import login_blueprint
from controllers.register_controller import register_blueprint  # Import the register blueprint
import config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Initialize the database
init_db(app)

# Register blueprints
app.register_blueprint(login_blueprint)  # Register the login blueprint
app.register_blueprint(register_blueprint)  # Register the register blueprint

# Home Route
@app.route('/')
def home():
    # Check if user is logged in
    if 'user_id' in session:
        return render_template('index.html')  # Render your index page
    return redirect(url_for('login.login'))  # Redirect to login if not logged in

if __name__ == "__main__":
    app.run(debug=True)