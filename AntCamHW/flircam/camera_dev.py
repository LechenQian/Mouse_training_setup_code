import numpy as np
import cv2

"""This example is a PyDAQmx version of the ContAcq_IntClk.c example
It illustrates the use of callback functions
This example demonstrates how to acquire a continuous amount of
data using the DAQ device's internal clock. It incrementally stores the data
in a Python list.
"""

class CameraDev(object):
    
    def __init__(self,camera_id):
        self.camera_id=camera_id
        self.cap=cv2.VideoCapture(self.camera_id)
        self.fpath=""
        ret,self.frame=self.cap.read()
    
    def open(self):
        self.cap.open(self.camera_id)
    
    def close(self):
        self.cap.release()
    
    def read(self):
        ret,self.frame = self.cap.read()
        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        image = cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return image
    
    def open_file(self,fpath):
        self.fpath=fpath
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(self.fpath,fourcc, 20.0, (640,480))
        
    def write(self):
        self.out.write(cv2.rotate(self.frame, cv2.ROTATE_180))
    
    def close_file(self):
        self.out.release()
