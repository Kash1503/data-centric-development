import os
from flask import Flask, redirect, request, render_template, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'secret_key'

# Get the MySQL username from C9
username = os.getenv('C9_USER')

# Connect to the Recipes database
connection = pymysql.connect(host='localhost',
                            user=username,
                            password='',
                            db='Recipes')
                            
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/insert_user', methods=['POST'])
def insert_user():
    
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
    
    # Store username entered by the user in a variable
    form_username = request.form.get('username')
    
    with connection.cursor() as cursor:
            
        cursor.execute('SELECT * FROM User WHERE Username = %s;', form_username.lower())
        result = cursor.fetchone()
        
        if result != None:
            # If it does, redirect to the user page
            return redirect(url_for('user_page', username=form_username))
                
        else:
            # If not, display Flash message and return to the login page
            flash('Sorry, this is not a valid username')
            return redirect(url_for('login'))

@app.route('/user_page/<username>')
def user_page(username):
    
    with connection.cursor() as cursor:
        
        # Search for the full user data to pass to 'user'html'
        cursor.execute('SELECT * FROM User WHERE Username = %s;', username.lower())
        result = cursor.fetchone()
        
    return render_template('user.html', user_data=result)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)