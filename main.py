#!/usr/bin/env python

##########################################################################
# Auteurs:  Francois Charles Hebert & Samuel Fournier
# Projet:   Système d'alarme d'une maison.
##########################################################################

# Imports
import RPi.GPIO as GPIO
from gpiozero import Device, LED, Buzzer, Button
from ADCDevice import *
import time


## PINS (header)
# BTN = 17
# Buzzer = 27

# Global variables
Leds = [None, None]

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

# Fonction principale qui loop
def loop():
    while True:
        pass

"""
MQTT Related Functions and Callbacks
"""
def on_connect(client, user_data, flags, connection_result_code):
    """on_connect is called when our program connects to the MQTT Broker.
       Always subscribe to topics in an on_connect() callback.
       This way if a connection is lost, the automatic
       re-connection will also results in the re-subscription occurring."""

    if connection_result_code == 0: 
        # 0 = successful connection
        logger.info("Connected to MQTT Broker")
    else:
        # connack_string() gives us a user friendly string for a connection code.
        logger.error("Failed to connect to MQTT Broker: " + mqtt.connack_string(connection_result_code))

    # Subscribe to the topic 
    #client.subscribe(TOPIC[0], qos=2)   # Led
    #client.subscribe(TOPIC[1], qos=2)   # Door
    #client.subscribe(TOPIC[2], qos=2)   # Alarm  



def on_disconnect(client, user_data, disconnection_result_code):                         
    """Called disconnects from MQTT Broker."""
    logger.error("Disconnected from MQTT Broker")



def on_message(client, userdata, msg):
    """Callback called when a message is received on a subscribed topic."""
    logger.debug("Received message for topic {}: {}".format( msg.topic, msg.payload))

    data = None

    try:
        data = json.loads(msg.payload.decode("UTF-8"))
    except json.JSONDecodeError as e:
        logger.error("JSON Decode Error: " + msg.payload.decode("UTF-8"))

    #if msg.topic == TOPIC[0]: 
    #    set_led_state(data) 
    #elif msg.topic == TOPIC[1]:
    #    set_door_state(data) 
    #elif msg.topic == TOPIC[2]: 
    #    set_buzzer_state(data)   
    #else:
    #    logger.error("Unhandled message topic {} with payload " + str(msg.topic, msg.payload))



def signal_handler(sig, frame):
    """Capture Control+C and disconnect from Broker."""
    #global led_principale
    #global led_secondaire
    #global buzzer

    logger.info("You pressed Control + C. Shutting down, please wait...")

    client.disconnect() # Graceful disconnection.
    #led_principale.off()
    #led_secondaire.off()
    #buzzer.off()
    sys.exit(0)



def init_mqtt():
    global client

    # Our MQTT Client. See PAHO documentation for all configurable options.
    # "clean_session=True" means we don"t want Broker to retain QoS 1 and 2 messages
    # for us when we"re offline. You"ll see the "{"session present": 0}" logged when
    # connected.
    client = mqtt.Client(                                                                      # (15)
        client_id=CLIENT_ID,
        clean_session=False)

    # Route Paho logging to Python logging.
    client.enable_logger()                                                                     # (16)

    # Setup callbacks
    client.on_connect = on_connect                                                             # (17)
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to Broker.
    client.connect(BROKER_HOST, BROKER_PORT)                                                   # (18)


### DEBUT DU SCRIPT ####
if __name__ == '__main__':
    	init()
    try:
        loop()
    except KeyboardInterrupt: 
        GPIO.cleanup()
        print ('The end !')