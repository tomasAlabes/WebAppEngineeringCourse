from google.appengine.ext import db

class History(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)


    @classmethod
    def by_title(cls, title):
        h = db.GqlQuery('SELECT * FROM History WHERE title= :1', title)
        return h