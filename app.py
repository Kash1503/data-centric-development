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


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)