from sqlalchemy import create_engine
import csv

def create_and_fill_books_table(engine):
    engine.connect().execute("create table if not exists books (\
                            id integer primary key,\
                            isbn text unique,\
                            title text,\
                            author text,\
                            year text\
    );")
    with open('books.csv') as csvfile:
        booksreader = csv.DictReader(csvfile)
        for row in booksreader:
            engine.connect().execute("insert into books (isbn, title, author, year) values (?, ?, ?, ?)",
                                     row['isbn'], row['title'], row['author'], row['year'])

def create_users_table(engine):
    engine.connect().execute("create table if not exists users ( \
                                id integer primary key,\
                                login text,\
                                email text,\
                                password_hash text\
    );")

def create_reviews_table(engine):
    engine.connect().execute("create table if not exists reviews ( \
                                book_id integer,\
                                user_id integer,\
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