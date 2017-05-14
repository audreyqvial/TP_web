from modules.tasktimer import call_repeatedly

liste = [
    "toto",
    "titi"
]

# fonction appelée périodiquement
def urlcall(toBeProcessed):
    if toBeProcessed["elements"]:
        call = toBeProcessed["elements"].pop(0)
        print("page visitée: ", call)
        return False
    else:
        return True

# mise en route d'un appel toutes les 5s de la fonction urlcall avec un dictionnaire
# qui contient les paramètres passés à chaque appel de la fonction
call_repeatedly(5, urlcall, { "elements": liste })



