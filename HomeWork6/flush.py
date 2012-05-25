from google.appengine.api import memcache
from templateHandler import TemplateHandler

__author__ = 'Tomi'

class FlushCacheHandler(TemplateHandler):
    def get(self):
        memcache.flush_all()
        self.redirect("/blog")

