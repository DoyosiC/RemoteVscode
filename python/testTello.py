#!/usr/bin/env python
 
import socket
import time
 
#Create a UDP socket
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1' , 8889)
 
#command-mode : 'command'
socket.sendto('command'.encode('utf-8'),tello_address)
print ('start')
 
socket.sendto('takeoff'.encode('utf-8'),tello_address)
print ('takeoff')
 
time.sleep(5)
socket.sendto(' forward 200'.encode('utf-8'),tello_address)
time.sleep(5)
socket.sendto('right 100'.encode('utf-8'),tello_address)
time.sleep(5)
socket.sendto(' back 200'.encode('utf-8'),tello_address)
time.sleep(5)
socket.sendto('left 100'.encode('utf-8'),tello_address)
ime.sleep(5)
 
socket.sendto('land'.encode('utf-8'),tello_address)
print ('land')