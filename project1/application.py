import os

from flask import Flask, session, render_template,request,g,redirect,url_for
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


@app.before_request
def before_request():
	username=None
	if 'username' in session:
		username=session['username']




#index page , search fn
@app.route("/")
def home():
	if 'username' in session:
		return redirect(url_for('index'))
	return render_template('entry.html')
@app.route('/index',methods=["GET","POST"])
def index():
	if 'username' in session:
		username=session['username']
		if request.method=='POST':
			name=request.form.get('search')
			book=request.form.get('category')

			# print(book)
			# print(name)
			if name=='':
				return render_template('error.html',message="Please enter name of author,book or isbn_id")
			if book=='title':
				title_input=db.execute(f"SELECT * FROM myBooks WHERE title LIKE '%{name}%'").fetchall()
				# print(title_input)
				if title_input==[]:
					return render_template('error.html',message="Sorry, no such book in our database.")
				return render_template('search.html',name_input=title_input)
			elif book=='author':
				author_input=db.execute(f"SELECT * FROM myBooks WHERE author LIKE '%{name}%'").fetchall()
				if author_input==[]:
					return render_template('error.html',message="Sorry, no such author in our database.")
				return render_template('search.html',name_input=author_input)
			else:
				isbn_input=db.execute(f"SELECT * FROM myBooks WHERE isbn_id LIKE '%{name}%'").fetchall()
				if isbn_input==[]:
					return render_template('error.html',message="Sorry, no such isbn in our database.")
				return render_template('search.html',name_input=isbn_input)
		return render_template('index.html',username=username)
		
			
	return redirect(url_for('signin'))
	

# @app.route("/register", methods=['GET','POST'])
# def register():
# 	form = RegistrationForms
# 	return render_template('registration.html',form=form)

@app.route('/index/<int:book_id>')
def search(book_id):
	bookDetails=db.execute("SELECT * FROM myBooks WHERE book_id =:b_id",{"b_id":book_id}).fetchone()
	username=session['username']
	user_id=db.execute(f"SELECT id FROM users2 WHERE username=:username",{"username":username}).fetchone()
	user_id=user_id[0]
	print(user_id)
	bookReviews=db.execute("SELECT review,username FROM reviews LEFT JOIN users2 ON (reviews.user_id=users2.id) WHERE reviews.book_id=:book_id",{'book_id':book_id}).fetchall()
	print(bookReviews)
	return render_template('bookinfo.html',bookDetails=bookDetails, bookReviews=bookReviews)

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
	# bookReviews=db.execute(f"SELECT review,username,title,isbn,author,year FROM reviews INNER JOIN users2 ON reviews.user_id=users2.user_id INNER JOIN myBooks ON reviews.book_id=myBooks.book_id").fetchall()
	# if bookReviews is None:
		# return render_template('review.html',book)
	# print(bookReviews)

	if request.method=='POST':
		review=request.form.get('review')
		# print(review)
		username=session['username']
		user_id=db.execute(f"SELECT id FROM users2 WHERE username=:username",{"username":username}).fetchone()
		user_id=user_id[0]
		print(user_id)

		if review=='':
			return render_template('error.html',message="Please write your review in the field provided.")
		elif db.execute(f"SELECT user_id FROM reviews WHERE book_id=:book_id",{"book_id":book_id}).rowcount != 0:
			return render_template('error.html',message="Oops!You have already reviewed this book.Each user is allowed only one review for each book.")
		# elif db.execute(f"SELECT book_id FROM reviews WHERE book_id=:book_id",{"book_id":book_id}).rowcount != 0:
		# 	return render_template('error.html',message="Oops! You have already reviewed this book. Please try anoher book!")
		else:
			db.execute(f"INSERT INTO reviews(user_id,book_id,review) VALUES(:user_id,:book_id,:review)",{"user_id":user_id,"book_id":book_id, "review":review})
			db.commit()
			return render_template('success.html',message="Your review has been added to the book. Thank you for your valuable contributions!")
	return render_template("review.html")


