from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField,
                     SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, ValidationError,
                                Email, EqualTo, Length)
# from app.models import User


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password= PasswordField('Password',validators=[DataRequired()])
	submit = SubmitField('Register')

	def user_validate(self,username):
		user=db.execute("SELECT * FROM users2 WHERE username=:username",{"username":username}).fetchone()
		if user is not None:
			raise ValidationError("Please enter a different username")
		



class LoginForm(object):
	username=StringField('Username',validators=[DataRequired()])
	email=StringField("Email",validators=[DataRequired(),Email()])
	password=PasswordField('Password',validators=[DataRequired()])
	rememberMe=BooleanField('remember me')
	submit=SubmitField('Log In')

	def user_validate(self,username):
		user=db.execute("SELECT * FROM users2 WHERE username=:username",{"username":username}).fetchone()
		if user is None:
			raise ValidationError("Invalid username")