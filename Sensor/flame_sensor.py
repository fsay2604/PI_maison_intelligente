#!/usr/bin/env python

##########################################################################
# Auteurs:  Francois Charles Hebert & Samuel Fournier
# Classe:	Représente le sensor de flamme.
##########################################################################

import RPi.GPIO as GPIO
from ADCDevice import *
from time import sleep

class Flame_Sensor:
    FlamePin = 15

    # Constructeur
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.FlamePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.FlamePin, GPIO.FALLING, callback=self.myISR)

    # Callback qui s'execute lors de la detection de l'event
    def myISR(self,ev=None):
        print("Flame is detected !")
        if GPIO.input(self.FlamePin):
            print('HI')
        else:
            print('LOW')

    # Fonction qui lit la valeur et la renvoit.
    def read(self, adc):
        res = adc.analogRead(0) # read ADC value of channel 0
        print('res = ', res)
        return res

if __name__ == "__main__":
    adc = ADCDevice()

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
        
    f = Flame_Sensor()
    while True:
        
        f.read(adc)
        sleep(0.5)
        
