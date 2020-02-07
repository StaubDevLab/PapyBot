from app.papybot import PapyBot
import pytest


@pytest.fixture(autouse=True)
def initialize_papybot_class():
    papybot = PapyBot()
    return papybot


wikipedia_client_answer = {"title": "Flèche de Notre-Dame de Paris",
                           "wiki_url": "https://fr.wikipedia.org/wiki/Fl%C3%A8che_de_Notre-Dame_de_Paris",
                           "extract": "La flèche de Notre-Dame de Paris est la flèche qui surmonte la croisée du "
                                      "transept de la cathédrale Notre-Dame de Paris."}

google_client_answer = {"coordinates": {"lat": 48.85296820000001, "lng": 2.3499021},
                        "full_address": "6 Parvis Notre-Dame - Pl. Jean-Paul II, 75004 Paris, France",
                        "types_place": ["church"]}


def test_papy_bot_main_return_good_format(monkeypatch, initialize_papybot_class):
    result_good_format = {"papybot_answer": wikipedia_client_answer,
                          "position": google_client_answer,
                          "research": "notre dame de paris",
                          "error": None}

    def mock_google_client(*args, **kwargs):
        return google_client_answer

    def mock_wikipedia_client(*args, **kwargs):
        return wikipedia_client_answer

    monkeypatch.setattr("app.google_client.GoogleClient.get_location", mock_google_client)
    monkeypatch.setattr("app.wikipedia_client.WikiClient.search_page", mock_wikipedia_client)

    assert initialize_papybot_class.main("Je veux aller à Notre Dame de Paris") == result_good_format


def test_papy_bot_main_return_an_random_error(monkeypatch, initialize_papybot_class):
    result_error_format = {"papybot_answer": wikipedia_client_answer,
                           "position": {"coordinates": "",
                                        "full_address": "",
                                        "types_place": "",
                                        "error": "GoogleMaps API : No Result Found"},
                           "research": "notre dame de paris",
                           "error": None}

    def mock_google_client(*args, **kwargs):
        return {"coordinates": "",
                "full_address": "",
                "types_place": "",
                "error": "GoogleMaps API : No Result Found"}

    def mock_wikipedia_client(*args, **kwargs):
        return wikipedia_client_answer

    monkeypatch.setattr("app.google_client.GoogleClient.get_location", mock_google_client)
    monkeypatch.setattr("app.wikipedia_client.WikiClient.search_page", mock_wikipedia_client)

    assert initialize_papybot_class.main("Je veux aller à Notre Dame de Paris") == result_error_format
