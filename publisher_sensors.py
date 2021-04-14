#!/usr/bin/env python3

##########################################################################
# Auteurs:  Francois Charles Hebert & Samuel Fournier
# Projet:   Système d'alarme d'une maison.
##########################################################################

# Imports
import paho.mqtt.client as mqtt
import signal
import sys
import logger
from ADCDevice import *
from Sensor.flame_sensor import Flame_Sensor
from Sensor.gas_sensor import Gas_Sensor
import json
import time

# Global variables
FlameSensor = None
GasSensor = None
#Temp_sensor = None #(DHT)
adc = ADCDevice()

TOPIC = 'SENSORS'
BROKER_HOST = '127.0.0.1'
BROKER_PORT = 1883
CLIENT_ID = 'SYS_ALARME_SENSORS'
client = None

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

    FlameSensor = Flame_Sensor()
    GasSensor = Gas_Sensor()
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
            data = {'FLAME_STATE':'ON'}
            client.publish(TOPIC, payload=data, qos=0, retain=False)
            print("send {data} to {TOPIC}")
            time.sleep(1)
            

        # Récupération de la valeur du sensor et envoit du msg
        gas_val = GasSensor.read(adc)
        if(gas_val > 50):
            data = {'GAS_STATE':'ON'}
            client.publish(TOPIC, payload=data, qos=0, retain=False)
            print("send {data} to {TOPIC}")
            time.sleep(1)

        # Récupération de la valeur du sensor et envoit du msg
        #TempSensor.read()

####
# Fonctions pour le MQTT
####
def on_connect(client, userdata, flags, rc):
    print("Connected with result code {rc}")

def signal_handler(sig, frame):
    """Capture Control+C and disconnect from Broker."""
    logger.info("You pressed Control + C. Shutting down, please wait...")
    client.disconnect() # Graceful disconnection.
    sys.exit(0)

def init_mqtt():
    global client

    client = mqtt.Client(client_id=CLIENT_ID, clean_session=False)
    client.on_connect = on_connect

    # create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
    client.connect(BROKER_HOST, BROKER_PORT)


init()
init_mqtt()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Capture Control + C   
    client.loop_start()
    signal.pause()
