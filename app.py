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
    recipes = mongo.db.recipes.find({'user': username.lower()}).sort([('upvotes', -1), ('views', -1)])
    
    return render_template('user.html', username=username, user_data=user_data, recipes=recipes)
    

@app.route('/browse/<username>')
def browse(username):
    
# Load the browse page and pass in data from the recipes, allergens and 
# cuisine collections for use with filtering

    # Store the searches in variables
    recipes = mongo.db.recipes.find().sort([('upvotes', -1), ('views', -1)])
    allergens = mongo.db.allergens.find()
    cuisine = mongo.db.cuisine.find()
    
    # Create filter options to pass to browse.html
    time_options = ['1-30', '31-60', '61-90', '91-120', '121-150', '151-180']
    servings_options = ['1-5', '6-10', '11-15', '16-20']
    calories_options = ['1-250', '251-500', '501-750', '751-1000']
    
    # Render the browse.html page and pass in data, keeping the 
    # username to pass back to user page if needed
    return render_template('browse.html', username=username,
                                            recipes=recipes,
                                            allergens=allergens,
                                            cuisine=cuisine,
                                            time_options=time_options,
                                            servings_options=servings_options,
                                            calories_options=calories_options)


@app.route('/recipe_details/<username>/<source>/<recipe_id>')
def recipe_details(username, source, recipe_id):
    
# Using the recipe ID, display the recipe details page and pass
# the data in. Also pass username to pass back to user if needed.
# Also add 1 to the views for the recipe when this page is loaded.
    
    # Store the data from mongoDB in variables
    recipe_views = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    # Add one to the views for the recipe
    mongo.db.recipes.update({'_id': ObjectId(recipe_id)}, { '$set': {'views': recipe_views['views'] + 1}})
    # Store recipe in new variable with update 'views' field to pass to render template
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    # Render the recipe details page, passing in the relevant data
    return render_template('recipedetails.html', username=username, source=source, recipe=recipe)

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
        'servings': int(request.form.get('servings')),
        'time': int(request.form.get('time')),
        'cuisine': request.form.get('cuisine').lower(),
        'views': 0,
        'user': username.lower(),
        'description': request.form.get('description'),
        'allergen': request.form.get('allergen').lower(),
        'upvotes': 0,
        'carbs': int(request.form.get('carbs')),
        'protein': int(request.form.get('protein')),
        'fat': int(request.form.get('fat')),
        'calories': int(request.form.get('calories')),
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
        'servings': int(request.form.get('servings')),
        'time': int(request.form.get('time')),
        'cuisine': request.form.get('cuisine').lower(),
        'views': recipe['views'],
        'user': username.lower(),
        'description': request.form.get('description'),
        'allergen': request.form.get('allergen').lower(),
        'upvotes': recipe['upvotes'],
        'carbs': int(request.form.get('carbs')),
        'protein': int(request.form.get('protein')),
        'fat': int(request.form.get('fat')),
        'calories': int(request.form.get('calories')),
    }
    
    # Store the collection connection to a variable
    recipes = mongo.db.recipes
    # Update with the updated recipe into the recipes collection
    recipes.update({'_id': ObjectId(recipe_id)}, updated_recipe)
    # redirect back to the user page, passing in the username
    return redirect(url_for('user_page', username=username.lower()))


@app.route('/delete_recipe/<username>/<recipe_id>')
def delete_recipe(username, recipe_id):

# Using the id of the recipe, delete it from the collection
    
    # Store the collection connection in a variable
    recipes = mongo.db.recipes
    # Delete the recipe from the collection
    recipes.remove({'_id': ObjectId(recipe_id)})
    # Redirect back to the user page
    return redirect(url_for('user_page', username=username))


@app.route('/filter_recipes/<username>', methods=['POST'])
def filter_recipes(username):
    
