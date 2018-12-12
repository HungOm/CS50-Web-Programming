import os

# from models import User
from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session

from flask_login import LoginManager



app = Flask(__name__)
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
if not os.getenv("DATABASE_URL"):
	raise RuntimeError("DATABASE_URL is not set")
app.config['SECRET_KEY'] = 'you-will-never-guess'
# db=SQLAlchemy(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

login = LoginManager(app)
login.login_view = 'login'
