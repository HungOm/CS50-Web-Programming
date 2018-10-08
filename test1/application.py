import os
import requests

from flask import Flask, session, render_template,request,g,redirect,url_for,json,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY']='Shh_what?'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



#if the user is not logged in , username is not kept in session. 
#when the user logged in, new user name is kept in session

@app.before_request
def before_request():
	username=None
	if 'username' in session:
		username=session['username']




#index page , 
#if user is logged in , this will return and index(which is search page) page. Otherwise, it will return entry page which display a welcome
# note, log in link and signup link
@app.route("/")
def home():
	if 'username' in session:
		return redirect(url_for('index'))
	return render_template('entry.html')



@app.route('/index',methods=["GET","POST"])
def index():
	# ensure the user is logged in for user privilege to access the content
	if 'username' in session:
		username=session['username']


		#if the use click submit , flask will get info input from user and proceed to match it would database to return desired results
		if request.method=='POST':

			#name/title/isbn input
			name=request.form.get('search')

			#category of search type , e.g : title/author or name of book
			book=request.form.get('category')

			#if user did not type but clicked search, this function return an action suggestion
			if name=='':
				return render_template('error.html',message="Please enter name of author,book or isbn_id")

			#if the user chose title as category , this will ensure the search is based on the title of the book	
			if book=='title':
				title_input=db.execute(f"SELECT * FROM myBooks WHERE title LIKE '%{name}%'").fetchall()
				# print(title_input)


				#if the searched book did not match any book in database, it will return empty list
				if title_input==[]:
					return render_template('error.html',message="Sorry, no such book in our database.")
				return render_template('search.html',name_input=title_input)

			#the search is base on the author of the book
			#Therefor, this will return any books that were written by the search author from database
			elif book=='author':
				author_input=db.execute(f"SELECT * FROM myBooks WHERE author LIKE '%{name}%'").fetchall()
				if author_input==[]:
					return render_template('error.html',message="Sorry, no such author in our database.")
				return render_template('search.html',name_input=author_input)


			#if the user chose isbn, it will return a book that match the isbn	
			else:
				isbn_input=db.execute(f"SELECT * FROM myBooks WHERE isbn_id LIKE '%{name}%'").fetchall()
				if isbn_input==[]:
					return render_template('error.html',message="Sorry, no such isbn in our database.")
				return render_template('search.html',name_input=isbn_input)
		return render_template('index.html',username=username)
		
			
	return redirect(url_for('signin'))
	


#search books
#Once a list of books from the user search is returned, this link proceed to display details of the book

@app.route('/index/<int:book_id>')
def search(book_id):
	if 'username' in session:
		bookDetails=db.execute("SELECT * FROM myBooks WHERE book_id =:b_id",{"b_id":book_id}).fetchone()
		bookIsbn=bookDetails.isbn_id
		res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "wGl6R3MomAtyu1Uur0Sbw", "isbns": "{}".format(bookIsbn)})
		data = res.json()
		username=session['username']
		user_id=db.execute(f"SELECT id FROM users2 WHERE username=:username",{"username":username}).fetchone()
		user_id=user_id[0]
		bookReviews=db.execute("SELECT review,username,ratings FROM reviews LEFT JOIN users2 ON (reviews.user_id=users2.id) WHERE reviews.book_id=:book_id",{'book_id':book_id}).fetchall()
		return render_template('bookinfo.html',bookDetails=bookDetails, bookReviews=bookReviews,data=data)
	return render_template('userNotLogged.html')

@app.route('/signup',methods=["GET","POST"])
def signup():
	# return "Please Sign up to use the service"
	form=RegistrationForm()
	if form.validate_on_submit():
		username=form.username.data
		email=form.email.data
		password=form.password.data
		if db.execute("SELECT * FROM users2 WHERE username = :username",{"username":username}).rowcount==0:
			db.execute("INSERT INTO users2(username, email, password) VALUES(:username, :email, :password)",
				{"username":username,"email":email,"password":password})
			db.commit()
			return render_template("success.html")
		else:
			return render_template('error.html',message="User already registered. Please use another username")
	return render_template("signup.html",form=form)


@app.route('/signin',methods=["GET","POST"])
def signin():
	if request.method=='POST':
		username=request.form['username']
		if username=='':
			return render_template('error.html',message="Please enter your username and password")
		password=db.execute("SELECT password FROM users2 WHERE username=:username",{"username":username}).fetchone()
		if password is None:
			return render_template('error.html',message="Invalid username or password")

		if request.form['password']==password[0]:
			session['username']=request.form['username']
			username=session['username']
			# print(username)
		return redirect(url_for('index',username=username))
	return render_template('login.html')


