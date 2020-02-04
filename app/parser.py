import unidecode
import re


class Parser:

    def __init__(self, question: str):
        self.question = question

    def _regex(self):
        regex = re.compile(r"(l'adresse de|ou se situe|aller (\w)*|partir (\w)*|ou est)\s+(?P<lieu>[^.?!,]*)")
        result = regex.search(self.question)
        self.question = result.group("lieu")
        return self.question

    def clean(self):
        self.question = self.question.lower()
        self.question = unidecode.unidecode(self.question)
        self._regex()
        return self.question


if __name__ == "__main__":
    pass
