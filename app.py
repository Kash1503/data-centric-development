import os
from flask import Flask, redirect, request, render_template, url_for
import pymysql

app = Flask(__name__)

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
        
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)