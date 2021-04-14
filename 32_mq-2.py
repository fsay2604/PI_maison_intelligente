#!/usr/bin/env python
from ADCDevice import *
import time

adc = ADCDevice()
# Faire une classe gas_sensor?
def init():
	global adc
	if(adc.detectI2C(0x48)): # Detect the pcf8591.
		adc = PCF8591()
	elif(adc.detectI2C(0x4b)): # Detect the ads7830
		adc = ADS7830()
	else:
		print("No correct I2C address found, \n"
		"Please use command 'i2cdetect -y 1' to check the I2C address! \n"
		"Program Exit. \n");
		exit(-1)

def loop():
	while True:
		res = adc.analogRead(0)
		Gas_concentration = res
		print ('Gas concentration:', Gas_concentration)
		time.sleep(0.1)

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		GPIO.cleanup()
		print ('The end !')
