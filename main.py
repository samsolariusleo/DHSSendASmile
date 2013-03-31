import webapp2	# web application framework
import jinja2	# template engine
import os		# access file system
import datetime # format date time
from google.appengine.api import users	# Google account authentication
from google.appengine.ext import db		# datastore
from google.appengine.api import mail	# send email

import databasefile

# initialize template
template_dir = os.path.join(os.path.dirname(__file__), '')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Posts(db.Model):
	sender = db.StringProperty()
	receiver = db.StringProperty(required = True)
	smile = db.StringProperty(required = True)
	message = db.StringProperty()
	created = db.DateTimeProperty(auto_now_add = True)
	
class Personas(db.Model):
	username = db.StringProperty(required = True)
	classes = db.StringProperty(required = True)
	nickname = db.StringProperty(required = True)
	
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
		
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
	
class MainPage(Handler):
	def render_index(self, sender = '', receiver = '', message = '', error_msg = '', error_receiver = '',
						success = ''):
		posts = db.GqlQuery('SELECT * FROM Posts'
							'ORDER BY created DESC')
		self.render('index.html', sender = sender, receiver = receiver, message = message, error_msg = error_msg,
					error_receiver = error_receiver, success = success)
					
	def render_error(self, sender = '', receiver = '', message = '', error_msg = '', error_receiver = '',
						success = ''):
		self.render('error.html', sender = sender, receiver = receiver, message = message, error_msg = error_msg,
					error_receiver = error_receiver, success = success)
		
	def get(self):
		user = users.get_current_user()
		
		if user:
			personas = db.GqlQuery('SELECT * FROM Personas ORDER BY pid ASC')
			self.render('index.html', signout = users.create_logout_url('/'), personas=personas)
			
		else:
			self.redirect(users.create_login_url('/'))
			
	def post(self):
		personas = db.GqlQuery('SELECT * FROM Personas ORDER BY ID ASC')
		sender = users.get_current_user()
		receiver = self.request.get('receiver')
		smile = self.request.get('smile')
		message = self.request.get('message')
			
		if sender and receiver and smile:
			if receiver not in personas:
				success = "Error!"
				error_receiver = "Error! There is no such user or you are not entering the correct username."
				self.render_error(success = success, error_receiver = error_receiver)
				
			else:
				post = Posts(sender = sender, receiver = receiver, smile = smile, message = message)
				post.put()
				success = "Success!"
				error_msg = "Your smile was sent successfully!"
				self.render_error(success = success, error_msg = error_msg)
				
		elif len(message) > 140:
			success = "Error!"
			error_msg = "Messages should not be more than 140 characters."
			self.render_error(success = success, error_msg = error_msg)
				
		else:
			success = "Error!"
			error_msg = "Error! You have not entered the username of the receipient."
			self.render_error(success = success, error_msg = error_msg)
	
class ErrorHandler(Handler):
	def get(self):
		self.render('error.html', error_msg = error_msg, error_receiver = error_receiver, success = success)
	
# class SendSmile(Handler):
	# def render_index(self, sender = '', receiver = '', message = '', error_msg = ''):
		# posts = db.GqlQuery('SELECT * FROM Posts'
							# 'ORDER BY created DESC')
		# self.render('index.html', sender = sender, receiver = receiver, message = message, error_msg = error_msg)
		
	# def get(self):
		# pass
		
	# def post(self):
		# sender = users.get_current_user().nickname()
		# receiver = self.request.get('receiver')
		# smile = self.request.get('smile')
		# message = self.request.get('message')
		
		# if len(message) > 140:
			# error_msg = "Messages should not be more than 140 characters."
			# self.render_index(receiver, message)
			
		# elif sender and receiver and smile:
			# p = Posts(sender = sender, receiver = receiver, smile = smile, message = message)
			# p.put()
			
			# self.redirect('/')
						
class Signout(Handler):
	def get(self):
		self.render('signout.html', signout = users.create_logout_url('/'))
	
# main

app = webapp2.WSGIApplication([('/', MainPage),('/signout', Signout),('/error', ErrorHandler)],
                              debug=True)