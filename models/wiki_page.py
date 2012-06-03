from google.appengine.ext import db

class Wiki(db.Model):
    title = db.StringProperty(required= True)
    content = db.TextProperty(required= True)
    created = db.DateProperty(auto_now_add= True)
    last_modified = db.DateTimeProperty(auto_now = True)


    @classmethod
    def by_title(cls, title):
        w = Wiki.all().filter('title =', title).get()
        return w