from database.init_db import db
from models.user import User

class UserRepository:
    @staticmethod
    def get_all_users():
        """Fetch all users from the database."""
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        """Fetch a user by their ID."""
        return User.query.get(user_id)

    @staticmethod
    def update_user(user, user_data):
        """Update user details."""
        user.name = user_data['name']
        user.email = user_data['email']
        user.username = user_data['username']
        user.role = user_data['role']
        db.session.commit()

    @staticmethod
    def delete_user(user_id):
        """Delete a user by their ID."""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()