from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from repositories.login import UserRepository
from controllers.protected_routes.protected_route import adminrole

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/users', methods=['GET'])
def manage_users():
    # Check if the logged-in user is an admin
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.home'))  # Redirect to home if not admin

    # Fetch all users from the repository
    users = UserRepository.get_all_users()
    return render_template('admin_users.html', users=users)

@admin_blueprint.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@adminrole
def edit_user(user_id):
    # Check if the logged-in user is an admin
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.home'))  # Redirect to home if not admin

    user = UserRepository.get_user_by_id(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.manage_users'))

    if request.method == 'POST':
        # Update user details from the form
        user_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'username': request.form.get('username'),
            'role': request.form.get('role')
        }

        try:
            UserRepository.update_user(user, user_data)
            flash('User updated successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')

        return redirect(url_for('admin.manage_users'))

    # Render the edit user form
    return render_template('admin_edit_user.html', user=user)

@admin_blueprint.route('/users/delete/<int:user_id>', methods=['POST'])
@adminrole
def delete_user(user_id):
    # Check if the logged-in user is an admin
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.home'))

    try:
        UserRepository.delete_user(user_id)
        flash('User deleted successfully.', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('admin.manage_users'))