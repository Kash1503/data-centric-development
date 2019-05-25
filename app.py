# Imports
import os
from flask import Flask, redirect, request, render_template, url_for, flash
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.objectid import ObjectId
from bson.json_util import dumps


app = Flask(__name__)

app.config["MONGO_DBNAME"] = "recipesDB"
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

app.secret_key = os.getenv('SECRET_KEY')

mongo = PyMongo(app)

# Variables
time_options = ['1-30', '31-60', '61-90', '91-120', '121-150', '151-180']
servings_options = ['1-5', '6-10', '11-15', '16-20']
calories_options = ['1-250', '251-500', '501-750', '751-1000']
    
# Render Templates

@app.route('/')
@app.route('/login')
def login():
    
    """Render the 'login.html' template"""

    return render_template('login.html')


@app.route('/register')
def register():
    
    """Render the 'register.html' template"""
    
    return render_template('register.html')


@app.route('/add_recipe/<username>')
def add_recipe(username):
    
    """
    Render the 'addrecipe.html' template and pass in the username from user.html 
    and pass in the cuisine and allergen collections
    """
    
    return render_template('addrecipe.html', username=username, 
                                            allergens=mongo.db.allergens.find(), 
                                            cuisine=mongo.db.cuisine.find())
    
@app.route('/edit_recipe', defaults={'username': 'testuser', 'source': 'browse', 'recipe_id': '5ce95bc41c9d440000985a6b'})
@app.route('/edit_recipe/<username>/<source>/<recipe_id>')
def edit_recipe(username, source, recipe_id):
    
    """
    Render the 'editrecipe.html' template and pass in the username from user.html
    and pass in the cuisine and allergen collections
    """
    
    return render_template('editrecipe.html', username=username, 
                                            allergens=mongo.db.allergens.find(), 
                                            cuisine=mongo.db.cuisine.find(),
                                            recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}),
                                            source=source)


@app.route('/user_page', defaults={'username': 'testuser'})
@app.route('/user_page/<username>')
def user_page(username):

    """
    Query all of the information for the user and then render the 
    'user.html' template, passing in the result from the query
    """
    
    user_data = mongo.db.user.find_one({'username': username})
    recipes = mongo.db.recipes.find({'user': username}).sort([('upvotes', -1), ('views', -1)])
    return render_template('user.html', username=username, 
                                        user_data=user_data, 
                                        recipes=recipes,
                                        allergens=mongo.db.allergens.find(), 
                                        cuisine=mongo.db.cuisine.find(),
                                        time_options=time_options,
                                        servings_options=servings_options,
                                        calories_options=calories_options)
    

@app.route('/browse', defaults={'username': 'testuser'})
@app.route('/browse/<username>')
def browse(username):
    
    """
    Load the browse page and pass in data from the recipes, allergens and 
    cuisine collections for use with filtering
    """

    recipes = mongo.db.recipes.find().sort([('upvotes', -1), ('views', -1)])
    return render_template('browse.html', username=username,
                                            recipes=recipes,
                                            allergens=mongo.db.allergens.find(), 
                                            cuisine=mongo.db.cuisine.find(),
                                            time_options=time_options,
                                            servings_options=servings_options,
                                            calories_options=calories_options)


@app.route('/recipe_details', defaults={'username': 'testuser', 'source': 'browse', 'recipe_id': '5ce95bc41c9d440000985a6b'})
@app.route('/recipe_details/<username>/<source>/<recipe_id>')
def recipe_details(username, source, recipe_id):
    
    """
    Using the recipe ID, display the recipe details page and pass
    the data in. Also pass username to pass back to user if needed.
    Also add 1 to the views for the recipe when this page is loaded.
    """
    
    recipe_views = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    mongo.db.recipes.update({'_id': ObjectId(recipe_id)}, { '$set': {'views': recipe_views['views'] + 1}})
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    user = mongo.db.user.find_one({'username': recipe['user']})
    
    return render_template('recipedetails.html', username=username, source=source, recipe=recipe, user=user)


@app.route('/analytics_page/<username>')
def analytics_page(username):
    
    """Take the user to the analytics page and pass in the username"""
    
    return render_template('analytics.html', username=username)


# Functions, queries and redirects

