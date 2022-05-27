from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db, User_Song
import crud
import jinja2
from os import environ 
import base64
import requests
from datetime import datetime
import random
import json

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
            session["user_id"] = user.user_id 
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
        print(genres_list)
        return render_template('homepage.html', genres=genres_list)

@app.route('/homepage', methods=['POST'])
def spotify_requests():
    '''All requests to Spotify API'''


    #Users genre choice from "ajaxhomepage.js"
    genre_choice = request.json

    headers = {
        'Authorization' : f"Bearer {session['auth_token']['access_token']}",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    '''Request for current Spotify user Id'''

    get_current_user_id_endpoint = 'https://api.spotify.com/v1/me'
    spotify_user_id_request = requests.get(url=get_current_user_id_endpoint, headers=headers)
    spotify_user_id_request_json = spotify_user_id_request.json()

    spotify_user_id = spotify_user_id_request_json['id']

    '''Request for current Spotify user's playlists'''

    get_current_users_playlists_endpoint = f'https://api.spotify.com/v1/users/{spotify_user_id}/playlists'
    spotify_users_playlists_request = requests.get(url=get_current_users_playlists_endpoint, headers=headers)
    spotify_users_playlists_request_json = spotify_users_playlists_request.json()

    #Randomly selecting a users playlist id
    playlist_choice = random.choice(spotify_users_playlists_request_json['items'])
    playlist_id = playlist_choice['id']


    '''Request to get chosen playlists items(songs)'''

    get_users_playlist_items_endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    spotify_users_playlist_items = requests.get(url=get_users_playlist_items_endpoint, headers=headers)
    spotify_users_playlist_items_json = spotify_users_playlist_items.json()
    


    #Randomly selecting a song from the randomly selected playlist
    song_choice = random.choice(spotify_users_playlist_items_json['items'])
    song_id = song_choice['track']['id']
    artist_id = song_choice['track']['artists'][0]['id']


    '''Request to put all previous responses together and get a Spotify recommendation response'''

    get_recommendation_request_endpoint = f"https://api.spotify.com/v1/recommendations?limit=1&seed_artists={artist_id}&seed_genres={genre_choice}&seed_tracks={song_id}"
    get_recommendation_request = requests.get(url=get_recommendation_request_endpoint, headers=headers)
    get_recommendation_request_json = get_recommendation_request.json()
  
    #TO-DO: if tracks not in response from spotify, get new response
    '''Declaring variables for data entry into database'''

    recommended_song_id = get_recommendation_request_json['tracks'][0]['id']


    # unusable_song = True
 
    while True:
        song_obj = crud.get_song_id_by_spotify_id(recommended_song_id) #recommended_song_id
        if song_obj != None:
            checking_if_user_listened = crud.check_if_song_exists_for_user(user_id=session['user_id'], song_id=song_obj.song_id)
            if checking_if_user_listened == None:  
                #do everything again
                # crud.enter_new_song_to_user(user_id=3, song=checking_song_obj, genre_name=genre_choice)
                # unusable_song = False
                break
            else:
                song_choice = random.choice(spotify_users_playlist_items_json['items'])
                song_id = song_choice['track']['id']
                artist_id = song_choice['track']['artists'][0]['id']
                get_recommendation_request_endpoint = f"https://api.spotify.com/v1/recommendations?limit=1&seed_artists={artist_id}&seed_genres={genre_choice}&seed_tracks={song_id}"
                get_recommendation_request = requests.get(url=get_recommendation_request_endpoint, headers=headers)
                get_recommendation_request_json = get_recommendation_request.json()
                recommended_song_id = get_recommendation_request_json['tracks'][0]['id']
                break

        else:
            # make a song obj
            recommended_song_name = get_recommendation_request_json['tracks'][0]['name'] # these lines may not need to happen until you have a viable song
            recommended_song_artist = get_recommendation_request_json['tracks'][0]['album']['artists'][0]['name']
            recommended_song_album = get_recommendation_request_json['tracks'][0]['album']['name']
            recommended_song_release_date = get_recommendation_request_json['tracks'][0]['album']['release_date']
            # overwriting song_obj variable name so that it's no longer None
            song_obj = crud.enter_new_song_to_song_table(spotify_song_id=recommended_song_id, song_name=recommended_song_name, artist=recommended_song_artist, album=recommended_song_album, release_date=recommended_song_release_date)
            # unusable_song = False
            break
    crud.enter_new_song_to_user(user_id=session['user_id'], song=song_obj, genre_name=genre_choice)



    # recommended_song_name = get_recommendation_request_json['tracks'][0]['name'] # these lines may not need to happen until you have a viable song
    # recommended_song_artist = get_recommendation_request_json['tracks'][0]['album']['artists'][0]['name']
    # recommended_song_album = get_recommendation_request_json['tracks'][0]['album']['name']
    # recommended_song_release_date = get_recommendation_request_json['tracks'][0]['album']['release_date']

    #Database entry
    # checking_song_obj = crud.get_song_id_by_spotify_id('0sdhpuSSWjRvrVAYDyWaBc')
    # print(checking_song_obj)

    # print(f"SESSION USER ID = {session['user_id']}")
    # print('i am after the None')
    # if checking_song_obj != None:

    #     print('i am in side database now')
    #     #checking if a user has listened to this song (returns song obj or None)
    #     checking_if_user_listened = crud.check_if_song_exists_for_user(user_id=3, song_id=checking_song_obj.song_id)
    #     print(checking_if_user_listened)


    #     if checking_if_user_listened == None:

    #         # crud.enter_new_song_to_user(user_id=session['user_id'],spotify_song_id=recommended_song_id, song_name=recommended_song_name, artist=recommended_song_artist, album=recommended_song_album, release_date=recommended_song_release_date, genre_name=genre_choice)
    #         # user_id=session['user_id']
    #         crud.enter_new_song_to_user(user_id=3, song=checking_song_obj, genre_name=genre_choice)
    #         #need to write new function to replace this ^ that connects existing
    #         #song in song table to specific user
    #         return jsonify('0sdhpuSSWjRvrVAYDyWaBc')
    #         # return ('ya')
    #     else:
    #         print('i exist idiot')
    #         return ('no')
    #         spotify_requests()
    # else:

    #     # crud.enter_new_song_to_user(user_id=session['user_id'],spotify_song_id=1RwwmiVtLAtPmxAqKVfwgG, song_name=recommended_song_name, artist=recommended_song_artist, album=recommended_song_album, release_date=recommended_song_release_date, genre_name=genre_choice)
    #     crud.enter_new_song_to_song_table(spotify_song_id=recommended_song_id, song_name=recommended_song_name, artist=recommended_song_artist, album=recommended_song_album, release_date=recommended_song_release_date, genre_name=genre_choice)
    #     return jsonify(recommended_song_id)




    # crud.enter_new_song_to_user(user_id=session['user_id'],spotify_song_id=recommended_song_id, song_name=recommended_song_name, artist=recommended_song_artist, album=recommended_song_album, release_date=recommended_song_release_date, genre_name=genre_choice)

    return jsonify(recommended_song_id)



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