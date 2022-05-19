from model import db, User, User_Song, Song, Song_Genre, Genre, User_Genres, connect_to_db

def create_new_user(email, password, username):
    
    user = User(email=email, password=password, username=username)

    db.session.add(user)
    db.session.commit()
    return user


def get_by_email(email):
    '''returns an entire object, not just email'''
    return User.query.filter(User.email == email).first()

def get_by_username(username):
    '''returns an entire object, not just username'''
    return User.query.filter(User.username == username).first()

def enter_new_song_to_user(user_id, song_name, artist, album, release_date, spotify_song_id):

    song = Song(name=song_name, artist=artist, album=album, release_date=release_date, spotify_song_id=spotify_song_id)
    song.songs_to_user_songs.append(User_Song(user_id=user_id))
    db.session.add(song)
    db.session.commit()
    return song


# def check_password_by_username(username, password):



# function for reponse from spotify api into song and genre table


# functions for showing user profile information
#     -show genres by user id as an <a> link 
#     -show all songs by user id 

if __name__ == "__main__":
    from server import app
    # DebugToolbarExtension(app)
    connect_to_db(app, "appdb")

