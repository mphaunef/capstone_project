from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import jinja2


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/newuser')
def create_new_user():
    return render_template('create_user.html')

@app.route('/home')
def homepage():
    return render_template('homepage.html')

#@app.route('/??profile??')
#def profile_page():
# return render_template('user_profile.html')