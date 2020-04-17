from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi

app = Flask(__name__)

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurant_list = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurant_list)

@app.route('/restaurants/new', methods = ['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        restaurant_name = request.form['name']

        if (restaurant_name.strip() == ''):
            return redirect(url_for('newRestaurant'))
        else:
            new_restaurant = Restaurant(name = restaurant_name)
            session.add(new_restaurant)
            session.commit()
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    if request.method == 'POST':
        edit_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one_or_none()
        if edit_restaurant == None:
            return redirect(url_for('showRestaurants'))
        else:
            restaurant_name = request.form['name']

            edit_restaurant.name = restaurant_name
            session.add(edit_restaurant)
            session.commit()
            return redirect(url_for('showRestaurants'))
    else:
        edit_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one_or_none()
        if edit_restaurant == None:
            return redirect(url_for('showRestaurants'))
        else:
            return render_template('editRestaurant.html', restaurant = edit_restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return 'This page will be for deleting %s' % restaurant_id

@app.route('/restaurants/<int:restaurant_id>')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return 'This page is the menu of the restaurant %s' % restaurant_id

@app.route('/restaurants/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return 'This page is for making a new item for restaurant %s' % restaurant_id

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return 'This page is for editing menu item %s' % menu_id

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return 'This page is for deleting menu item %s' % menu_id

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)