from refpin import pin_charge_condo
from refpin import pin_tir

def charge_condo():
    """
    Prend en argument l'objet associé au pin
    de commande de charge de condensateur.
    Envoie la consigne de charge.
    """
    pin_charge_condo.write_digital(1)


def commande_tir(prct):
    """
    Prend en arguments les objets associés aux pins
    pin_charge_condo et pin_tir, et un entier prct.
    Arrête la commande de charge du condensateur, et
    envoie une consigne de tir dont la puissance est
    donnée par prct
    """
    pin_charge_condo.write_digital(0)
    pin_tir.write_digital(1)
    sleep(20 * (prct / 100))
    pin_tir.write_digital(0)
    charge_condo()
    
