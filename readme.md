This project is a CRUD project including JSON API done with Flask.
I am doing this to practice my backend skills with python.

#### JSON API
/restaurants/JSON
returns all the restaurants in the database

/restaurants/<restaurant_id:int>/menu/JSON
returns all the menu items of the restaurant in database

/restaurants/<restaurant_id:int>/menu/<menu_id:int>/JSON
returns the specified menu item in the database

# If you want to try it on your computer

1. You need python v3.x to run this code
2. With cmd navigate to the folder where you extracted it
3. Run the command 'python3 database_setup.py'
4. Now run the command 'python3 server.py'
5. Open browser with link 'http://127.0.0.1:5000/' or 'http://0.0.0.0:5000/'

Enjoy :)

Attension, this has nothing to do with the front-end only back-end