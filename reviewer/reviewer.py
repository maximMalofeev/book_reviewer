from flask import Blueprint, render_template

bp = Blueprint('reviewer', __name__)

@bp.route('/')
def index():
    return render_template('reviewer/index.html', content='test content')