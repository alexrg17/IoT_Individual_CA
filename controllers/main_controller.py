from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.room import Room  # Import the Room model
from database.init_db import db  # Import db directly

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))  # Redirect to login if not logged in

    user_id = session['user_id']  # Get the logged-in user's ID
    rooms = Room.query.filter_by(user_id=user_id).all()  # Fetch rooms for the logged-in user
    return render_template('index.html', rooms=rooms)  # Pass rooms to the template

@main_blueprint.route('/add-room', methods=['POST'])
def add_room():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))  # Redirect to login if not logged in

    room_name = request.form.get('room_name')  # Get the room name from the form
    user_id = session['user_id']  # Get the logged-in user's ID

    if not room_name:
        flash('Room name cannot be empty.', 'danger')
        return redirect(url_for('main.home'))

    # Add the new room to the database
    try:
        new_room = Room(name=room_name, user_id=user_id)
        db.session.add(new_room)
        db.session.commit()
        flash('Room added successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        db.session.rollback()

    return redirect(url_for('main.home'))