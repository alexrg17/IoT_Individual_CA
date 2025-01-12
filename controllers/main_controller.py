from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.room import Room
from database.init_db import db
from controllers.protected_routes.protected_route import normaluser

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    rooms = Room.query.filter_by(user_id=user_id).all()
    return render_template('index.html', rooms=rooms)

@main_blueprint.route('/add-room', methods=['POST'])

def add_room():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    room_name = request.form.get('room_name')
    user_id = session['user_id']

    if not room_name:
        flash('Room name cannot be empty.', 'danger')
        return redirect(url_for('main.home'))

    try:
        new_room = Room(name=room_name, user_id=user_id)
        db.session.add(new_room)
        db.session.commit()
        flash('Room added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('main.home'))

@main_blueprint.route('/edit-room/<int:room_id>', methods=['POST'])

def edit_room(room_id):
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    room = Room.query.get(room_id)
    if not room or room.user_id != session['user_id']:
        flash("Room not found or you don't have permission to edit it.", 'danger')
        return redirect(url_for('main.home'))

    room_name = request.form.get('room_name')
    if not room_name:
        flash('Room name cannot be empty.', 'danger')
        return redirect(url_for('main.home'))

    try:
        room.name = room_name
        db.session.commit()
        flash('Room updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('main.home'))

@main_blueprint.route('/delete-room/<int:room_id>', methods=['POST'])

def delete_room(room_id):
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    room = Room.query.get(room_id)
    if not room or room.user_id != session['user_id']:
        flash("Room not found or you don't have permission to delete it.", 'danger')
        return redirect(url_for('main.home'))

    try:
        db.session.delete(room)
        db.session.commit()
        flash('Room deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('main.home'))