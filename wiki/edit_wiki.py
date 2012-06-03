import cgi
from loginout.cookies import CookieManager
from models.history import History
from models.user import User
from models.wiki_page import Wiki
from templateHandler import TemplateHandler

class EditPageHandler(TemplateHandler):
    def get(self, wiki_title):
        uid = CookieManager.read_secure_cookie('user_id', self.request)
        self.user = uid and User.by_id(int(uid))
        if self.user:
            wiki = Wiki.by_title(wiki_title)
            if not wiki:
                self.render('edit_wiki.html', title= wiki_title)
            else:
                self.render('edit_wiki.html', title= wiki_title, content= wiki.content)
        else:
            self.redirect('/'+wiki_title)

    def post(self, wiki_title):
        wiki_content = self.request.get("content")

        wiki = Wiki.by_title(wiki_title)
        if not wiki:
            newWiki = Wiki(title= wiki_title, content = wiki_content)
            newWiki.put()
        else:
            wiki.content = wiki_content
            wiki.put()

        newHistory = History(title = wiki_title, content = cgi.escape(wiki_content))
        newHistory.put()

        self.redirect('/'+wiki_title)