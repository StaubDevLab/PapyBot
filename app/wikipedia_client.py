import requests
import logging


class GPSCoordinatesError(Exception):
    pass


class WikiClient:

    def __init__(self):
        self.coordinates = None
        self._url = "https://fr.wikipedia.org/w/api.php"
        self._payload_geosearch = {
            "action": "query",
            "list": "geosearch",
            "gscoord": "",
            "format": "json",
            "gradius": 3000}
        self._pageids = None
        self._payload_search_page = {
            "action": "query",
            "prop": "info|extracts",
            "pageids": "",
            "inprop": "url",
            "exchars": 300,
            "explaintext":"",
            "format": "json"
        }
        self.result = {"title": "", "wiki_url": "", "extract": "", "error": ""}

    def is_valid(self, coords):
        try:
            dict_coords = f"{coords['coordinates']['lat']}|{coords['coordinates']['lng']}"
        except KeyError:
            self.result["error"] = "Wrong format of gps coordinates"
            raise GPSCoordinatesError
        return dict_coords

    def _clean_searchpage(self, dict_to_clean):
        self.result = {"title": dict_to_clean["query"]["pages"][str(self._pageids)]["title"],
                       "wiki_url": dict_to_clean["query"]["pages"][str(self._pageids)]["fullurl"],
                       "extract": dict_to_clean["query"]["pages"][str(self._pageids)]["extract"],
                       "error": ""}
        return self.result

    def _geosearch(self, coords):
        self._payload_geosearch['gscoord'] = self.is_valid(coords)
        result_requests = requests.get(self._url, params=self._payload_geosearch)
        result_json = result_requests.json()
        geo_coords = result_json["query"]["geosearch"][0]["pageid"]
        return geo_coords

    def search_page(self, coords):
        try:
            self._pageids = self._geosearch(coords)
            self._payload_search_page["pageids"]= self._pageids
            result_requests = requests.get(self._url, params=self._payload_search_page)
            result_json = result_requests.json()
            self.result = self._clean_searchpage(result_json)
        except requests.exceptions.HTTPError:
            logging.critical(
                f"There is a problem with the server HTTP - Code HTTP : %s", result_requests.status_code())
            self.result["error"] = "Problem Server"
        except (AssertionError, KeyError):
            logging.error("ERROR :: There is a problem with MediaWiki searchpage answer")
            self.result["error"] = "No result found in Wikipedia"
        except GPSCoordinatesError:
            self.result["error"] = "Wrong GPS coordinates format"
        finally:
            return self.result


if __name__ == "__main__":
    pass
