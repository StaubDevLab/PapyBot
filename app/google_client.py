import requests
import os
import logging
import config.config


class GoogleClient:

    def __init__(self, question):
        self._payload = {"address": question, "key": os.getenv("GMAPS_API_KEY")}
        self._url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.result = {}

    def _clean(self):
        try:
            self.result = self.result["results"][0]["geometry"]["location"]
        except KeyError:
            self.result = {}
            pass
        return self.result

    def get_location(self):
        try:
            result_request = requests.get(self._url, params=self._payload)
            self.result = result_request.json()
            if self.result["results"]:
                self._clean()
            elif self.result["status"] == "REQUEST_DENIED":
                logging.error("Google Maps API KEY has expired or is incorrect")
                raise AssertionError
            else:
                self.result = {}
        except requests.exceptions.HTTPError:
            logging.critical(
                f"There is a problem with the server HTTP - Code HTTP : %s", result_request.status_code())
        except requests.exceptions.RequestException:
            pass
        except (AssertionError, KeyError):
            self.result = {}
            pass
        return self.result
