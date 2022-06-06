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

def enter_new_song_to_song_table(song_name, artist, album, spotify_song_id, release_date=None):
    song = Song(name=song_name, artist=artist, album=album, release_date=release_date, spotify_song_id=spotify_song_id)
    db.session.add(song)
    return song

def enter_new_song_to_user(user_id, song, genre_name):
    #need to take out user connection and put into another crud function
    # song = Song(name=song_name, artist=artist, album=album, release_date=release_date, spotify_song_id=spotify_song_id)
    print(song)
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
    
    song_obj = Song.query.filter(Song.spotify_song_id == spotify_song_id).first()
    #this will return None is there is no song id at that spotify id`
    return song_obj

def check_if_song_exists_for_user(user_id, song_id):

    # song = db.session.query(User_song.song_id).filter(User_song.user_id) == user_id).first()
    #getting a song_id based on the passed spotify_id
    # song_id = db.session.query(Song.song_id).filter(spotify_song_id == Song.spotify_song_id).first()
    #this will return None is there is no song id at that spotify id
    
    #checking if song_id exists
    listened  = db.session.query(User_Song).filter(song_id == User_Song.song_id, user_id == User_Song.user_id).first()
    #returns song object
    #in server, if this function returns anything but None, a user HAS listened to the song
    print(song_id)
    print(user_id)
    return listened



# query to songs table to find the song id that relates to the spotify id
# user song id to see if user id has song id





# def check_password_by_username(username, password):



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
    print("genre_id_lst", genre_id_lst)
    for genre_id in genre_id_lst:
        print("\tgenre_id", genre_id)
        song_ids_obj.append(db.session.execute(f"""SELECT song_id
                        FROM user_songs
                        JOIN songs USING (song_id)
                        JOIN songs_genres USING (song_id)
                        WHERE user_id={user_id} AND songs_genres.genre_id={genre_id}""").fetchall())
        print("\tsong_ids_obj", song_ids_obj, "******")

    # song_ids = []
    # for song in song_ids_obj:
    #     song_ids.append(song[0])
    #     print("\tsong", song)
    
    # print("song_ids", song_ids)
    


# x = db.session.query(User_Song.song_id, User_Song.user_id,Song_Genre.genre_id).join(Song).filter(User_Song.song_id == 1).join(Song_Genre).filter(Song_Genre.genre_id==1)

# # select song_id, user_id, songs_genres.genre_id from user_songs
# join songs
# using (song_id)
# join songs_genres
# using (song_id)
# where user_id = ??? and songs_genres.genre_id = ???;

# db.session.execute(f"""SELECT song_id, user_id, songs_genres.genre_id FROM user_songs
#                         JOIN songs USING (song_id)
#                         JOIN songs_genres USING (song_id)
#                         WHERE user_id={1} AND songs_genres.genre_id={1}""")

# functions for showing user profile information
#     -show genres by user id as an <a> link 
#     -show all songs by user id 



    """
    # query for all of user's songs,
    # place each song in the correct list based on what genre it is
    song_by_genre_dict = {"pop": [<Song_obj>]}
    genre_name--> user.users_to_users_genres[0].users_genres_to_genre.genre_name
    list of songs--> user.users_to_user_songs[0].user_songs_to_songs
    list of gernres related to soing
--> user.users_to_user_songs[0].user_songs_to_songs.songs_to_songs_genres    

session["user_id"]
we have a user
get users user_genres and user songs

we make a dict with genre_objs as keys
        lists of songs_objects as values"""

def make_user_profile_dictionary(user_id):

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


'''



songs_by_genre_dict = { 87: # genre_id
                            {"genre": <genre_obj>, "song_list": [<song_obj>, <song_obj>]}}

{% for genre_id in songs_by_genre_dict% }
    <button> {{songs_by_genre_dict[genre_id]["genre"].genre_name}}</button> # <button>Pop</button>
        <ul>
            for song in songs_by_genre_dict[genre_id]["songs"]
            <li> {{song.song_name}} </lil>
        </ul>


{user_genre : song, song, song, song, song}
{"pop":[ song_obj, song_obj], "brazil": song_obj, song_obj}
"""


#     genres = [ user_genre.users_genres_to_genre for user_genre in user.users_to_users_genres]

# list comprtehension
#             expression                for        item        in   iterable
#                   num * 2                                  num     in     nums
#                   obj.attr              for         obj         in      list

##double_list.append(num*2) -> this is expression in list comprehension
'''


def find_favorite_songs(user_id):
    '''In users_songs at user_id & song_id, where like=True'''
    liked_song_ids = db.session.query(User_Song.song_id).filter(User_Song.user_id == user_id, User_Song.like == True).all()

    song_id_list = [] 
    liked_songs_information = []

    for liked_song_id in liked_song_ids:
        song_id_list.append(liked_song_id[0])

    for song_id in song_id_list:
        liked_songs_information.append(Song.query.get(song_id))

    print(liked_songs_information)

    return liked_songs_information

if __name__ == "__main__":
    from server import app
    # DebugToolbarExtension(app)
    connect_to_db(app, "appdb")
