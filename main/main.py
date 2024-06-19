from Detectors.ColorDetector import ColorDetector
import numpy as np
import Steering
import cv2
import atexit
from time import sleep
from FPSCounter import FPSCounter
fps_counter = FPSCounter()


def main():
    # Initialize detectors and steering wheel
    RedCubeDetector = ColorDetector(np.array([133, 156, 0]), np.array([179, 255, 255]))
    GreenCubeDetector = ColorDetector(np.array([25, 147, 0]), np.array([95, 255, 83]))
    SteeringWheel = Steering.SteeringWheel(False)
    SteeringWheel.MAX_degree = 90+50
    SteeringWheel.MIN_degree = 90-50


    # Start video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # Ensure cleanup on exit
    @atexit.register
    def cleanup():
        cap.release()
        cv2.destroyAllWindows()
        print("CLEANED UP!")
    
    while True:
        fps_counter.update()
        ret, frame = cap.read()
        if not ret:
            print('NO CAMERA PICTURE')
            sleep(1)
            continue

        # Constants
        ANGLE_RANGE = 180
        CENTER_ANGLE_OFFSET = 90
        TOO_FAR_THRESHOLD = 3000
        NO_DETECTION_TEXT = "NO DETECTION"
        TOO_FAR_TEXT = "TOO FAR"
        RED_COLOR = (0, 0, 255)
        GREEN_COLOR = (0, 255, 0)
        YELLOW_COLOR = (0, 250, 250)

        # Detect cubes
        red_center_x, red_center_y = RedCubeDetector.detect(frame)
        green_center_x, green_center_y = GreenCubeDetector.detect(frame)

        # Decision making
        if red_center_x or green_center_x:
            if red_center_x and (RedCubeDetector.largest_contour_area > GreenCubeDetector.largest_contour_area):
                angle = -(red_center_x / frame.shape[1] * ANGLE_RANGE - CENTER_ANGLE_OFFSET)
                cv2.circle(frame, (red_center_x, red_center_y), 5, RED_COLOR, -1)

                if RedCubeDetector.largest_contour_area < TOO_FAR_THRESHOLD:
                    cv2.putText(frame, TOO_FAR_TEXT, (red_center_x, red_center_y), cv2.FONT_HERSHEY_SIMPLEX, .5, RED_COLOR, 3)
                    SteeringWheel.Steer(CENTER_ANGLE_OFFSET)

            elif green_center_x:
                angle = green_center_x / frame.shape[1] * ANGLE_RANGE - CENTER_ANGLE_OFFSET
                cv2.circle(frame, (green_center_x, green_center_y), 5, GREEN_COLOR, -1)

                if GreenCubeDetector.largest_contour_area < TOO_FAR_THRESHOLD:
                    cv2.putText(frame, TOO_FAR_TEXT, (green_center_x, green_center_y), cv2.FONT_HERSHEY_SIMPLEX, .5, GREEN_COLOR, 3)
                    SteeringWheel.Steer(CENTER_ANGLE_OFFSET)
            
            SteeringWheel.Steer(angle)
        else:
            SteeringWheel.Steer(CENTER_ANGLE_OFFSET)
            cv2.putText(frame, NO_DETECTION_TEXT, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, YELLOW_COLOR, 3)
        cv2.putText(frame,f"FPS: {fps_counter.fps:.2f}",(0,frame.shape[0]),cv2.FONT_HERSHEY_COMPLEX,1,YELLOW_COLOR,3)

        # Show the frame
        cv2.imshow("FRAME", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
