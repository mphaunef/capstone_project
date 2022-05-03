from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)

    #relationships

    def __repr__(self):

class User_Song(db.Model):

    __tablename__ = 'user_songs'

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    song_id = db.Column(db.Integer, db.ForeignKey("songs.song_id"))
    like = db.Column(db.Boolean)

    #relationships

    def __repr__(self):


class Song(db.Model):

    __tablename__ = 'songs'

    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    album = db.Column(db.String, nullable=False)
    release_date = db.Column(db.datetime, nullable=False)

    #relationships?

    def __repr__(self):


class Song_Genre(db.Model):

    __tablename__ = 'songs_genres'

    song_genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'))
    genre_id = db.Column(db.String, db.ForeignKey('genres.genre_id'))

    #relationships

    def __repr__(self):

