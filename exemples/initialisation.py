from microbit import *
import music
from refpin import *
from tircharge import *

"""
Voici un exemple de code à mettre au début de main.py pour
assurer une bonne initialisation du robot
"""
idRobot = 2


def initialisation():
    music.play(music.BA_DING) # son à la mise sous tension
    display.show(Image.HAPPY)
    sleep(500)
    display.clear()
    # Initialise le protocole uart pour le mx12
    uart.init(baudrate=115200, tx=pin_tx, rx=pin_rx)
    charge_condo()
