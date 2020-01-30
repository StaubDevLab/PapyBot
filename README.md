[![Badge langage](https://img.shields.io/static/v1?label=langage&message=Français&color=blue)](https://github.com/GuillaumeStaub/PapyBot/blob/master/README_fr.md)
[![Badge langage](https://img.shields.io/static/v1?label=langage&message=English&color=blue)](https://github.com/GuillaumeStaub/PapyBot/blob/master/README.md)

# PapyBot

##Why this program?
**PapyBot** is a *chatbot* that aims to tell the story of the place we want to visit?
It is therefore enough for the user to use the dialog window and to indicate a location to PapyBot, the latter will be responsible for sorting the information written by the user and will only remember the location. After a few seconds of reflection he will display this place on a map and tell the story from [**Wikipedia**](https://fr.wikipedia.org/wiki/Wikipédia:Accueil_principal).
So if you want to discover the secret of the region near you, **ask to PapyBot**.

## General operation
First you have to retrieve information about a place in the user's message. For this I use the regex which allow me to parse the message and extract only the address using certain keywords. Then PapyBot must search for the place, for that it uses the API of Google Maps and launches a request with the extracted place using the parser. Google maps returns GPS coordinates and a map that indicates the desired location. PapyBot then uses GPS data to make a request to the MediaWiki API and display a Wikipedia article linked to the location sought. PapyBot thus displays the beginning of the article and offers a link to the entire article to the user. When the user refreshes the page PapyBot resumes its script from zero.