from ultralytics import YOLO


class AICubeDetector:

    def __init__(self, model_path,**kwargs):
        # Load the YOLO model
        self.model = YOLO(model_path,**kwargs)
        self.box_number = 0
        self.largest_box = None
        self.center = (None,None)
        self.results = None
        self.classID = None
        

    def Detect(self,frame,**kwargs):
        return  self.model.predict(frame,**kwargs)        #args=   imgsz=256, stream=True, verbose=False

    def Get_Largest_Box_Extended(self,boxes):
        largest_area = 0
        largest_box_number = 0
        for i in range(boxes.shape[0]):
            # Extract the coordinates of the box
            x1, y1, x2, y2 = boxes.xyxy[i]
            width = x2 - x1
            height = y2 - y1
            area = width * height

            # Check if this is the largest box so far
            if area > largest_area:
                largest_area = area
                self.largest_box = (x1, y1, x2, y2)
                self.largest_box_number = i

        return self.largest_box_number,self.largest_box

    def Get_Largest_Box(self,*args):
        return self.Get_Largest_Box_Extended(*args)[0]
    
    def Get_Point(self,frame):
        self.results = self.Detect(frame=frame,imgsz=256, stream=True, verbose=False)

        for result in self.results:
            self.box_number,largest_box = self.Get_Largest_Box_Extended(result.boxes)
            if len(result.boxes.cls)!=0:
                self.classID = result.boxes.cls[self.box_number]

        if largest_box is not None:
            x1, y1, x2, y2 = largest_box
            self.center = (int((x1 + x2) / 2),int((y1 + y2) / 2))
        else:
            self.center[0] = frame.shape[1]/2
            
            self.center[1] = frame.shape[0]/2
            
        return self.center