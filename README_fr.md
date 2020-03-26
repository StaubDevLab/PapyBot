[![Badge langage](https://img.shields.io/static/v1?label=langage&message=Français&color=blue)](https://github.com/GuillaumeStaub/PapyBot/blob/master/README_fr.md)
[![Badge langage](https://img.shields.io/static/v1?label=langage&message=English&color=blue)](https://github.com/GuillaumeStaub/PapyBot/blob/master/README.md)

# PapyBot
**Lien vers l'application :** [papybot-py.com](http://papybot-py.herokuapp.com/)

## Pourquoi ce programme?
**PapyBot** est un *chatbot* qui a pour but de raconter l'histoire du lieu que nous souhaitons visiter.
Il suffit donc à l'utilisateur d'utiliser la fenêtre de dialogue et d'indiquer un lieu à PapyBot, ce dernier se chargera
de trier les informations écrites par l'utilisateur et n'en retiendra que le lieu. Après quelques secondes de réflexion,
il affichera ce lieu sur une carte et en racontera l'histoire tiré de
[**Wikipedia**](https://fr.wikipedia.org/wiki/Wikipédia:Accueil_principal).
Si vous voulez donc percer le secret des lieux proche de chez vous, **demandez donc à PapyBot**.

## Fonctionnement général
Tout d'abord, il faut récupérer les **informations sur un lieu** dans le message de l'utilisateur. Pour cela j'utilise
les **regex** qui me permettent de parser le message et d'en **extraire uniquement l'adresse** à l'aide de certains mots-clés. 
Ensuite, PapyBot doit rechercher le lieu, pour cela, il utilise
[l'API de Google Maps](https://developers.google.com/places/web-service/details?hl=Language) et lance une requête avec le lieu extrait à l'aide du parser. Google maps retourne des **coordonnées GPS**. PapyBot utilise ensuite les coordonnées GPS pour réaliser une requête vers
[l'API MediaWiki](https://www.mediawiki.org/w/api.php) et affiche un **article Wikipedia** lié au lieu recherché. 
PapyBot affiche ainsi un extrait de l'article et propose un lien vers ce dernier à l'utilisateur. 
L'application utilise également les **coordonnées GPS** pour afficher **une carte** centrée sur le lieu recherché par l'utilisateur. 
Lorsque l'utilisateur réactualise la page PapyBot reprend son script à zéro. 
*Diagrramme du fonctionnement général:* 
![general_operation](datas/general_operation.png)
## Visuel
### Démonstration du parcours utilisateur : 
![visual_data](datas/visual_gene.png)

## Dépendances
* Python 3.7.4
* Flask 1.1.1
* Gunicorn 20.0.4
* Requests 2.23.0
* Pytest 5.4.1
* Unidecode 1.1.1

## Compétences mobilisées
* Créer un site web avec HTML5, le mettre en forme avec CSS3 et le dynamiser avec JavaScript
* Rendre un site responsive
* Développer en suivant la méthodologie Test Driven Development (TDD)
* Utiliser des API REST avec Python (GMaps, MediaWiki)
* Utiliser un framework Python (Flask)
* Déployer une application web sur Heroku

## Comment ça marche ?
Explications des méthodes de chaque package de l'application. Avant tout, il faut définir deux variables d'environnement, dans un fichier .env par exemple. **Attention, je fais remarquer ici que mon code est ultra décomposé, j'aurais pu diviser le nombre de lignes par deux, j'ai volontairement voulu décomposer chaque étape et non pas réaliser 10 opérations sur une seule ligne. Ce code est à visée pédagogique**

```python
GMAPS_API_KEY = "" #Clé d'API privé qui permettra les requêtes vers Geocode
GMAPS_API_KEY_PUBLIC = "" #Clé d'API publique qui est utilisée côté front pour l'affichage de la carte
```

### Parser
Package qui permet d'analyser le texte écrit par l'utilisateur et d'en extraire que l'information utile comme le lieu, l'adresse, le monument ...

```python
sentence = Parser()
sentence_parse = sentence.clean()
```
**La méthode clean** met la phrase en minuscule, retire tous les accents et utilise une méthode privée `_regex()` qui utilise les expressions régulières pour extraire l'information attendue. 

### GoogleClient
Package qui envoie une requête à l'API *Geocode* de Google Maps à partir des éléments extraits par le **Parser**. L'API renvoie un fichier json contenant notamment des coordonnées GPS et d'autres informations autour du lieu recherché.

```python
sentence_parse = GoogleClient(sentence)
coordinates = sentence_parse.get_location()
```
La méthode `get_location()` utilise requests pour interroger l'API Geocode puis procède à une anlayse du résultat. Tout d'abord, la méthode vérifie si les données attendues sont bien présentes puis les nettoie avec la méthode privée `_clean()`, intercepte les éventuelles erreurs et renvoie le résultat sous forme de dictionnaire. 

## WikiClient
Ce package utilise les coordonnées GPS renvoyées par GoogleClient pour rechercher un article proche de ce lieu. 

```python
wiki = WikiClient()
article = wiki.search_page(coordinates)
```

Ce package est en apparence simple, mais le mécanisme derrière est assez complexe. La méthode `search_page()` fait appel aux méthodes privées `_geosearch()` qui recherche l'id d'un article à parrtir des coordonnées GPS, puis après avoir recherché l'article à partir de son id avec *requests* elle utilise `_clean_searchpage()` pour nettoyer le résultat obtenu et ne garder que l'essentiel. De nombreuses erreurs sont interceptées et gérées. La méthode renvoie un dictionnaire contenant l'extrait de l'article, son titre et l'url vers Wikipedia.

## PapyBot
PappyBot est la classe qui initialise toutes les autres, elle joue un peu le rôle d'une fonction `main()`. Elle est très simple sa méthode main initialise chaque classe les unes après les autres transmettant les informations à chacune d'entre elles. Elle renvoie à la fin un condensé des réponses de chaque classe. 

```python
papy = PapyBot()
papy_answer = papy.main(sentence)
```

## Contribuer au programme
* Fork le
* Créez votre banche git checkout -b my-new-feature
* Commit les changements git commit -am 'Add some feature'
* Push ta branche git push origin my-new-feature
* Créez une Pull Request
