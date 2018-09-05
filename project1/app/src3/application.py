import os

from flask import Flask, render_template, request,redirect,url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import RegistrationForm,LoginForm
from flask_login import login_required,LoginManager,login_user,logout_user,current_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "I love flask"
login=LoginManager(app)
# app.config['SESSON']

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
@login_required
def index():
	flights=db.execute("SELECT * FROM flights").fetchall()
	return render_template("index.html",flights=flights)


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
	return render_template("signup.html",form=form)



@app.route('/login',methods=["GET","POST"])
def login():
	if current_user.is_authenticated():
		redirect(url_for('index'))
	form=LoginForm()
	if form.validate_on_submit():
		username=form.username.data
		email=form.email.data 
		password=form.password.data
		user=db.execute("SELECT * FROM users2 WHERE username=:username AND password=:password",{"username":username, "password":password}).fetchone()
		if user is None:
			return render_template('error.html',message="In correct username or password")
		logout_user(user)
		return redirect(url_for('index'))
	return render_template("login.html",form=form)

@app.route('/signin',methods=["GET","POST"])
def signin():
	if request.method=="POST":
		session['username']=form.username.data['username']
		return redirect(url_for('index'))
	return render_template("login.html")