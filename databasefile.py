from google.appengine.ext import db

class User(db.Model):
	user = db.UserProperty()	# indicates first column
	nickname = db.StringProperty()
	email = db.StringProperty()
	userclass = db.StringProperty()
	
class Posts(db.Model):
	post_id = db.IntegerProperty()	# first column, id of post
	title = db.StringProperty(multiline = False)	# removes multiline purpose
	smile = db.StringProperty() # the id of the smile/gift
	message = db.StringProperty(str)
	
	post_time = db.DateTimeProperty(auto_now_add = True)
	sender = db.ReferenceProperty(User, collection_name = 'sender')
	receiver = db.ReferenceProperty(User, collection_name = 'posts') # "User" refers to database, "posts" refers
																	# to the function you call to retrieve data
	
class Favourites(db.Model):
	user_fav = db.ReferenceProperty(User, collection_name = 'user_fav')
	no_of_favs = db.IntegerProperty()
	favs = db.ReferenceProperty(User, collection_name = 'favs')