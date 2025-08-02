#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import cv2
import numpy as np
import math
import joblib
import sys
import types

# Comprehensive patching for old sklearn models
def patch_sklearn_externals():
    """Patch sklearn.externals modules for compatibility with old models"""
    if 'sklearn.externals' not in sys.modules:
        # Create mock sklearn.externals module
        sklearn_externals = types.ModuleType('sklearn.externals')
        sklearn_externals.__dict__['joblib'] = joblib
        sys.modules['sklearn.externals'] = sklearn_externals
        sys.modules['sklearn.externals.joblib'] = joblib
    
    # Patch _packaging as well
    if 'sklearn.externals._packaging' not in sys.modules:
        try:
            from packaging import version
            sklearn_externals_packaging = types.ModuleType('sklearn.externals._packaging')  
            sklearn_externals_packaging.__dict__['version'] = version
            sys.modules['sklearn.externals._packaging'] = sklearn_externals_packaging
            sys.modules['sklearn.externals._packaging.version'] = version
        except ImportError:
            # If packaging not available, install it
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'packaging'])
            from packaging import version
            sklearn_externals_packaging = types.ModuleType('sklearn.externals._packaging')
            sklearn_externals_packaging.__dict__['version'] = version
            sys.modules['sklearn.externals._packaging'] = sklearn_externals_packaging
            sys.modules['sklearn.externals._packaging.version'] = version

# Apply the patch
patch_sklearn_externals()


class CalcDetectResultThread(QThread):
    """Thread for calculating detection results"""
    resultSignal = pyqtSignal([str,int])
    def __init__(self, imgArray):
        super().__init__()
        self.imgArray = imgArray
        self.model = './model/fog_model.pkl'
        
        try:
            self.clf = joblib.load(self.model)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            # Create a dummy classifier for testing
            from sklearn.ensemble import RandomForestClassifier
            import numpy as np
            self.clf = RandomForestClassifier(n_estimators=10, random_state=42)
            # Fit with dummy data matching the expected 4 features
            X_dummy = np.random.rand(10, 4)
            y_dummy = np.random.randint(0, 4, 10)
            self.clf.fit(X_dummy, y_dummy)
            print("Using dummy model for testing")

    def run(self):
        f=[]
        resultNums = ''
        for i in range(4):
            f.append(self.imgCalculate(i*50+50))
            resultNums = resultNums + '{:.4f}'.format(f[i]) + ', '

        resultClassify = int(self.clf.predict([f]))
        print(f, '\n', resultClassify)
        
        self.resultSignal.emit(resultNums, resultClassify)

    def imgCalculate(self, value):  
        img = self.imgArray    
        b, g, r = cv2.split(img) # Channel separation
        img_GBF = cv2.GaussianBlur(b, (5,5), 0) # Image filtering

        # Difference statistics and entropy calculation
        Img_height = img.shape[0]
        Img_width = img.shape[1]

        for i in range(Img_height):
            for j in range(Img_width):
                if i <= 1  or j <= 1 or i >= Img_height-2 or j >= Img_width-2:   
                    img_GBF[i,j] = 0
                else:
                    g5 = img_GBF[i-2,j+2]
                    g6 = img_GBF[i+2,j+2]
                    g7 = img_GBF[i-2,j-2]
                    g8 = img_GBF[i+2,j-2]
                    
                    G1 = abs(g5 - g8)
                    G2 = abs(g6 - g7)
                    if G1 < value and G2 < value:
                        img_GBF[i,j] = 0  

        tmp = []

        for i in range(256):  
            tmp.append(0)  
        val = 0  
        k = 0  
        res = 0   
        for i in range(len(img_GBF)):  
            for j in range(len(img_GBF[i])):  
                val = img_GBF[i][j]  
                tmp[val] = float(tmp[val] + 1)  
                k =  float(k + 1)  
        for i in range(len(tmp)):  
            tmp[i] = float(tmp[i] / k)  
        for i in range(len(tmp)):  
            if(tmp[i] == 0):  
                res = res  
            else:  
                res = float(res + tmp[i] * math.log(tmp[i]))     #/ math.log(2.0))) 
        
        return -res