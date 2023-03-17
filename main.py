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


initialisation()
telecom = Telecom(15)
testRoutine()
    
while True :
    
    telecom.receiveCommand()
