import unidecode
import re


class Parser:
    """
    Parser class allows to recover the text entered by the user,
    to use built-in methods to clean up accents and capital letters
    and with regex to recover useful information.

    Returns :
        str : question
    """

    def __init__(self):
        """
        Initialize a question attribute to none which will then take the value of user input
        """
        self.question = None

    def _regex(self):
        """Private method that simply creates a regular expression and searches for that expression in user input.
        The regex extracts information included in a group.

        Args:
            question (str) : contains input user

        Returns:
            str : important information from user input

        """
        regex = re.compile(r"(l'adresse de|ou se situe|aller (\w)*|partir (\w)*|ou est)\s+(?P<lieu>[^.?!,]*)")
        result = regex.search(self.question)
        self.question = result.group("lieu")
        return self.question

    def clean(self, question):
        """This method cleans up user input, it removes capital letters and accents
        then calls the _regx private method by sending it a cleaned str.

        Args:
            question (str) : contains input user

        Returns:
            str : Contains only the information that will be used to request the APIs
        """
        self.question = question.lower()
        self.question = unidecode.unidecode(self.question)
        self._regex()
        return self.question


if __name__ == "__main__":
    pass
