from djitellopy import Tello
import cv2,math,time
tello=Tello()

tello.connect()

tello.takeoff()

while True:
    key = cv2.waitKey(1) & 0xff
    if key == 27: # ESC:
         # "ESC"キーが押されたらTelloのend()メソッドを呼び出して終了
        break

    else:
        tello.move_forward(100)
        tello.move_back(100)
      
tello.land()