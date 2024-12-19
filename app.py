from flask import Flask, render_template
from models.sensor_data import db
import config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Initialize the database
db.init_app(app)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')  # Render the main design page

if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask development server