# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:40:31 2017

@author: quessada
"""

from tasktimer import call_repeatedly
from urllib.request import urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup

liste = [
    "http://www.freepatentsonline.com/CCL-359-1.html",
    "http://www.freepatentsonline.com/crazy.html",
    "http://www.freepatentsonline.com/ACC-706.html",
    "http://www.freepatentsonline.com/ACC-720.html",
    "http://www.freepatentsonline.com/ACC-704.html"
]


path = "/home/audrey/Audrey/Cours/INF344/TP/TP_crawler/"
#path1 = "/cal/homes/quessada/TP02/"
filename2 = path+"result_etape04.txt"
base_url = "http://www.freepatentsonline.com"
print("longueur liste: ", len(liste))

#fonction pour récupérer le contenu brut d'une page web
def getURL(link):
    params = urlencode({
    'format': 'json',  # format
    'action': 'parse',  
    'prop': 'text',  
    'redirects':'True', 
    'page': link})
    try:
        response = urlopen(link+ "?" + params)
        content = response.read().decode('utf-8')
        return content
    except KeyError:
        return None

#fonction pour récupérer les liens contenus dans les pages visitées
def parseTagContent(link):
    content = getURL(link)
    try:
        soup = BeautifulSoup(content, 'html.parser')
        tags = soup('a')
        table_url = [tag.get('href') for tag in tags if tag.get('href') is not None]
        return tags, table_url
    except KeyError:
        return None, None

#fonction qui vérifie le lien:
def check_url(link):
    if base_url in link:
        return link
    else:
        return base_url+link

#fonction qui permet de traiter la liste initiale d'URL et de l'imprimer dans un fichier
def urlcall(toBeProcessed, N):
    if toBeProcessed["elements"]:
        call = toBeProcessed["elements"].pop(0)
        call = check_url(call)
        print("page visitée: ", call)
        tags, table_url = parseTagContent(call) #parsing des tags pour récupérer les liens
        #on ne garde que les urls uniques pour éviter de charger plusieurs fois la même page
        url_unique = [u for u in set(table_url) if u not in toBeProcessed["elements"]]
        toBeProcessed["elements"].extend(url_unique) #stockage des liens
        #on compte le nombre de liens par page à visiter
        n_url = len(table_url)
        n_url_unique = len(url_unique)
        #on compte le nombre de pages visitées
        toBeProcessed["nb_visite"] += n_url_unique
        print("Nombre de liens par page: ", n_url)
        print(" ")
        print("taille set d'URL pas encore dans le dictionaire: ", n_url_unique)
        print(" ")
        print("nb de pages à visiter: ", toBeProcessed["nb_visite"])
        print("****************")
        #on enregistre les résultats dans un fichier
        with open(filename2, 'a') as f2:
            print(toBeProcessed["elements"], file=f2)
            if toBeProcessed["nb_visite"] > N:
                print("nb de liens restants: ", toBeProcessed["nb_visite"]-N)
                f2.close()
                return True
            return False
    else:
        return True




# mise en route d'un appel toutes les 5s de la fonction urlcall avec un dictionnaire
# qui contient les paramètres passés à chaque appel de la fonction
if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    call_repeatedly(5, urlcall, { "elements": liste, "nb_visite": 0 }, 300)