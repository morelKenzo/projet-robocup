##################################
# Programme principal du robot
# Initialisation, test et reception des messages
##################################

from microbit import *
from tircharge import *
from mx12 import *
from telecom import *
from initialisation import *
from test import *
import micropython

idRobot = 0
# Le numéro de canal est donné en argument de Telecom
# Par convention, il doit être égal à :
# numéro de l'équipe * 10
groupe_canal = 10

micropython.kbd_intr(-1)
initialisation()
telecom = Telecom(groupe_canal)

# Teste les différentes fonctionnalités du robot.
# Peut être commenté
testRoutine()
    
while True:
    telecom.receiveCommand(idRobot)
