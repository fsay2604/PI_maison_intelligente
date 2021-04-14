#!/usr/bin/env python

##########################################################################
# Auteurs:  Francois Charles Hebert & Samuel Fournier
# Classe:	Représente le sensor de flamme.
##########################################################################

import RPi.GPIO as GPIO

class Flame_Sensor:
	FlamePin = None

	# Constructeur
	def __init__(self, FlamePin):
		self.FlamePin = FlamePin
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.FlamePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(self.FlamePin, GPIO.FALLING, callback=self.myISR)

	# Callback qui s'execute lors de la detection de l'event
	def myISR(self,ev=None):
		print("Flame is detected !")

	# Fonction qui lit la valeur et la renvoit.
	def read(self, adc):
		res = adc.analogRead(0) # read ADC value of channel 0
		print('res = ', res)
		return res

