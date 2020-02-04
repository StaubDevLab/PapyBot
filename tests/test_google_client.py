from app.google_client import GoogleClient as gclient
import pytest
import requests



@pytest.fixture(autouse=True)
def initialize_google_client_class():
    google = gclient("paris")
    return google


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


results = {"ZERO_RESULTS": {"results": [], "status": "ZERO_RESULTS"},
           "REQUEST_DENIED": {"results": [], "status": "REQUEST_DENIED"},
           "RESULT_NOT_EMPTY": {"results": [{"geometry": {"location": {"lat": 48.856614, "lng": 2.3522219}}
                                             }]}}


def test_get_location_return_correct_format(monkeypatch, initialize_google_client_class):
    correct_result = {"lat": 48.856614, "lng": 2.3522219}

    def mock_response_not_empty(*args, **kwargs):
        return MockRequestsGet(result=results["RESULT_NOT_EMPTY"])

    monkeypatch.setattr("requests.get", mock_response_not_empty)

    assert initialize_google_client_class.get_location() == correct_result


def test_get_location_when_api_return_nothing(monkeypatch, initialize_google_client_class):
    result_nothing = []

    def mock_response_empty(*args, **kwargs):
        return MockRequestsGet(result=results["ZERO_RESULTS"])

    monkeypatch.setattr("requests.get", mock_response_empty)

    assert initialize_google_client_class.get_location() == result_nothing


def test_get_location_when_api_return_access_denied(monkeypatch, tmpdir, initialize_google_client_class, capsys):
    result_access_denied = []

    def mock_response_access_denied(*args, **kwargs):
        return MockRequestsGet(result=results["REQUEST_DENIED"])

    def mock_logging_error(*args, **kwargs):
        print("Google Maps API KEY has expired or is incorrect", end='')

    monkeypatch.setattr("requests.get", mock_response_access_denied)
    monkeypatch.setattr("logging.error", mock_logging_error)

    assert initialize_google_client_class.get_location() == result_access_denied
    captured = capsys.readouterr()
    assert captured.out == "Google Maps API KEY has expired or is incorrect"


def test_get_location_when_requests_return_bad_status_code(tmpdir, monkeypatch, initialize_google_client_class, capsys):
    result_error_server = []

    def mock_response_error_server(*args, **kwargs):
        return MockRequestsGet(result=[], st_code=400)

    def mock_logging_critical(*args, **kwargs):
        print("CRITICAL :: There is a problem with the server HTTP - Code HTTP : 400", end='')

    monkeypatch.setattr("requests.get", mock_response_error_server)
    monkeypatch.setattr("logging.critical", mock_logging_critical)

    assert initialize_google_client_class.get_location() == result_error_server

    captured = capsys.readouterr()
    assert captured.out == "CRITICAL :: There is a problem with the server HTTP - Code HTTP : 400"


def test_get_location_requests_result_key_error(monkeypatch, initialize_google_client_class):
    result_key_error = []

    def mock_response_error_result(*args, **kwargs):
        return MockRequestsGet(result={"bad_key": ""})

    monkeypatch.setattr("requests.get", mock_response_error_result)

    assert initialize_google_client_class.get_location() == result_key_error
