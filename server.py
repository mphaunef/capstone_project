from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import jinja2

app = Flask(__name__)
app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined


@app.route('/')
def login():
    return render_template('login.html')

# @app.route('/handlelogin', methods=['POST'])
# def handle_login():

#     # .get email
#     # .get password
#     # .get user

#     # if user doesnt exist or if password is incorrect
#     #     flash message ('Incorrect user or password. Please try again.')
#     #     redirect to /login
#     # else:
#     #     session log in = True

#     #     redirect to /homepage

@app.route('/newuser')
def create_new_user():
    return render_template('create_user.html')

    #redirect to 

@app.route('/home')
def homepage():
    return render_template('homepage.html')

#@app.route('/??profile??')
#def profile_page():
# return render_template('user_profile.html')

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)