from time import sleep
import Steering.Steering
import Steering.UltrasonicDirectionDecider
from ColorSensor import *
import os

from gpiozero import DistanceSensor


import CameraThread


SPEED = 100
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'



def main():
    # Initialize detectors and steering wheel

    SteeringWheel = Steering.Steering.SteeringWheel(MAX_degree = 170,MIN_degree = 10)
    UltrasonicDirectionDecider = Steering.UltrasonicDirectionDecider.UltrasonicDirectionDecider(DistanceSensor(trigger=21, echo=20),DistanceSensor(trigger=26, echo=19),DistanceSensor(trigger=16, echo=12))

    Motor = Steering.Steering.Motor(16,18,22,starting_speed = SPEED)
    ColorSensor = ColorSensor(60)
    DecisionMaker = CameraThread.DecisionMaker()
    DecisionMaker.TOO_FAR_THRESHOLD = 3000
    sleep(3)
    #INIT CAMERA    
    while DecisionMaker.thread.is_alive():

        direction_x,direction_y = UltrasonicDirectionDecider.getDirection()
        #UltrasonicDirectionDecider.printAllSensorValues()
        #print(direction_x,direction_y)
        #   Motor.SetSpeed(0)
        #print(f"SPEED: {UltrasonicDirectionDecider.speedMultiplier*100*2}")
        if direction_y != -1 and DecisionMaker.NearestID!=0:
            if DecisionMaker.NearestID == DecisionMaker.RED_ID:
                angle = 180-(DecisionMaker.angle*90)
            elif DecisionMaker.NearestID == DecisionMaker.GREEN_ID:
                angle = DecisionMaker.angle*102
            SteeringWheel.Steer(angle)
            direction_y *= .75
            
            print(f"CAMERA Direction: {DecisionMaker.angle:.2f} ANGLE: {angle:.2f} DISTANCE: {DecisionMaker.NearestObjectDistance:.2f} ID: {DecisionMaker.NearestID} FPS: {DecisionMaker.fps_counter.fps:.2f}")
        else:
            angle = 102+direction_x*17.5
            SteeringWheel.Steer(angle)
            #print(f"Direction: {angle} X: {direction_x}")
            #print("GOING BY US")
        #print(DecisionMaker.NearestID)

        Motor.SetSpeed(SPEED*abs(direction_y))
        if direction_y > 0:
            Motor.forward()
        elif direction_y < 0:
            Motor.SetSpeed(50)
            Motor.backward()
        else:
            Motor.stop()
        sleep(.01)
            




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exited with keyboard")
        exit()
