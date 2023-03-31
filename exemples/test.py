from microbit import *
from tircharge import *
from mx12 import *
from telecom import *
from initialisation import *


"""
Exemple de fonction à mettre dans main pour tester les
différentes fonctionnalités du robot.
"""

def testRoutine():
    #test roue
    deplacement_robot(200,0,0)
    sleep(1000)
    deplacement_robot(0,200,0)
    sleep(1000)
    deplacement_robot(-200,0,0)
    sleep(1000)
    deplacement_robot(0,-200,0)
    sleep(1000)
    deplacement_robot(0,0,0)
    sleep(1000)

    #test tir
    charge_condo()
    commande_tir(10)
    sleep(500)

    #test drible
    commande_drible(20)
    sleep(1000)
    commande_drible(0)
    sleep(1000)

