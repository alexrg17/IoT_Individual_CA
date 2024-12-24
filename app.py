from flask import Flask, session, redirect, url_for
from database.init_db import db, init_db
from controllers.login_controller import login_blueprint
from controllers.register_controller import register_blueprint
from controllers.main_controller import main_blueprint
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

# Redirect root to the main.home endpoint
@app.route('/')
def home_redirect():
    return redirect(url_for('main.home'))  # Use the correct blueprint endpoint

if __name__ == "__main__":
    app.run(debug=True)