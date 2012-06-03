from loginout.cookies import CookieManager
from templateHandler import TemplateHandler
from models.user import User
import re

USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
PASSWORD_RE = re.compile('^.{3,20}$')
EMAIL_RE = re.compile('^[\S]+@[\S]+\.[\S]+$')

class SignUpHandler(TemplateHandler):
    def get(self):
        self.render("signUp.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
            email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if self.email and not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signUp.html', **params)
        else:
            u = User.by_name(self.username)
            if u:
                msg = 'That user already exists.'
                self.render('signUp.html', error_username = msg)
            else:
                if self.email:
                    u = User.register(self.username, self.password, self.email)
                else:
                    u = User.register(self.username, self.password)
                u.put()

                CookieManager.set_secure_cookie('user_id', str(u.key().id()), self.response)
                self.redirect('/?username=' + self.username)

def valid_username(username):
    return USER_RE.match(username)

def valid_email(email):
    return EMAIL_RE.match(email)

def valid_password(password):
    return PASSWORD_RE.match(password)

class WelcomeHandler(TemplateHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.render('welcome.html')

