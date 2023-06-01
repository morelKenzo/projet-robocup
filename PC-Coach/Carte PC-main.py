from microbit import *
import radio
import music
import micropython

#Désactivation de l'interruption sur la valeur 0x03 sur la reception de la liaison série
micropython.kbd_intr(-1)

# A configurer une bonne fois pour toute.
canal = 10

def Initialisation():
    uart.init(baudrate=115200) #initialisation de la communication série de la microbit
    radio.config(channel = canal) #initialisation du canal radio utilisé
    radio.on()
    music.play(music.BA_DING) #son à la mise sous tension
    display.show(Image.YES) #affichage sur les LED d'un symbole "validé" pour repérer la carte PC
    sleep(1000)
    display.clear()

#variables utiles pour l'affichage sur les LEDs
a=0
b=0

Initialisation() # lancement de l'initialisation

while True:

    #Réception depuis PC et transmission vers la carte robot
    msg_bytes=b''

    #reception du message sur la liaison série avec vérification de la longueur
    while len(msg_bytes)<22:
        if uart.any():
            byte_received = uart.read()
            msg_bytes+=byte_received
            
    #activation d'un LED quand réception sur la liaison série
    if a==0:
        display.set_pixel(0,0,9)
        a=1
    else:
        a=0
        display.set_pixel(0,0,0)
    #print(msg_bytes)

    #Envoie du message aux robot via la communication robot
    radio.send_bytes(msg_bytes)

    #Réception radio depuis la carte robot et transmission vers PC
    msg_radio=radio.receive()
    if msg_radio!=None:
        if b==0:
            display.set_pixel(1,0,9)
            b=1
        else:
            b=0
            display.set_pixel(1,0,0)
        print(str(msg_radio)) # a remplacer par uart.write() quand mise en place du retour d'information# Ecrit ton programme ici ;-)
