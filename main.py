#main.py backup

import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Post(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class Blog(Handler):
    def render_front(self):
    	posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")

    	self.render("front.html", posts=posts)

    def get(self):
        self.render_front()

class NewPost(Handler):
	def render_newpost(self, subject="", content="", error=""):
		self.render("newpost.html", subject=subject, content=content, error=error)

	def get(self):
		self.render_newpost()

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			p = Post(subject = subject, content = content)
			p.put()

			self.redirect("/blog")
		else:
			error = "Enter both a title and a post to continue."
			self.render_newpost(subject, content, error)

#class NewPost(Handler):
	# we were working right here, and it might be easier to completely start over with a new file
	# also, we want to figure out how to break all these classes out into their own files

app = webapp2.WSGIApplication([
	('/blog', Blog),
	('/blog/newpost', NewPost)
], debug=True)
