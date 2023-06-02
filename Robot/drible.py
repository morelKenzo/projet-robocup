##################################
#Programme de la commande du tir du robot
##################################

from refpin import pin_dribbleur

def commande_drible(prctVitesse):
    """
    Fonction de commande de dribble moteur.
    Il faut définir un pourcentage de la vitesse max voulu
    """
    consigne = int(prctVitesse*1023/100) #on transforme notre pourcentage de vitesse en commande
    pin_dribbleur.write_analog(consigne) #on envoie la consigne# 