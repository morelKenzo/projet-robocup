from microbit import *
import radio

cannal = 10
radio.on()
radio.config(cannal)


while True:
	message = radio.receive()
