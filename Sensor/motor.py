from gpiozero import Device, Motor, OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# defining variables
MOTOR_PINS = [23, 24]
ENABLE_PIN = 18
motor = None

# Initialize GPIO
Device.pin_factory = PiGPIOFactory()

# Function Definitions
def init():
    global motor
    motor = Motor(forward=MOTOR_PINS[1], backward=MOTOR_PINS[0],enable=ENABLE_PIN,pwm=True)
    motor.stop()
    
def loop(speed=0):
    global motor
    if(speed==0):
        motor.stop()
    elif(speed >0):
        motor.forward(speed)
    elif(speed < 0):
        speed = speed*-1
        motor.backward(speed)


def get_motor_value():
    global motor
    return motor.value

def destroy():
    global motor
    motor.stop()

