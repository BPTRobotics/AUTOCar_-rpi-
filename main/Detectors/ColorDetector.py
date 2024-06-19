import cv2
from time import time
import numpy as np
class ColorDetector:
    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self.largest_cnt = None

    def detect(self, img,contour_size_threshold=1000):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.largest_contour_area = 0
        self.largest_cnt = None

        for cnt in contours:
            contour_area = cv2.contourArea(cnt)
            if contour_area > self.largest_contour_area and contour_area > contour_size_threshold:
                self.largest_contour_area = contour_area
                self.largest_cnt = cnt

        center_x = None
        center_y = None
        if self.largest_cnt is not None:
            x, y, w, h = cv2.boundingRect(self.largest_cnt)
            center_x = int(x + w / 2)
            center_y = int(y + h / 2)

        return center_x, center_y
    

if __name__=='__main__':
    detector = ColorDetector(np.array([133, 156, 0]), np.array([179, 255, 255]))
    print("BENCHMARKING it'll take ~10 sec")
    img = cv2.imread('input.webp')

    count = 0

    startTime = time()
    while time()-startTime<10:
        detector.detect(img)
        count += 1
        
    print(f"{count} operation/10s")
    print(f'{count/10} fps')
    print(f'{1/(count/10)} ms')