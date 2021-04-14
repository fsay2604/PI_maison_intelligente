from gpiozero import Device, Motor, OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory

class ventilation:
    # defining variables
    MOTOR_PINS = [23, 24]
    ENABLE_PIN = 18
    motor = None
    
    def __init__(self):
        self.motor = Motor(forward=self.MOTOR_PINS[1], backward=self.MOTOR_PINS[0],enable=self.ENABLE_PIN,pwm=True)
        self.motor.stop()
        pass
    
    def move(self,speed=0):
        if(speed==0):
            self.motor.stop()
        elif(speed >0):
            self.motor.forward(speed)
        elif(speed < 0):
            speed = speed*-1
            self.motor.backward(speed)
    