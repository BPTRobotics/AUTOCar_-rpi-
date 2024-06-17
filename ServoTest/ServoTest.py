import RPi.GPIO as GPIO
import time
def remap(v, a, b, c, d):
       return (v-a) / (b-a) * (d-c) + c
    
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50)

servo1.start(0)
duty=0
try:
    while (duty!=69):
        inp = int(input("Degrees (0-180): "))
        duty=remap(inp,0,180,2,12)
        print(duty,inp)
        servo1.ChangeDutyCycle(duty)
finally:
    print("Exiting")
    servo1.ChangeDutyCycle(7)
