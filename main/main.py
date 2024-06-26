
import cv2
import Steering.Steering
import Steering.UltrasonicDirectionDecider

from gpiozero import DistanceSensor


import CameraThread







def main():
    # Initialize detectors and steering wheel

    SteeringWheel = Steering.Steering.SteeringWheel(MAX_degree = 90+50,MIN_degree = 90-50)
    UltrasonicDirectionDecider = Steering.UltrasonicDirectionDecider.UltrasonicDirectionDecider(DistanceSensor(trigger=21, echo=20),DistanceSensor(trigger=26, echo=19),DistanceSensor(trigger=16, echo=12))

    Motor = Steering.Steering.Motor(16,18,22,starting_speed=80)

    DecisionMaker = CameraThread.DecisionMaker()
    
    #INIT CAMERA
    
    while True:

        direction_x,direction_y = UltrasonicDirectionDecider.getDirection()
        #UltrasonicDirectionDecider.printAllSensorValues()

        if direction_y != -1 and DecisionMaker.NearestID!=0:
            SteeringWheel.Steer(DecisionMaker.angle)
            print(f"CAMERA Direction: {DecisionMaker.angle}")
        else:
            direction_duty = 7.75+direction_x
            SteeringWheel.Steer_duty(direction_duty)
            print(f"Direction: {direction_duty} X: {direction_x}")
            #print("GOING BY US")
        
        
        if direction_y == 1:
            Motor.forward()
        elif direction_y == -1:
            Motor.backward()
        else:
            Motor.stop()
            




if __name__ == '__main__':
    main()
