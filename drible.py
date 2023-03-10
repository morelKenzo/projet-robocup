from refpin import pin_dribbleur #on trouve le pin attitré au dribbleur (pin0)


def commande_drible(prctVitesse):
        consigne = int(prctVitesse*1023/100) #on transforme notre pourcentage de vitesse en commande
        pin_dribbleur.write_analog(consigne) #on envoie la consigne# 
