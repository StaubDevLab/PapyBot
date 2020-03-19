import requests
import os
import logging


class GoogleClient:
    """
        GoogleClient class takes the address or place previously retrieved by the Parser class
        and makes a request via the Google Maps API to obtain GPS coordinates and
        information on this place.

        Returns :
            dict : Dictionary containing all the information extracted from Google Maps API and/or an error message.
        """

    def __init__(self, question: str):
        """
        Initializes 3 parameters, the parameters which will be used for the request towards the API of Google Maps
        it is here that this finds the information extracted from the user input. The request url.
        And the preformatted dictionary which will be used as the basis of return.
        Args:
            question: string sends by Parser
        """
        self._payload = {"address": question, "key": os.getenv("GMAPS_API_KEY")}
        self._url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.result = {"coordinates": "",
                       "full_address": "",
                       "types_place": "",
                       "error": ""}

    def _clean(self, dict_to_clean):
        """This private method allows you to retrieve useful information from the dictionary
        returned by the Google Maps API. This method will be used in a try block which will
        catch any KeyError if the API does not find information on the location.

        Args:
            dict_to_clean (dict): Dictionary returned by Google Maps API

        Returns:
            dict : Dictionary that contains only useful information or an empty preformatted dictionary.

        """
        for ind, value in enumerate(dict_to_clean["results"][0]["address_components"]):
            if "locality" in value["types"]:
                town = value["long_name"]
            elif "administrative_area_level_1" in value["types"]:
                department = value["long_name"]

        self.result = {"coordinates": dict_to_clean["results"][0]["geometry"]["location"],
                       "full_address": dict_to_clean["results"][0]["formatted_address"],
                       "types_place": dict_to_clean["results"][0]["types"],
                       "town": town,
                       "error": ""}

    def get_location(self):
        """This method makes a request to the Google Maps API with the parameters defined in the class's __init__ method.
        The method uses the _clean private method with the dictionary sent by Google Maps as a parameter
        to retrieve useful information. In this method all possible errors are captured and indicated
        in an error message in the returned dict.

        Returns:
            dict : Dictionary containing either useful information or a preformatted dictionary
                   with an error message if an error has been encountered
                """
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
        finally:
            return self.result


if __name__ == "__main__":
    pass
