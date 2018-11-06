from flask import Blueprint, render_template, request, flash, redirect, url_for
from reviewer.db import get_db
from reviewer.auth import login_required

bp = Blueprint('reviewer', __name__)

@bp.route('/')
def index():
    return render_template('reviewer/index.html', content='test content')

@bp.route('/search', methods=['POST'])
@login_required
def search():
    target = request.form['search']
    db = get_db()
    suitable_books = None

    if target is "":
        suitable_books = db.execute('select * from books limit 20').fetchall()
    else:
        if target.isdigit():
            suitable_books = db.execute(f"select * from books where isbn ilike :target or title ilike :target or author ilike :target or year = {target}",
                {"target": f'%{target}%'}).fetchall()
        else:
            suitable_books = db.execute(f"select * from books where isbn ilike :target or title ilike :target or author ilike :target",
                {"target": f'%{target}%'}).fetchall()

    return render_template('reviewer/search_results.html', content=suitable_books)

@bp.route('/book_info/<isbn>', methods=['GET'])
@login_required
def book_info(isbn):
    db = get_db()
    error = None
    book = db.execute(f"select * from books where isbn = :isbn", {"isbn": isbn}).fetchone()
    
    if book is None:
        error = f'Book with isbn {isbn} not exists'
        flash(error)
        return redirect(url_for('index'))

    reviews = db.execute('select * from reviews where book_id = :book_id', {"book_id": book['id']})
    return render_template('reviewer/book_info.html', book=book, reviews=reviews)
