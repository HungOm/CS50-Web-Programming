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
	books =db.execute("SELECT book_id,isbn_id,title,author,year FROM myBooks LIMIT 30").fetchall()
	# for book in books:
	# 	print(f"{book.book_id},Book name{book.title},ISBN:{book.isbn_id},  written by {book.author} in {book.year}.")
	return render_template('index.html', books=books)

@app.route("/books",methods=['GET','POST'])
def book():
	book =request.form.get('search')
	booksSearch = db.execute("SELECT * FROM myBooks WHERE title =:book_name OR isbn_id=:book_name",{"book_name":book}).fetchall()
	return render_template('bookSearch.html',booksSearch=booksSearch)

@app.route("/books/<string:bookname>")
def books(bookname):
	booksDetails=db.execute("SELECT * FROM myBooks WHERE title =:b_id",{"b_id":bookname}).fetchone()
	if booksDetails is None:
		return render_template("error.html",message="No such book")
	return render_template("bookDetails.html",booksDetails=booksDetails)



@app.route("/register", methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user =form.email.data(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Congratulation, you are now a register user!")
		return redirect(url_for("index"))
	return render_template('registration.html',form=form, title="Register")

