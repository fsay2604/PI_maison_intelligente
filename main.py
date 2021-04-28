#!/usr/bin/env python

##########################################################################
# Auteurs:  Francois Charles Hebert & Samuel Fournier
# Projet:   Système d'alarme d'une maison.
##########################################################################

# Imports
import RPi.GPIO as GPIO
from gpiozero import Device, LED, Buzzer, Button
from gpiozero.pins.pigpio import PiGPIOFactory
from ADCDevice import *
from Sensor.ventilation import ventilation
from Sensor.lcd import lcd
import signal
import json

import paho.mqtt.client as mqtt
import time

# Initialize GPIO
Device.pin_factory = PiGPIOFactory() # Set GPIOZero to use PiGPIO by default.


# Global Variables
BROKER_HOST = "127.0.0.1"                                                                       # (2)
BROKER_PORT = 1883
CLIENT_ID = "SYS_ALARME"                                                                         # (3)
TOPIC = "SENSORS"                                                                                   # (4)
client = None   # MQTT client instance. See init_mqtt()   

## PINS (header)
ButtonPin = 17
ButtonState = None
BuzzerPin = 27
buzzer = None

# Global variables
Leds = [None, None]

ventilation = ventilation()
lcd = lcd()


fire_state = {
    'status' : 'off'
}


gas_state = {
    'status' : 'off'
}



def button_pressed():
    pass


# Functions
def init():
    global leds
    global ButtonState
    global buzzer
    
    
    Leds[0] = LED(16)
    Leds[0].off()
    Leds[1] = LED(21)
    Leds[1].off()
   
   
    ButtonState = Button(ButtonPin, pull_up=True, bounce_time=0.1)
    ButtonState.when_pressed = button_pressed

    buzzer = Buzzer(BuzzerPin,active_high = False)
    buzzer.off()




"""
MQTT Related Functions and Callbacks
"""
def on_connect(client, user_data, flags, connection_result_code):
    """on_connect is called when our program connects to the MQTT Broker.
       Always subscribe to topics in an on_connect() callback.
       This way if a connection is lost, the automatic
       re-connection will also results in the re-subscription occurring."""

    # Subscribe to the topic 
    client.subscribe(TOPIC, qos=2)   # Led 



def on_disconnect(client, user_data, disconnection_result_code):                         
    """Called disconnects from MQTT Broker."""
    pass



def on_message(client, userdata, msg):
    """Callback called when a message is received on a subscribed topic."""
    #logger.debug("Received message for topic {}: {}".format( msg.topic, msg.payload))
    
    data = None


    data = json.loads(msg.payload.decode("UTF-8"))


    if "FLAME_STATE" in data:
        print("message received", str(msg.payload.decode("utf-8")))
        print("message Topic= ", msg.topic)
        #setLed(data)
    if "GAS_STATE" in data:
        print("message received", str(msg.payload.decode("utf-8")))
        print("message Topic= ", msg.topic)
        #setDoor(data)
    if "VENTILATION" in data:
        pass
        #setAlarm(data)
            
   


def signal_handler(sig, frame):
    """Capture Control+C and disconnect from Broker."""
    global buzzer
    global Leds

    #logger.info("You pressed Control + C. Shutting down, please wait...")

    client.disconnect() # Graceful disconnection.
    Leds[0].off()
    Leds[1].off()
    buzzer.off()
    sys.exit(0)



def init_mqtt():
    global client
    global CLIENT_ID
    global TOPIC

    # Our MQTT Client. See PAHO documentation for all configurable options.
    # "clean_session=True" means we don"t want Broker to retain QoS 1 and 2 messages
    # for us when we"re offline. You"ll see the "{"session present": 0}" logged when
    # connected.
    client = mqtt.Client(                                                                      # (15)
        client_id=CLIENT_ID,
        clean_session=False)

    # Route Paho logging to Python logging.                                                                    # (16)

    # Setup callbacks
    client.on_connect = on_connect                                                             # (17)
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to Broker.
    client.connect(BROKER_HOST, BROKER_PORT)
    
    #subscribe au file qui a flask
    #client.subscribe(TOPIC, qos=2)



### DEBUT DU SCRIPT ####
if __name__ == '__main__':
    print("program starting..")
    init()
    print("Apres init")
    init_mqtt()
    print("Apres init MQTT")
    try:
        signal.signal(signal.SIGINT, signal_handler)  # Capture Control + C   
        client.loop_forever()
    except KeyboardInterrupt: 
        GPIO.cleanup()
        buzzer.off()
        print ('The end !')