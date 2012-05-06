__author__ = 'Tomi'

import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape= True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    subject = db.StringProperty(required= True)
    content = db.TextProperty(required= True)
    date = db.DateProperty(auto_now_add= True)


class BlogHandler(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY date DESC LIMIT 10")
        self.render("blog.html", posts= posts)

class NewPostHandler(Handler):
    def get(self):
        self.render("newPost.html")
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            newPost = Post(subject=subject, content=content)
            newPostKey = newPost.put()
            self.redirect('/blog/%s' % newPostKey.id())
        else:
            error = "We need both subject and content!"
            self.render("newPost.html", subject=subject, content=content, error= error)



class PostHandler(Handler):
    def get(self, postId):
        post = Post.get_by_id(int(postId))
        self.render("post.html", post= post)
