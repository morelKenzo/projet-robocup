from microbit import *
from tircharge import *
from mx12 import *
from telecom import *
from initialisation import *


def testRoutine():    
    #test roue

    deplacement_robot(200,0,0)
    sleep(500)
    deplacement_robot(0,200,0)
    sleep(500)
    deplacement_robot(-200,0,0)
    sleep(500)
    deplacement_robot(0,-200,0)
    sleep(500)
    deplacement_robot(0,0,0)
    sleep(500)
    

    
    #test tir
    charge_condo()
    commande_tir(10)
    sleep(500)
    


    #test drible
    commande_drible(20)
    sleep(500)
    commande_drible(0)
    sleep(500)

    
    
