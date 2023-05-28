from microbit import *

##################################
# Module permettant à l'utilisateur
# d'accéder à un menu où il peut modifier
# l'identifiant du robot et le canal de transmission.

##################################

def afficher_menu(idRobot, groupe_canal):
    """ L'accès à ce menu est réalisé par la fonction afficher_menu.
    Pour accéder à ce menu il faut appuyer sur le bouton b.
    Pour changer la sélection, il faut appuyer sur le bouton b.
    Pour confirmer un choix, attendre 5 secondes sans rien toucher.
    En-dehors du menu, la ligne la plus haute indique l'identifiant du robot
    et la ligne juste en-desssous, le canal de transmission.
    """
    display.set_pixel(4, idRobot, 9)
    numero_groupe = int(groupe_canal/10)
    display.set_pixel(3, numero_groupe - 1, 9)
    menu = ["C", "I"]
    index_menu1 = 0
    # Accès au premier menu de sélection lorsque le bouton b est pressé
    # où l'utilisateur choisit ce qu'il veut modifier :
    # soit C (le canal de transmission), soit I (l'identifiant du robot) 
    if button_b.was_pressed():
        # Variable pour stocker le temps du dernier appui sur le bouton B
        dernier_appui = running_time()
        while True:
            display.show(menu[index_menu1])
            # Change de sélection à chaque appui du bouton b
            if button_b.was_pressed():
                index_menu1 = (index_menu1 + 1)%len(menu)
                dernier_appui = running_time()
            # Accès au sous-menu correspondant à la sélection précédente (C ou I)
            # après 5 seconde d'inactivité
            if running_time() - dernier_appui >= 5000:
                display.clear()
                if menu[index_menu1] == "C":
                    # 4 choix de canal de transmission
                    # 1 pour groupe 1, 2 pour groupe 2 ... 4 pour groupe 4.
                    dernier_appui = running_time()
                    while True:
                        display.show(numero_groupe)
                        if button_b.was_pressed():
                            numero_groupe = ((numero_groupe) % 4) + 1
                            dernier_appui = running_time()
                        if running_time() - dernier_appui >= 5000:
                            groupe_canal = numero_groupe * 10
                            display.clear()
                            break
                    break
                
                if menu[index_menu1] == "I":
                    # 2 choix pour l'identifiant : soit 0 ou 1
                    dernier_appui = running_time()
                    while True:
                        display.show(idRobot)
                        if button_b.was_pressed():
                            idRobot = ((idRobot + 1) % 2)
                            dernier_appui = running_time()
                        if running_time() - dernier_appui >= 5000:
                            display.clear()
                            break
                    break
                    