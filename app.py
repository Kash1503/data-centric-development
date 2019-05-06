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
                            



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)