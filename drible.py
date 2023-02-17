from refpin import pin_dribbleur

def commandeDrible(self, prctVitesse) :
        consigne = int(prctVitesse*1023/100)
        self.pinDrible.write_analog(consigne)
