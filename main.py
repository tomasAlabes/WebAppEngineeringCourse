import webapp2
from loginout.login import LogoutHandler, LoginHandler
from loginout.signup import SignUpHandler, WelcomeHandler
from wiki.edit_wiki import EditPageHandler
from wiki.history import HistoryPageHandler
from wiki.new_wiki import WikiPageHandler

PAGE_RE = r'((?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
    ('/signup', SignUpHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/_history/' + PAGE_RE, HistoryPageHandler),
    ('/_edit/' + PAGE_RE, EditPageHandler),
    ('/' + PAGE_RE, WikiPageHandler)],
    debug=True)