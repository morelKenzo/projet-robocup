from microbit import *
from refpin import pin_tx
from refpin import pin_rx
from math import pi, cos, sin

def initialisation_uart():
    # Initialise le protocole uart pour le mx12
    uart.init(baudrate=115200, tx=pin_tx, rx=pin_rx)

def build_frame(idMot, instruction, typeRegistre, value):
    """
    Prend en arguments :
    idMot : identifiant moteur MX12
    instruction : ping, read ou write
    typeRegistre : ex speedGoal
    value : valeur à mettre dans le registre
    renvoie la trame correspondante à la commande.
    """

    dict_instruct_HEX = {"ping": 0x01, "read": 0x02, "write": 0x03}

    # Access : Read & Write
    dict_registreRW_HEX = {
        "ledStatus": 0x19,  # 25
        "gainD": 0x1A,  # 26
        "gainI": 0x1B,  # 27
        "gainP": 0x1C,  # 28
        "positionGoal": 0x1E,  # 30
        "speedGoal": 0x20,  # 32
    }

    dict_size = {
        "ledStatus": 1,
        "gainD": 1,
        "gainI": 1,
        "gainP": 1,
        "positionGoal": 2,
        "speedGoal": 2,
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
    def __init__(self, idMot, angle_roue, position_roue_x, position_roue_y):
        self.rayon_roue = 0.019
        self.idMot = idMot
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
        frame = build_frame(self.idMot, "write", "speedGoal", vitesse_alg)
        uart.write(frame)

    def deplacement(self, vit_x, vit_y, vit_rot):
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
