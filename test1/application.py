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
	g.username=None
	if 'username' in session:
		g.username=session['username']




#index page , search fn
@app.route("/")
@app.route('/index',methods=["GET","POST"])
def index():
	if g.username:
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
		return render_template('index.html')
	return redirect(url_for('signin'))
	

# @app.route("/register", methods=['GET','POST'])
# def register():
# 	form = RegistrationForms
# 	return render_template('registration.html',form=form)

@app.route('/index/<int:book_id>',methods=['GET','POST'])
def search(book_id):
	username=session['username']
	print(username)
	bookDetails=db.execute("SELECT * FROM myBooks WHERE book_id =:b_id",{"b_id":book_id}).fetchone()
	reviews=db.execute("SELECT * FROM reviews JOIN myBooks ON myBooks.book_id=reviews.:book_id",{'book_id':book_id}).fetchone()
	if request.method=='POST':
		post=request.form.get('review')
		if post=='':
			return render_template('error.html',message="Please, enter your review")
		if db.execute(f"SELECT * FROM reviews JOIN myBooks ON myBooks.book_id=reviews.book_id").rowcount==0:
			user_id=(f"SELECT id FROM users2 WHERE username=:username",{"username":username}).fetchone()
			print(user_id)
			db.execute(f"INSERT INTO reviews(id,review) VALUES (:id, :review)",{'id':user_id,'review':post})
			db.commit()
			return render_template('success.html',message="Review added. Thank you for sharing your valuable thoughts.")

	return render_template('bookinfo.html',bookDetails=bookDetails,reviews=reviews)

@app.route('/addReview')
def addReview():
	bookDetails=db.execute("SELECT * FROM myBooks WHERE book_id =:b_id",{"b_id":book_id}).fetchone()
	reviews=db.execute("SELECT * FROM reviews JOIN myBooks ON myBooks.book_id=:book_id",{'book_id':book_id}).fetchall()
	if request.method=='POST':
		post=request.form.get('review')
		if post=='':
			return render_template('error.html',message="Please, enter your review")
		if db.execute(f"SELECT * FROM reviews JOIN myBooks ON myBooks.book_id=reviews.book_id").rowcount==0:
			user_id=(f"SELECT id FROM users2 WHERE username=:username",{"username":username}).fetchone()
			db.execute(f"INSERT INTO reviews(review,id) VALUES (:post,:id)",{'post':post,'user_id':user_id})
			db.commit()
			return render_template('success.html',message="Review added. Thank you for sharing your valuable thoughts.")

	return render_template('bookinfo.html',bookDetails=bookDetails,reviews=reviews)


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