# filter the recipes on the browsing page based on selections made by the user
    
    # Create variables to hold the data taken from the filter form
    
    # Split the value passed in from the form in order to use as part of the range
    time_split = request.form.get('time').split('-')
    servings_split = request.form.get('servings').split('-')
    calories_split = request.form.get('calories').split('-')
    
    # Check to see if the cuisine and allergens form are not equal to 'any', if so 
    # create a variable with the form data, else do not create variable
    if request.form.get('cuisine') != 'all':
        cuisine_filter = request.form.get('cuisine')
    if request.form.get('allergens') != 'all':
        allergens_filter = request.form.get('allergens')
    
    # Pass the split form data as integers to the variables to be used for the mongoDB find
    servings_filter = { '$gte': int(servings_split[0]), '$lte': int(servings_split[1])}
    time_filter = { '$gte': int(time_split[0]), '$lte': int(time_split[1])}
    calories_filter = { '$gte': int(calories_split[0]), '$lte': int(calories_split[1])}
    
    # Create new list of recipes based on the filter options
    # If 'any' was selected for allergens or cuisine, do not include in query parameters
    if (request.form.get('allergens') != 'all') and (request.form.get('cuisine') == 'all'):
        recipes = mongo.db.recipes.find(
        {
            'allergen': allergens_filter, 
            'servings': servings_filter, 
            'time': time_filter, 
            'calories': calories_filter
        }).sort([('upvotes', -1), ('views', -1)])
    elif (request.form.get('allergens') == 'all') and (request.form.get('cuisine') != 'all'):
        recipes = mongo.db.recipes.find(
        {
            'cuisine': cuisine_filter, 
            'servings': servings_filter, 
            'time': time_filter, 
            'calories': calories_filter
        }).sort([('upvotes', -1), ('views', -1)])
    elif (request.form.get('allergens') != 'all') and (request.form.get('cuisine') != 'all'):
        recipes = mongo.db.recipes.find(
        {
            'cuisine': cuisine_filter, 
            'allergen': allergens_filter, 
            'servings': servings_filter, 
            'time': time_filter, 
            'calories': calories_filter
        }).sort([('upvotes', -1), ('views', -1)])
    else: 
        recipes = mongo.db.recipes.find(
        {
            'servings': servings_filter, 
            'time': time_filter, 
            'calories': calories_filter
        }).sort([('upvotes', -1), ('views', -1)])
    
    # Create a dict of the active filters to pass to the browse.html page
    active_filters = {
        'time': request.form.get('time'),
        'servings': request.form.get('servings'),
        'calories': request.form.get('calories'),
        'cuisine': request.form.get('cuisine'),
        'allergens': request.form.get('allergens')
    }
    
    # Store collections for cuisine and allergens in variables to pass to browse.html
    allergens = mongo.db.allergens.find()
    cuisine = mongo.db.cuisine.find()
    
    # Create filter options to pass to browse.html
    time_options = ['1-30', '31-60', '61-90', '91-120', '121-150', '151-180']
    servings_options = ['1-5', '6-10', '11-15', '16-20']
    calories_options = ['1-250', '251-500', '501-750', '751-1000']
    
    # Redirect back to the browse page, with the new filtered recipe list
    return render_template('browse.html', username=username, 
                                        allergens=allergens, 
                                        cuisine=cuisine, 
                                        recipes=recipes,
                                        time_options=time_options,
                                        servings_options=servings_options,
                                        calories_options=calories_options,
                                        active_filters=active_filters)

  
@app.route('/upvote/<username>/<source>/<recipe_id>')
def upvote(username, source, recipe_id):

# When the 'like' button is pressed, add one to the total upvotes for the recipe

    # Store the data from mongoDB in variables
    recipe_upvotes = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    # Find the relevant recipe and add one to the total upvotes
    mongo.db.recipes.update({'_id': ObjectId(recipe_id)}, { '$set': {'upvotes': recipe_upvotes['upvotes'] + 1}})
    # Store the updated recipe data in a new variable, with the updated upvotes
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    # return back to the recipe details page, with the updated upvotes
    return render_template('recipedetails.html', username=username, source=source, recipe=recipe)
    
    
# Get the IP address and PORT number from the os and run the app
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)