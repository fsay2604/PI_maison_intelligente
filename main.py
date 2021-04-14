##########################################################################
# Auteurs:  Francois Charles Hebert & Samuel Fournier
# Projet:   Système d'alarme d'une maison.
##########################################################################

# Imports
import RPi.GPIO as GPIO
from ADCDevice import *
import time
from Sensor import *

## PINS (header)
# BTN = 17

# Global variables
FlamePin = 22         # A verifier
FlameSensor = None
GasSenson = None

# Functions
def init():
    global adc, FlamePin
    # ADC
	if(adc.detectI2C(0x48)): # Detect the pcf8591.
		adc = PCF8591()
	elif(adc.detectI2C(0x4b)): # Detect the ads7830
		adc = ADS7830()
	else:
		print("No correct I2C address found, \n"
		"Please use command 'i2cdetect -y 1' to check the I2C address! \n"
		"Program Exit. \n");
		exit(-1)

    global FlameSensor = Sensor.Flame_Sensor(FlamePin)
    

		
# Fonction de callback de la detection du detecteur de flammes.
def myISR(ev=None):
	print("Flame is detected !")

# Fonction principale qui loop
def loop():
	while True:
		res = adc.analogRead(0) # read ADC value of channel 0
		print('res = ', res)
		time.sleep(0.1)

### DEBUT DU SCRIPT ####
if __name__ == '__main__':
    	init()
	try:
		loop()
	except KeyboardInterrupt: 
		GPIO.cleanup()
		print ('The end !')