@app.route('/insert_user', methods=['POST'])
def insert_user():

    """Take data from the form on the registration page and insert into the User table"""
    
    user = mongo.db.user
    
    if user.find_one({'username': request.form.get('username')}) == None:
        new_user = {
            'username': request.form.get('username').lower(),
            'firstname': request.form.get('firstname').lower(),
            'lastname': request.form.get('lastname').lower(),
            'country': request.form.get('country').lower()
        }
        user.insert_one(new_user)
        return redirect(url_for('login'))
    else:
        flash('Sorry, this username has already been taken')
        return redirect(url_for('register'))
    
    
@app.route('/get_user', methods=['POST'])
def get_user():

    """
    Take username entered by the user and use it to query the User table. 
    If the result is not None, redirect the user to the user page and 
    pass the entered username to the user_page function
    """

    form_username = request.form.get('username')
    user = mongo.db.user.find_one({'username': form_username.lower()})
    
    if user != None:
        return redirect(url_for('user_page', username=user['username']))
    else:
        flash('Sorry, this is not a valid username')
        return redirect(url_for('login'))
        

@app.route('/insert_recipe', defaults={'username': 'testuser'}, methods=['POST'])
@app.route('/insert_recipe/<username>', methods=['POST'])
def insert_recipe(username):
    
    """
    Take data from the add recipe form and 
    create new entry in the recipe collection
    """
    
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
        'isTest': 'False',
        'imageURL': request.form.get('imageURL')
    }
    
    recipes = mongo.db.recipes
    recipes.insert_one(new_recipe)
    
    return redirect(url_for('user_page', username=username))
    

@app.route('/update_recipe', defaults={'username': 'testuser', 'recipe_id': '5ce95bc41c9d440000985a6b'}, methods=['POST'])
@app.route('/update_recipe/<username>/<recipe_id>', methods=['POST'])
def update_recipe(username, recipe_id):
    
    """
    Take new data from the edit recipe form and 
    update entry in the recipe collection
    """
    
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    
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
        'isTest': recipe['isTest'],
        'imageURL': request.form.get('imageURL')
    }
    
    recipes = mongo.db.recipes
    recipes.update({'_id': ObjectId(recipe_id)}, updated_recipe)
    
    return redirect(url_for('user_page', username=username))


@app.route('/delete_recipe', defaults={'username': 'testuser', 'recipe_id': '2f1ebf38bcee491dd7187c25'})
@app.route('/delete_recipe/<username>/<recipe_id>')
def delete_recipe(username, recipe_id):

    """Using the id of the recipe, delete it from the collection"""
    
    recipes = mongo.db.recipes
    recipes.remove({'_id': ObjectId(recipe_id)})
    
    return redirect(url_for('user_page', username=username))
    
    
def browse_filter(form_allergen, form_cuisine, allergens, cuisine, time, servings, calories):
    if (form_allergen != 'all') and (form_cuisine == 'all'):
        recipes = mongo.db.recipes.find(
        {
            'allergen': { '$not': { '$regex': allergens }}, 
            'servings': servings, 
            'time': time, 
            'calories': calories
        }).sort([('upvotes', -1), ('views', -1)])
    elif (form_allergen == 'all') and (form_cuisine != 'all'):
        recipes =  mongo.db.recipes.find(
        {
            'cuisine': cuisine, 
            'servings': servings, 
            'time': time, 
            'calories': calories
        }).sort([('upvotes', -1), ('views', -1)])
    elif (form_allergen != 'all') and (form_cuisine != 'all'):
        recipes = mongo.db.recipes.find(
        {
            'cuisine': cuisine, 
            'allergen': { '$not': { '$regex': allergens }}, 
            'servings': servings, 
            'time': time, 
            'calories': calories
        }).sort([('upvotes', -1), ('views', -1)])
    else: 
        recipes = mongo.db.recipes.find(
        {
            'servings': servings, 
            'time': time, 
            'calories': calories
        }).sort([('upvotes', -1), ('views', -1)])

    return recipes

