__author__ = 'Tomi'

from HomeWork4.login import empty_cookie
from HomeWork4.hashes import HashManager
from templateHandler import TemplateHandler
from google.appengine.ext import db

hashManager = HashManager()

class Post(db.Model):
    subject = db.StringProperty(required= True)
    content = db.TextProperty(required= True)
    date = db.DateProperty(auto_now_add= True)


class BlogHandler(TemplateHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY date DESC LIMIT 10")
        self.render("blog.html", posts= posts)

class NewPostHandler(TemplateHandler):
    def get(self):
        idHash = self.request.cookies.get("user_id")
        if empty_cookie(idHash) and hashManager.validStringHash(idHash):
            self.render("newPost.html")
        else:
            self.redirect("/blog/signup")

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



class PostHandler(TemplateHandler):
    def get(self, postId):
        post = Post.get_by_id(int(postId))
        self.render("post.html", post= post)
