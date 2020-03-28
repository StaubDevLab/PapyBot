[![Badge langage](https://img.shields.io/static/v1?label=langage&message=Français&color=blue)](https://github.com/GuillaumeStaub/PapyBot/blob/master/README_fr.md)
[![Badge langage](https://img.shields.io/static/v1?label=langage&message=English&color=blue)](https://github.com/GuillaumeStaub/PapyBot/blob/master/README.md)

# PapyBot
**link to the application :** [papybot-py.com](http://papybot-py.herokuapp.com/)

## Why this program?
**PapyBot** is a *chatbot* that aims to tell the story of the place we want to visit?
It is therefore enough for the user to use the dialog window and to indicate a location to PapyBot, the latter will be responsible for sorting the information written by the user and will only remember the location. After a few seconds of reflection he will display this place on a map and tell the story from [**Wikipedia**](https://fr.wikipedia.org/wiki/Wikipédia:Accueil_principal).
So if you want to discover the secret of the region near you, **ask to PapyBot**.

## General operation
First you have to retrieve **information about a place** in the user's message. For this I use the **regex** which allow me to parse the message and **extract only the address** using certain keywords. Then PapyBot must search for the place, for that it uses the [API of Google Maps](https://developers.google.com/places/web-service/details?hl=Language) and launches a request with the extracted place using the parser. Google maps returns GPS coordinates and a map that indicates the desired location. PapyBot then uses **GPS data** to make a request to the [MediaWiki API](https://www.mediawiki.org/w/api.php) and display a **Wikipedia article** linked to the location sought. PapyBot thus displays the beginning of the article and offers a link to the entire article to the user. When the user refreshes the page PapyBot resumes its script from zero.
*General operation diagram:*
![general_operation](datas/general_operation.png)

## Visual
### User Storie Démo : 
![visual_data](datas/visual_gene.png)

## Dependencies
* Python 3.7.4
* Flask 1.1.1
* Gunicorn 20.0.4
* Requests 2.23.0
* Pytest 5.4.1
* Unidecode 1.1.1

## Skills mobilized
* Create a website with HTML5, format it with CSS3 and boost it with JavaScript
* Make a site responsive
* Develop following the Test Driven Development (TDD) methodology
* Use REST APIs with Python (GMaps, MediaWiki)
* Use a Python framework (Flask)
* Deploy a web application on Heroku

## How does it work? 
Explanation of the methods for each application package. First of all, two environment variables must be defined, in a .env file for example.Attention, I point out here that my code is ultra decomposed, I could have divided the number of lines by two, I deliberately wanted to decompose each step and not to carry out 10 operations on a single line. This code is for educational purposes.

```python
GMAPS_API_KEY = "" #Private API KEY for Geocode API les requêtes vers Geocode
GMAPS_API_KEY_PUBLIC = "" #Public API KEY  used on the front side to display the map
```
### Parser
Package which allows to analyze the text written by the user and to extract from it only useful information such as place, address, monument ...

```python
sentence = Parser()
sentence_parse = sentence.clean()
```
**The clean method** lowers the sentence, removes all accents and uses a private method `_regex ()` which uses regular expressions to extract the expected information.

### GoogleClient
Package which sends a request to the API *Geocode* of Google Maps from the elements extracted by the **Parser**. The API returns a json file containing in particular GPS coordinates and other information around the place sought.

```python
sentence_parse = GoogleClient(sentence)
coordinates = sentence_parse.get_location()
```

The `get_location ()` method uses requests to query the Geocode API and then analyzes the result. First, the method checks whether the expected data is present and then cleans it up with the private method `_clean ()`, catches any errors and returns the result in the form of a dictionary.

## WikiClient
This package uses the GPS coordinates returned by GoogleClient to search for an article near this location.

```python
wiki = WikiClient()
article = wiki.search_page(coordinates)
```
This package is apparently simple, but the mechanism behind it's complex. The `search_page ()` method uses the private methods `_geosearch ()` which searches for the id of an article from GPS coordinates, then after searching for the article from its id with *requests* it uses `_clean_searchpage ()` to clean up the result and keep only the essentials. Many errors are caught and managed. The method returns a dictionary containing the extract of the article, its title and the url to Wikipedia.

## PapyBot
PappyBot is the class that initializes all the others, it plays the role of a `main ()` function. It is very simple its main method initializes each class one after the other transmitting the information to each of them. It returns at the end a summary of the responses of each class.

```python
papy = PapyBot()
papy_answer = papy.main(sentence)
```

# Contribute to the program 

* Fork it
* Create your feature branch (`git checkout -b my-new-feature`)
* Commit your changes (`git commit -am 'Add some feature'`)
* Push to the branch (`git push origin my-new-feature`)
* Create new Pull Request