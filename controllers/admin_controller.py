from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from database.init_db import db

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/users', methods=['GET'])
def manage_users():
    # Check if the logged-in user is an admin
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.home'))  # Redirect to home if not admin

    # Fetch all users from the database
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@admin_blueprint.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Check if the logged-in user is an admin
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.home'))  # Redirect to home if not admin

    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.manage_users'))

    if request.method == 'POST':
        # Update user details from the form
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.username = request.form.get('username')
        user.role = request.form.get('role')

        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {e}', 'danger')

        return redirect(url_for('admin.manage_users'))

    # Render the edit user form
    return render_template('admin_edit_user.html', user=user)

@admin_blueprint.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Check if the logged-in user is an admin
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.home'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.manage_users'))

    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('admin.manage_users'))