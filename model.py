from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)

    #relationships
    users_to_user_songs = db.relationship('User_Song', back_populates="user_songs_to_users")
    users_to_users_genres = db.relationship('User_Genres', back_populates="users_genres_to_users")

    def __repr__(self):
        return (f"<User user_id={self.user_id} email={self.email} password={self.password} username={self.username}>")


class User_Song(db.Model):

    __tablename__ = 'user_songs'

    user_songs_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    song_id = db.Column(db.Integer, db.ForeignKey("songs.song_id"))
    like = db.Column(db.Boolean)

    #relationships
    user_songs_to_users = db.relationship('User', back_populates="users_to_user_songs")
    user_songs_to_songs = db.relationship('Song', back_populates="songs_to_user_songs")

    def __repr__(self):
        return (f"<User_Song user_id={self.user_id} song_id={self.song_id} like={self.like}>")


class Song(db.Model):

    __tablename__ = 'songs'

    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    album = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime)
    spotify_song_id = db.Column(db.String, unique=True)

    #relationships?
    songs_to_user_songs = db.relationship('User_Song', back_populates="user_songs_to_songs")
    songs_to_songs_genres = db.relationship('Song_Genre', back_populates="songs_genres_to_songs")

    def __repr__(self):
        return (f"<Song song_id={self.song_id} name={self.name} artist={self.artist} album={self.album} release_date={self.release_date} spotify_song_id={self.spotify_song_id}>")


class Song_Genre(db.Model):

    __tablename__ = 'songs_genres'

    song_genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))

    #relationships
    songs_genres_to_songs = db.relationship('Song', back_populates="songs_to_songs_genres")
    songs_genres_to_genre = db.relationship('Genre', back_populates="genre_to_songs_genre")

    def __repr__(self):
        return (f"<Song_Genre song_genre_id={self.song_genre_id} song_id={self.song_id} genre_id={self.genre_id}>")


class Genre(db.Model):

    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre_name = db.Column(db.String)

    #relationships
    genre_to_songs_genre = db.relationship('Song_Genre', back_populates="songs_genres_to_genre")
    genre_to_users_genres = db.relationship('User_Genres', back_populates="users_genres_to_genre")
    
    def __repr__(self):
        return (f"<Genre genre_id={self.genre_id} genre_name={self.genre_name}>")


class User_Genres(db.Model):

    __tablename__ = 'users_genres'

    ''' All users playlists/genres '''
    user_genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    #relationships
    users_genres_to_genre = db.relationship('Genre', back_populates="genre_to_users_genres")
    users_genres_to_users = db.relationship('User', back_populates="users_to_users_genres")
    
    def __repr__(self):
        return (f"<User_Genres user_genre_id={self.user_genre_id} genre_id={self.genre_id} user_id={self.user_id}>")


def connect_to_db(flask_app, db_name):

    # db_uri= f"postgresql:///{db_name}", echo=True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    flask_app.config["SQLALCHEMY_ECHO"] = True
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app, "appdb")

