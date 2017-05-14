# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:40:31 2017

@author: quessada
"""

from tasktimer import call_repeatedly
from urllib.request import urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
import json

liste = [
    "http://www.freepatentsonline.com/8908487.html",
    "http://www.freepatentsonline.com/CCL-359-1.html",
    "http://www.freepatentsonline.com/crazy.html",
    "http://www.freepatentsonline.com/ACC-706.html",
    "http://www.freepatentsonline.com/ACC-720.html",
    "http://www.freepatentsonline.com/ACC-704.html"
]

path = "/home/audrey/Audrey/Cours/INF344/TP/TP_crawler/"
#path1 = "/cal/homes/quessada/TP02/"
filename = path+"result_etape7.json"
base_url = "http://www.freepatentsonline.com"
print("longueur liste: ", len(liste))

#fonction qui vérifie le lien:
def check_url(link):
    if base_url in link:
        return link
    elif '/' in link:
        return base_url+link
    else:
        return base_url+'/'+link


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
    #pour l'étape 6, on utilise une regex pour ne garder que les liens intéressants
    #pour trouver les pages de brevets de type /7847238.html
    pattern1 = re.compile("^(?:\D*\d){7}\.html$")
    #pour trouver les pages de descriptions de brevets de type /CCL-359-1-p2.html
    pattern2 = re.compile("^\/[A-Z]{3}\-(?:\d{3})*")
    content = getURL(link)
    try:
        soup = BeautifulSoup(content, 'html.parser')
        tags = soup('a')  
        table_url = [tag.get('href') for tag in tags if tag.get('href') is not None]
        interesting_url = []
        patent = []
        for url in table_url:
            if pattern1.match(url):
                patent.append(url)
            if pattern2.match(url) or base_url in url:
                interesting_url.append(url)
        return tags, interesting_url, patent
    except KeyError:
        return None, None


#fonction qui permet de traiter la liste initiale d'URL et de l'imprimer dans un fichier
def urlcall(toBeProcessed, N):
    if toBeProcessed["elements"]:
        call = toBeProcessed["elements"].pop(0)
        call = check_url(call)
        print("page visitée: ", call)
        dico_json = {}
        list_fields = ['Title:', 'Inventors:', 'Publication Date:', 'Assignee:', 'Primary Examiner:']
        content = getURL(call)
        soup = BeautifulSoup(content, 'html.parser')
        for div in soup.find_all('div', class_='disp_doc2'):
            list_title = div.find_all('div', class_='disp_elm_title')
            #print(list_title)
            list_description = div.find_all('div', class_='disp_elm_text')
            #print(list_description)
            for t,d in zip(list_title, list_description ):
                t = t.text
                t = t.strip().replace('\n', '')
                t = ' '.join(t.split())
                if t in list_fields:
                    description = d.text
                    description = description.strip().replace('\n', '')
                    description = ' '.join(description.split())
                    #print(description)
                    dico_json[t] = description
        #print(dico_json )
        #print("---------------")
        tags, table_url, patent = parseTagContent(call) #parsing des tags pour récupérer les liens
        #on ne récupère que les pages de brevets
        url_unique = [u for u in set(patent) if u not in toBeProcessed["elements"]]
        toBeProcessed["elements"].extend(url_unique) #stockage des liens
        n_url = len(table_url)
        n_url_unique = len(url_unique)
        toBeProcessed["nb_visite"] += n_url_unique
        print("Nombre de liens par page: ", n_url)
        print(" ")
        print("taille set d'URL pointant vers des brevets: ", n_url_unique)
        print(" ")
        print("nb de pages à visiter: ", toBeProcessed["nb_visite"])
        print("****************")
        with open(filename, 'a', encoding='utf8') as f:
            if dico_json:
                print("la description est écrite dans le fichier")
                dico_json['url'] = call
                json.dump(dico_json, f, indent=4)
            if toBeProcessed["nb_visite"] > N:
                print("nb de liens restants: ", toBeProcessed["nb_visite"]-N)
                f.close()
                return True
            return False
    else:
        return True




# mise en route d'un appel toutes les 5s de la fonction urlcall avec un dictionnaire
# qui contient les paramètres passés à chaque appel de la fonction
if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    call_repeatedly(5, urlcall, { "elements": liste, "nb_visite": 0 }, 350)