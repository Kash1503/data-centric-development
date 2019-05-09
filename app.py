# Imports
import os
from flask import Flask, redirect, request, render_template, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "recipesDB"
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

app.secret_key = os.getenv('SECRET_KEY')

mongo = PyMongo(app)

# Render Templates

@app.route('/')
@app.route('/login')

# Render the 'login.html' template

def login():
    return render_template('login.html')


@app.route('/register')

# Render the 'register.html' template

def register():
    return render_template('register.html')


@app.route('/user_page/<username>')
def user_page(username):

# Query all of the information for the user and then render the 
# 'user.html' template, passing in the result from the query
    
    # Search for the user in user collection using the username passed 
    # into user_page function and store returned dict in a variable
    user_data = mongo.db.user.find_one({'username': username.lower()})
    
    # Search for the recipes created by the user and store information in a variable
    recipes = mongo.db.recipes.find({'user': username.lower()})
    
    return render_template('user.html', user_data=user_data, recipes=recipes)
    
    
# Functions, queries and redirects

@app.route('/insert_user', methods=['POST'])
def insert_user():

# Take data from the form on the registration page and insert into the User table
    
    # Store the user collection in variable 'user'
    user = mongo.db.user
    # Insert the form data into the user collection
    user.insert_one(request.form.to_dict())
    # Go back to the login page
    return redirect(url_for('login'))


@app.route('/get_user', methods=['POST'])
def get_user():

# Take username entered by the user and use it to query the User table. 
# If the result is not None, redirect the user 
# to the user page and pass the entered username to the user_page function

    # Store username entered by the user in a variable
    form_username = request.form.get('username')
    # Search for a user in the user collection and store the result in a variable
    user = mongo.db.user.find_one({'username': form_username.lower()})
    
    # Check to see if the form username returns an entry from the user collection
    if user != None:
        # If it does, redirect to the user page
        return redirect(url_for('user_page', username=user['username']))
    else:
        # If not, add Flash message and return to the login page
        flash('Sorry, this is not a valid username')
        return redirect(url_for('login'))
        

# Get the IP address and PORT number from the os and run the app
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)