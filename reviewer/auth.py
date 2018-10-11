from flask import Blueprint, render_template, request, flash, redirect, url_for

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']

        flash(f'Received login: {login}, email: {email}, password: {password}')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        flash(f'Received login: {login}, password: {password}')
        return redirect(url_for('index'))
    
    return render_template('auth/login.html')

@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    pass