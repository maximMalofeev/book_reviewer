from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv

def create_and_fill_books_table(engine):
    db = scoped_session(sessionmaker(bind=engine))
    db.execute("create table if not exists books (\
                            id serial primary key,\
                            isbn text unique,\
                            title text,\
                            author text,\
                            year integer\
    );")

    with open('books.csv') as csvfile:
        booksreader = csv.DictReader(csvfile)
        for row in booksreader:
            db.execute("insert into books (isbn, title, author, year) values (:isbn, :title, :author, :year)",
                                     {"isbn": row['isbn'], "title": row['title'], "author": row['author'], "year": int(row['year'])})
    db.commit()

def create_users_table(engine):
    engine.connect().execute("create table if not exists users ( \
                                id serial primary key,\
                                login text,\
                                email text,\
                                password_hash text\
    );")

def create_reviews_table(engine):
    engine.connect().execute("create table if not exists reviews ( \
                                book_id serial,\
                                user_id serial,\
                                review text,\
                                foreign key(book_id) references books(id),\
                                foreign key(user_id) references users(id)\
                                \
    );")

if __name__ == "__main__":
    engine = create_engine('postgres://btwllvfoiyvmgf:0c8b72031ade0229949bad8d53b7dd4370be1d32b980c097e2576e697c60f378@ec2-46-137-75-170.eu-west-1.compute.amazonaws.com:5432/d3luchuf6f5921')
    create_and_fill_books_table(engine)
    create_users_table(engine)
    create_reviews_table(engine)