import os

from flask import Flask, session, render_template,flash,url_for,redirect,request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from forms import RegistrationForm

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "I love flask"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/",methods=['GET','POST'])
@app.route("/index", methods=['GET','POST'])
def index():
	books =db.execute("SELECT book_id,isbn_id,title,author,year FROM myBooks LIMIT 10").fetchall()
	# for book in books:
	# 	print(f"{book.book_id},Book name{book.title},ISBN:{book.isbn_id},  written by {book.author} in {book.year}.")
	if request.method=="POST":
		book =request.form.get('search')
		print(book)
		if book is "":
			return render_template("error.html", message="Please, enter book name or isbn id.")
		booksSearch=db.execute(f"SELECT * FROM myBooks WHERE title LIKE '%{book}%' OR isbn_id LIKE '%{book}%' OR author LIKE '%{book}%'").fetchall()
		print(booksSearch)
		if booksSearch ==[]:
			return render_template('error.html',message="Sorry, No book is found under such name")
		return render_template('bookSearch.html',booksSearch=booksSearch)

	return render_template("bookSearch.html")
	return render_template('index.html', books=books)

@app.route("/books",methods=['GET','POST'])
def books():
	if request.method=="POST":
		book =request.form.get('search')
		print(book)
		if book is "":
			return render_template("error.html", message="Please, enter book name or isbn id.")
		booksSearch=db.execute(f"SELECT * FROM myBooks WHERE title LIKE '%{book}%' OR isbn_id LIKE '%{book}%' OR author LIKE '%{book}%'").fetchall()
		print(booksSearch)
		if booksSearch ==[]:
			return render_template('error.html',message="Sorry, No book is found under such name")
		return render_template('bookSearch.html',booksSearch=booksSearch)

	return render_template("bookSearch.html")


@app.route("/books/<int:book_id>")
def book(book_id):
	booksDetails=db.execute("SELECT * FROM myBooks WHERE book_id =:b_id",{"b_id":book_id}).fetchone()
	if booksDetails is None:
		return render_template("error.html",message="No such book")
	return render_template("bookDetails.html",booksDetails=booksDetails)


