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

    '''get entire list of genre choices and put into database'''

    genre = Genre(genre_name=genre_name)
    
    db.session.add(genre)
    db.session.commit()
    return genre


def enter_new_song_to_song_table(song_name, artist, album, spotify_song_id, release_date=None):

    song = Song(name=song_name, artist=artist, album=album, release_date=release_date, spotify_song_id=spotify_song_id)
    db.session.add(song)
    return song


def enter_new_song_to_user(user_id, song, genre_name):

    song.songs_to_user_songs.append(User_Song(user_id=user_id))
    db.session.add(song)

    #step 1
    genre_obj = Genre.query.filter(Genre.genre_name == genre_name).first()
    genre_id = genre_obj.genre_id

    song_genre = Song_Genre(song_id=song.song_id, genre_id=genre_id)
    db.session.add(song_genre)

    #step 2
    user_genre = User_Genres(user_id=user_id, genre_id=genre_id)
    db.session.add(user_genre)

    db.session.commit()
    return song


def get_song_id_by_spotify_id(spotify_song_id):

    #this will return None is there is no song id at that spotify id
    song_obj = Song.query.filter(Song.spotify_song_id == spotify_song_id).first()
    
    return song_obj


def check_if_song_exists_for_user(user_id, song_id):

    #returns song object
    #in server, if this function returns anything but None, a user HAS listened to the song

    listened  = db.session.query(User_Song).filter(song_id == User_Song.song_id, user_id == User_Song.user_id).first()

    return listened


def get_genre_id_for_user(user_id):
    #get information from user_genres table

    genre_objs = db.session.query(User_Genres.genre_id).filter(User_Genres.user_id == user_id).all()
    
    genre_ids = []
    for genre_obj in genre_objs:
        genre_id = genre_ids.append(genre_obj.genre_id)

    return genre_ids


def get_genre_name_by_id(genre_id):

    genre_name_obj = db.session.query(Genre.genre_name).filter(Genre.genre_id == genre_id).one()
    genre_name = genre_name_obj.genre_name
    
    return genre_name


def get_user_songs_id_by_genre(user_id, genre_id_lst): #1, [87, 117, 11, 1, 1]
    song_ids_obj = [] #[2, 3, 4, [4,7,8], [4,7,8] ]

    for genre_id in genre_id_lst:

        song_ids_obj.append(db.session.execute(f"""SELECT song_id
                        FROM user_songs
                        JOIN songs USING (song_id)
                        JOIN songs_genres USING (song_id)
                        WHERE user_id={user_id} AND songs_genres.genre_id={genre_id}""").fetchall())


def make_user_profile_dictionary(user_id):
    '''
        # query for all of user's songs,
        # place each song in the correct list based on what genre it is
        song_by_genre_dict = {"pop": [<Song_obj>]}
        genre_name --> user.users_to_users_genres[0].users_genres_to_genre.genre_name
        list of songs --> user.users_to_user_songs[0].user_songs_to_songs
        list of gernres related to song --> user.users_to_user_songs[0].user_songs_to_songs.songs_to_songs_genres    

        make a dict with genre_objs as keys
        lists of songs_objects as values
            
        songs_by_genre_dict = { 87: # genre_id
                                {"genre": <genre_obj>, "song_list": [<song_obj>, <song_obj>]}}
    '''

    songs_by_genre_dict= {}


    user = User.query.get(user_id) # User.query.get(user_id_goes_here)


    genres = [ user_genre.users_genres_to_genre for user_genre in user.users_to_users_genres]
    
    for user_genre in user.users_to_users_genres:
        songs_by_genre_dict[user_genre.genre_id] = {"genre":
             user_genre.users_genres_to_genre.genre_name, 
             "song_list": []}
    

    songs = [ user_song.user_songs_to_songs for user_song in user.users_to_user_songs ]
    for song in songs:
        genre_id = song.songs_to_songs_genres[0].genre_id
        if genre_id in songs_by_genre_dict:
            songs_by_genre_dict[genre_id]['song_list'].append(song)

    return songs_by_genre_dict


def find_favorite_songs(user_id):

    '''In users_songs at user_id & song_id, where like=True'''

    liked_song_ids = db.session.query(User_Song.song_id).filter(User_Song.user_id == user_id, User_Song.like == True).all()

    song_id_list = [] 
    liked_songs_information = []

    for liked_song_id in liked_song_ids:
        song_id_list.append(liked_song_id[0])

    for song_id in song_id_list:
        liked_songs_information.append(Song.query.get(song_id))

    return liked_songs_information


if __name__ == "__main__":
    from server import app
    # DebugToolbarExtension(app)
    connect_to_db(app, "appdb")
