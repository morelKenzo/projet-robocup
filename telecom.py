from microbit import *
import radio

cannal = 10 #definition du canal de communication avec le moteur.



#initialisation de la radio
radio.config(cannal)
radio.on()





def reception(message,idMoteur):
	message = radio.receive
        if message :

            listMessage = message.split(",") #on découpe le message d'entrée avec les virgules /!\ au protocole de communication avec Noah
            if listMessage[0] == idMoteur and listMessage[-1] == "fin":
                
                vit_x = int(listMessage[1])
                vit_y = int(listMessage[2])
                vit_rot = int(listMessage[3])
                tir = int(listMessage[4])
                passe = int(listMessage[5])
                dribble = int(listMessage[6])
            message = False
	return vitesse_long
