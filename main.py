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
BROKER_HOST = '192.168.137.213'                                                                       # (2)
BROKER_PORT = 1883
CLIENT_ID = "SYS_ALARME"                                                                         # (3)
TOPIC = "SENSORS" 
TOPIC_PUB = "MAINBOARD_WEB"  
TOPIC_SUB = "MAINBOARD"                                                                                # (4)
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
fire_state = { 'flame_state' : 'off' }
gas_state = { 'gas_state' : 'off' }
ventilation_state = {'ventilation' : 'off'}
previous_ventilation_state = 'off'
alarm_state = {'alarm' : 'off'}

def button_pressed():
    global alarm_state
    if alarm_state['alarm'] == 'on':
        alarm_state['alarm'] = 'off'
    elif alarm_state['alarm'] == 'off':
        alarm_state['alarm'] = 'on'
    client.publish(TOPIC_SUB,json.dumps(alarm_state))  
    client.publish(TOPIC_PUB,json.dumps(alarm_state))
    


# Functions
def init():
    global Leds
    global ButtonState
    global buzzer
    global ventilation
    lcd.set_message("Alarm active.")
    
    Leds[0] = LED(16) # Red
    Leds[0].on()
    Leds[1] = LED(21) # Green
    Leds[1].off()
   
    ButtonState = Button(ButtonPin, pull_up=True, bounce_time=0.1)
    ButtonState.when_pressed = button_pressed

    buzzer = Buzzer(BuzzerPin,active_high = False)
    buzzer.off()

# Fonction qui gere les receptions de messages 
def logic():
    global fire_state
    global gas_state
    global ventilation_state
    global previous_ventilation_state
    global alarm_state
    

    global buzzer
    global Leds 
    global ventilation
    global lcd


    if previous_ventilation_state != ventilation_state['ventilation'] :
        if ventilation_state['ventilation'] == 'on':
            ventilation.move(0.25)  # part la ventilation
            previous_ventilation_state = 'on'
        elif ventilation_state['ventilation'] == 'off':
            ventilation.move(0)
            previous_ventilation_state = 'off'

    # Si l'alarme est active
    if alarm_state['alarm'] == 'on':
        Leds[1].on()
        # Verifie si l'alarme doit partir en fonction des states
        
        
        if fire_state['flame_state'] or gas_state['gas_state'] == 'on':
            buzzer.on()     # part l'alarme
            Leds[0].blink() # set la lumiere rouge a blink pour signifier un probleme
            lcd.set_message("Alarm active \n and triggered!")

            # Part la ventilation si le gas est detecté
            if gas_state['gas_state'] == 'on':
                ventilation_state['ventilation'] = 'on'
                if previous_ventilation_state != ventilation_state['ventilation'] : 
                    if ventilation_state['ventilation'] == 'off':
                        ventilation.move(0.25)  # part la ventilation
                        previous_ventilation_state = 'on'
                    else:
                        ventilation.move(0) # Ferme la ventilation
                        previous_ventilation_state = 'off'
            
            if fire_state['flame_state'] == 'on':
                time.sleep(5)
                fire_state['flame_state'] = 'off'
                client.publish(TOPIC_PUB,json.dumps(fire_state))

        #  Reinitilise les composants
        if fire_state['flame_state'] and gas_state['gas_state'] == 'off':
            buzzer.off()    # Ferme l'alarme
            Leds[0].off()   # Ferme la led rouge
            Leds[1].on()    # Allume la led verte
            ventilation.move(0) # Ferme la ventilation
            previous_ventilation_state = 'off'
            lcd.set_message("Alarm active.")
    else:
        Leds[0].on()
        Leds[1].off()
        lcd.set_message("Alarm inactive.")
    time.sleep(0.2)

"""
MQTT Related Functions and Callbacks
"""
def on_connect(client, user_data, flags, connection_result_code):
    """on_connect is called when our program connects to the MQTT Broker.
       Always subscribe to topics in an on_connect() callback.
       This way if a connection is lost, the automatic
       re-connection will also results in the re-subscription occurring."""

    # Subscribe to the topic 
    client.subscribe(TOPIC, qos=0)   # Recevoir les donnees des sensors
    client.subscribe(TOPIC_SUB, qos=0)   # Recevoir les donnees du web


def on_disconnect(client, user_data, disconnection_result_code):                         
    """Called disconnects from MQTT Broker."""
    pass


def on_message(client, userdata, msg):
    """Callback called when a message is received on a subscribed topic."""
    global fire_state
    global gas_state
    global ventilation_state
    global alarm_state

    data = None
        
    data = json.loads(msg.payload.decode("UTF-8"))

    if "VENTILATION" in data:
        # Gestion du state de la ventilation
        if data['VENTILATION'] == 'on':
            ventilation_state['ventilation'] = 'on'
        if data['VENTILATION'] == 'off':
            ventilation_state['ventilation'] = 'off'
            
        client.publish(TOPIC_PUB,json.dumps(ventilation_state))
        
    if "ALARM" in data:
        # Gestion du state du systeme d'alarme
        if data['ALARM'] == 'on':
            alarm_state['alarm'] = 'on'
        if data['ALARM'] == 'off':
            alarm_state['alarm'] = 'off'
        client.publish(TOPIC_PUB,json.dumps(alarm_state))
        
        
    if alarm_state['alarm'] == 'on':
        if "FLAME_STATE" in data:
            #print("message received", str(msg.payload.decode("utf-8")))
            #print("message Topic= ", msg.topic)
            # Gestion du state de la ventilation
            if data['FLAME_STATE'] == 'on':
                fire_state['flame_state'] = 'on'
            if data['FLAME_STATE'] == 'off':
                fire_state['flame_state'] = 'off'
            
            client.publish(TOPIC_PUB,json.dumps(fire_state))


        if "GAS_STATE" in data:
            #print("message received", str(msg.payload.decode("utf-8")))
            #print("message Topic= ", msg.topic)
            # Gestion du state de la ventilation
            if data['GAS_STATE'] == 'on':
                gas_state['gas_state'] = 'on'
            if data['GAS_STATE'] == 'off':
                gas_state['gas_state'] = 'off'
            
            
            client.publish(TOPIC_PUB,json.dumps(gas_state))




           



        # Gestion de la logique en fonction des states
        
        
        #print(data)
    logic()


def signal_handler(sig, frame):
    """Capture Control+C and disconnect from Broker."""
    global buzzer
    global Leds

    #logger.info("You pressed Control + C. Shutting down, please wait...")

    client.disconnect() # Graceful disconnection.
    Leds[0].off()
    Leds[1].off()
    buzzer.off()
    GPIO.cleanup()
    #sys.exit(0)



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

init()
init_mqtt()

### DEBUT DU SCRIPT ####
if __name__ == '__main__':
    print("program starting..")

    signal.signal(signal.SIGINT, signal_handler)  # Capture Control + C   
    client.loop_forever()
    signal.pause()
