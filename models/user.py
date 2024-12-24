from database.init_db import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Full Name
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Relationship to Room table
    rooms = db.relationship('Room', back_populates='user', lazy=True)

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)  # Hash the password