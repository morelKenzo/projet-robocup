from microbit import *


##################################
# Module permettant à l'utilisateur
# d'accéder à un menu où il peut modifier
# l'identifiant du robot et le canal de transmission.
##################################


def afficher_menu(idRobot, groupe_canal):
    display.set_pixel(4, idRobot, 9)
    numero_groupe = int(groupe_canal/10)
    display.set_pixel(3, numero_groupe - 1, 9)
    menu = ["C", "I"]
    index_menu1 = 0
    # Acces au premier menu de sélection à l'appui du bouton b
    if button_b.was_pressed():
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
                    