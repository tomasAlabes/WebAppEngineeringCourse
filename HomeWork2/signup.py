__author__ = 'Tomi'

import re
from templateHandler import TemplateHandler
from HomeWork4.userModel import User
from HomeWork4.hashes import HashManager

USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
PASSWORD_RE = re.compile('^.{3,20}$')
EMAIL_RE = re.compile('^[\S]+@[\S]+\.[\S]+$')

hashManager = HashManager()

class SignUpHandler(TemplateHandler):
    def get(self):
        self.render("signUp.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        err_user = ""
        if not USER_RE.match(username):
            err_user = "That's not a valid username."

        err_passw1 = ""
        err_passw2 = ""
        if len(password)==0 or not PASSWORD_RE.match(password):
            err_passw1 = "Type a password"
        elif password != verify:
            err_passw2 = "Your passwords didn't match."

        err_email = ""
        if len(email) != 0 and not EMAIL_RE.match(email):
            err_email = "That's not a valid email address"

        if err_user or err_passw1 or err_passw2 or err_email:
            self.render("signUp.html", username = username, email = email, err_user = err_user, err_passw1 = err_passw1,
                err_passw2 = err_passw2, err_email = err_email)
        else:
            password_hash = hashManager.makePasswordHash(username, password)
            if email:
                newUser = User(name = username, password_hash = password_hash, email = email)
            else:
                newUser = User(name = username, password_hash = password_hash)
            newUserKey = newUser.put()
            newUserId = str(newUserKey.id())
            self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % hashManager.makeStringHash(newUserId))
            self.redirect("/welcome")

def valid_username(username):
    return USER_RE.match(username)

def valid_email(email):
    return EMAIL_RE.match(email)

def valid_password(password):
    return PASSWORD_RE.match(password)

COOKIE_RE = re.compile(r'.+=; Path=/')
def valid_cookie(cookie):
    return cookie and COOKIE_RE.match(cookie)

class WelcomeHandler(TemplateHandler):
    def get(self):
        idHash = self.request.cookies.get("user_id")
        if not valid_cookie(idHash) or hashManager.validStringHash(idHash):
            validId = int(idHash.split('|')[0])
            username = (User.get_by_id(validId))
            self.render("welcome.html", username= str(username.name))
        else:
            self.redirect("/signup")

