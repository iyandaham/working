from application import db
from application.models import Post, Rating, User, Restaurant


db.drop_all()
db.create_all()

