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

def add_genre_to_database(genre_name):
    #get entire list of genre choices and put into database
    genre = Genre(genre_name=genre_name)
    
    db.session.add(genre)
    db.session.commit()
    return genre



def enter_new_song_to_user(user_id, song_name, artist, album, spotify_song_id, genre_name, release_date=None):

    song = Song(name=song_name, artist=artist, album=album, release_date=release_date, spotify_song_id=spotify_song_id)
    song.songs_to_user_songs.append(User_Song(user_id=user_id))
    db.session.add(song)
    # .append(songs_genres(genre_id=genre_name))
    #step 1
    # User.query.filter(User.email == email).first()
    genre_obj = Genre.query.filter(Genre.genre_name == genre_name).first()
    genre_id = genre_obj.genre_id
    #need query from genre table getting genre_id by genre_name
    song_genre = Song_Genre(song_id=song.song_id, genre_id=genre_id)
    #add song id to the songs_genres table
    #adding song information to song_genres table
    db.session.add(song_genre)

    #step 2
    #using the same query from genre table (genre id) we can then populate users_genres

    user_genre = User_Genres(user_id=user_id, genre_id=genre_id)

    db.session.add(user_genre)
    print('successful add')
    db.session.commit()
    return song

# print(db.session.query(User_songs.song_id).filter_by(User.user_id == session["user_id"]).first())

def get_song_id_by_spotify_id(spotify_song_id):
    
    song_id = db.session.query(Song.song_id).filter(spotify_song_id == Song.spotify_song_id).first()
    #this will return None is there is no song id at that spotify id`
    return song_id

def check_if_song_exists_for_user(user_id, song_id):

    # song = db.session.query(User_song.song_id).filter(User_song.user_id) == user_id).first()
    #getting a song_id based on the passed spotify_id
    # song_id = db.session.query(Song.song_id).filter(spotify_song_id == Song.spotify_song_id).first()
    #this will return None is there is no song id at that spotify id
    
    #checking if song_id exists
    listened  = db.session.query(User_Song).filter(song_id == User_Song.song_id, user_id == User_Song.user_id).first()
    #returns song object
    #in server, if this function returns anything but None, a user HAS listened to the song
    return listened



# query to songs table to find the song id that relates to the spotify id
# user song id to see if user id has song id


# def enter_song_into_genre_for_user(user_id, song_name, genre_id, genre_name)
#     song_genre = 


# def check_password_by_username(username, password):



# function for reponse from spotify api into song and genre table


# functions for showing user profile information
#     -show genres by user id as an <a> link 
#     -show all songs by user id 

if __name__ == "__main__":
    from server import app
    # DebugToolbarExtension(app)
    connect_to_db(app, "appdb")

