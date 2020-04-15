from flask import Flask
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import cgi

app = Flask(__name__)

# engine = create_engine('sqlite:///database.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind = engine)
# session = DBSession()

@app.route('/')
@app.route('/restaurants')
def ShowRestaurants():
    return 'This page will show all the restaurants'

@app.route('/restaurants/new')
def newRestaurant():
    return 'This page will be for making a new restaurant'

@app.route('/restaurants/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    return 'This page will be for editing %s' % restaurant_id

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