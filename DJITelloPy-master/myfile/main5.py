from djitellopy import Tello
import keyboard
import cv2
from time import sleep
import numpy as np

tel = Tello()
tel.connect()
sleep(0.5)
tel.streamon()

cv2.namedWindow("OpenCV Window")

def nothing(x):
    pass

cv2.createTrackbar("H_min", "OpenCV Window", 0, 179, nothing)
cv2.createTrackbar("H_max", "OpenCV Window", 9, 179, nothing)       # Hueの最大値は179
cv2.createTrackbar("S_min", "OpenCV Window", 128, 255, nothing)
cv2.createTrackbar("S_max", "OpenCV Window", 255, 255, nothing)
cv2.createTrackbar("V_min", "OpenCV Window", 128, 255, nothing)
cv2.createTrackbar("V_max", "OpenCV Window", 255, 255, nothing)

try:
    while True:
        if keyboard.is_pressed('esc'):
            break
        else:
            frame = tel.get_frame_read().frame
            image = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            bgr_image = cv2.resize(image,dsize=(480.360))

except (KeyboardInterrupt,SystemExit):
    tel.end()
    cv2.destroyAllWindows()        