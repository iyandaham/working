

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User, Restaurant, Rating
from flask_login import current_user

class PostForm(FlaskForm):
	title = StringField('Title', validators =[DataRequired(), Length(min=4, max=100)])	
	content = StringField('Content', validators =[DataRequired()])
	submit = SubmitField('Post!')

class RegistrationForm(FlaskForm):
	first_name = StringField('First Name', validators =[DataRequired(), Length(min=4, max=30)])
	last_name = StringField('Last Name', validators =[DataRequired(), Length(min=4, max=30)])
	email = StringField('Email',validators = [DataRequired(),Email()])
	password = PasswordField('Password',validators = [DataRequired(),])
	confirm_password = PasswordField('Confirm Password',validators = [DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign up')
	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()

		if user:
			raise ValidationError('Email already in use')


class RatingForm(FlaskForm):
	rating_value = StringField('Rating_value', validators=[DataRequired()])
	submit = SubmitField('Submit rating!')

class UpdateRatingForm(FlaskForm):
	rating_value = StringField ('Rating_value', validators =[DataRequired()])
	submit = SubmitField('Update')
	def validate_rating(self,rating_value):
		if rating_value.data != current_user.rating_value:
			rating = Rating.query.filter_by(rating_value=rating_value.data).first()
			if rating:
				raise ValidationError('Rating already in use')

class RestaurantForm(FlaskForm):
	rest_name = StringField('rest_name', validators = [DataRequired()])
	meal = StringField('meal', validators=[DataRequired()])
	location = StringField('locaton', validators =[DataRequired()])
	submit = SubmitField('Submit Restaurent')

class UpdateRestaurantForm(FlaskForm):
	rest_name = StringField('rest_name', validators = [DataRequired()])
	meal =	StringField('meal', validators =[DataRequired()])
	location = StringField('location', validators =[DataRequired()])
	submit = SubmitField('Update')


class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(), Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
        first_name = StringField('First Name',validators=[DataRequired(), Length(min=4, max=30)])
        last_name = StringField('Last Name', validators =[DataRequired(), Length(min=4, max=30)])
        email = StringField('Email',validators=[DataRequired(), Email()])
        submit = SubmitField('Update')
        def validate_email(self,email):
                if email.data != current_user.email:
                        user = User.query.filter_by(email=email.data).first()
                        if user:
                                raise ValidationError('Email already in use')

class RestaurantDeleteForm(FlaskForm):
	rest_name = StringField('rest_name', validators = [DataRequired()])
	meal =  StringField('meal', validators =[DataRequired()])
	location = StringField('location', validators =[DataRequired()])
	submit = SubmitField('Delete')
