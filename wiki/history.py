from models.history import History
from templateHandler import TemplateHandler


class HistoryPageHandler(TemplateHandler):
    def get(self, wiki_title):
        histories = History.by_title(wiki_title)

        self.render('history.html', title = wiki_title, histories= histories)
