##################################
#
#Programme d'initialisation du robot
#    -Initialisation de la liaison série des moteurs
#    -Mesure de la tension et si elle est trop basse(<11V)
#          on signifie que c'est pas bon avec de la musique
##################################


from microbit import *
import music
from refpin import *
from tircharge import *
from mx12 import *

# Régler idRobot soit à 0 soit à 1 
idRobot = 1

# Le numéro de canal est donné en argument de Telecom
# Par convention, il doit être égal à :
# numéro de l'équipe * 10
# Exemple : pour l'équipe 3, groupe_canal = 30
groupe_canal = 30

def initialisation():
    """Programme d'initialisation du robot:
    Mise en place de la liaison série avec les moteurs
    Vérification de la tension batterie
    """
    display.show(Image.HAPPY)
    sleep(500)
    display.clear()
    # Initialise le protocole uart pour le mx12
    uart.init(baudrate=115200, tx=pin_tx, rx=pin_rx)
    Tension_robot()
    charge_condo()


def Tension_robot():
    """Mesure de la tension du robot en faisnt la moyenne des tensions des moteurs"""
    
    Tension_mot1=mot1.demandeTension()
    sleep(20)
    Tension_mot2=mot2.demandeTension()
    sleep(20)
    Tension_mot3=mot3.demandeTension()
    Tension_moyenne_V=(Tension_mot1+ Tension_mot2+Tension_mot3)/3
    display.scroll(round(Tension_moyenne_V,1))
    if Tension_moyenne_V>=14:
        for i in range(0,5):
            display.set_pixel(0,i,9)
    elif Tension_moyenne_V>=13:
        for i in range(1,5):
            display.set_pixel(0,i,9)
    elif Tension_moyenne_V>=12:
        for i in range(2,5):
            display.set_pixel(0,i,9)
    elif Tension_moyenne_V>=11:
        for i in range(3,5):
            display.set_pixel(0,i,9)
    else:
        for i in range(4,5):
            display.set_pixel(0,i,9)
        



    