@app.route('/signout',methods=["GET","POST"])
def signout():
	session.pop('username',None)
	return render_template('signout.html')



@app.route('/review/<int:book_id>',methods=["GET","POST"])
def review(book_id): 

	if 'username' in session:
	# bookReviews=db.execute(f"SELECT review,username,title,isbn,author,year FROM reviews INNER JOIN users2 ON reviews.user_id=users2.user_id INNER JOIN myBooks ON reviews.book_id=myBooks.book_id").fetchall()
	# if bookReviews is None:
		# return render_template('review.html',book)
	# print(bookReviews)
		bookDetails1=db.execute("SELECT * FROM myBooks WHERE book_id =:b_id",{"b_id":book_id}).fetchone()

		if request.method=='POST':
			review=request.form.get('review')
			rating=(request.form.get('selected_rating'))
			if rating=='':
				rating=None
			# print("Rating:",rating[0])
			username=session['username']
			user_id=db.execute(f"SELECT id FROM users2 WHERE username=:username",{"username":username}).fetchone()
			user_id=user_id[0]

			
			# print(user_id)
			if review=='':
				return render_template('error.html',message="Please write your review in the field provided.")
			elif db.execute(f"SELECT user_id FROM reviews WHERE book_id=:book_id AND user_id=:user_id",{"book_id":book_id,"user_id":user_id}).rowcount != 0:
				return render_template('error.html',message="Oops!You have already reviewed this book.Each user is allowed only one review for each book.")
		# elif db.execute(f"SELECT book_id FROM reviews WHERE book_id=:book_id",{"book_id":book_id}).rowcount != 0:
		# 	return render_template('error.html',message="Oops! You have already reviewed this book. Please try anoher book!")
			else:
				db.execute(f"INSERT INTO reviews(user_id,book_id,review,ratings) VALUES(:user_id,:book_id,:review, :ratings)",{"user_id":user_id,"book_id":book_id, "review":review,"ratings":rating})
				db.commit()
				return render_template('success.html',message="Your review has been added to the book. Thank you for your valuable contributions!",bookDetails1=bookDetails1)
		return render_template("review.html",bookDetails1=bookDetails1)

	return render_template('userNotLogged.html')

# Api access

@app.route('/api',methods=["GET","POST"])
def api():
	if 'username' in session:
		if request.method=='POST':
			name = request.form.get('isbn')
			title_input=db.execute(f"SELECT * FROM myBooks WHERE title LIKE '%{name}%' OR isbn_id LIKE '{name}' OR author LIKE '%{name}%'").fetchall()
					# print(title_input)
			if title_input==[]:
				return render_template('error.html',message="Sorry, no such book in our database.")
			if title_input is None:
				return render_template('api_Access.html',message="Please search name of book/author/isbn")
			return render_template('api_Access.html', title_input=title_input)
		return render_template('api_Access.html')
	return render_template('userNotLogged.html')



@app.route('/api/<isbn_id>',methods=["GET","POST"])
def api_Access(isbn_id):
	if 'username' in session:
		ratings=db.execute("SELECT ratings FROM reviews LEFT JOIN myBooks on(reviews.book_id=myBooks.book_id) WHERE myBooks.isbn_id=:isbn_id GROUP BY ratings ORDER BY ratings DESC NULLS LAST",{"isbn_id":isbn_id}).fetchall()
		average = []
		if ratings:
			for i in ratings:
				if i[0]==None:
					break
				average.append(i[0])
				# print(average)
				average=[int(i) for i in average]
			numOfRatings=len(average)
			if numOfRatings >= 1:
				total = sum(average)
				averageRatings=total/numOfRatings
				ratings={
				"Number of ratings":numOfRatings,
				"average" : averageRatings
				}
			else:
				ratings="Users did not rate but reviewed."
			
		else:
			ratings="No ratings available from users for this book"
		bookReviews=db.execute("SELECT reviews.ratings,myBooks.title,myBooks.author,myBooks.isbn_id,myBooks.year FROM reviews LEFT JOIN myBooks ON myBooks.isbn_id=:isbn_id",{"isbn_id":isbn_id}).fetchone()
		if bookReviews is None:
			return jsonify({"error":"Invalid isbn ID"})
		return jsonify({
		"title":bookReviews.title,
		"Author":bookReviews.author,
		"year":bookReviews.year,
		"ISBN":bookReviews.isbn_id,
		"ratings":ratings

		})

		# return render_template('api_Access.html',ratings=ratings,bookReviews=bookReviews)



	return render_template('userNotLogged.html', )