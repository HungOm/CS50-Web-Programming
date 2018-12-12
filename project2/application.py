import os

from flask import Flask,render_template,url_for,session
from flask_socketio import SocketIO, emit
from forms import LoginForm, RegistrationForm
from models import User
from config import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, logout_user,login_required


socketio = SocketIO(app)


@app.route("/")


@app.route('/index')
@login_required
def index():
    return render_template('index.html',title="Home")


@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	return render_template("login.html",form=form, title="Sign In")


@app.route('/register',methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user =User(username=form.username.data,email=form.email.data,)
		# user.set_password(form.password.data)
		db.add(user)
		db.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('registration.html',title = 'Register', form=form)
