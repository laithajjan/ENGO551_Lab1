# Project 1

ENGO 551 Lab1

Requirements:
_______________________________________________________________________________________________
1. Registration

register.html
input username and password, which saves it into a database called "users"

_______________________________________________________________________________________________
2. Login

login.html
input username and password, which looks it up in the "users" database
if user found, take to user_profile.html
if user not found, flash error and go back to login page

_______________________________________________________________________________________________
3. Logout

session is cleared
go back to index.html
_______________________________________________________________________________________________
4. Import

import.py
use .to_sql function from sqlalchemy
table columns are index, isbn, title, author, and year
_______________________________________________________________________________________________
5. Search

search.html
if no results are found, message says "No results found"
if results found, there are multiple cards that show the title, author, isbn, and date.
_______________________________________________________________________________________________
6. Book page

book.html
you can see title, author, date, and isbn
