import RPi.GPIO as GPIO
import atexit
from time import sleep
import random
class SteeringWheel:
    def __init__(self,reset_wheel = True):

        @atexit.register
        def cleanup():
            if reset_wheel:
                self.servo1.ChangeDutyCycle(7)
                sleep(.5)
            GPIO.cleanup()
            print("STEERING-MECHANISM CLEANED UP!")

        
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(11,GPIO.OUT)
        self.servo1 = GPIO.PWM(11,50)

        self.servo1.start(7)

        self.Direction = 90

        self.MAX_degree = 150
        self.MIN_degree = 30
    #érték -90 és +90 között
    @staticmethod
    def remap(v):
        return v / 18 + 2

    def Steer_duty(self,duty):
        self.servo1.ChangeDutyCycle(duty)

    def Steer(self,degrees,lock=True):
        print("Steer:",degrees)
        if degrees==self.Direction: return
        if lock:
            if degrees > self.MAX_degree: degrees = self.MAX_degree
            elif degrees < self.MIN_degree  : degrees = self.MIN_degree
        
        self.Direction = degrees
        self.Steer_duty(SteeringWheel.remap(degrees))

if __name__=='__main__':
    SteeringWheel().Steer_duty(7)


        
    
