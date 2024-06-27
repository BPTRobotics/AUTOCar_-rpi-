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
        
    
    def printAllSensorValues(self):
        for x in range(len(self.sensors)):
            if x==0:
                sensor="LEFT_SENSOR"
            elif x==1:
                sensor="MIDDLE_SENSOR"
            elif x==2:
                sensor=="RIGHT_SENSOR"
            print(f"{sensor}: {self.sensors[x].distance*100:.2f}cm")
    
    def getDirection(self) -> (int, int):

        # Determine which sensor detects the furthest distance
        max_sensor = max(self.sensors, key=lambda sensor: sensor.distance)
        min_sensor = min(self.sensors, key=lambda sensor: sensor.distance)
        self.speedMultiplier = min_sensor.distance
        x,y=0,1
    
        if max_sensor == self.left_sensor:
            x = 1
            y=.75
        elif max_sensor == self.middle_sensor:
            x = 0
            y=1
        elif max_sensor == self.right_sensor:
            x = -1
            y=.75
       
        if min_sensor.distance < .25:
            if(min_sensor.distance<.125):
                y = -.5
                x*=-1
            else:
                y = .75
                x *= 3

        elif self.middle_sensor.distance == 1:
           x,y=0,1.5
        
        if max_sensor.distance-self.middle_sensor.distance>.5 :
            x*=2

        return x,y
