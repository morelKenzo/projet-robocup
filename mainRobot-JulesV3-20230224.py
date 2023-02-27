from microbit import *
from math import *
import radio
import music
import time
import micropython
micropython.kbd_intr(-1)


class Motor() :

    def __init__(self, idMot) :

        self.idMot = idMot

    def buildFrameMX12(self, instruction, typeRegistre, value) :

        dict_instruct_HEX = {'ping' : 0x01, 'read' : 0x02, 'write' : 0x03 }

        # Access : Read & Write
        dict_registreRW_HEX = {
            'ledStatus'    : 0x19, # 25
            'gainD'        : 0x1a, # 26
            'gainI'        : 0x1b, # 27
            'gainP'        : 0x1c, # 28
            'positionGoal' : 0x1e, # 30
            'speedGoal'    : 0x20, # 32
            'tension':42
            }

        dict_size = {
            'ledStatus'       : 1,
            'gainD'           : 1,
            'gainI'           : 1,
            'gainP'           : 1,
            'positionGoal'    : 2,
            'speedGoal'       : 2,
            'tension':1,
            }

        header = 0xff
        idMot = self.idMot
        lenght_bytes_value = dict_size[typeRegistre]
        instruct = dict_instruct_HEX[instruction]
        registre = dict_registreRW_HEX[typeRegistre]

        lenghtFrame = 6 + lenght_bytes_value + 1

        frame = bytearray(lenghtFrame)

        frame[0] = header
        frame[1] = header
        frame[2] = idMot
        frame[3] = lenght_bytes_value + 3
        frame[4] = instruct
        frame[5] = registre

        if lenght_bytes_value>0:
            valBytearray = value.to_bytes(lenght_bytes_value, 'little')

            n = 6
            for i, byte in enumerate(valBytearray) :
                frame[n+i] = byte

        checksum = 0
        for i in range(2,len(frame)):
            checksum += frame[i]

        # Complement a un
        checksum=(~checksum)&0xff

        frame[-1] = checksum.to_bytes(1, 'big')[0]

        return frame

    def demandeTension(self):
        trame=self.buildFrameMX12('read','tension',1)
        tampon=uart.read(15)
        uart.write(trame)

        #Vide le buffer
        tampon=uart.read(1)
        while tampon==None:
            tampon=uart.read(1)
        reponse=[]
        a=0
        while tampon!=None:
            if a==0:
                display.set_pixel(0,0,9)
                a=1
            else:
                a=0
                display.set_pixel(0,0,0)


            reponse.append(tampon)
            tampon=uart.read(1)

        #Récupere la valeur de reponse
        tampon=uart.read(1)
        while tampon==None:
            tampon=uart.read(1)
        reponse=[]
        a=0
        while len(reponse)<7:
            if a==0:
                display.set_pixel(0,0,9)
                a=1
            else:
                a=0
                display.set_pixel(0,0,0)


            reponse.append(tampon)
            tampon=uart.read(1)

        #int.from_bytes(reponse[1:3],'big')
        display.scroll(int.from_bytes(reponse[-2],'big')/10)


    def setSpeedRotation(self, val) : # val en rad.s-1

        # ~~~~ Conversions ~~~~
        valRPM = (60/(2*pi))*val
        val1024_alg = int(valRPM/0.916) #937.1 = w_max en RPM pour un moteur à vide

        # saturation de -1023 à 1023
        if val1024_alg > 1023 :
            val1024_alg = 1023
        elif val1024_alg < -1023 :
            val1024_alg = -1023

        # val1024_alg est algébrique de -1024 à 1024
        if val1024_alg >= 0 :
            v2048 = val1024_alg
        else :
            v2048 = 1024 - val1024_alg

        # ~~~ Envoie trame ~~~~
        frame = self.buildFrameMX12('write', 'speedGoal', v2048)
        uart.write(frame)


