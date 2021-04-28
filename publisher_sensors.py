#!/usr/bin/env python3

##########################################################################
# Auteurs:  Francois Charles Hebert & Samuel Fournier
# Projet:   Système d'alarme d'une maison.
##########################################################################

# Imports
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import signal
import sys
from ADCDevice import *
from Sensor.flame_sensor import Flame_Sensor
from Sensor.gas_sensor import Gas_Sensor
import json
import time

# Global variables
FlamePin = 15

GasSensor = None
GAS_SENSOR_PREVIOUS_VAL = 0
#Temp_sensor = None #(DHT)
#TEMP_SENSOR_PREVIOUS_VAL = 0
adc = ADCDevice()

TOPIC = 'SENSORS'
BROKER_HOST = '127.0.0.1'
BROKER_PORT = 1883
CLIENT_ID = 'SYS_ALARME_SENSORS'
client = None



# Callback qui s'execute lors de la detection de l'event
def myISR(ev=None):
    global TOPIC
    print("Flame is detected !")
    data = {'FLAME_STATE':'ON'}
    client.publish(TOPIC, payload=json.dumps(data), qos=0, retain=False)
    print("send {data} to {TOPIC}")


def init():
    global FlameSensor
    global GasSensor
    global FlamePin
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

    #Flame sensor init
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(FlamePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(FlamePin, GPIO.FALLING, callback=myISR)
    
    GasSensor = Gas_Sensor()
    #TempSensor = Sensor.Freenove_DHT.DHT()

# Fonction qui va loop a l'infini et va lire les valeurs lu des differents sensor.
# Lorsque les valeurs depassent un certain niveau, on va publier un message.
def loop():
    global TOPIC
    global FlameSensor
    global FLAME_SENSOR_PREVIOUS_VAL
    global GAS_SENSOR_PREVIOUS_VAL
    global GasSensor
    #global TempSensor
    global adc

    while True:
        
        # Récupération de la valeur du sensor et envoit du msg
        #flame_val = FlameSensor.read(adc)
        readFlamme()
        # Récupération de la valeur du sensor et envoit du msg
        gas_val = GasSensor.read(adc)
        if(gas_val > 50):
            data = {'GAS_STATE':'ON'}
            client.publish(TOPIC, payload=json.dumps(data), qos=0, retain=False)
            print("send {data} to {TOPIC}")
            time.sleep(1)
            
        if (GAS_SENSOR_PREVIOUS_VAL >= 50 and gas_val < 50):
            data = {'GAS_STATE':'OFF'}
            client.publish(TOPIC, payload=json.dumps(data), qos=0, retain=False)
            print("send {data} to {TOPIC}")
            time.sleep(1)
        

        # Récupération de la valeur du sensor et envoit du msg
        #TempSensor.read()
        
        
        GAS_SENSOR_PREVIOUS_VAL = gas_val
        time.sleep(0.5)
        
        
        


# Fonction qui lit la valeur et la renvoit.
def readFlamme():
    global adc
    res = adc.analogRead(0) # read ADC value of channel 0
    #print('res = ', res)
    return res        

####
# Fonctions pour le MQTT
####



def on_connect(client, userdata, flags, rc):
    print("Connected with result code {rc}")

def signal_handler(sig, frame):
    """Capture Control+C and disconnect from Broker."""
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
    loop()
    signal.pause()
