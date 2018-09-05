import os

from flask import Flask, render_template, request,redirect,url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import RegistrationForm,LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "I love flask"
# app.config['SESSON']

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
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
def signup():
	form=