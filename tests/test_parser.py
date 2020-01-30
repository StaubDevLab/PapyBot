from app.parser import Parser
import pytest


@pytest.fixture
def initialize_parser_class():
    pars = Parser("Pourrais tu me où se situe la Tour Eiffel")
    return pars


def test_clean_del_accent(initialize_parser_class):
    result = initialize_parser_class.clean()
    for letter in "àâäéèêëïîôöùûüÿç":
        assert letter not in result


def test_clean_just_lower_carc(initialize_parser_class):
    result = initialize_parser_class.clean()
    assert result == result.lower()


def test_clean_just_place(initialize_parser_class):
    result = initialize_parser_class.clean()
    assert result == "la tour eiffel"
