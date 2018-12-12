import os
from flask import Flask,render_template,url_for,session

from models import *


app = Flask(__name__)
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# if not os.getenv("DATABASE_URL"):
# 	raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv["DATABASE_URL"]
# app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
	db.create_all()
	
if __name__ == '__main__':
	with app.app.context():
		main()
