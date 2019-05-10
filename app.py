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


@app.route('/add_recipe/<username>')

# Render the 'addrecipe.html' template and pass in the username from user.html
# and pass in the cuisine and allergen collections

def add_recipe(username):
    return render_template('addrecipe.html', username=username, 
                                            allergens=mongo.db.allergens.find(), 
                                            cuisine=mongo.db.cuisine.find())
    

@app.route('/edit_recipe/<username>/<recipe_id>')

# Render the 'editrecipe.html' template and pass in the username from user.html
# and pass in the cuisine and allergen collections

def edit_recipe(username, recipe_id):
    return render_template('editrecipe.html', username=username, 
                                            allergens=mongo.db.allergens.find(), 
                                            cuisine=mongo.db.cuisine.find(),
                                            recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}))


@app.route('/user_page/<username>')
def user_page(username):

# Query all of the information for the user and then render the 
# 'user.html' template, passing in the result from the query
    
    # Search for the user in user collection using the username passed 
    # into user_page function and store returned dict in a variable
    user_data = mongo.db.user.find_one({'username': username.lower()})
    
    # Search for the recipes created by the user and store information in a variable
    recipes = mongo.db.recipes.find({'user': username.lower()})
    
    return render_template('user.html', username=username, user_data=user_data, recipes=recipes)
    

@app.route('/browse/<username>')
def browse(username):
    
# Load the browse page and pass in data from the recipes, allergens and 
# cuisine collections for use with filtering

    # Store the searches in variables
    recipes = mongo.db.recipes.find()
    allergens = mongo.db.allergens.find()
    cuisine = mongo.db.allergens.find()
    
    # Render the browse.html page and pass in data, keeping the 
    # username to pass back to user page if needed
    return render_template('browse.html', username=username,
                                            recipes=recipes,
                                            allergens=allergens,
                                            cuisine=cuisine)

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
        

@app.route('/insert_recipe/<username>', methods=['POST'])
def insert_recipe(username):
    
# Take data from the add recipe form and 
# create new entry in the recipe collection
    
    # Take data from the form and add it to a new dict, including default values
    # such as the views, upvotes and user, then store in a variable
    new_recipe = {
        
        'title': request.form.get('title'),
        'instructions': request.form.get('instructions'),
        'ingredients': request.form.get('ingredients'),
        'servings': request.form.get('servings'),
        'time': request.form.get('time'),
        'cuisine': request.form.get('cuisine'),
        'views': 0,
        'user': username.lower(),
        'description': request.form.get('description'),
        'allergen': request.form.get('allergen'),
        'upvotes': 0,
        'carbs': request.form.get('carbs'),
        'protein': request.form.get('protein'),
        'fat': request.form.get('fat'),
        'calories': request.form.get('calories'),
    }
    
    # Store the collection connection to a variable
    recipes = mongo.db.recipes
    # Insert the new recipe into the recipes collection
    recipes.insert_one(new_recipe)
    # redirect back to the user page, passing in the username
    return redirect(url_for('user_page', username=username.lower()))
    

@app.route('/update_recipe/<username>/<recipe_id>', methods=['POST'])
def update_recipe(username, recipe_id):
    
# Take new data from the edit recipe form and 
# update entry in the recipe collection
    
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    
    # Take data from the form and add it to a new dict, ensuring to retain values
    # such as the views, upvotes and user, then store in a variable
    updated_recipe = {
        
        'title': request.form.get('title'),
        'instructions': request.form.get('instructions'),
        'ingredients': request.form.get('ingredients'),
        'servings': request.form.get('servings'),
        'time': request.form.get('time'),
        'cuisine': request.form.get('cuisine'),
        'views': recipe['views'],
        'user': username.lower(),
        'description': request.form.get('description'),
        'allergen': request.form.get('allergen'),
        'upvotes': recipe['upvotes'],
        'carbs': request.form.get('carbs'),
        'protein': request.form.get('protein'),
        'fat': request.form.get('fat'),
        'calories': request.form.get('calories'),
    }
    
    # Store the collection connection to a variable
    recipes = mongo.db.recipes
    # Update with the updated recipe into the recipes collection
    recipes.update({'_id': ObjectId(recipe_id)}, updated_recipe)
    # redirect back to the user page, passing in the username
    return redirect(url_for('user_page', username=username.lower()))
    
    
# Get the IP address and PORT number from the os and run the app
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)