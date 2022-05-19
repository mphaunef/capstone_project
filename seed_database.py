import os
import model
import server
import crud


os.system("dropdb appdb")
os.system("createdb appdb")
model.connect_to_db(server.app, "appdb")
model.db.create_all()


