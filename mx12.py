""" Controle d'un dynamixel par Kenzo Morel-Handa """
from microbit import *
from refpin import pin_tx
from refpin import pin_rx

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


class Roue:
    def __init__(self, idMot):
        self.idMdot = idMot

    def envoi_vitesse(self, vitesse):
        frame = build_frame("write", "speedGoal", vitesse)
        uart.write(frame)
