import functools
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, g
from reviewer.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('select * from users where id = :id', {"id": user_id}).fetchone()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not login:
            error = 'Login is required'
        elif not password:
            error = 'Password is required'
        elif db.execute('select id from users where login = :login', {"login": login}).fetchone() is not None:
            error = f'Login {login} already in use'

        if error is None:
            db.execute("insert into users (login, email, password_hash) values(:login, :email, :password_hash)",
                        {"login": login, "email": email, "password_hash": generate_password_hash(password)})
            db.commit()
            flash(f'Received login: {login}, email: {email}, password: {password}')
            return redirect(url_for('auth.login'))
        
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute('select * from users where login = :login', {"login": login}).fetchone()
        if user is None:
            error = 'Uncorrect login'
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('index'))