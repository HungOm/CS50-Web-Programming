
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.VARCHAR(64),index=True,unique=True)
    email = db.Column(db.VARCHAR(120),primary_key=True,unique=True)
    password = db.Column(db.VARCHAR(120))
    authenticated = db.Column(db.Boolean, default=False)


    def __repr__(self):
    	return '<User {}>'.format(self.username)
    def set_password(self, password):
    	self.password_hash = generate_password_hash(password)
    def check_password(self, password):
    	return check_password_hash(self.password_hash, password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False