from microbit import *
from refpin import pin_charge_condo
from refpin import pin_tir

def charge_condo():
    """
    Lance la charge des condensateur pour le tir.
    """
    pin_charge_condo.write_digital(1)


def commande_tir(prct):
    """Fonction de tir qui prend comme argument un pourcentage qui correspond à la force du tir
    """
    pin_charge_condo.write_digital(0)
    pin_tir.write_digital(1)
    sleep(20 * (prct / 100))
    pin_tir.write_digital(0)
    charge_condo()
    
