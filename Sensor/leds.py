from gpiozero import Device, LED, Buzzer
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Initialize GPIO
Device.pin_factory = PiGPIOFactory()

class My_leds:
    _leds_pins = {"Green":None, "Yellow":None, "Red":None}
    _leds = {"Green":None, "Yellow":None, "Red":None}

    def __init__(self, green_led_pin, yellow_led_pin, red_led_pin):
        self._leds_pins['Green'] = green_led_pin
        self._leds['Green'] = LED(self._leds_pins['Green'])
        self._leds['Green'].off()

        self._leds_pins['Yellow'] = yellow_led_pin
        self._leds['Yellow'] = LED(self._leds_pins['Yellow'])
        self._leds['Yellow'].off()

        self._leds_pins['Red'] = red_led_pin
        self._leds['Red'] = LED(self._leds_pins['Red'])
        self._leds['Red'].off()

    def open_light(self, color_key):
        self._leds[color_key].on()

    def close_light(self, color_key):
        self._leds[color_key].off()
    
    def blink_light(self,color_key):
        self._leds[color_key].blink()

    def destroy(self):
        self._leds['Red'].off()
        self._leds['Yellow'].off()
        self._leds['Green'].off()

if __name__ == '__main__':
    try:
        leds = My_leds(4,17,27)
        leds.open_light('Red');
        leds.destroy()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        print("Program is closing....\n")
        leds.destroy()            