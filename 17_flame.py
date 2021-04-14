#!/usr/bin/env python
import RPi.GPIO as GPIO
from ADCDevice import *
import time

FlamePin_S = 22
adc = ADCDevice()
# Faire une class flame_sensor?
def init():
	global adc
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(FlamePin_S, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(FlamePin_S, GPIO.FALLING, callback=myISR)

	if(adc.detectI2C(0x48)): # Detect the pcf8591.
		adc = PCF8591()
	elif(adc.detectI2C(0x4b)): # Detect the ads7830
		adc = ADS7830()
	else:
		print("No correct I2C address found, \n"
		"Please use command 'i2cdetect -y 1' to check the I2C address! \n"
		"Program Exit. \n");
		exit(-1)
		

def myISR(ev=None):
	print("Flame is detected !")

def loop():
	while True:
		res = adc.analogRead(0) # read ADC value of channel 0
		print('res = ', res)
		time.sleep(0.1)

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt:
		GPIO.cleanup()
		print('The end !')
