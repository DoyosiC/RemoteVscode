from djitellopy import Tello
import pygame
import keyboard
from time import sleep
import cv2 

tel=Tello()

tel.__init__()
tel.connect()
tel.streamon()

try:
    while True:
        if keyboard.is_pressed('q'):
            break
        else:
            frame = tel.get_frame_read()
            img = frame.frame
            img = cv2.namedWindow("drone",cv2.WINDOW_NORMAL)
            img = cv2.resizeWindow("drone",360,240)
            cv2.imshow("drone",img)
            cv2.waitKey(0.7)
    tel.streamoff()
    cv2.destroyAllWindows()
        
except KeyboardInterrupt:
    tel.end()
    cv2.destroyAllWindows()


