import cv2
import numpy as np
from time import sleep
import atexit
from threading import Thread

from FPSCounter import FPSCounter

from Detectors.ColorDetector import ColorDetector

HEADLESS = True
if HEADLESS:
    cv2.imshow = lambda *args: None
    cv2.putText = lambda *args: None#print(args[1])
    cv2.circle = lambda *args: None
    cv2.rectangle = lambda *args: None

class DecisionMaker:
    def __init__(self,onThread=True):
        
        # Ensure cleanup on exit
        @atexit.register
        def cleanup():
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
            print("CLEANED UP!")
        self.angle = 90
        self.cap = None
        self.NearestID = 0
        self.NearestObjectDistance = 9999999999
        #self.Detecting()
        
        self.RED_ID = 1
        self.GREEN_ID = 2
        self.TOO_FAR_THRESHOLD = 3000
        self.fps_counter = None
        if onThread:
            Thread(target=self.Detecting,daemon=True).start()
        else:
            self.Detecting()

    def Detecting(self):
        if not HEADLESS:
            NO_DETECTION_TEXT = "NO DETECTION"
            TOO_FAR_TEXT = "TOO FAR"
            RED_COLOR = (0, 0, 255)
            GREEN_COLOR = (0, 255, 0)
            YELLOW_COLOR = (0, 250, 250)
        self.fps_counter = FPSCounter()
        
        # Start video capture
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()
        self.RedCubeDetector = ColorDetector(np.array([118, 53, 109]), np.array([179, 255, 245]))
        self.GreenCubeDetector = ColorDetector(np.array([69, 76, 25]), np.array([94, 255, 187]))

        while True:
            #print(self.angle)
            self.fps_counter.update()
            #print(f"{self.fps_counter.fps}fps")
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
                    self.NearestID = self.RED_ID
                    center = (red_center_x,red_center_y)
                    self.NearestObjectDistance = self.RedCubeDetector.largest_contour_area
                    isTooFar = self.NearestObjectDistance < self.TOO_FAR_THRESHOLD
                    self.angle = red_center_x / frame.shape[1]
                    if not HEADLESS:
                        color = RED_COLOR


                elif green_center_x:
                    self.NearestID = self.GREEN_ID
                    center = (green_center_x,green_center_y)
                    self.NearestObjectDistance = self.GreenCubeDetector.largest_contour_area
                    isTooFar = self.NearestObjectDistance < self.TOO_FAR_THRESHOLD
                    self.angle = green_center_x / frame.shape[1] 
                    if not HEADLESS:
                        color = GREEN_COLOR

                if isTooFar:
                        if not HEADLESS:cv2.putText(frame, TOO_FAR_TEXT, (red_center_x, red_center_y), cv2.FONT_HERSHEY_SIMPLEX, .5, RED_COLOR, 3)
                        self.angle = .5
                        self.NearestID = 0
                if not HEADLESS:
                    cv2.circle(frame, (center[0], center[1]), 5, color, -1)
                    cv2.rectangle(frame,(center[0],0),(0 if self.NearestID==self.RED_ID else frame.shape[1],frame.shape[0]),color,1)
            else:
                self.NearestID = 0
                self.angle = .5
                if not HEADLESS: cv2.putText(frame, NO_DETECTION_TEXT, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, YELLOW_COLOR, 3)
            
            if not HEADLESS: cv2.putText(frame,f"FPS: {self.fps_counter.fps:.2f}",(0,frame.shape[0]),cv2.FONT_HERSHEY_COMPLEX,1,YELLOW_COLOR,3)

            if not HEADLESS: cv2.imshow("FRAME", frame)

if __name__=='__main__':
    dm = DecisionMaker()
    dm.TOO_FAR_THRESHOLD = 3000
    while True:
        print(f"ANGLE: {dm.angle} DetectionID: {dm.NearestID} Distance: {dm.NearestObjectDistance}")
        sleep(.1)