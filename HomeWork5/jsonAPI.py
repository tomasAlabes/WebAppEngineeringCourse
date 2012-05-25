from HomeWork3.blog import Post
from templateHandler import TemplateHandler
import json

#[{"content": "again", "subject": "the suit is back!"}, {"content": "hurray!", "subject": "a new post!"}, {"content": "H", "subject": "Huzzah!"}]

class JsonPostHandler(TemplateHandler):
    def get(self):
        self.response.headers['Content-Type'] = "application/json; charset=UTF-8"
        posts = Post.all().order('-created')
        jsonList = []
        for post in posts:
            jsonList.append({"content": post.content, "subject": post.subject})
        self.response.out.write(json.dumps(jsonList))

class PostJsonHandler(TemplateHandler):
    def get(self, postId):
        self.response.headers['Content-Type'] = "application/json; charset=UTF-8"
        post = Post.get_by_id(int(postId))
        self.response.out.write(json.dumps({"content": post.content, "subject": post.subject}))
