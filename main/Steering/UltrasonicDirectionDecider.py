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
        self.isBack = False
        # Check if any sensor detects an object closer than 10 cm
        for sensor in self.sensors:
            if sensor.distance < 0.07:
                self.isBack = True
                break

        # Determine which sensor detects the furthest distance
        max_sensor = max(self.sensors, key=lambda sensor: sensor.distance)
        self.speedMultiplier = max_sensor.distance
        x,y=0,1

        if max_sensor == self.left_sensor:
            x = 1
        elif max_sensor == self.middle_sensor:
            x = 0
        elif max_sensor == self.right_sensor:
            x = -1

        if self.middle_sensor != max_sensor and (max_sensor.distance - self.middle_sensor.distance) > 0.5:
            x*=2
        
        if self.isBack:
            x *= -1
            y *= -1
        #elif self.middle_sensor.distance == 1:
        #    x,y=0,1
        return x,y
    def printAllSensorValues(self):
        for x in range(len(self.sensors)):
            print(f"sensor{x}: {self.sensors[x].distance*100:.2f}cm")