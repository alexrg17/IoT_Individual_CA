from app import app
from models.sensor_data import db
from sqlalchemy import text  # Import the text function

# Test the database connection
with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))  # Use text() to wrap the SQL query
        print("Database connection successful!")
    except Exception as e:
        print("Database connection failed:", e)