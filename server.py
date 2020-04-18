from flask import Flask, render_template, url_for, request, redirect, flash
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
            flash('The field \'name\' was empty')
            return redirect(url_for('newRestaurant'))
        else:
            new_restaurant = Restaurant(name = restaurant_name)
            session.add(new_restaurant)
            session.commit()
            # OTOD: send the notification to the user
            flash('New restaurant added')
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    edit_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one_or_none()

    if edit_restaurant == None:
        flash('No restaurant found to edit')
        return redirect(url_for('showRestaurants'))
    else:
        if request.method == 'POST':
            edit_restaurant.name = request.form['name']
            session.add(edit_restaurant)
            session.commit()

            flash('Restaurant edited successfully')
            return redirect(url_for('showRestaurants'))
        else:
            # OTOD: send the notification to the user
            return render_template('editRestaurant.html', restaurant = edit_restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    delete_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one_or_none()

    if delete_restaurant == None:
        flash('No restaurant found to delete')
        return redirect(url_for('showRestaurants'))
    else:
        if request.method == 'POST':
            menu_item_list_deleted = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).delete()
            session.delete(delete_restaurant)
            session.commit()

            flash('Restaurant with %d menus deleted successfully' % menu_item_list_deleted)
            return redirect(url_for('showRestaurants'))
        else:
            return render_template('deleteRestaurant.html', restaurant = delete_restaurant)

@app.route('/restaurants/<int:restaurant_id>')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one_or_none()

    if restaurant == None:
        flash('No restaurant found')
        return redirect(url_for('showRestaurants'))
    else:
        items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
        return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one_or_none()
    if restaurant == None:
        flash('No restaurant found')
        return redirect(url_for('showRestaurants'))
    else:
        if request.method == 'POST':
            name = str(request.form['name']).strip()
            description = str(request.form['description']).strip()
            price = str(request.form['price']).strip()
            course = str(request.form['course']).strip()

            if name == '' or description == '' or price == '' or course == '':
                flash('One or more fields were empty')
                return redirect(url_for('newMenuItem', restaurant_id = restaurant_id))
            else:
                new_menu_item = MenuItem(name = name, description = description, price = price, course = course, restaurant_id = restaurant_id)
                session.add(new_menu_item)
                session.commit()
                flash('Menu Item created successfully')
                return redirect(url_for('showMenu', restaurant_id = restaurant_id))
        else:
            return render_template('newMenuItem.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant_list = session.query(Restaurant).all()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one_or_none()
    menu_item = session.query(MenuItem).filter_by(id = menu_id).one_or_none()

    if restaurant == None:
        flash('No restaurant found')
        return redirect(url_for('showRestaurants'))
    elif menu_item == None:
        flash('No menu item found')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        if request.method == 'POST':
            name = str(request.form['name']).strip()
            description = str(request.form['description']).strip()
            price = str(request.form['price']).strip()
            course = str(request.form['course']).strip()
            new_restaurant_id = str(request.form['new_restaurant_id']).strip()

            if name == '' or description == '' or price == '' or course == '':
                flash('One or more fields were empty')
                return redirect(url_for('editMenuItem', restaurant_id = restaurant_id, menu_id = menu_id))
            else:
                if new_restaurant_id == '':
                    new_restaurant_id = restaurant_id

                new_restaurant = session.query(Restaurant).filter_by(id = new_restaurant_id).one_or_none()

                if new_restaurant == None:
                    flash('No restaurant found')
                    return render_template('editMenuItem.html', restaurant = restaurant, menu_item = menu_item, restaurant_list = restaurant_list)
                
                menu_item.name = name
                menu_item.description = description
                menu_item.price = price
                menu_item.course = course
                menu_item.restaurant_id = new_restaurant_id

                session.add(menu_item)
                session.commit()

                flash('Menu item edited successfully')
                return redirect(url_for('showMenu', restaurant_id = restaurant_id))
        else:
            return render_template('editMenuItem.html', restaurant = restaurant, menu_item = menu_item, restaurant_list = restaurant_list)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one_or_none()
    menu_item = session.query(MenuItem).filter_by(id = menu_id).one_or_none()

    if restaurant == None:
        flash('No restaurant found')
        return redirect(url_for('showRestaurants'))
    elif menu_item == None:
        flash('No menu item found')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        if request.method == 'POST':
            session.delete(menu_item)
            session.commit()

            flash('Menu item deleted successfully')
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
        else:
            return render_template('deleteMenuItem.html', restaurant = restaurant, menu_item = menu_item)

if __name__ == '__main__':
    app.debug = True
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(host = '0.0.0.0', port = 5000)