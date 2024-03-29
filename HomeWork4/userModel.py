from HomeWork4.hashes import HashManager
from google.appengine.ext import db

class User(db.Model):
    name = db.StringProperty(required= True)
    pw_hash = db.StringProperty(required= True)
    email = db.EmailProperty(required= False)
    created = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = HashManager.make_pw_hash(name, pw)
        return User(parent = users_key(),
            name = name,
            pw_hash = pw_hash,
            email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and HashManager.valid_pw(name, pw, u.pw_hash):
            return u


def users_key(group = 'default'):
    return db.Key.from_path('users', group)