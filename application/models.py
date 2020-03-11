from application import db
from application import login_manager
from flask_login import UserMixin
from datetime  import datetime

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False, unique=True)
	content = db.Column(db.String(1000), nullable=False, unique=True)
	date_posted =db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
                return ' '.join([
                        'UserID: ', str (self.id), '\r\n', 'Email: ', self.email,
                        'Title: ', self.title, '\r\n', self.content
                ])

class Rating(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Rating_value = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	rest_id= db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

	def __repr__(self):
		return ' '.join([
			'RatingID: ', str(self.id), '\r\n',
			'Rating: ', str(self.Rating_value),'\r\n',
		])



@login_manager.user_loader
def load_user(id):
        return User.query.get(int(id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(150), nullable=False, unique=True)
	first_name = db.Column(db.String(150), nullable=False)
	last_name = db.Column(db.String(150), nullable=False)
	password = db.Column(db.String(200), nullable=False)
	rating = db.relationship('Rating', backref='user', lazy=True)
	author = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
                return ''.join([
			'User: ',self.first_name, ' ' , self.last_name, '\r\n',
                        'Tile: ',self.title, '\r\n', self.content,
                        'Name: ', self.first_name, ' ', self.last_name
                        ])

class Restaurant(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	rest_name = db.Column(db.String(150), nullable=False)
	meal = db.Column(db.String(150), nullable=False)
	location = db.Column(db.String(150), nullable=False)
	rating = db.relationship('Rating', backref='restaurant', lazy=True)

	def __repr__(self):
		return''.join ([
			'Restaurant ID: ', str(self.id), '\r\n',
			'Restaurant: ', self.rest_name, '\r\n',
			'Meal: ', self.meal, '\r\n',
			'location: ',self.location, '\r\n',
			])
