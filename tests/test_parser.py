from app.parser import Parser
import pytest

sentence_to_parse = ["Pourrais-tu me dire où se situe la Tour Eiffel",
                     "Bonjour je voudrais connaître l'adresse de la Tour Eiffel",
                     "Je veux aller à la Tour Eiffel",
                     "Salut, comments-tu vas? J'aimerais vraiment partir à la Tour Eiffel"]


@pytest.fixture(params=sentence_to_parse)
def initialize_parser_class(request):
    pars = Parser()
    yield pars.clean(request.param)


def test_clean_del_accent(initialize_parser_class):
    result = initialize_parser_class
    for letter in "àâäéèêëïîôöùûüÿç":
        assert letter not in result


def test_clean_just_lower_carc(initialize_parser_class):
    result = initialize_parser_class
    assert result == result.lower()


def test_clean_just_place(initialize_parser_class):
    result = initialize_parser_class
    assert result == "la tour eiffel"
