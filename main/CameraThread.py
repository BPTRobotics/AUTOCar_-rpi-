import cv2
import numpy as np
from time import sleep
import atexit
from threading import Thread

from FPSCounter import FPSCounter

from Detectors.ColorDetector import ColorDetector

HEADLESS = False
if HEADLESS:
    cv2.imshow = lambda *args: None
    cv2.putText = lambda *args: print(args[1])
    cv2.circle = lambda *args: None
    cv2.rectangle = lambda *args: None

class DecisionMaker:
    def __init__(self):
        
        # Ensure cleanup on exit
        @atexit.register
        def cleanup():
            self.cap.release()
            cv2.destroyAllWindows()
            print("CLEANED UP!")
        self.angle = 90
        self.NearestID = 0
        #self.Detecting()
        Thread(target=self.Detecting,daemon=True).start()
    def Detecting(self):
        ANGLE_RANGE = 180
        CENTER_ANGLE_OFFSET = 90
        TOO_FAR_THRESHOLD = 3000
        NO_DETECTION_TEXT = "NO DETECTION"
        TOO_FAR_TEXT = "TOO FAR"
        RED_COLOR = (0, 0, 255)
        GREEN_COLOR = (0, 255, 0)
        YELLOW_COLOR = (0, 250, 250)
        RED_ID = 1
        GREEN_ID = 2
        
        self.fps_counter = FPSCounter()
        
        # Start video capture
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()
        self.RedCubeDetector = ColorDetector(np.array([162, 152, 43]), np.array([179, 247, 111]))
        self.GreenCubeDetector = ColorDetector(np.array([0, 0, 0]), np.array([0, 0, 0]))

        while True:
            print(self.angle)
            self.fps_counter.update()
            ret, frame = self.cap.read()
            if not ret:
                print('NO CAMERA PICTURE')
                sleep(1)
                continue

            
            # Detect cubes
            red_center_x, red_center_y = self.RedCubeDetector.detect(frame)
            green_center_x, green_center_y = self.GreenCubeDetector.detect(frame)

            center = (0,0)
            isTooFar = False

            # Decision making
            if red_center_x or green_center_x:
                if red_center_x and self.RedCubeDetector.largest_contour_area > self.GreenCubeDetector.largest_contour_area:
                    self.NearestID = RED_ID
                    center = (red_center_x,red_center_y)

                    isTooFar = self.RedCubeDetector.largest_contour_area < TOO_FAR_THRESHOLD
                    self.angle = -(red_center_x / frame.shape[1] * ANGLE_RANGE - CENTER_ANGLE_OFFSET)

                    color = RED_COLOR


                elif green_center_x:
                    self.NearestID = GREEN_ID
                    center = (green_center_x,green_center_y)

                    isTooFar = self.GreenCubeDetector.largest_contour_area < TOO_FAR_THRESHOLD
                    self.angle = green_center_x / frame.shape[1] * ANGLE_RANGE - CENTER_ANGLE_OFFSET
                    
                    color = GREEN_COLOR

                if isTooFar:
                        cv2.putText(frame, TOO_FAR_TEXT, (red_center_x, red_center_y), cv2.FONT_HERSHEY_SIMPLEX, .5, RED_COLOR, 3)
                        self.angle = CENTER_ANGLE_OFFSET
                        self.NearestID = 0
                
                cv2.circle(frame, (center[0], center[1]), 5, color, -1)
                cv2.rectangle(frame,(center[0],0),(0 if self.NearestID==RED_ID else frame.shape[1],frame.shape[0]),color,1)
            else:
                self.angle = CENTER_ANGLE_OFFSET
                cv2.putText(frame, NO_DETECTION_TEXT, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, YELLOW_COLOR, 3)
            
            cv2.putText(frame,f"FPS: {self.fps_counter.fps:.2f}",(0,frame.shape[0]),cv2.FONT_HERSHEY_COMPLEX,1,YELLOW_COLOR,3)

            cv2.imshow("FRAME", frame)

if __name__=='__main__':
    DecisionMaker()
    sleep(10)