from flask_sqlalchemy import SQLAlchemy
from database.init_db import db



class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    id = db.Column(db.Integer, primary_key=True)           # Unique ID
    sensor_type = db.Column(db.String(50), nullable=False) # e.g., PIR, Button
    status = db.Column(db.String(50), nullable=False)      # e.g., Detected, Pressed
    timestamp = db.Column(db.DateTime, default=db.func.now())