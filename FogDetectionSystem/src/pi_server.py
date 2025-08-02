#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket, time
import cv2
import numpy as np

# Receive image size information
def recv_size(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    print(buf)
    return buf.decode('utf-8')

# Receive image
def recv_all(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(1024)
        if not newbuf: 
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# socket.AF_INET for server-to-server network communication
# socket.SOCK_STREAM represents TCP-based stream socket communication
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set address and port, if receiving connections from any IP to this server, address can be empty, but port must be set
address = ('169.254.196.152', 22)
s.bind(address) # Bind Socket to address
s.listen(True) # Start listening for incoming TCP connections
print ('Waiting for images...')
# Accept TCP connection and return (conn, addr), where conn is a new socket object that can be used to receive and send data, addr is the address of the connecting client
conn, addr = s.accept()

while 1:
    length = recv_size(conn,5) # First receive size information sent from client
    if isinstance (length,str): # If size information is successfully received, further receive the entire image
        byteData = recv_all(conn, int(length))
        data = np.fromstring(byteData, np.uint8)
        decimg=cv2.imdecode(data,1) # Decode processing, return mat image
        cv2.imshow('SERVER',decimg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 
        print('Image recieved successfully!')
        conn.send(b'Server has recieved messages!')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

s.close()
cv2.destroyAllWindows()