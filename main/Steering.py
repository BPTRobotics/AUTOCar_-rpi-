import RPi.GPIO as GPIO

class SteeringWheel:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(11,GPIO.OUT)
        self.servo1 = GPIO.PWM(11,50)

        self.servo1.start(0)

        self.Direction = 90

    #érték -90 és +90 között
    def remap(self,v):
        return (v + 90) / 180 * 10 + 2

    def Steer_duty(self,duty):
        self.servo1.ChangeDutyCycle(duty)

    def Steer(self,degrees):
        if degrees<0: degrees = 0
        if degrees>180:degrees = 180
        self.Direction = degrees
        self.Steer_duty(self.remap(degrees))
    
