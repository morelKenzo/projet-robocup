from microbit import *
import refpin as rp
import tircharge

while True:
    # Test du tir du robot
    if button_a.is_pressed():
        tircharge.charge_condo(rp.pin_charge_condo)
    if button_b.was_pressed():
        tircharge.commande_tir(rp.pin_charge_condo, pin_tir, 50)
