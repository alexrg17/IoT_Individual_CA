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
        """
        Initialize a Room instance.

        :param name: Name of the room
        :param user_id: ID of the user who owns the room
        """
        self.name = name
        self.user_id = user_id

    def update_room(self, new_name):
        """
        Update the room name.

        :param new_name: The new name for the room
        """
        self.name = new_name
        db.session.commit()

    @staticmethod
    def delete_room(room_id):
        """
        Delete a room from the database.

        :param room_id: The ID of the room to be deleted
        """
        room = Room.query.get(room_id)
        if room:
            db.session.delete(room)
            db.session.commit()