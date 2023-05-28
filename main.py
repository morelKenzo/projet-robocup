##################################
#
# Programme principal du robot
# Initialisation puis test en faisant faire un carré au robot
# Ensuite on vérifie l'arrivé de messages et on les traite
# Configuration possible du canal de transmission et
# de l'identifiant du robot par le menu.
#
##################################

from microbit import *
from menu import *
from tircharge import *
from mx12 import *
from telecom import *
from initialisation import *
from test import *
import micropython

micropython.kbd_intr(-1)
initialisation()

# groupe_canal doit être modifié selon le numéro du groupe
groupe_canal = 30
telecom = Telecom(groupe_canal)

# Teste les différentes fonctionnalités su robot.
# Peut être commenté
testRoutine()

Tension_robot()
    
while True:
    afficher_menu(idRobot, groupe_canal)
    telecom.receiveCommand()