def user_filter(form_allergen, form_cuisine, username, allergens, cuisine, time, servings, calories):
    if (form_allergen != 'all') and (form_cuisine == 'all'):
        recipes = mongo.db.recipes.find(
        {
            'user': username,
            'allergen': { '$not': { '$regex': allergens }}, 
            'servings': servings, 
            'time': time, 
            'calories': calories
        }).sort([('upvotes', -1), ('views', -1)])
    elif (form_allergen == 'all') and (form_cuisine != 'all'):
        recipes =  mongo.db.recipes.find(
        {
            'user': username,
            'cuisine': cuisine, 
            'servings': servings, 
            'time': time, 
            'calories': calories
        }).sort([('upvotes', -1), ('views', -1)])
    elif (form_allergen != 'all') and (form_cuisine != 'all'):
        recipes = mongo.db.recipes.find(
        {
            'user': username,
            'cuisine': cuisine, 
            'allergen': { '$not': { '$regex': allergens }}, 
            'servings': servings, 
            'time': time, 
            'calories': calories
        }).sort([('upvotes', -1), ('views', -1)])
    else: 
        recipes = mongo.db.recipes.find(
        {
            'user': username,
            'servings': servings, 
            'time': time, 
            'calories': calories
        }).sort([('upvotes', -1), ('views', -1)])

    return recipes
    
    
@app.route('/filter_recipes', defaults={'username': 'testuser', 'source': 'browse.html'}, methods=['POST'])
@app.route('/filter_recipes/<username>/<source>', methods=['POST'])
def filter_recipes(username, source):
    
    """filter the recipes on the browsing page based on selections made by the user"""
    
    time_split = request.form.get('time').split('-')
    servings_split = request.form.get('servings').split('-')
    calories_split = request.form.get('calories').split('-')
    
    if request.form.get('cuisine') != 'all':
        cuisine_filter = request.form.get('cuisine')
    else:
        cuisine_filter = 'all'
    if request.form.get('allergens') != 'all':
        allergens_filter = request.form.get('allergens')
    else:
        allergens_filter = 'all'
    
    servings_filter = { '$gte': int(servings_split[0]), '$lte': int(servings_split[1])}
    time_filter = { '$gte': int(time_split[0]), '$lte': int(time_split[1])}
    calories_filter = { '$gte': int(calories_split[0]), '$lte': int(calories_split[1])}
    
    if source == 'browse.html':
        recipes = browse_filter(form_allergen=request.form.get('allergens'),
                                form_cuisine=request.form.get('cuisine'),
                                allergens=allergens_filter, 
                                cuisine=cuisine_filter, 
                                time=time_filter, 
                                servings=servings_filter, 
                                calories=calories_filter)
    else:
        recipes = user_filter(form_allergen=request.form.get('allergens'),
                                form_cuisine=request.form.get('cuisine'),
                                username=username,
                                allergens=allergens_filter, 
                                cuisine=cuisine_filter, 
                                time=time_filter, 
                                servings=servings_filter, 
                                calories=calories_filter)
    
    active_filters = {
        'time': request.form.get('time'),
        'servings': request.form.get('servings'),
        'calories': request.form.get('calories'),
        'cuisine': request.form.get('cuisine'),
        'allergens': request.form.get('allergens')
    }
    
    if source == 'user.html':
        user_data = mongo.db.user.find_one({'username': username.lower()})
    else:
        user_data = None
    
    return render_template(source, username=username, 
                                    user_data=user_data,
                                    allergens=mongo.db.allergens.find(), 
                                    cuisine=mongo.db.cuisine.find(), 
                                    recipes=recipes,
                                    time_options=time_options,
                                    servings_options=servings_options,
                                    calories_options=calories_options,
                                    active_filters=active_filters)


@app.route('/upvote', defaults={'username': 'testuser', 'source': 'browse', 'recipe_id': '5ce95bc41c9d440000985a6b'})
@app.route('/upvote/<username>/<source>/<recipe_id>')
def upvote(username, source, recipe_id):

    """When the 'like' button is pressed, add one to the total upvotes for the recipe"""

    recipe_upvotes = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    mongo.db.recipes.update({'_id': ObjectId(recipe_id)}, { '$set': {'upvotes': recipe_upvotes['upvotes'] + 1}})
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    user = mongo.db.user.find_one({'username': recipe['user']})
    
    return render_template('recipedetails.html', username=username, source=source, recipe=recipe, user=user)


@app.route('/create_graph_data')
def create_graph_data():
    
    """
    Take data taken from a query of the recipes collection
    and store data as json to be used by dc.js, unless it
    is the recipe used for testing
    """
    
    recipes = mongo.db.recipes.find()
    json_recipes = []
    for recipe in recipes:
        if recipe['cuisine'] == 'testcuisine':
            continue
        elif recipe['allergen'] == 'testallergen':
            continue
        else:
            json_recipes.append(recipe)
    json_recipes = json.dumps(json_recipes, default=json_util.default)
    
    return json_recipes
    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)