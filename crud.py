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



# def check_password_by_username(username, password):



# function for reponse from spotify api into song and genre table


# functions for showing user profile information
#     -show genres by user id as an <a> link 
#     -show all songs by user id 

if __name__ == "__main__":
    from server import app
    # DebugToolbarExtension(app)
    connect_to_db(app, "appdb")

