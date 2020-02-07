from app.google_client import GoogleClient
from app.wikipedia_client import WikiClient
from app.parser import Parser


class PapyBot:

    def __init__(self):
        self.question = None
        self.parser = None
        self.google_answer = None
        self.wiki_answer = None
        self.papy_answer = None
        self.error = None

    def _format_return_datas(self):
        return {"papybot_answer": self.wiki_answer,
                "position": self.google_answer,
                "research": self.parser,
                "error": self.error}

    def main(self, question):
        initialize_parser = Parser()
        self.parser = initialize_parser.clean(question)

        initialize_google_client = GoogleClient(self.parser)
        self.google_answer = initialize_google_client.get_location()

        initialize_wiki_client = WikiClient()
        self.wiki_answer = initialize_wiki_client.search_page(self.google_answer)

        self.papy_answer = self._format_return_datas()
        return self.papy_answer


if __name__ == "__main__":
    pass
