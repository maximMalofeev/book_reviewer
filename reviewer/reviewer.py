from flask import Blueprint, render_template, request, flash, redirect, url_for, g, abort, jsonify
from reviewer.db import get_db
from reviewer.auth import login_required
import requests

bp = Blueprint('reviewer', __name__)

@bp.route('/')
def index():
    return render_template('reviewer/index.html', content='Welcome to Book Reviewer')

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

@bp.route('/book_info/<isbn>', methods=['GET', 'POST'])
@login_required
def book_info(isbn):
    db = get_db()
    error = None
    book = db.execute("select * from books where isbn = :isbn", {"isbn": isbn}).fetchone()

    if book is None:
        error = f'Book with isbn {isbn} not exists'
        flash(error)
        return redirect(url_for('index'))

    if request.method == 'GET':
        user_has_review = db.execute('select count(*) from reviews where book_id = :book_id and user_id = :user_id',
            {"book_id": book['id'], "user_id": g.user['id']}).fetchone()['count']
        print(user_has_review)
        reviews = db.execute('select * from reviews where book_id = :book_id', {"book_id": book['id']})
        goodreads_book_info = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "B6TzCnQELh3QA2sdBI8A", "isbns": isbn})
        reviews_list = []
        for review in reviews:
            user_login = db.execute('select login from users where id = :user_id', {"user_id": review['user_id']}).fetchone()
            review_dict = dict(review.items())
            review_dict['user_login'] = user_login['login']
            reviews_list.append(review_dict)

        return render_template('reviewer/book_info.html', book=book, reviews=reviews_list,
            goodreads_book_info=goodreads_book_info.json()['books'][0], user_has_review=user_has_review)

    else:
        review = request.form['review']
        rating = request.form['rating']

        if review is None:
            error = 'Review is required'
        elif rating is None:
            error = 'Rating is required'

        if error is None:
            db.execute('insert into reviews (book_id, user_id, review, rating) values (:book_id, :user_id, :review, :rating)',
                {"book_id": book['id'], "user_id": g.user['id'], "review": review, "rating": int(rating)})
            db.commit()
        else:
            flash(error)

        return redirect(url_for('reviewer.book_info', isbn=isbn))

@bp.route('/api/<isbn>')
def api_book_info(isbn):
    db = get_db()
    book = db.execute("select * from books where isbn = :isbn", {"isbn": isbn}).fetchone()

    if book is None:
        abort(404)
    else:
        return jsonify(dict(book.items()))
    


        
