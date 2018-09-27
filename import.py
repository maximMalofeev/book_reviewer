import csv

def load_books(books_file):
    with open(books_file, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"{row['isbn']} {row['title']} {row['author']} {row['year']}")

load_books('books.csv')