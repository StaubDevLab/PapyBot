import requests
import logging


class WikiClient:

    def __init__(self, coordinates: dict):
        self.coordinates = coordinates
        self._url = "https://fr.wikipedia.org/w/api.php"
        self._payload_geosearch = {
            "action": "query",
            "list": "geosearch",
            "gscoord": f"{self.coordinates['lat']}|{self.coordinates['lng']}",
            "format": "json",
            "gradius": 3000}
        self._pageids = None
        self._payload_search_page = {
            "action": "query",
            "prop": "info|extracts",
            "pageids": self._pageids,
            "inprop": "url",
            "exchars": 300,
            "format": "json"
        }
        self.result = {}

    def _clean_geosearch(self):
        try:
            self.result = self.result["query"]["geosearch"][0]["pageid"]
        except KeyError:
            logging.error("There is a problem with MediaWiki geosearch answer")
            self.result = {}
        return self.result

    def _clean_searchpage(self):
        try:
            self.result = {"title": self.result["query"]["pages"][str(self._pageids)]["title"],
                           "wiki_url": self.result["query"]["pages"][str(self._pageids)]["fullurl"],
                           "extract": self.result["query"]["pages"][str(self._pageids)]["extract"]}
        except KeyError:
            logging.error("There is a problem with MediaWiki searchpage answer")
            self.result = {}
        return self.result

    def _geosearch(self):
        try:
            result_requests = requests.get(self._url, params=self._payload_geosearch)
            self.result = result_requests.json()
            if self.result["query"]["geosearch"]:
                self._clean_geosearch()
            elif self.result['error']:
                logging.error("Bad usage api, error : %s", self.result["error"]["code"])
                raise AssertionError
            else:
                self.result = {}
        except requests.exceptions.HTTPError:
            logging.critical(
                f"There is a problem with the server HTTP - Code HTTP : %s", result_requests.status_code())
        except requests.exceptions.RequestException:
            pass
        except (AssertionError, KeyError):
            self.result = {}
        finally:
            return self.result

    def search_page(self):
        self._pageids = self._geosearch()
        try:
            result_requests = requests.get(self._url, params=self._payload_search_page)
            self.result = result_requests.json()
            if self.result["query"]:
                self._clean_searchpage()
            else:
                raise KeyError
        except requests.exceptions.HTTPError:
            logging.critical(
                f"There is a problem with the server HTTP - Code HTTP : %s", result_requests.status_code())
        except requests.exceptions.RequestException:
            pass
        except (AssertionError, KeyError):
            self.result = {}
        finally:
            return self.result