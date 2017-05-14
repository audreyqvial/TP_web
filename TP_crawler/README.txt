Audrey Quessada
INF344

TP02 CRAWLING:

-----------------------------------------------------------------------------------------
PARTIE 1: Crawls élémentaires avec wget:

Q1: 

wget http://www.freepatentsonline.com/8937756.html
On récupère la page en html mais sans la mise en forme


Q2: 
wget -r --wait=1 http://www.freepatentsonline.com/CCL-359-1.html
On télécharge un dossier intitulé www.freepatentsonline.com, qui contient un sous dossier css et images et des fichiers html

Q3: 
wget -np -r --wait=1 http://www.freepatentsonline.com/
On a essayé également avec l'URL précédente

Pour la première URL, on récupère des pages HTML correspondant à design-patents.html (pas de description), l'index, patent-apps.html, register.html, search.html, tools-resources.html, uspatents.html

Q05:
 wget -np --reject-regex 'search.*|index.*|register.*|tools\-resources.*' -r --wait=1 http://www.freepatentsonline.com/
En fait ça marche sauf pour index

--------------------------------------------------------------------------------------------

PARTIE2: Crawl systématique par programme Python

Pour la suite du TP, je vais utiliser la librairie Beautifulsoup

Etape 1: 
J'utilise la librairie urrlib.request pour récupérer le contenu d'une URL. Celui-ci est sauvegardé dans un fichier text grâce à une modification de la fonction urlcall. La fonction getURL avait déjà été implémentée dans un TP précédent.

Etape 2 : 
On reprends l'étape 1 et on rajoute une liste de liens. On enregistre le contenu de ces liens dans un fichier text.

Etape 3 : 
On rajoute une fonction parseTagContent(link) qui permet de récupérer tous les liens du contenu d'une page web. Cette fonction permet de retourner les tags "a" et la liste des liens s'ils existent.
J'ai modifié la fonction urlcall pour rajouter une condition d'arrêt. Chaque lien trouvé dans la page visitée est rajouté au dictionaire toBeProcessed["elements"]. Si la taille de celui-ci est plus grand qu'un nombre N fixé par l'utilisateur, le programme s'arrête et retourne le nombre de pages restant à visiter. On a également rajouté un champ au dictionaire toBeProcessed["nb_visite"] qui compte le nombre de liens par page. On imprime dans un fichier txt la liste de tous les liens récupérés.

Etape 4 : 
On va modifier la fonction urlcall pour ne garder qu'une liste de liens sans doublons: c'est la liste url_unique. Le dictionnaire s'agrandit cette fois avec cette liste et non plus la liste de tous les liens. On rajoute également une fonction check_url(link) qui permet d'avoir un lien valide.

Etape 5:
On remarque qu'un certains nombres de liens ne sont pas intéressants et ne pointent pas vers des brevets. On va donc modifier la fonction parseTagContent pour les éviter à partir d'une listes de liens déterminés empiriquement. Les liens de cette liste ne seront pas récupérés en revanche tous les autes supposés pointer vers des brevets le seront. Pour donner quelques exemples ce sont des liens comme "http://research.freepatentsonline.com/help".

Etape 6 : 
Au lieu de créer à la main une liste de liens indésirables, on va utiliser des regex pour ne garder que les liens qui nous intéressent. Encore une fois nous allons modifier la fonction parseTagContent(link) pour rajouter ces regex.

Etape 7 :
On va récupérer cette fois d'autres informations comme le titre, les inventeurs, la date de publication du brevet, l'assigné et l'examinateur principal. Cette modification sera implémentée dans la fonction urlcall. 
On a amélioré la fonction check_url pour n'avoir que des liens récupérés valides.
On a légèrement modifié la fonction parseTagContent pour ne récupérer que les liens qui pointent vers des brevets et non plus des liens qui pointent vers des pages avec une liste de résumés de brevets. Ces liens qui pointent vers des brevets sont stockés dans la liste patent.
Pour la fonction urlcall, on crée un dictionaire qui va stocker le contenu des champs qui nous intéressent. Ce dictionaire sera enregistré dans un fichier json.








