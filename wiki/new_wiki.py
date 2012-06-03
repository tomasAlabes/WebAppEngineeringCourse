import time
from google.appengine.api import memcache
from loginout.cookies import CookieManager
from models.user import User
from models.wiki_page import Wiki
from templateHandler import TemplateHandler

# use memcache to store the wikis the user visited


class WikiPageHandler(TemplateHandler):
    def get(self, wiki_title):
        wiki = Wiki.by_title(wiki_title)

        uid = CookieManager.read_secure_cookie('user_id', self.request)
        self.user = uid and User.by_id(int(uid))
        if self.user:
            if not wiki:
                self.redirect('/_edit/' + wiki_title)
            else:
                self.render("wiki.html", title = wiki_title, content= wiki.content) #, secondsAgo = secondsAgo)
        else:
            self.render("wiki.html", title = wiki_title)
        #now = int(time.time())
        #wikiTimeKey = "time" + wiki_title
        #wikiTimeCached = memcache.get(wikiTimeKey)
        #if not wikiTimeCached:
        #    memcache.set(wikiTimeKey, now)

        #secondsAgo = now - int(memcache.get(wikiTimeKey))