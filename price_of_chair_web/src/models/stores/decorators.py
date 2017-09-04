from functools import wraps
from src.app import app
from flask import session, url_for, request
from werkzeug.utils import redirect


def requires_admin(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in app.config.ADMINS:
            return redirect(url_for('users.login_user'))
        return func(*args, **kwargs)
    return decorated_func

