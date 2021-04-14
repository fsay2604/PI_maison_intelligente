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
# Buzzer = 27

# Global variables
FlameSensor = None
GasSensor = None

# Functions
def init():
    global adc, FlameSensor, GasSensor
    # ADC
    if(adc.detectI2C(0x48)):    # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)):  # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)

    FlameSensor = Sensor.Flame_Sensor()
    GasSensor = Sensor.Gas_Sensor()

# Fonction principale qui loop
def loop():
    while True:
        pass

### DEBUT DU SCRIPT ####
if __name__ == '__main__':
    	init()
    try:
        loop()
    except KeyboardInterrupt: 
        GPIO.cleanup()
        print ('The end !')