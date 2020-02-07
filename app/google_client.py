import requests
import os
import logging
import config.config


class GoogleClient:

    def __init__(self, question: str):
        self._payload = {"address": question, "key": os.getenv("GMAPS_API_KEY")}
        self._url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.result = {"coordinates": "",
                       "full_address": "",
                       "types_place": "",
                       "error": ""}

    def _clean(self, dict_to_clean):
        self.result = {"coordinates": dict_to_clean["results"][0]["geometry"]["location"],
                       "full_address": dict_to_clean["results"][0]["formatted_address"],
                       "types_place": dict_to_clean["results"][0]["types"],
                       "error": ""}

    def get_location(self):
        try:
            result_request = requests.get(self._url, params=self._payload)
            result_json = result_request.json()
            if result_json["results"]:
                self._clean(result_json)
            elif result_json["status"] == "REQUEST_DENIED":
                logging.error("Google Maps API KEY has expired or is incorrect")
                raise AssertionError
            else:
                self.result["error"] = "GoogleMaps API : No Result Found"
        except requests.exceptions.HTTPError:
            logging.critical(
                f"There is a problem with the server HTTP - Code HTTP : %s", result_request.status_code())
            self.result['error'] = "GoogleMaps API : Problem Server"
        except requests.exceptions.RequestException:
            pass
        except (AssertionError, KeyError):
            self.result['error'] = "GoogleMaps API : No Result Found"
        return self.result


if __name__ == "__main__":
    pass
