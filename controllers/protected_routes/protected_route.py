from flask import redirect, session, flash
from functools import wraps

# Decorator to protect admin routes
def adminrole(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Access denied. Admins only.', 'danger')
            return redirect('/admin/users')  # Redirect to login if not admin
        return func(*args, **kwargs)
    return wrapper

# Decorator to protect normal user routes
def normaluser(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'user':
            flash('Access denied. Normal users only.', 'danger')
            return redirect('/login')  # Redirect to login if not a normal user
        return func(*args, **kwargs)
    return wrapper