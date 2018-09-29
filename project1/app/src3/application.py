import os

from flask import Flask, render_template, request,redirect,url_for,session,g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import RegistrationForm,LoginForm
from flask_login import login_required,LoginManager,login_user,logout_user,current_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "I love flask"
login=LoginManager(app)
login.login_view='login'
# app.config['SESSON']

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
@app.route('/index',methods=["GET","POST"])
def index():
	if g.username:
		flights=db.execute("SELECT * FROM flights JOIN passengers ON passengers.flight_id=flisht_id").fetchall()
		return render_template("index.html",flights=flights)
	return redirect(url_for('signin'))

	# if 'username' in session:
	# 	flights=db.execute("SELECT * FROM flights").fetchall()
	# 	return render_template("index.html",flights=flights)
	# return redirect(url_for('signin'))

@app.route('/book',methods=['POST'])
def book():
	name = request.form.get('name')
	print(name)
	try:
		flight_id=int(request.form.get('flight_id'))
	except ValueError:
		return render_template('error.html',message="Invalid flight number.")

	if db.execute('SELECT * FROM flights WHERE flisht_id=:flisht_id',{"flisht_id":flight_id}).rowcount==0:
		return render_template('error.html',message="No such flight with this ID")
	print(flight_id)
	if db.execute("SELECT * FROM passengers WHERE name=:name AND flight_id=:flight_id",{"name":name,"flight_id":flight_id}).rowcount !=0:
		return render_template('error.html',message="Passenger already registered for this flight!")

	db.execute("INSERT INTO passengers(name,flight_id) VALUES(:name,:flight_id)",
		{'name':name,"flight_id":flight_id})
	db.commit()
	return render_template('booked.html')	
@app.before_request
def before_request():
	g.username=None
	if 'username' in session:
		g.username=session['username']




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
			return redirect(url_for('index'))
		return render_template('error.html',message=message)

	return render_template('login.html')


@app.route('/signout',methods=["GET","POST"])
def signout():
	session.pop('username',None)
	return render_template('signout.html')

# @app.route('/book',methods=["GET","POST"])
# def book():
# 	if request.method=="POST":
# 		flight =request.form['ps_name']
# 		db.execute("INSERT INTO passenger(name) VALUES(:flight)",
# 				{"flight":flight})
# 		db.commit()
# 	return