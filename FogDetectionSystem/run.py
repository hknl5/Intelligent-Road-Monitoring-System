#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import cv2
import numpy as np

"""Main function"""
app = QApplication(sys.argv)
app.setApplicationName("Haze Detection")
app.setQuitOnLastWindowClosed(True)

from src import *

if getattr(sys, 'frozen', False):
    rootPath = os.path.dirname(sys.executable)
elif __file__:
    rootPath = os.path.dirname(__file__)  
print("Root directory:", rootPath)


class MainWindow(QMainWindow, QWidget):
    """Main window"""
    def __init__(self):
        super().__init__()  
        self.imageArray = np.array([]) # Matrix for storing images
        self.calcDetectResultThreadRunning = 0 # 1 means thread is running
        self.ui = mainWindowUi.MainWindowUi()
        self.connectSignalSlot()
        self.ui.showUi()
        
    def connectSignalSlot(self):
        """Connect signals and slots"""
        self.ui.openAFrameImageButton.clicked.connect(self.openAFrameImage) 
        self.ui.openVideoButton.clicked.connect(self.openVideo) 
        self.ui.closeVideoButton.clicked.connect(self.closeVideo) 
        self.ui.calcResultButton.clicked.connect(self.startCalcDetectResult) 
        self.ui.openLocalCameraButton.clicked.connect(self.openLocalCamera) 
        self.ui.openWebCameraButton.clicked.connect(self.openWebCamera) 
        self.ui.closeLocalCameraButton.clicked.connect(self.closeLocalCamera) 
        self.ui.closeWebCameraButton.clicked.connect(self.closeWebCamera) 
        self.ui.pingIPButton.clicked.connect(self.pingIP) 
        
    def openAFrameImage(self):
        """Open single image"""
        fileName, fileType = QFileDialog.getOpenFileName(self, "Open file", "./img", "Image files(*.bmp; *.jpg)")
        if self.ui.imageToShow.load(fileName):
            self.ui.imageToShowLabel.setPixmap(QPixmap.fromImage(self.ui.imageToShow))
        # Extract original image    
        self.imageArray = cv2.imread(fileName)
        
        
    def openVideo(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "Open file", "./img", "Image files(*.mp4;*.avi)")
        self.video = video.Video(fileName)
        self.video.refreshVideoImgSignal.connect(self.refreshVideoImage)
        self.video.refreshVideoImgArraySignal.connect(self.refreshVideoImageArray)
        self.video.videoTimer.start()
    
    def closeVideo(self):
        """Close video"""
        if not self.video.videoTimer.isStoped():
            self.video.videoTimer.stop()
            # Extract original image
            while not self.video.imageArrayQueue.empty():
                self.imageArray = self.video.imageArrayQueue.get()
        # Destroy local camera object
        del self.video    
    
    def refreshVideoImage(self):
        """"""
        while not self.video.imageQueue.empty():
            image = self.video.imageQueue.get()
            self.ui.imageToShowLabel.setPixmap(QPixmap.fromImage(image))    
        
    def refreshVideoImageArray(self):
        """Video, update ImageArray, calculate detection results"""    
        if self.ui.autoCalcButton.isChecked(): 
            while not self.video.imageArrayQueue.empty():
                self.imageArray = self.video.imageArrayQueue.get()    
            self.startCalcDetectResult()   

    
    def openLocalCamera(self):
        """Open local camera"""
        self.localCamera = localCamera.LocalCamera()
        self.localCamera.refreshLocalCameraImgSignal.connect(self.refreshLocalCameraImage)
        self.localCamera.refreshLocalCameraImgArraySignal.connect(self.refreshLocalCameraImageArray)
        self.localCamera.localCameraTimer.start()
        
    def closeLocalCamera(self):
        """Close local camera"""
        if not self.localCamera.localCameraTimer.isStoped():
            self.localCamera.localCameraTimer.stop()
            # Extract original image
            while not self.localCamera.imageArrayQueue.empty():
                self.imageArray = self.localCamera.imageArrayQueue.get()
        # Destroy local camera object
        del self.localCamera
              
    def refreshLocalCameraImage(self):
        """Local camera, update image on window"""
        while not self.localCamera.imageQueue.empty():
            image = self.localCamera.imageQueue.get()
            self.ui.imageToShowLabel.setPixmap(QPixmap.fromImage(image))
            
    def refreshLocalCameraImageArray(self):
        """Local camera, update ImageArray, calculate detection results"""    
        if self.ui.autoCalcButton.isChecked(): 
            while not self.localCamera.imageArrayQueue.empty():
                self.imageArray = self.localCamera.imageArrayQueue.get()    
            self.startCalcDetectResult()   
                
    def pingIP(self):
        """Ping IP address"""
        self.webCameraIP = self.ui.webCameraIPLineEdit.text()
        print("Testing IP:", self.webCameraIP)
        # Use macOS compatible ping command
        import platform
        if platform.system() == "Darwin":  # macOS
            connected = not os.system("ping -c 1 -t 1 %s > /dev/null 2>&1" % self.webCameraIP)
        else:  # Windows/Linux
            connected = not os.system("ping -n 1 -w 1 %s > /dev/null 2>&1" % self.webCameraIP)
        print("IP connectivity:", connected)
        return connected
        
    def openWebCamera(self):
        """Open network camera"""   
        if self.pingIP():
            print("Connecting to this IP:", self.ui.webCameraIPLineEdit.text())
            self.webCameraSeverThread = webCamera.WebCameraSeverThread((self.ui.webCameraIPLineEdit.text(), int(self.ui.webCameraPortLineEdit.text()))) 
            self.webCameraSeverThread.refreshWebCameraImgSignal.connect(self.refreshWebCameraImage)
            self.webCameraSeverThread.refreshWebCameraImgArraySignal.connect(self.refreshWebCameraImageArray)
            self.webCameraSeverThread.start()  
         
    def closeWebCamera(self):
        """Close network camera"""
        if not self.webCameraSeverThread.isStoped():
            self.webCameraSeverThread.stop()
            # Extract original image
            while not self.webCameraSeverThread.imageArrayQueue.empty():
                self.imageArray = self.webCameraSeverThread.imageArrayQueue.get()
        # Destroy network camera object
        del self.webCameraSeverThread
         
            
    def refreshWebCameraImage(self):
        """Network camera, update image on window"""
        while not self.webCameraSeverThread.imageQueue.empty():
            image = self.webCameraSeverThread.imageQueue.get()
            self.ui.imageToShowLabel.setPixmap(QPixmap.fromImage(image))
            
    def refreshWebCameraImageArray(self):
        """Network camera, update ImageArray, calculate detection results"""
        if self.ui.autoCalcButton.isChecked(): 
            while not self.webCameraSeverThread.imageArrayQueue.empty():
                self.imageArray = self.webCameraSeverThread.imageArrayQueue.get()    
            self.startCalcDetectResult()    
         
    def startCalcDetectResult(self): 
        """Start calculating detection results, create a new thread"""
        print("Starting detection result calculation")
        if self.imageArray.size > 0 and (not self.calcDetectResultThreadRunning): # Image matrix is not empty
            self.calcDetectResultThreadRunning = 1
            self.calcDetectResultThread = detector.CalcDetectResultThread(self.imageArray)         
            self.calcDetectResultThread.resultSignal.connect(self.refreshDetectResult)
            self.calcDetectResultThread.start()        
            
    def refreshDetectResult(self, resultNums, resultClassify):
        """Update detection results"""
        print("Detection result calculation completed")
        self.calcDetectResultThreadRunning = 0
        self.ui.resultNumLineEdit.setText(resultNums)
        self.ui.resultTextLineEdit.setText(str(resultClassify))
        
        if self.ui.resultImage.load("./icon/level" + str(resultClassify) + ".png"):
            self.ui.resultImageLabel.setPixmap(QPixmap.fromImage(self.ui.resultImage))
        
        
            
  
"""Main function"""
window = MainWindow()
sys.exit(app.exec_())