import cv2

class ColorDetector:
    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self.largest_cnt = None

    def detect(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour_area = 0
        self.largest_cnt = None

        for cnt in contours:
            contour_area = cv2.contourArea(cnt)
            if contour_area > largest_contour_area and contour_area > 1000:
                largest_contour_area = contour_area
                self.largest_cnt = cnt

        center_x = None
        center_y = None
        if self.largest_cnt is not None:
            x, y, w, h = cv2.boundingRect(self.largest_cnt)
            center_x = int(x + w / 2)
            center_y = int(y + h / 2)

        return center_x, center_y
    

