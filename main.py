from microbit import *
from tircharge import *
from mx12 import *
from telecom import *

# Ne pas oublier d'initialiser correctement 

# Exemple de code d'initialisation du robot :
# from exemples import initialisation
# initialisation.initialisation()

# Exemple de code de test du robot :
# from exemples import test
# test.testRoutine()

telecom = Telecom()
while True :
    telecom.receiveCommand()
