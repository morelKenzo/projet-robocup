##################################
#
#Programme de la télécom entre le robot et le PC
#Initialisation avec le choix du canal
#Réception et décodage de messages
#
##################################
from microbit import *
import radio
from initialisation import idRobot
from mx12 import deplacement_robot
from tircharge import *
from drible import *



class Telecom():
    """Classe qui s'occupe de lagestion de la transmission radio du robot.
    Il faut définir le canal (valeur entre 0 et 255).
    Attention a ne pas envoyer deux message sur le meme canal radio.
    """

    def __init__(self,canal):
        self.dict_donnees = {'robot': idRobot,'vitesse_long_mm_s':0,'vitesse_lat_mm_s':0,'vitesse_rot_mrad_s':0,'charge':0,'puissance_tir':0,'angle_tir':0,'dribble':0}
        self.dernier_dict_donnees = {'robot': idRobot,'vitesse_long_mm_s':0,'vitesse_lat_mm_s':0,'vitesse_rot_mrad_s':0,'charge':0,'puissance_tir':0,'angle_tir':0,'dribble':0}
        self.pixel = 0

        #initialisation de la radio
        radio.config(group = canal)
        radio.on()
        
        
    def Decode_Message(self,msg_radio):
        """Fonction de décode des messages
        Il y a une vérification que le message est bien adressé au robot grace a son identifiant
        """
    
        if int.from_bytes(msg_radio[0:1],'big')==idRobot:
            
            #la conversion en entier signé n'est pas implémenté dans micropython
            vitesseL = int.from_bytes(msg_radio[1:3],'big')
            if vitesseL > 32767 :
                vitesseL -= 65536
            self.dict_donnees['vitesse_long_mm_s']=vitesseL
            vitesseT = int.from_bytes(msg_radio[3:5],'big')
            if vitesseT > 32767 :
                vitesseT -= 65536
            self.dict_donnees['vitesse_lat_mm_s']=vitesseT
            vitesseR = int.from_bytes(msg_radio[5:7],'big')
            if vitesseR > 32767 :
                vitesseR -= 65536
                
            self.dict_donnees['vitesse_rot_mrad_s']=vitesseR
            self.dict_donnees['charge']=int.from_bytes(msg_radio[7:8],'big')
            self.dict_donnees['puissance_tir']=int.from_bytes(msg_radio[8:9],'big')
            self.dict_donnees['angle_tir']=int.from_bytes(msg_radio[9:10],'big')
            self.dict_donnees['dribble']=int.from_bytes(msg_radio[10:11],'big')


    def receiveCommand(self) :
        """Fonction qui récupère un message, décode le message et applique les demandes du coach.
        """

        msg_radio=radio.receive_bytes()
        
        if msg_radio != None:
            self.Decode_Message(msg_radio)
            #print(self.DictDonnees)
            if self.pixel == 1 :
                display.set_pixel(1,0,9)
                self.pixel = 0
            else :
                display.set_pixel(1,0,0)
                self.pixel = 1
                
            #Mouvement du robot
            vlCmd, vtCmd, vrCmd = self.dict_donnees['vitesse_long_mm_s'], self.dict_donnees['vitesse_lat_mm_s'], self.dict_donnees['vitesse_rot_mrad_s']
            deplacement_robot(vlCmd, vtCmd, vrCmd)
            if vlCmd == 75 :
                display.set_pixel(2,0,9)
            else :
                display.set_pixel(2,0,0)

            if vlCmd == 300 :
                display.set_pixel(3,0,9)
            else :
                display.set_pixel(3,0,0)
            #print(self.DictDonnees['vitesse_long_mm_s'])


            #commande de tir
            if self.dict_donnees['puissance_tir'] != self.dernier_dict_donnees["puissance_tir"] :
                if self.dict_donnees['puissance_tir'] :
                    commande_tir(self.dict_donnees['puissance_tir'])
                    display.set_pixel(4,3,9)
                else : display.set_pixel(4,3,0)
                self.dernier_dict_donnees["puissance_tir"] = self.dict_donnees['puissance_tir']
            
            
            #commande de dribble
            if self.dict_donnees["dribble"] != self.dernier_dict_donnees["dribble"] :
                
                if self.dict_donnees["dribble"]>0 :
                    commande_drible(20)
                    display.set_pixel(4,4,9)
                else :
                    commande_drible(0)
                    display.set_pixel(4,4,0)
                self.dernier_dict_donnees["dribble"] = self.dict_donnees["dribble"]
           
            
