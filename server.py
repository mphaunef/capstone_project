from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
import jinja2

app = Flask(__name__)
app.secret_key = "7adc57a711cb4d5fa1aa9fd264397a89"
# app.jinja_env.undefined = StrictUndefined



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
            session['logged_in'] = True
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
        session["logged_in"] = True
        return redirect('/homepage')


@app.route('/grantspotify')
def display_spotify_button():
    return render_template('spotifybutton.html')


@app.route('/homepage')
def display_homepage():
    if user not in session:
        return redirect('/')
    else:
        # get spotify genre seeds to populate dropdown menu
        return render_template('homepage.html')

#@app.route('/??profile??')
#def profile_page():
# return render_template('user_profile.html')

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app, "appdb")
    app.run(host="0.0.0.0", debug=True)