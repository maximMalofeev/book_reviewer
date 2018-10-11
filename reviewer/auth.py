from flask import Blueprint, render_template

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    pass

@bp.route('/login', methods=('GET', 'POST'))
def login():
    pass

@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    pass