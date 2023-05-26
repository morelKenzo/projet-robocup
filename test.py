from microbit import *
from tircharge import *
from mx12 import *
from telecom import *
from initialisation import *


def testRoutine():    
    """Fonction de test qui consiste a faire faire un carré"""
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
    commande_tir(10)
    sleep(10)
    charge_condo()
    sleep(500)
    


    #test drible
    commande_drible(20)
    sleep(1000)
    commande_drible(0)
    sleep(1000)

    
    