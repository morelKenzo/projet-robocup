from microbit import *
from tircharge import *
from mx12 import *
from telecom import *
from initialisation import *
from test import *


initialisation()
telecom = Telecom()
testRoutine()
while True :
    telecom.receiveCommand()
