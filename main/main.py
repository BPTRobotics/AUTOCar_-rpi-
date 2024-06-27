from time import sleep
import Steering.Steering
import Steering.UltrasonicDirectionDecider

from gpiozero import DistanceSensor


import CameraThread


SPEED = 0




def main():
    # Initialize detectors and steering wheel

    SteeringWheel = Steering.Steering.SteeringWheel(MAX_degree = 170,MIN_degree = 10)
    UltrasonicDirectionDecider = Steering.UltrasonicDirectionDecider.UltrasonicDirectionDecider(DistanceSensor(trigger=21, echo=20),DistanceSensor(trigger=26, echo=19),DistanceSensor(trigger=16, echo=12))

    Motor = Steering.Steering.Motor(16,18,22,starting_speed = SPEED)

    DecisionMaker = CameraThread.DecisionMaker()
    
    #INIT CAMERA    
    while True:

        direction_x,direction_y = 0,0#UltrasonicDirectionDecider.getDirection()
        #UltrasonicDirectionDecider.printAllSensorValues()
        #print(direction_x,direction_y)
        #   Motor.SetSpeed(0)
        #print(f"SPEED: {UltrasonicDirectionDecider.speedMultiplier*100*2}")
        if direction_y != -1 and DecisionMaker.NearestID!=0:
            #SteeringWheel.Steer(DecisionMaker.angle)
            print(f"CAMERA Direction: {DecisionMaker.angle}")
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
