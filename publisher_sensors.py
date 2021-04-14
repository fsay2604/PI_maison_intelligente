#!/usr/bin/env python

##########################################################################
# Auteurs:  Francois Charles Hebert & Samuel Fournier
# Projet:   Système d'alarme d'une maison.
##########################################################################

# Imports
import paho.mqtt.client as mqtt
from Sensor import *
from ADCDevice import *

# Global variables
FlameSensor = None
GasSensor = None
#Temp_sensor = None #(DHT)
adc = ADCDevice()
TOPIC = 'SENSORS'

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

    FlameSensor = Sensor.flame_sensor.Flame_Sensor()
    GasSensor = Sensor.gas_sensor.Gas_Sensor()
    #TempSensor = Sensor.Freenove_DHT.DHT()

# Fonction qui va loop a l'infini et va lire les valeurs lu des differents sensor.
# Lorsque les valeurs depassent un certain niveau, on va publier un message.
def loop():
    global TOPIC
    global FlameSensor
    global GasSensor
    #global TempSensor
    global adc

    while True:
        # Récupération de la valeur du sensor et envoit du msg
        flame_val = FlameSensor.read(adc)
        if(flame_val > 50):
            client.publish(TOPIC, payload={ "stateLight": "off" }, qos=0, retain=False)
            print("send to {TOPIC}")
            time.sleep(1)
            

        # Récupération de la valeur du sensor et envoit du msg
        gas_val = GasSensor.read(adc)
        if(gas_val > 50):
            client.publish(TOPIC, payload={ "stateLight": "off" }, qos=0, retain=False)
            print("send to {TOPIC}")
            time.sleep(1)

        # Récupération de la valeur du sensor et envoit du msg
        #TempSensor.read()

####
# Fonctions pour le MQTT
####
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


# Setting up la connection
client = mqtt.Client()
client.on_connect = on_connect

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
#client.connect("broker.emqx.io", 1883, 60)

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
#client.loop_forever()