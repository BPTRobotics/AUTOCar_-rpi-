# Getting the libraries we need
from gpiozero import DistanceSensor
from time import sleep

# Initialize ultrasonic sensor
sensor1 = DistanceSensor(trigger=21, echo=20)
sensor2 = DistanceSensor(trigger=26, echo=19)
sensor3 = DistanceSensor(trigger=16, echo=12)
sensors = [sensor1,sensor2,sensor3]
while True:
	sleep(.1)
	# Get the distance in metres
	for x in range(len(sensors)):
		print(f"s{x+1}: {sensors[x].distance*100:.2f}cm")
	print('\n')