from microbit import *
import refpin as rp
import tircharge
import mx12

roue1 = mx12.Roue(1)
while True:
    # Test du tir du robot
    if button_a.is_pressed():
        roue1.envoi_vitesse(500)
