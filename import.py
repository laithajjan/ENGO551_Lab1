import csv
import os
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:laith123@localhost/postgres"
db = SQLAlchemy(app)

class Books(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, unique=True)
    title = db.Column(db.String, unique=False)
    author = db.Column(db.String, unique=False)
    year = db.Column(db.Integer, unique=False)

    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

def import_books():
    with open("books.csv", "r") as file:
        reader = csv.reader(file)
        header = True
        for row in reader:
            if header:
                header = False
                continue
            book = Books(row[0], row[1], row[2], row[3])
            db.session.add(book)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        import_books()
