from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5



class User(UserMixin):
	db.execute("CREATE TABLE IF NOT EXISTS Books(id SERIAL PRIMARY KEY NOT NULL,ISBN VARCHAR NOT NULL,Title VARCHAR, Author VARCHAR, Year VARCHAR)")")
	id = db.execute()
	"""docstring for User"""
	def __init__(self, arg):
		super(User, self).__init__()
		self.arg = arg
		