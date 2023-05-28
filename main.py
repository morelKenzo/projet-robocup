##################################
# Programme principal du robot
# Initialisation, test et reception des messages
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
    
while True:
    afficher_menu(idRobot, groupe_canal)
    telecom.receiveCommand()
