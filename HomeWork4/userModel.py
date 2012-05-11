__author__ = 'Tomi'

from google.appengine.ext import db

class User(db.Model):
    name = db.StringProperty(required= True)
    password_hash = db.StringProperty(required= True)
    email = db.EmailProperty(required= False)
    created = db.DateTimeProperty(auto_now_add = True)