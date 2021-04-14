#!/usr/bin/env python

##########################################################################
# Auteurs:  Francois Charles Hebert & Samuel Fournier
# Projet:   Système d'alarme d'une maison.
##########################################################################

# Imports
from Sensor import *
from ADCDevice import *

# Global variables
FlameSensor = None
GasSensor = None
#Temp_sensor = None
adc = ADCDevice()

def init():
    global FlameSensor
    global GasSensor
    #global TempSensor
    global adc

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
    #TempSensor = Sensor.DHT11()

# Fonction qui va loop a l'infini et va lire les valeurs lu des differents sensor.
# Lorsque les valeurs depassent un certain niveau, on va publier un message.
def loop():
    global FlameSensor
    global GasSensor
    #global TempSensor
    global adc

    while True:
        FlameSensor.read(adc)