class Robot() :

    def __init__(self, idRobot=2, radioGroup=15) :

        uart.init(baudrate=115200, tx=pin1, rx=pin2)

        self.idRobot = idRobot

        self.pinDrible = pin16     # pin0
        self.pinChargeCondo = pin9 # pin8
        self.pinTir = pin8         # pin16

        self.driblePowerPrct = 30
        self.stateDrible = self.driblePowerPrct

        self.rayonRoue = 19 # en mm

        #self.posMot1 = (0, -0.072) #roue arriere
        #self.posMot2 = (0.0616, 0.0376)
        #self.posMot3 = (-0.0616, 0.0376)

        self.th1, self.th2, self.th3 = 4.74, 0.523, 2.64
        self.th1, self.th2, self.th3 = 2.64, 0.523, 4.74 # Correction : translation long et trans ok mais pas rotation sur place

        self.posMot1 = (-0.0616, 0.0376) #moteur gauche
        self.posMot2 = (0.0616, 0.0376) #moteur droit
        self.posMot3 = (0, -0.072) #moteur arriere


        self.mot1, self.mot2, self.mot3 = Motor(1), Motor(2), Motor(3)

        # Ordre des informations dans la trame radio : idRobot, vl, vt, vr, tir, passe, drible, charge
        self.DictDonnees = {'robot': self.idRobot,'vitesse_long_mm_s':0,'vitesse_lat_mm_s':0,'vitesse_rot_mrad_s':0,'charge':0,'puissance_tir':0,'angle_tir':0,'dribble':0}
        self.lastDictDonnees = {'robot': self.idRobot,'vitesse_long_mm_s':0,'vitesse_lat_mm_s':0,'vitesse_rot_mrad_s':0,'charge':0,'puissance_tir':0,'angle_tir':0,'dribble':0}
        self.pixel = 0
        radio.config(group=radioGroup)
        radio.on()

    def move(self, vl, vt, vr) : # En mm.s-1 et rad.s-1

        vectVitesse = [vl,vt,vr]

        # Problème commande moteur identifié suite à la correction : move(0, 0, v) entraine une translation selon un axe diagonale et non un rotation sur place
        # Solutions ?
        # --> Modifier la commande moteur
        # --> Modifier l'id des moteurs de sorte à échanger le 1 avec le 3
        matriceCommande = [[cos(self.th1), sin(self.th1), self.posMot1[0]*cos(self.th1)+self.posMot1[1]*sin(self.th1)],
                           [cos(self.th2), sin(self.th2), self.posMot2[0]*cos(self.th2)+self.posMot2[1]*sin(self.th2)],
                           [cos(self.th3), sin(self.th3), self.posMot3[0]*cos(self.th3)+self.posMot3[1]*sin(self.th3)]]

        vectCommande = [0]*3

        # vectCommande =  matrice_commande @ vectVitesse

        # Multiplication matrice-vecteur
        for i, l in enumerate(matriceCommande) :
            for j, e in enumerate(l) :
                vectCommande[i] += e*vectVitesse[j]

        self.mot1.setSpeedRotation(vectCommande[0]/self.rayonRoue)
        self.mot2.setSpeedRotation(vectCommande[1]/self.rayonRoue)
        self.mot3.setSpeedRotation(vectCommande[2]/self.rayonRoue)


    def commandeDrible(self, prctVitesse) :

        consigne = int(prctVitesse*1023/100)
        self.pinDrible.write_analog(consigne)


    def chargeCondo(self) :

        self.pinChargeCondo.write_digital(0)
        sleep(5)
        self.pinChargeCondo.write_digital(1)

        t0=time.ticks_us()#Permet de charger le condo sans bloqué le robot pendant 1s
        while (time.ticks_us()-t0)/1e6<1:
            self.receiveCommand()
        self.pinChargeCondo.write_digital(0)

    def commandeTir(self, prct) :

        # Envoie d'une MLI qu'on arrête au bon moment pour avoir un seul front
        rapport = int(200*((prct)/100))

        self.pinTir.set_analog_period(100)
        self.pinTir.write_analog(rapport)
        sleep(20)
        self.pinTir.write_digital(0)

    #fonction de conversion bytes vers entiers
    def Decode_Message(self,msg_radio):
        if int.from_bytes(msg_radio[0:1],'big')==self.idRobot:
            #la conversion en entier signé n'est pas implémenté dans micropython
            vitesseL = int.from_bytes(msg_radio[1:3],'big')
            if vitesseL > 32767 :
                vitesseL -= 65536
            self.DictDonnees['vitesse_long_mm_s']=vitesseL
            vitesseT = int.from_bytes(msg_radio[3:5],'big')
            if vitesseT > 32767 :
                vitesseT -= 65536
            self.DictDonnees['vitesse_lat_mm_s']=vitesseT
            vitesseR = int.from_bytes(msg_radio[5:7],'big')
            if vitesseR > 32767 :
                vitesseR -= 65536
            self.DictDonnees['vitesse_rot_mrad_s']=vitesseR
            self.DictDonnees['charge']=int.from_bytes(msg_radio[7:8],'big')
            self.DictDonnees['puissance_tir']=int.from_bytes(msg_radio[8:9],'big')
            self.DictDonnees['angle_tir']=int.from_bytes(msg_radio[9:10],'big')
            self.DictDonnees['dribble']=int.from_bytes(msg_radio[10:11],'big')

        '''
        elif int.from_bytes(msg_radio[0:1],'big') in DictDemande:
            message=int.from_bytes(msg_radio[0:1],'big')
            if message ==180:
                self.DictDonnees={'robot': self.idRobot,'vitesse_long_mm_s':0,'vitesse_lat_mm_s':0,'vitesse_rot_mrad_s':0,'charge':0,'puissance_tir':0,'angle_tir':0,'dribble':0}

            elif message ==181:
                pass #A modifier #############################################################
        '''

    def receiveCommand(self) :

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
            vlCmd, vtCmd, vrCmd = self.DictDonnees['vitesse_long_mm_s'], self.DictDonnees['vitesse_lat_mm_s'], self.DictDonnees['vitesse_rot_mrad_s']
            self.move(vlCmd, vtCmd, vrCmd)
            if vlCmd == 75 :
                display.set_pixel(2,0,9)
            else :
                display.set_pixel(2,0,0)

            if vlCmd == 300 :
                display.set_pixel(3,0,9)
            else :
                display.set_pixel(3,0,0)
            #print(self.DictDonnees['vitesse_long_mm_s'])
            #print(vlCmd)


            puissance_tir, cmdDrible, cmdCharge = self.DictDonnees['puissance_tir'], bool(self.DictDonnees["dribble"]), bool(self.DictDonnees["charge"])

            #commande de tir
            if puissance_tir != self.lastDictDonnees["puissance_tir"] and puissance_tir :
                self.commandeTir(puissance_tir)



            #commande de dribble
            if cmdDrible != self.lastDictDonnees["dribble"] and cmdDrible :
                self.stateDrible = self.driblePowerPrct - self.stateDrible
                self.commandeDrible(self.stateDrible)


            #commande charge
            #if cmdCharge != self.lastDictDonnees["charge"] and cmdCharge :
                #self.chargeCondo()

            self.lastDictDonnees = self.DictDonnees


def init():
    music.play(music.BA_DING)
init()
robot=Robot()
display.show(Image.HAPPY)
robot.mot2.setSpeedRotation(0)

while True:
    if button_a.is_pressed():
        display.show(Image.NO)
        robot.mot2.setSpeedRotation(512)
        sleep(1000)

    if button_b.is_pressed():
        display.show(Image.YES)
        robot.mot2.demandeTension()





