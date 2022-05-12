from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
import jinja2
from os import environ 
import base64
import requests
from datetime import datetime
import random

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

    if 'username' not in session or 'auth_token' not in session:
        return redirect('/')
    elif check_if_token_is_expired(session['auth_token']['arrival_time']): 
        return redirect('/auth')
    else:
        # get spotify genre seeds to populate dropdown menu
        genre_endpoint = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
        headers = {
        'Authorization' : f"Bearer {session['auth_token']['access_token']}",
        'Content-Type' : 'application/json'
        }
        genres_request = requests.get(url=genre_endpoint, headers=headers)
        genres_json = genres_request.json()
        genres_list = []
        for genres in genres_json['genres']:
            genres_list.append(genres)
        
        return render_template('homepage.html', genres=genres_list)

@app.route('/homepage', methods=['POST'])
def spotify_requests():
    genre_choice = request.form.get('genre_selection')

    get_current_user_id_endpoint = 'https://api.spotify.com/v1/me'

    headers = {
        'Authorization' : f"Bearer {session['auth_token']['access_token']}",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    spotify_user_id_request = requests.get(url=get_current_user_id_endpoint, headers=headers)
    spotify_user_id_request_json = spotify_user_id_request.json()
    # print(spotify_user_id_request.json())
    spotify_user_id = spotify_user_id_request_json['id']
    # print(spotify_user_id)

    get_current_users_playlists_endpoint = f'https://api.spotify.com/v1/users/{spotify_user_id}/playlists'
    spotify_users_playlists_request = requests.get(url=get_current_users_playlists_endpoint, headers=headers)
    spotify_users_playlists_request_json = spotify_users_playlists_request.json()
    # print(spotify_users_playlists_request_json)
    playlist_choice = random.choice(spotify_users_playlists_request_json['items'])
    # print(playlist_choice)
    playlist_id = playlist_choice['id']
    # print(playlist_id)


    get_users_playlist_items_endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    spotify_users_playlist_items = requests.get(url=get_users_playlist_items_endpoint, headers=headers)
    spotify_users_playlist_items_json = spotify_users_playlist_items.json()
    song_choice = random.choice(spotify_users_playlist_items_json['items'])
    # print(spotify_users_playlist_items_json['items'][0])
    song_id = song_choice['track']['id']
    artist_id = song_choice['track']['artists'][0]['id']
    # print(artist_id)


    get_recommendation_request_endpoint = f"https://api.spotify.com/v1/recommendations?limit=1&seed_artists={artist_id}&seed_genres={genre_choice}&seed_tracks={song_id}"
    get_recommendation_request = requests.get(url=get_recommendation_request_endpoint, headers=headers)
    get_recommendation_request_json = get_recommendation_request.json()
    print(get_recommendation_request_json)

    return "terminal"
    # doo all my requests here???

    # return json object 


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