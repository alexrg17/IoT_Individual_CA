from database.init_db import db
from models.user import User  # Import the User model

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)               # Unique ID for the room
    name = db.Column(db.String(100), nullable=False)           # Room name
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to users table

    # Relationship to the User table
    user = db.relationship('User', back_populates='rooms')

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id