# Imports
import os
from flask import Flask, redirect, request, render_template, url_for, flash
import pymysql

app = Flask(__name__)

# Create secret key
app.secret_key = 'secret_key'

# Get the MySQL username from C9
username = os.getenv('C9_USER')

# Connect to the Recipes database
connection = pymysql.connect(host='localhost',
                            user=username,
                            password='',
                            db='Recipes')
                         

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

    with connection.cursor() as cursor:
        
        # Search for the full user data to pass to 'user'html'
        cursor.execute('SELECT * FROM User WHERE Username = %s;', username.lower())
        result = cursor.fetchone()
        
    return render_template('user.html', user_data=result)
    
    
# Functions, queries and redirects

@app.route('/insert_user', methods=['POST'])
def insert_user():

# Take data from the form on the registration page and insert into the User table

    try:
        with connection.cursor() as cursor:
            # Create a tuple from the form data on the registration page
            row = (request.form.get('username').lower(), 
                    request.form.get('country'), 
                    request.form.get('firstname'), 
                    request.form.get('lastname'))
            
            # Insert the new row into the User table
            cursor.execute('INSERT INTO User (Username, Country, Firstname, Lastname) VALUES (%s, %s, %s, %s);', row)
            connection.commit()
    finally:
        # Close the connection
        connection.close()
    
    # Go back to the login page
    return redirect(url_for('login'))


@app.route('/get_user', methods=['POST'])
def get_user():
    
# Take username entered by the user and use it to query the User table. 
# If the result is not None, redirect the user 
# to the user page and pass the entered username to the user_page function

    # Store username entered by the user in a variable
    form_username = request.form.get('username')
    
    with connection.cursor() as cursor:
        
        # Query the database, using the variable created above
        cursor.execute('SELECT * FROM User WHERE Username = %s;', form_username.lower())
        result = cursor.fetchone()
        
        if result != None:
            # If it does, redirect to the user page
            return redirect(url_for('user_page', username=form_username))
                
        else:
            # If not, add Flash message and return to the login page
            flash('Sorry, this is not a valid username')
            return redirect(url_for('login'))

# Get the IP address and PORT number from the os and run the app
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)