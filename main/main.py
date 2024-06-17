#from Detectors.AIDetector import AICubeDetector
from Detectors.ColorDetector import ColorDetector
import numpy as np
import Steering
import cv2
import atexit
from time import time,sleep



def main():
    SteeringWheel = Steering.SteeringWheel()
    #CubeDetector = AICubeDetector('best_full_integer_quant_edgetpu.tflite')
    RedCubeDetector = ColorDetector(np.array([133, 156, 0]), np.array([179, 255, 255]))
    GreenCubeDetector = ColorDetector(np.array([0, 147, 0]), np.array([95, 255, 83]))
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    @atexit.register
    def cleanup():
        cap.release()
        cv2.destroyAllWindows()
        print("CLEANED UP!")
    
    while True:
        ret,frame=cap.read()
        sweetspot = int((0.5*frame.shape[1]))
        if not ret:
            print('NO CAMERA PICTURE')
            sleep(1)
            continue
        
        red_center_x, red_center_y = RedCubeDetector.detect(frame)


        cv2.line(frame, (sweetspot,0), (sweetspot,frame.shape[0]), (255,0,0), 3)
        if red_center_x:
            SteeringWheel.Steer(-(red_center_x/frame.shape[1]*180-90))
            cv2.circle(frame, (red_center_x,red_center_y), 5, (0,0,255), -1)
        else:
            SteeringWheel.Steer(90)
        cv2.imshow("",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break


















































if __name__=='__main__':
    main()
