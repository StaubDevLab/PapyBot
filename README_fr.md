[![Badge langage](https://img.shields.io/static/v1?label=langage&message=Français&color=blue)](https://github.com/GuillaumeStaub/PapyBot/blob/master/README_fr.md)
[![Badge langage](https://img.shields.io/static/v1?label=langage&message=English&color=blue)](https://github.com/GuillaumeStaub/PapyBot/blob/master/README.md)

# PapyBot

##Pourquoi ce programme?
**PapyBot** est un *chatbot* qui a pour but de raconter l'histoire du lieu que nous souhaitons visiter? 
Il suffit donc à l'utilisateur d'utiliser la fenêtre de dialogue et d'indiquer un lieu à PapyBot, ce dernier se chargera de trier les informations écrites par l'utilisateur et n'en retiendra que le lieu. Après quelques secondes de réflexion il affichera ce lieu sur une carte et en racontera l'histoire tiré de [**Wikipedia**](https://fr.wikipedia.org/wiki/Wikipédia:Accueil_principal).
Si vous voulez donc percer le secret des parages proche de chez vous, **demandez donc à PapyBot**.

## Fonctionnement général
Tout d'abord, il faut récupérer les **informations sur un lieu** dans le message de l'utilisateur. Pour cela j'utilise les **regex** qui me permettent de parser le message et d'en **extraire uniquement l'adresse** à l'aide de certains mots-clés. 
Ensuite, PapyBot doit rechercher le lieu, pour cela, il utilise [l'API de Google Maps](https://developers.google.com/places/web-service/details?hl=Language) et lance une requête avec le lieu extrait à l'aide du parser. Google maps retourne des **coordonnées GPS** et une carte qui indique le lieu souhaité.
PapyBot utilise ensuite les coodonnées GPS pour réaliser une requête vers [l'API MediaWiki](https://www.mediawiki.org/w/api.php) et affiche un **article Wikipedia** lié au lieu recherché. 
PapyBot affiche ainsi le début de l'article et propose un lien vers l'article entier à l'utilisateur. 
Lorsque l'utilisateur réactualise la page PapyBot reprend son script à zéro. 