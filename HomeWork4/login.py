__author__ = 'Tomi'

import re
from templateHandler import TemplateHandler
from HomeWork4.hashes import HashManager
from google.appengine.ext import db

hashManager = HashManager()

class LoginHandler(TemplateHandler):
    def get(self):
        idHash = self.request.cookies.get("user_id")
        if empty_cookie(idHash) and hashManager.validStringHash(idHash):
            self.render("blog.html")
        else:
            self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        db_password_hash = self.getDBPasswordHash(username)
        if db_password_hash and hashManager.validPassword(username, password, db_password_hash):
            self.redirect("/blog/welcome")
        else:
            self.render("login.html", error= "Wrong User/Password")

    def getDBPasswordHash(self, username):
        hash = db.GqlQuery("SELECT * FROM User WHERE name = :username", username=username)
        if hash.count() > 0:
            return hash[0].password_hash

COOKIE_RE = re.compile(r'.+=;\s*Path=/')
def empty_cookie(cookie):
    return cookie is not None and COOKIE_RE.match(cookie)

class LogoutHandler(TemplateHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.redirect("/blog/signup")