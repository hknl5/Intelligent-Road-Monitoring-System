#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MainWindowUi(QMainWindow, QWidget):
    """Main window UI"""
    def __init__(self):
        super().__init__()  
        self.setupMainWindow()   

    def setupMainWindow(self):
        """Initialize main window"""
        self.setupUi()
        self.setupLayout()
        # self.connectSignalSlot()
        
    def setupUi(self):
        """Initialize main window UI"""
        self.createButton()
        self.createImageLabel()
        self.createDetectResultLabel()

    def showUi(self):
        """Show main window"""
        self.show()
        self.setWindowIcon(QIcon("./icon/cloud.png"))
        
    def createButton(self):
        """Create buttons"""
        self.openLocalCameraButton = QPushButton("Open Local Camera", self)
        self.closeLocalCameraButton = QPushButton("Close Local Camera", self)
        
        self.openVideoButton = QPushButton("Open Video", self)
        self.closeVideoButton = QPushButton("Close Video", self)
        self.openAFrameImageButton = QPushButton("Open Image", self)
        
        self.webCameraIPLabel = QLabel("IP Address",self)
        self.webCameraIPLineEdit = QLineEdit(self)
        self.webCameraIPLineEdit.setText("169.254.196.152")
        self.webCameraPortLabel = QLabel("Port",self)
        self.webCameraPortLineEdit = QLineEdit(self)
        self.webCameraPortLineEdit.setText("22")
        self.pingIPButton = QPushButton("Test IP Address", self)
        self.openWebCameraButton = QPushButton("Open Network Camera", self)
        self.closeWebCameraButton = QPushButton("Close Network Camera", self)

     
    def createImageLabel(self):
        """Create image labels"""
        # Image label
        self.imageToShow = QImage()
        self.imageToShowLabel = QLabel(self)
        if self.imageToShow.load("./icon/blank_640x480.jpg"):
            self.imageToShowLabel.setPixmap(QPixmap.fromImage(self.imageToShow))
        # Detection result image label
        self.resultImage = QImage()
        self.resultImageLabel = QLabel(self)
        if self.resultImage.load("./icon/blank_256x128.jpg"):
            self.resultImageLabel.setPixmap(QPixmap.fromImage(self.resultImage))
        
    def createDetectResultLabel(self): 
        """Create calculation result labels"""
        self.calcResultButton = QPushButton("Calculate Pollution Level", self)
        self.autoCalcButton = QRadioButton('Video Auto Calculate',  self)  
        # self.autoCalcButton.setFocusPolicy(Qt.NoFocus)
        self.resultNumLabel = QLabel("Entropy",self)
        self.resultNumLineEdit = QLineEdit(self)
        self.resultTextLabel = QLabel("Pollution Level",self)
        self.resultTextLineEdit = QLineEdit(self)
       
    def setupLayout(self):
        """Initialize layout"""
        self.createGroupBox_For_AFrameImage()
        self.createGroupBox_For_Video()
        self.createGroupBox_For_LocalCamera()
        self.createGroupBox_For_ImageToShow()
        self.createGroupBox_For_DetectResult()
        self.createGroupBox_For_resultImage()
        self.createGroupBox_For_WebCamera()

        leftSideLayout = QVBoxLayout() 
        leftSideLayout.addWidget(self.aFrameImageGroupBox)
        leftSideLayout.addWidget(self.videoGroupBox)
        leftSideLayout.addWidget(self.localCameraGroupBox)
        leftSideLayout.addWidget(self.webCameraGroupBox)
        leftSideLayout.addStretch()# Add stretch after the last widget so all widgets are displayed at the top
         
        rightSideLayout = QVBoxLayout()
        rightSideLayout.addWidget(self.detectResultGroupBox)
        rightSideLayout.addWidget(self.resultImageGroupBox)
        rightSideLayout.addStretch() 
         
         
        mainLayout = QHBoxLayout() 
        mainLayout.addLayout(leftSideLayout)
        mainLayout.addWidget(self.imageToShowGroupBox)
        mainLayout.addLayout(rightSideLayout)
        mainLayout.addStretch()# Add stretch after the last widget so all widgets are displayed on the left
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)    
        
    def createGroupBox_For_AFrameImage(self):
        """Single image GroupBox"""
        self.aFrameImageGroupBox = QGroupBox("aFrameImage")
        layout = QVBoxLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.openAFrameImageButton)
        self.aFrameImageGroupBox.setLayout(layout)
        
    def createGroupBox_For_Video(self):
        """Video GroupBox"""
        self.videoGroupBox = QGroupBox("video")
        layout = QVBoxLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.openVideoButton)
        layout.addWidget(self.closeVideoButton)
        self.videoGroupBox.setLayout(layout)      
        
        
    def createGroupBox_For_LocalCamera(self):
        """Local camera GroupBox"""
        self.localCameraGroupBox = QGroupBox("localCamera")
        layout = QVBoxLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.openLocalCameraButton)
        layout.addWidget(self.closeLocalCameraButton)
        self.localCameraGroupBox.setLayout(layout)  
        
    def createGroupBox_For_WebCamera(self):
        """Network camera GroupBox"""
        self.webCameraGroupBox = QGroupBox("webCamera")
        layout = QVBoxLayout()
        layout.setSpacing(10)      
        layout.addWidget(self.webCameraIPLabel)
        layout.addWidget(self.webCameraIPLineEdit)
        layout.addWidget(self.webCameraPortLabel)
        layout.addWidget(self.webCameraPortLineEdit)
        layout.addWidget(self.pingIPButton)
        layout.addWidget(self.openWebCameraButton)
        layout.addWidget(self.closeWebCameraButton)
        self.webCameraGroupBox.setLayout(layout)  
        
        
        

    def createGroupBox_For_ImageToShow(self):
        """Image GroupBox"""
        self.imageToShowGroupBox = QGroupBox("imageToShow")
        layout = QVBoxLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.imageToShowLabel)
        self.imageToShowGroupBox.setLayout(layout)  
        
    def createGroupBox_For_resultImage(self):
        """Detection result image GroupBox"""
        self.resultImageGroupBox = QGroupBox("resultImage")
        layout = QVBoxLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.resultImageLabel)
        self.resultImageGroupBox.setLayout(layout)     
        
    def createGroupBox_For_DetectResult(self):
        """Calculation result GroupBox"""
        self.detectResultGroupBox = QGroupBox("detectResult")
        layout = QVBoxLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.calcResultButton)
        layout.addWidget(self.autoCalcButton)
        layout.addWidget(self.resultNumLabel)
        layout.addWidget(self.resultNumLineEdit)
        layout.addWidget(self.resultTextLabel)
        layout.addWidget(self.resultTextLineEdit)
        self.detectResultGroupBox.setLayout(layout)