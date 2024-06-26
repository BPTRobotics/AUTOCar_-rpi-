# Getting the libraries we need
from gpiozero import DistanceSensor
from varname import nameof

class UltrasonicDirectionDecider:
    def __init__(self,left_sensor:DistanceSensor , middle_sensor:DistanceSensor , right_sensor:DistanceSensor):
        
        self.left_sensor = left_sensor
        self.middle_sensor = middle_sensor
        self.right_sensor = right_sensor

        
        self.sensors = [self.left_sensor,self.middle_sensor,self.right_sensor]

        self.isBack = False
        self.speedMultiplier = 1

    def getDirection(self) -> (int, int):

        # Determine which sensor detects the furthest distance
        max_sensor = max(self.sensors, key=lambda sensor: sensor.distance)
        min_sensor = min(self.sensors, key=lambda sensor: sensor.distance)
        self.speedMultiplier = min_sensor.distance
        x,y=0,1
        if min_sensor.distance < .1:
            if min_sensor == self.left_sensor:
                x = -1
            elif min_sensor == self.middle_sensor:
                x = 0
            elif min_sensor == self.right_sensor:
                x = 1
            y = -1
        else:
            if max_sensor == self.left_sensor:
                x = -1
            elif max_sensor == self.middle_sensor:
                x = 0
            elif max_sensor == self.right_sensor:
                x = 1

        if self.middle_sensor != max_sensor and (max_sensor.distance - self.middle_sensor.distance) > 0.3:
            x*=2
        
        #elif self.middle_sensor.distance == 1:
        #    x,y=0,1
        return x,y
    def printAllSensorValues(self):
        for x in range(len(self.sensors)):
            print(f"sensor{x}: {self.sensors[x].distance*100:.2f}cm")