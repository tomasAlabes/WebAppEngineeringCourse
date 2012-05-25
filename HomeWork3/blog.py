__author__ = 'Tomi'

import webapp2
from HomeWork3.postModel import Post
from HomeWork4.cookies import CookieManager
from HomeWork4.userModel import User
from templateHandler import TemplateHandler
from google.appengine.api import memcache
import time

class BlogHandler(TemplateHandler):
    def top_posts(self, update = False):
        key = "top"
        tops = memcache.get(key)
        now = int(time.time())
        if tops is None or update:
            tops = Post.all().order('-created')
            memcache.set(key, tops)
            memcache.set("time", now)
        secondsAgo = now - int(memcache.get("time"))
        return [tops, secondsAgo]

    def get(self):
        posts = self.top_posts()
        self.render("blog.html", posts = posts[0], secondsAgo = posts[1])

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = CookieManager.read_secure_cookie('user_id', self.request)
        self.user = uid and User.by_id(int(uid))


class NewPostHandler(BlogHandler):
    def get(self):
        if self.user:
            self.top_posts(True)
            self.render("newPost.html")
        else:
            self.redirect("/blog/login")

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newPost.html", subject=subject, content=content, error=error)


class PostHandler(BlogHandler):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))

        if not post:
            self.error(404)
            return

        now = int(time.time())
        postTimeKey = "time" + post_id
        postTimeCached = memcache.get(postTimeKey)
        if not postTimeCached:
            memcache.set(postTimeKey, now)

        secondsAgo = now - int(memcache.get(postTimeKey))

        self.render("post.html", post = post, secondsAgo = secondsAgo)
