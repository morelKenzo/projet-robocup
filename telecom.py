from microbit import *
import radio

cannal = 10 #definition du canal de communication avec le moteur.



#initialisation de la radio
radio.config(cannal)
radio.on()





def reception(message):
	message = radio.receive
        if message :

            listMessage = message.split(",") #on découpe le message d'entrée avec les virgules /!\ au protocole de communication avec Noah
            if listMessage[-1] == "fin":
                
                vit_x = int(listMessage[0])
                vit_y = int(listMessage[1])
                vit_rot = int(listMessage[2])
                tir = int(listMessage[3])
                passe = int(listMessage[4])
                dribble = int(listMessage[5])
            message = False
	return vitesse_long
