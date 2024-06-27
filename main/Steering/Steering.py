import RPi.GPIO as GPIO
import atexit
from time import sleep

class SteeringWheel:
    def __init__(self,PORT=11,MAX_degree=170,MIN_degree=0):

        @atexit.register
        def cleanup():
            self.servo1.stop()
            GPIO.cleanup()
            print("STEERING-MECHANISM CLEANED UP!")

        
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(PORT,GPIO.OUT)
        self.servo1 = GPIO.PWM(PORT,50)

        self.servo1.start(0)

        self.Direction = 90

        self.MAX_degree = MAX_degree
        self.MIN_degree = MIN_degree
        

    @staticmethod
    def remap(v):
        return v / 18 + 2

    def Steer_duty(self,duty):
        #if duty>12 or duty<0:
        #    raise Exception(f"DUTY CANT BE GREATER THAT 12, nor less than 0. DUTY: {duty}")
        self.servo1.ChangeDutyCycle(duty)

    def Steer(self,degrees,lock=True):
        #print("Steer:",degrees)
        if degrees==self.Direction: return
        if lock:
            if degrees > self.MAX_degree: degrees = self.MAX_degree
            elif degrees < self.MIN_degree  : degrees = self.MIN_degree
        
        self.Direction = degrees
        self.Steer_duty(SteeringWheel.remap(degrees))

class Motor:
    def __init__(self,in1:int,in2:int,en:int,starting_speed = 0):
        # Define GPIO pins
        self.in1 = in1 #original pin: 24
        self.in2 = in2 #original pin: 23
        self.en  = en  #original pin: 25

        # Setup GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.en, GPIO.OUT)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

        self.__Speed = starting_speed

        # Setup PWM
        self.p = GPIO.PWM(self.en, 1000)
        self.p.start(self.__Speed)
        self.SetSpeed(starting_speed)


    def backward(self):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
    def forward(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

    def SetSpeed(self,speed):
        if speed>100:speed=100
        elif speed<0:speed = 0
        self.__Speed = speed
        self.p.ChangeDutyCycle(speed)
    def GetSpeed(self):
        return self.__Speed
    

def TEST():
    motor = Motor(16,18,22,starting_speed=35)
    while True:
        motor.forward()
if __name__=='__main__':
    wheel = SteeringWheel()
    from threading import Thread
    Thread(target=TEST).start()
    while True:
        wheel.Steer(int(input('Steerng direction: ')))
    

    #motor = Motor(16,18,22,starting_speed=50)
    #motor.forward()
    #sleep(3)

        
    
