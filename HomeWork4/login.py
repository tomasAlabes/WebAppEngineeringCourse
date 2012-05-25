__author__ = 'Tomi'

from templateHandler import TemplateHandler
from HomeWork4.cookies import CookieManager
from HomeWork4.userModel import User

class LoginHandler(TemplateHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            CookieManager.set_secure_cookie('user_id', str(u.key().id()), self.response)
            self.redirect('/blog')
        else:
            msg = 'Invalid user/password'
            self.render('login.html', error = msg)


class LogoutHandler(TemplateHandler):
    def logout(self):
        CookieManager.set_empty_cookie(self.response)
        self.redirect("/blog")