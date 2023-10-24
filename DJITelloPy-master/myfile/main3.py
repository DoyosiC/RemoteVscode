from djitellopy import Tello
from controls import CTRL
import time, keyboard
import cv2

tello = Tello()
ctrl = CTRL()
tello.connect()
tello.turn_motor_on()


tello.streamoff()
tello.streamon()

try:
    frag = 0
    while True:
        frame_read = tello.get_frame_read()
        img = frame_read.frame
        img = cv2.resize(img,(480,360))
        image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        cv2.waitKey(1)
        cv2.imshow("drone",image)

        if keyboard.is_pressed('esc'):
            break
        elif keyboard.is_pressed('q') & frag == 1:
            tello.land()
            break
        elif keyboard.is_pressed('t'):
            tello.turn_motor_off()
            frag = 1
            time.sleep(1)
            tello.takeoff()
        elif keyboard.is_pressed('l'):
            tello.land()
        elif keyboard.is_pressed('w'):
            ctrl.ctrl_forward()
        elif keyboard.is_pressed('s'):
            ctrl.ctrl_back()
        elif keyboard.is_pressed('a'):
            ctrl.ctrl_left()
        elif keyboard.is_pressed('d'):
            ctrl.ctrl_right()
        elif keyboard.is_pressed('up'):
            ctrl.ctrl_up()
        elif keyboard.is_pressed('down'):
            ctrl.ctrl_down()
        elif keyboard.is_pressed('left'):
            ctrl.ctrl_yaw_left()  # 左に45速度
        elif keyboard.is_pressed('right'):
            ctrl.ctrl_yaw_right()  # 右に45速度
        else:
            ctrl.ctrl_hover()


    time.sleep(0.5)
    tello.streamoff()
    cv2.destroyAllWindows()
    
    print("Finish!")

except KeyboardInterrupt:
    tello.end()
    cv2.destroyAllWindows()
    print("Interrupted by the user.")
