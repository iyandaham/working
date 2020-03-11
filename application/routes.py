from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt, login_manager
from application.models import Post, User, Rating, Restaurant
from application.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm, RatingForm, RestaurantForm, UpdateRestaurantForm, UpdateRatingForm, RestaurantDeleteForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
        form = UpdateAccountForm()
        if form.validate_on_submit():
                current_user.first_name = form.first_name.data
                current_user.last_name = form.last_name.data
                current_user.email = form.email.data
                db.session.commit()
                return redirect(url_for('account'))
        elif request.method =='GET':
                form.first_name.data = current_user.first_name
                form.last_name.data = current_user.last_name
                form.email.data = current_user.email
        return render_template('account.html', title='Account', form=form)


@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
        user = current_user.id
        account = User.query.filter_by(id=user).first()
        posts = User.query.filter_by(id=user).all()
        logout_user()
        for post in posts:
                db.session.delete(post)
        db.session.delete(account)
        db.session.commit()
        return redirect(url_for('register'))

@app.route("/restaurant/delete/<rest_id>", methods=["GET","POST"])
@login_required
def delete_rest_id(rest_id):
		rating = Rating.query.filter_by(rest_id = rest_id).first()
		db.session.delete(rating)
		db.session.commit()
		restaurant = Restaurant.query.filter_by(id=rest_id).first()
		db.session.delete(restaurant)
		db.session.commit()
		return redirect(url_for('home'))


@app.route("/login", methods=['GET', 'POST'])
def login():
        if current_user.is_authenticated:
                return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
                user=User.query.filter_by(email=form.email.data).first()
                if user and bcrypt.check_password_hash(user.password, form.password.data):
                        login_user(user, remember=form.remember.data)
                        next_page = request.args.get('next')
                        if next_page:
                                return redirect(next_page)
                        else:
                                return redirect(url_for('home'))
        print('form is not valid')
        return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
        logout_user()
        return redirect(url_for('login'))

@app.route('/rating/<rest_id>', methods=['GET', 'POST'])
def rating(rest_id):
	form = RatingForm()
	if form.validate_on_submit():
		restaurant = Restaurant.query.filter_by(id=rest_id).first()
		rating = Rating(
			Rating_value = form.rating_value.data,
			rest_id =rest_id,
			user_id = current_user.id)
		db.session.add(rating)
		db.session.commit()
		return redirect(url_for('home'))
	else:
		print(form.errors)
	return render_template('rating.html', title='Rating', form=form)


@app.route('/restaurant', methods=['GET', 'POST'])
def restaurant():
	form = RestaurantForm()
	restaurants=Restaurant.query.all()
	if form.validate_on_submit():
		restaurant = Restaurant(
			rest_name = form.rest_name.data,
			meal = form.meal.data,
			location = form.location.data)
		db.session.add(restaurant)
		db.session.commit()
		rest = Restaurant.query.filter_by(
				rest_name=form.rest_name.data,
				meal = form.meal.data,
				location = form.location.data).first()

		return redirect(url_for('rating', rest_id = restaurant.id))
	else:
		print(form.errors)
	return render_template('restaurant.html', title='Restaurant', form = form, restaurants = restaurants)


@app.route('/restaurants/all')
def restaurantall ():
	restaurants = Restaurant.query.filter_by(id=rest_id).all()



@app.route('/update/<rest_id>', methods=['GET','POST'])
def update(rest_id):
	restaurants = Restaurant.query.filter_by(id=rest_id).first()
	form = UpdateRestaurantForm()
	if form.validate_on_submit():
		restaurants.rest_name = form.rest_name.data
		restaurants.meal = form.meal.data
		restaurants.location = form.location.data
		db.session.commit()
		rating = Rating.query.filter_by(rest_id = rest_id).first()
		db.session.delete(rating)
		db.session.commit()
		return redirect(url_for('rating', rest_id = restaurants.id))
	else:
		print(form.errors)
	return render_template('restaurant.html', title='Restuarant', restaurants = restaurants, form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
        if  current_user.is_authenticated:
                return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
                hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(first_name =form.first_name.data, last_name=form.last_name.data, email = form.email.data, password = hash_pw)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('post'))
        return render_template('register.html', title='Register', form=form)

@app.route('/Post', methods=['GET','POST'])
@login_required
def post():
        form = PostForm()
        if form.validate_on_submit():
                post = Post(
                        title = form.title.data,
                        content = form.content.data,
                        author = current_user)
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('home'))
        return render_template("post.html", form=form)

@app.route('/')
@app.route('/home')
def home():
	restaurants = Restaurant.query.all()
	posts = Post.query.all()
	rating = Rating.query.all()
	return render_template("home.html", title='Home', posts=posts, rating_value=rating, restaurants=restaurants)

@app.route('/about')
def About():
        return render_template('About.html', title='About')


