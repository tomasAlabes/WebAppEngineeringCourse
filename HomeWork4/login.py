__author__ = 'Tomi'

from templateHandler import TemplateHandler
from HomeWork4.hashes import HashManager
from google.appengine.ext import db

class LoginHandler(TemplateHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        hashManager = HashManager()

        db_password_hash = self.getDBPasswordHash(username)
        if db_password_hash and hashManager.validPassword(username, password, db_password_hash):
            self.redirect("/welcome")
        else:
            self.render("login.html", error= "Wrong User/Password")

    def getDBPasswordHash(self, username):
        query = "SELECT * FROM User WHERE name = '" + username + "'"
        hash = db.GqlQuery(query)
        if hash:
            return hash[0].password_hash


class LogoutHandler(TemplateHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.redirect("/signup")