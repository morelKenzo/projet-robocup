##################################
#
#Programme de gestion du moteur des roues
#Création des frame pour les moteurs
#Création d'un classe roues qui paramètre les moteurs
#    -définir la vitesse de la roue
#    -mesure de la tension aux bornes de la roue
##################################

from microbit import *
from math import *


def build_frame(idMot, instruction, typeRegistre, value):
    """
    Prend en arguments :
    idMot : identifiant moteur MX12
    instruction : ping, read ou write
    typeRegistre : ex speedGoal
    value : valeur de vitesse à mettre dans le registre
    renvoie la trame correspondante à la commande.
    """

    dict_instruct_HEX = {"ping": 0x01, "read": 0x02, "write": 0x03}

    # Access : Read & Write
    dict_registreRW_HEX = {
            'ledStatus'    : 0x19, # 25
            'gainD'        : 0x1a, # 26
            'gainI'        : 0x1b, # 27
            'gainP'        : 0x1c, # 28
            'positionGoal' : 0x1e, # 30
            'speedGoal'    : 0x20, # 32
            'tension'      :   42
        }

    dict_size = {
        'ledStatus'       : 1,
        'gainD'           : 1,
        'gainI'           : 1,
        'gainP'           : 1,
        'positionGoal'    : 2,
        'speedGoal'       : 2,
        'tension'         : 1,
        }

    header = 0xFF
    idMot = idMot
    lenght_bytes_value = dict_size[typeRegistre]
    instruct = dict_instruct_HEX[instruction]
    registre = dict_registreRW_HEX[typeRegistre]

    lenghtFrame = 6 + lenght_bytes_value + 1

    frame = bytearray(lenghtFrame)
    # En tetes standards
    frame[0] = header
    frame[1] = header
    frame[2] = idMot
    # Nombre d'octets nécessaires pour la commande voulue
    frame[3] = lenght_bytes_value + 3
    frame[4] = instruct
    frame[5] = registre

    valBytearray = value.to_bytes(lenght_bytes_value, "little")

    n = 6
    for i, byte in enumerate(valBytearray):
        frame[n + i] = byte
    checksum = 0
    for i in range(2, len(frame)):
        checksum += frame[i]
    # Complement a un
    checksum = ~checksum
    frame[-1] = checksum.to_bytes(1, "big")[0]
    return frame


class Roue():
    """Classe permettant la gestion des moteurs liées au roues.
    Il faut définir l'identifiant du moteur, l'angle de la roue, la position de la roue selon x puis selon y."""
    
    def __init__(self, idMot, angle_roue, position_roue_x, position_roue_y):
        self.rayon_roue = 19
        self.idMdot = idMot
        # Position angulaire de la roue par rapport au repere du robot
        self.angle_roue = angle_roue
        # Position de la roue rapport au repere du robot
        self.position_roue_x = position_roue_x
        self.position_roue_y = position_roue_y

    def consigne_vitesse(self, vitesse):
        """
        Envoie une consigne de vitesse au moteur MX12
        Prend en arguments une consigne de vitesse en rad/s
        """
        vitesse_rpm = (60/(2*pi))*vitesse # Convertit la vitesse de consigne en tour/min
        vitesse_alg = int((1023/937.1)*vitesse_rpm) # Convertit la vitesse dans une plage de 0 à 1023 (937,1 étant la vitesse maximale du moteur)
        # En fonction du signe de la vitesse, on met la vitesse dans la plage [0, 1023] ou dans [1024, 2048]
        if vitesse_alg >= 0 :
            vitesse_2048 = vitesse_alg
        else :
            vitesse_2048 = 1024 - vitesse_alg
        frame = build_frame(self.idMdot,"write", "speedGoal", vitesse_2048)
        
        uart.write(frame)

    def deplacement(self, vit_y, vit_x, vit_rot):
        """
        Prend en arguments :
        - vit_x : (float) vitesse de translation laterale qu'on aimerait avoir sur le robot
        - vit_y : (float) vitesse de translation longitudinal qu'on aimerait avoir sur le robot
        - vit_rot : (float) vitesse de rotation propre du robot qu'on aimerait avoir
        Envoie une consigne de vitesse au moteur afin que l'ensemble des roues puissent
        deplacer le robot comme souhaite
        """
        # Calcul de la vitesse angulaire du moteur MX12 (cf formule documentation)
        vitesse_mot = (sin(self.angle_roue)*vit_x - cos(self.angle_roue)*vit_y + (self.position_roue_x*cos(self.angle_roue)+self.position_roue_y*sin(self.angle_roue))*vit_rot)/self.rayon_roue
        # Envoie la consigne
        self.consigne_vitesse(vitesse_mot)

        
    def demandeTension(self):
        """
        Procède à la mesure de la tension aux bornes du moteur qui est la tension batterie.
        """
        #Faire attention le temps de réponse est paramétrable sur les moteurs donc il n'y a pas beoin de vider le buffer si 100 micro-secondes
    
        #Vide buffer
        tampon=uart.read(1)
        while tampon!=None:
            tampon=uart.read(1)
    
        trame=build_frame(self.idMdot,'read','tension',1)
        uart.write(trame)
    
        sleep(1)
    
        reponse=[]
        a=0
        tampon=uart.read(1)
    
        while tampon!=None:
            if a==0:
                display.set_pixel(0,0,9)
                a=1
            else:
                a=0
                display.set_pixel(0,0,0)
            reponse.append(tampon)
            tampon=uart.read(1)
        tension_V=int.from_bytes(reponse[-2],'big')/10
    
        return(tension_V)


th1, th2, th3 = 0.523, 2.618, 4.712
#th1, th2, th3 = 1.047, 0.523, 4.74     
x1,y1 = 0.0616, 0.0376 #moteur droit
x2,y2 = -0.0616, 0.0376 #moteur gauche
x3,y3 = 0, -0.072 #moteur arriere

#Création des moteurs
mot1, mot2, mot3 = Roue(1,th1,x1,y1), Roue(2,th2,x2,y2), Roue(3,th3,x3,y3)

#Commande de déplacement pour les moteurs depuis les vitesses locales du robot
def deplacement_robot(vitesse_long_mm_s, vitesse_lat_mm_s,vitesse_rot_mrad_s):
    """Programme de déplacement du robot par la commande des 3 moteurs.
    Il faut définir les vitesses longitudinale, latéral et de roation dans la base local du robot.
    """
    mot1.deplacement(vitesse_long_mm_s,-vitesse_lat_mm_s,vitesse_rot_mrad_s)
    mot2.deplacement(vitesse_long_mm_s,-vitesse_lat_mm_s,vitesse_rot_mrad_s)
    mot3.deplacement(vitesse_long_mm_s,-vitesse_lat_mm_s,vitesse_rot_mrad_s)


