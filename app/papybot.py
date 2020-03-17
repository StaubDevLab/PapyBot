from app.google_client import GoogleClient
from app.wikipedia_client import WikiClient
from app.parser import Parser
import random


class PapyBot:
    """ Main class of the program. PaPyBot allows you to link all the other
        classes together. It is therefore here that the processing and the
        return to the user takes place.
    """

    def __init__(self):
        """
        Initializes all the parameters which will store the returns of each
        class. These parameters make it possible to build the dictionary
        returned to AJAX.
        """
        self.question = None
        self.parser = None
        self.google_answer = None
        self.wiki_answer = None
        self.papy_answer = None
        self.error = None

    def _format_return_datas(self):
        """
        Method which makes it possible to build the dict of return to AJAX from the data collected via APIs
        Returns:
            dict : formatted data
        """
        return {"papybot_answer": self.wiki_answer,
                "position": self.google_answer,
                "research": self.parser,
                "error": self.error}

    def welcome_sentences(self):
        sentences = []
        return random.choice(sentences)

    def main(self, question):
        """
        Main method which instantiates the classes necessary for the operation
        of the program, stores the collected data in parameters and returns a
        formatted dictionary.

        Args:
            question(str): input user

        Returns:
            dict : Formatted response returned to AJAX
        """
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
