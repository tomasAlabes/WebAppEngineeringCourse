from loginout.cookies import CookieManager
from models.user import User
from templateHandler import TemplateHandler

class LoginHandler(TemplateHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            CookieManager.set_secure_cookie('user_id', str(u.key().id()), self.response)
            self.redirect('/?username=' + username)
        else:
            msg = 'Invalid user/password'
            self.render('login.html', error = msg)


class LogoutHandler(TemplateHandler):
    def get(self):
        CookieManager.set_empty_cookie(self.response)
        self.redirect("/")