#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Raspberry Pi client program
"""
import socket
import numpy
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# Raspberry Pi camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

# socket.AF_INET for server-to-server network communication
# socket.SOCK_STREAM represents TCP-based stream socket communication
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Connect to server
address_server = ('169.254.196.152', 22)
sock.connect(address_server)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Convert the captured frame to be the same as the laptop's frame
    image = frame.array

    # First encode the image, '.jpg' means encode in jpg format
    result, imgencode = cv2.imencode('.jpg', image)
    data = numpy.array(imgencode)
    byteData = data.tobytes()

    # First send the length of the encoded image
    sock.send(str(len(byteData)).encode('utf-8'))

    # Then send the encoded content
    sock.send(byteData)

    #cv2.imshow("Frame", image)
    #key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    time.sleep(0.1)
    #if key == ord("q"):
        #break

sock.close()