import board
import adafruit_tcs34725
i2c = board.I2C()
from time import sleep

def main():
    try:
        sensor = adafruit_tcs34725.TCS34725(i2c)
        print('Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes))
        print('Temperature: {0}K'.format(sensor.color_temperature))
        print('Lux: {0}'.format(sensor.lux))
        exit()
    except ValueError as e:
        print("error","retrying")
        sleep(.5)
        main()

main()
