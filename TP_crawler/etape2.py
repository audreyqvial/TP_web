from tasktimer import call_repeatedly
from urllib.request import urlopen
from urllib.parse import urlencode

liste = [
    "http://www.freepatentsonline.com/8937756.html",
    "http://www.freepatentsonline.com/8922857.html",
    "http://www.freepatentsonline.com/8908487.html",
    "http://www.freepatentsonline.com/8903207.html"
]

path = "/home/audrey/Audrey/Cours/INF344/TP/TP_crawler/"
filename = path+"result_etape02.txt"

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

# fonction appelée périodiquement
def urlcall(toBeProcessed):
    if toBeProcessed["elements"]:
        call = toBeProcessed["elements"].pop(0)
        print("page visitée: ", call)
        content = getURL(call)
        with open(filename, 'a') as f:
            print(content, file=f)
        f.close()
        return False
    else:
        return True

# mise en route d'un appel toutes les 5s de la fonction urlcall avec un dictionnaire
# qui contient les paramètres passés à chaque appel de la fonction
if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
     call_repeatedly(5, urlcall, { "elements": liste })




