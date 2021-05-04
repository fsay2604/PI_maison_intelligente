#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2018/08/03
########################################################################
from Sensor import PCF8574
from Sensor import Adafruit_LCD1602
 

class lcd:
    mcp = None
    lcd = None
    
    def __init__(self):
        PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
        # Create PCF8574 GPIO adapter.
        try:
            self.mcp = PCF8574.PCF8574_GPIO(PCF8574_address)
        except:
            try:
                self.mcp = PCF8574.PCF8574_GPIO(PCF8574A_address)
            except:
                print ('I2C Address Error !')
                exit(1)
        # Create LCD, passing in MCP GPIO adapter.
        self.lcd = Adafruit_LCD1602.Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=self.mcp)
        self.mcp.output(3,1)     # turn on LCD backlight
        self.lcd.begin(16,2)     # set number of LCD lines and columns 
        
    def set_message(self,msg):
        self.lcd.clear()  
        self.lcd.setCursor(0,0)  # set cursor position
        self.lcd.message(msg)
        





