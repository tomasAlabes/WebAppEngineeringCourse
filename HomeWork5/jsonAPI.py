from HomeWork3.blog import Post

__author__ = 'Tomi'

from templateHandler import TemplateHandler
from google.appengine.ext import db
import json

#[{"content": "again", "subject": "the suit is back!"}, {"content": "hurray!", "subject": "a new post!"}, {"content": "H", "subject": "Huzzah!"}]

class JsonPostHandler(TemplateHandler):
    def get(self):
        self.response.headers['Content-Type'] = "application/json; charset=UTF-8"
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY date DESC LIMIT 10")
        postsList = list(posts)
        jsonList = []
        for post in postsList:
            jsonList.append({"content": post.content, "subject": post.subject})
        self.response.out.write(json.dumps(jsonList))

class PostJsonHandler(TemplateHandler):
    def get(self, postId):
        self.response.headers['Content-Type'] = "application/json; charset=UTF-8"
        post = Post.get_by_id(int(postId))
        self.response.out.write(json.dumps({"content": post.content, "subject": post.subject}))
