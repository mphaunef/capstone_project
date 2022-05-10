from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
import jinja2
from os import environ 
import base64
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined
CLIENT_ID = environ['CLIENT_ID']
CLIENT_SECRET = environ['CLIENT_SECRET']


def check_if_token_is_expired(session_arrival_time_value):
    now_time = datetime.utcnow()
    print(now_time)
    session_arrival_time_value = session_arrival_time_value.replace(tzinfo=None)
    print(session_arrival_time_value)
    time_difference = now_time - session_arrival_time_value
    return time_difference.total_seconds() > 3600
    

@app.route('/')
def show_login():
    return render_template('login.html')

@app.route('/handlelogin', methods=['POST'])
def handle_login():


    username = request.form.get('username')
    password = request.form.get('password')

    user = crud.get_by_username(username)

    if not user: 
        flash('Incorrect user or password. Please try again.')
        return redirect('/')
    if user:
        if user.password == password:
            session["username"] = user.username
            # session['logged_in'] = True
            return redirect('/grantspotify')
        else:
            flash('Incorrect user or password. Please try again.')
            return redirect('/login')



@app.route('/newuser')
def show_new_user_page():
    return render_template('create_user.html')


@app.route('/newuser', methods=['POST'])
def handle_new_user():

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_by_email(email)

    if user:
        flash('Account already exists. Please try again.')
        return redirect('/newuser')
    else: 
        user_information = crud.create_new_user(email, password, username)
        session["username"] = user_information.username
        # session["logged_in"] = True
        return redirect('/grantspotify')


@app.route('/grantspotify')
def display_spotify_button():
    return render_template('spotifybutton.html')




@app.route('/homepage')
def display_homepage():
    # #request.args
    # access_code = request.args.get('code')

    if 'username' not in session or 'auth_token' not in session:
        return redirect('/')
    elif check_if_token_is_expired(session['auth_token']['arrival_time']): 
        return redirect('/auth')
    else:
        # get spotify genre seeds to populate dropdown menu
        return render_template('homepage.html')


@app.route('/auth')
def handle_access_code():
    access_code = request.args.get('code')
    print(access_code)
    token_url = 'https://accounts.spotify.com/api/token'
    redirect_after_login = 'http://localhost:5000/auth'
    auth_header = base64.urlsafe_b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode()) 
    headers = { 
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth_header.decode("ascii")}'
    }

    if 'auth_token' not in session:
        payload = {
        'grant_type': 'authorization_code',
        'code': access_code,
        'redirect_uri': redirect_after_login
         }
        token_request = requests.post(url=token_url, data=payload, headers=headers)
        session['auth_token'] = token_request.json()
    else: 
        refresh_payload = {
        'grant_type': 'refresh_token',
        'refresh_token' : session['auth_token']['refresh_token']
        }
        token_request = requests.post(url=token_url, data=refresh_payload, headers=headers)
        data = token_request.json()
        session['auth_token'].update({'access_token':data['access_token']})
        session.modified = True 

    print(token_request.json())
    session['auth_token']['arrival_time'] = datetime.utcnow()
    

    return redirect('/homepage')




@app.route('/sign_out')
def sign_out():
    session.clear()
    return redirect('/')

#@app.route('/??profile??')
#def profile_page():
# return render_template('user_profile.html')

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app, "appdb")
    app.run(host="0.0.0.0", debug=True)