from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, forms, push_manager
from models import User, Property, Favorite
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import json

@app.route('/')
@app.route('/index')
def index():
    properties = Property.query.all()
    return render_template('index.html', properties=properties)

@app.route('/property/<int:property_id>')
def property(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('property.html', property=property)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/favorites')
@login_required
def favorites():
    user = User.query.get(current_user.id)
    favorites = user.favorites
    return render_template('favorites.html', favorites=favorites)

@app.route('/add_to_favorites/<int:property_id>')
@login_required
def add_to_favorites(property_id):
    property = Property.query.get_or_404(property_id)
    if property not in current_user.favorites:
        current_user.favorites.append(property)
        db.session.commit()
        flash('Property added to favorites', 'success')
    else:
        flash('Property already in favorites', 'info')
    return redirect(url_for('property', property_id=property_id))

@app.route('/remove_from_favorites/<int:property_id>')
@login_required
def remove_from_favorites(property_id):
    property = Property.query.get_or_404(property_id)
    if property in current_user.favorites:
        current_user.favorites.remove(property)
        db.session.commit()
        flash('Property removed from favorites', 'success')
    else:
        flash('Property not in favorites', 'info')
    return redirect(url_for('property', property_id=property_id))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search']
        properties = Property.query.filter(Property.name.ilike(f'%{search_term}%') | Property.location.ilike(f'%{search_term}%')).all()
        return render_template('index.html', properties=properties)
    return redirect(url_for('index'))

@app.route('/rate_property/<int:property_id>', methods=['POST'])
@login_required
def rate_property(property_id):
    property = Property.query.get_or_404(property_id)
    rating = request.form.get('rating')
    if rating:
        property.rating = rating
        db.session.commit()
        flash('Property rated successfully', 'success')
    else:
        flash('Please select a rating', 'danger')
    return redirect(url_for('property', property_id=property_id))

@app.route('/review_property/<int:property_id>', methods=['POST'])
@login_required
def review_property(property_id):
    property = Property.query.get_or_404(property_id)
    review = request.form.get('review')
    if review:
        property.review = review
        db.session.commit()
        flash('Property reviewed successfully', 'success')
    else:
        flash('Please enter a review', 'danger')
    return redirect(url_for('property', property_id=property_id))