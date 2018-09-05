from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField,
                     SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, ValidationError,
                                Email, EqualTo, Length)
# from app.models import User


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password1 = PasswordField('Password',validators=[DataRequired()])
	password2 = PasswordField('Repeat password',validators=[DataRequired(),EqualTo('password1')])
	submit = SubmitField('Register')