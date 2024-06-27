import board
import adafruit_tcs34725
from time import sleep
from threading import Thread

i2c = board.I2C()

class ColorSensor:
    def __init__(self,red_threshold,isThreading = True):
        self.sensor = adafruit_tcs34725.TCS34725(i2c)
        self.wasRed = False
        self.red_threshold = red_threshold
        if isThreading:
            Thread(target=self.Detecting(),daemon=True)
    def Detecting(self):
        while True:
            if self.GetIfWentThorugh(self.sensor[0]):
                print("\n"*3,"IT WENT THROUGH!!!","\n"*3)
    def GetIfWentThorugh(self,red_threshold) -> bool:
        if red_threshold>self.red_threshold:
            self.wasRed = True
        elif self.wasRed:
            return True
        return False