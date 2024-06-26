import RPi.GPIO as GPIO
import time
def remap(v, a, b, c, d):
       return (v-a) / (b-a) * (d-c) + c
    
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50)

servo1.start(7)
duty=0
isOne = False
starttime = time.time()
try:
    while True:
        servo1.ChangeDutyCycle(7)
        time.sleep(.1)
except KeyboardInterrupt:
     print(f"\n\nThe test was {time.time()-starttime}s long")
     GPIO.cleanup()
     exit()
try:
    while (duty!=69):
        inp = int(input("Degrees (0-180): "))
        duty=remap(inp,0,180,2,12)
        print(duty,inp)
        servo1.ChangeDutyCycle(duty)
finally:
    print("Exiting")
    servo1.ChangeDutyCycle(7)
