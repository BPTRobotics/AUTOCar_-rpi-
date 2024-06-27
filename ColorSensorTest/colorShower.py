import tkinter as tk
import random
import time

# Function to update the color of the canvas
def update_color(canvas):
    while True:
        # Simulating RGB values from a sensor
        #rgb = (random.random(), random.random(), random.random())
        
        # Convert RGB to hexadecimal color code
        rgb = sensor.color_rgb_bytes
        hex_color = "#%02x%02x%02x" % rgb
        print(*rgb)
        # Update the canvas color
        canvas.configure(bg=hex_color)
        
        # Update the GUI
        root.update()
        
        # Wait for a short period before the next update
        time.sleep(0.1)

import board
import adafruit_tcs34725
i2c = board.I2C()

sensor = adafruit_tcs34725.TCS34725(i2c)
# Create the main window
root = tk.Tk()
root.title("Real-time Color Display")

# Create a canvas to display the color
canvas = tk.Canvas(root, width=200, height=200)
canvas.pack()

# Start the color update loop
print(sensor.color_rgb_bytes)
update_color(canvas)

# Run the Tkinter event loop
root.mainloop()
