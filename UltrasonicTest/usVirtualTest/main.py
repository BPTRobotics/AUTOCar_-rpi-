# Getting the libraries we need
from gpiozero import DistanceSensor
import sys
from time import sleep
sys.path.append('/home/RPI/Documents/main/Steering')
from UltrasonicDirectionDecider import *
from Steering import *

# Initialize ultrasonic sensor
s1 = DistanceSensor(trigger=21, echo=20)
s2 = DistanceSensor(trigger=26, echo=19)
s3 = DistanceSensor(trigger=16, echo=12)

motor = Motor(16,18,22,starting_speed=80)
wheel = SteeringWheel()
UltrasonicDirectionDecider = UltrasonicDirectionDecider(s1,s2,s3)
while True:
    speed = UltrasonicDirectionDecider.speedMultiplier*150
    if speed<40:speed = 40
    motor.SetSpeed(speed)
    
    UltrasonicDirectionDecider.printAllSensorValues()
    x,y = UltrasonicDirectionDecider.getDirection()

    angle = 90+-25*x
    wheel.Steer(angle)
    
    if y == 1: motor.forward()
    elif y == -1: motor.backward()
    elif y == 0: motor.stop()
    print(f"X: {x} Y: {y} angle: {angle} speed: {speed}")


    sleep(.1)
'''
sensors = [s1,s2,s3]
wheel = SteeringWheel(11,True)

motor = Motor(16,18,22)
isBack = False
while True:
    motor.SetSpeed(50 )
    #for x in range(len(sensors)):
    #        print(f"s{x+1}: {sensors[x].distance*100:.2f}cm")



    is_back = False

    # Check if any sensor detects an object closer than 10 cm
    for sensor in sensors:
        if sensor.distance < 0.1:
            is_back = True
            #print(sensor, sensor.distance)
            break

    # Determine which sensor detects the furthest distance
    max_sensor = max(sensors, key=lambda sensor: sensor.distance)

    # Determine if the maximum sensor distance differs significantly from s2
   # y = 0 if (s2 != max_sensor and (max_sensor.distance - s2.distance) > 0.3) else 1

    # Determine direction based on the sensor with the maximum distance
    if max_sensor == s1:
        x = 1
    elif max_sensor == s2:
        x = 0
    elif max_sensor == s3:
        x = -1

    # Set motor speed and direction
    if not is_back:
        motor.forward()
        if s2 == 1:
            x=0
            continue
    else:
        motor.backward()
        x *= -1  # Reverse the direction when moving backward

    # Adjust steering direction
    if x == 1:
        wheel.Steer_duty(9)
    elif x == -1:
        wheel.Steer_duty(5)
    else:
        wheel.Steer_duty(7)

    print(f"ISBACK: {isBack}  X-Direction: {x} s1:{s1.distance*100:.2f} s2:{s2.distance*100:.2f} s3:{s3.distance*100:.2f}")

    '''
