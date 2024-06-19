# Getting the libraries we need
from gpiozero import DistanceSensor
from time import sleep

# Initialize ultrasonic sensor
sensor = DistanceSensor(trigger=18, echo=24)

while True:
	# Wait 2 seconds
	sleep(.5)
	
	# Get the distance in metres
	distance = sensor.distance
	print(f"Distance: {(distance*100):.3}cm ",flush=True,end='\r')