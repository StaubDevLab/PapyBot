from app.wikipedia_client import WikiClient as wikiclient
import pytest
import requests


@pytest.fixture(autouse=True)
def initialize_wikipedia_client_class():
    wikipedia = wikiclient({"lat": 48.856614, "lng": 2.3522219})
    return wikipedia


class MockRequestsGet:
    def __init__(self, url=None, params=None, result=None, st_code=200):
        self.result = result
        self.st_code = st_code

    def status_code(self):
        return self.st_code

    def json(self):
        if self.st_code != 200:
            raise requests.exceptions.HTTPError
        return self.result


results = {
    "ZERO_RESULTS": {
        "batchcomplete": "",
        "query": {
            "geosearch": []
        }
    },
    "NORMAL_RESULT_SEARCH_PAGE": {
        "batchcomplete": "",
        "query": {
            "pages": {
                "12495993": {
                    "pageid": 12495993,
                    "title": "Incendie de Notre-Dame de Paris",
                    "fullurl": "https://fr.wikipedia.org/wiki/Incendie_de_Notre-Dame_de_Paris",
                    "extract": "L’incendie de Notre-Dame de Paris est un incendie majeur survenu à la "
                               "cathédrale "
                               "Notre-Dame de Paris, les 15 et 16 avril 2019, pendant près de 15 heures."
                }
            }
        }
    },
    "KEY_EEROR_RESULT": {"query": {"page": {"1234": {}}}}
}


def test_wiki_client_geosearch_return_nothing(monkeypatch, initialize_wikipedia_client_class):
    result_nothing = {}

    def mock_response_empty(*args, **kwargs):
        return MockRequestsGet(result={})

    def mock_geosearch_response_noothing(*args, **kwargs):
        return result_nothing

    monkeypatch.setattr("requests.get", mock_response_empty)

    monkeypatch.setattr("app.wikipedia_client.WikiClient._geosearch", mock_geosearch_response_noothing)

    assert initialize_wikipedia_client_class.search_page() == result_nothing


def test_wiki_client_geosearch_return_pageids(monkeypatch, initialize_wikipedia_client_class):
    normal_result_geosearch = 12495993
    normal_result = {"title": "Incendie de Notre-Dame de Paris",
                     "wiki_url": "https://fr.wikipedia.org/wiki/Incendie_de_Notre-Dame_de_Paris",
                     "extract": "L’incendie de Notre-Dame de Paris est un incendie majeur survenu "
                                "à la cathédrale Notre-Dame de Paris, les 15 et 16 avril 2019, pendant près de "
                                "15 heures."}

    def mock_normal_response(*args, **kwargs):
        return MockRequestsGet(result=results["NORMAL_RESULT_SEARCH_PAGE"])

    def mock_geosearch_normal_response(*args, **kwargs):
        return normal_result_geosearch

    monkeypatch.setattr("requests.get", mock_normal_response)

    monkeypatch.setattr("app.wikipedia_client.WikiClient._geosearch", mock_geosearch_normal_response)

    assert initialize_wikipedia_client_class.search_page() == normal_result


def test_wiki_client_searchpage_requests_exception(monkeypatch, initialize_wikipedia_client_class, capsys):
    result_error_server = {}

    def mock_response_error_server(*args, **kwargs):
        return MockRequestsGet(result={}, st_code=400)

    def mock_logging_critical(*args, **kwargs):
        print("CRITICAL :: There is a problem with the server HTTP - Code HTTP : 400", end='')

    def mock_geosearch(*args, **kwargs):
        return result_error_server

    monkeypatch.setattr("requests.get", mock_response_error_server)
    monkeypatch.setattr("app.wikipedia_client.WikiClient._geosearch", mock_geosearch)
    monkeypatch.setattr("logging.critical", mock_logging_critical)

    assert initialize_wikipedia_client_class.search_page() == result_error_server

    captured = capsys.readouterr()
    assert captured.out == "CRITICAL :: There is a problem with the server HTTP - Code HTTP : 400"


def test_wiki_client_searchpage_return_keyerror(monkeypatch, initialize_wikipedia_client_class, capsys):
    result_key_error = {}

    def mock_response_error_server(*args, **kwargs):
        return MockRequestsGet(result=results["KEY_EEROR_RESULT"], st_code=200)

    def mock_logging_error(*args, **kwargs):
        print("ERROR :: There is a problem with MediaWiki searchpage answer", end='')

    def mock_geosearch(*args, **kwargs):
        return 123456

    monkeypatch.setattr("requests.get", mock_response_error_server)
    monkeypatch.setattr("app.wikipedia_client.WikiClient._geosearch", mock_geosearch)
    monkeypatch.setattr("logging.error", mock_logging_error)

    assert initialize_wikipedia_client_class.search_page() == result_key_error

    captured = capsys.readouterr()
    assert captured.out == "ERROR :: There is a problem with MediaWiki searchpage answer"