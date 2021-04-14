#!/usr/bin/env python

##########################################################################
# Auteurs:  Francois Charles Hebert & Samuel Fournier
# Classe:	Représente le sensor de gaz. (pour notre détecteur de fumé)
##########################################################################

class Gas_Sensor:
	# Constructeur
	def __init__(self):
    		pass

	# Fonction qui lit la valeur et la renvoit.
	def read(self, adc):
		value = adc.analogRead(0)			# Verifier le channel, probablement a changer! le sensor de flamme est sur le channel 0 aussi.
		print ('Gas concentration:', value)
		return value



