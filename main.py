##################################
#
#Programme principal du robot
#Initialisation de la radio avec le choix du canal
#Test en faisant faire un carré au robot
#
#Ensuite on vérifie l'arrivé de messages et on les traites
#
##################################

from microbit import *
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
    
while True :
    telecom.receiveCommand()
