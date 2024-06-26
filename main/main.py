from time import sleep
import cv2
import Steering.Steering
import Steering.UltrasonicDirectionDecider

from gpiozero import DistanceSensor


import CameraThread







def main():
    # Initialize detectors and steering wheel

    SteeringWheel = Steering.Steering.SteeringWheel(MAX_degree = 170,MIN_degree = 10)
    UltrasonicDirectionDecider = Steering.UltrasonicDirectionDecider.UltrasonicDirectionDecider(DistanceSensor(trigger=21, echo=20),DistanceSensor(trigger=26, echo=19),DistanceSensor(trigger=16, echo=12))

    Motor = Steering.Steering.Motor(16,18,22)

    DecisionMaker = CameraThread.DecisionMaker()
    
    #INIT CAMERA
    
    while True:

        direction_x,direction_y = UltrasonicDirectionDecider.getDirection()
        #UltrasonicDirectionDecider.printAllSensorValues()
        Motor.SetSpeed(70)
        #print(f"SPEED: {UltrasonicDirectionDecider.speedMultiplier*100*2}")
        if direction_y != -1 and DecisionMaker.NearestID!=0:
            SteeringWheel.Steer(DecisionMaker.angle)
            print(f"CAMERA Direction: {DecisionMaker.angle}")
        else:
            direction_duty = 9.7+direction_x
            SteeringWheel.Steer_duty(direction_duty)
            print(f"Direction: {direction_duty} X: {direction_x}")
            #print("GOING BY US")
        print(DecisionMaker.NearestID)
        
        
        if direction_y == 1:
            Motor.forward()
        elif direction_y == -1:
            Motor.SetSpeed(50)
            Motor.backward()
        else:
            Motor.stop()
        print(Motor.GetSpeed())
            




if __name__ == '__main__':
    main()
