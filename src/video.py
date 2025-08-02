#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time, queue
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cv2
import numpy as np

class Video(QObject):
    refreshVideoImgSignal = pyqtSignal()
    refreshVideoImgArraySignal = pyqtSignal()
    def __init__(self, fileName):
        super().__init__() 
        self.image = QImage()
        self.imageArray = np.array([]) 
        self.imageQueue = queue.Queue(maxsize = 5) 
        self.imageArrayQueue = queue.Queue(maxsize = 5) 
        self.refreshImageArrayCounter = 380
        
        self.fileName = fileName
        self.cap = cv2.VideoCapture(self.fileName)
        self.getVideoParam()
        
        print("Reading video:", self.fileName)
        print("Resolution:", self.height, self.width)
        
        self.videoTimer = Timer()    
        self.videoTimer.timeOutSignal.connect(self.getVideoImg)
        
        
    def getVideoParam(self):
        """Get video parameters"""
        # x,y = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),   
        # int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        
        
        if self.cap.isOpened():
            ret, frame= self.cap.read()      
            frame = cv2.resize(frame,(640,480),interpolation=cv2.INTER_CUBIC)
            self.height, self.width, self.bytesPerComponent = frame.shape             
            self.bytesPerLine = self.bytesPerComponent * self.width
            print(self.width, self.height, self.bytesPerLine)
            return self.width, self.height

    def getVideoImg(self):  
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame,(640,480),interpolation=cv2.INTER_CUBIC)
                self.imageArray = frame 
                if self.imageArrayQueue.full():
                    self.imageArrayQueue.get()
                self.imageArrayQueue.put(self.imageArray) 
                self.refreshImageArrayCounter = self.refreshImageArrayCounter + 1
                if self.refreshImageArrayCounter >= 400:
                    self.refreshImageArrayCounter = 0  
                    self.refreshVideoImgArraySignal.emit()                
                # Convert color space order
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
                # Convert to QImage object
                self.image = QImage(frame.data, self.width, self.height, self.bytesPerLine, QImage.Format_RGB888) 
                if self.imageQueue.full():
                    self.imageQueue.get()
                self.imageQueue.put(self.image)
                self.refreshVideoImgSignal.emit()
       
class Timer(QThread):
    """Timer thread"""
    timeOutSignal = pyqtSignal()
    def __init__(self, parent=None):
        super(Timer, self).__init__(parent)
        self.stopedFlag = False
        self.mutex = QMutex()
        
    def run(self):
        with QMutexLocker(self.mutex):
            self.stopedFlag= False
        while True:
            if self.stopedFlag:
                return
            self.timeOutSignal.emit()
            # Send signal every 40ms, 25 frames
            time.sleep(0.1)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopedFlag= True

    def isStoped(self):
        with QMutexLocker(self.mutex):
            return self.stopedFlag