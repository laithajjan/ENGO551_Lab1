import os, sys, requests, json, time, sqlalchemy

from flask import Flask, session, request, jsonify, redirect, url_for, abort, render_template, flash
from functools import wraps
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.expression import cast
from sqlalchemy import create_engine
from sqlalchemy import text
from flask_table import Table, Col

app = Flask(__name__, template_folder='template')

os.environ["DATABASE_URL"] = "postgresql://postgres:laith123@localhost/postgres"

# Check for environment variable
if not os.getenv('DATABASE_URL'):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# Requiring login to access site
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login before accessing the full site.')
            return redirect(url_for('login'))

    return wrap


# Definining the homepage where search queries will be made
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    error = None
    if request.method == 'POST':
        if not request.form['search'].strip():
            error = 'Invalid search. Please enter a valid query.'
        else:
            return redirect(url_for('booksearch'))
    return render_template('index.html', error=error)


# Defining the welcome page, where the initial page will be located.
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


# Defining the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'test' or request.form['password'] != 'test':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash("You are now logged into the Book Nook!")
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


# Defining Logout Setup
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You are logged out of the Book Nook!")
    return redirect(url_for('welcome'))


# Defining the search bar
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":  # refresh from book page to search again
        return render_template("search.html")

@app.route('/booksearch', methods=["GET", "POST"])
@login_required
def booksearch():
    # Will accept searches for title, authors and isbn numbers
    search = request.form.get('search')
    # check if search is None
    if not search:
        return render_template('index.html', message="Please enter a search term")
    # look up item in database
    sql_query = text("SELECT * FROM Books WHERE title LIKE :search OR isbn LIKE :search OR author LIKE :search")
    rows = db.execute(sql_query, {"search": f"%{search}%"})
    books = rows.fetchall()
    # if no results found
    if rows.rowcount == 0:
        return render_template('index.html', message="No results found for '" + search + "'")

    numfound = rows.rowcount
    return render_template('book.html', booksfound=books, numfound=numfound, search_name=search)



if __name__ == '__main__':
    app.run(debug=True)
