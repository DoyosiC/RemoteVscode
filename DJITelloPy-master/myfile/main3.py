from djitellopy import Tello
from controls import CTRL
import time, keyboard
import cv2


tello = Tello()
tello.connect()
ctrl = CTRL()
tello.set_speed(20)
tello.set_video_bitrate(0)
time.sleep(1)
tello.set_video_fps('high')
time.sleep(1)


tello.streamoff()
tello.streamon()
frame_read = tello.get_frame_read()

try:
    # if frame_read.stopped:
    #     tello.end()
    # # バッテリー残量を取得
    #     time.sleep(0.5)
    #     frame = frame_read.frame
    #     battery = tello.get_battery()
    #     temp = tello.get_temperature()

    #     # バッテリー残量が40％未満の場合は飛行停止
    #     if battery <= 40:
    #         print('\033[31m' + "Low battery!! Cannot fly!!" + '\033[0m')
    #         tello.end()
    #     else:
    #         print(f"Battery: {battery}%")
    #         print(f"Temperature: {temp}°C")
    #         cv2.imshow("drone",frame)
    #         time.sleep(2)

    while True:
        key = cv2.waitKey(1) & 0xff
        if keyboard.is_pressed('esc'):
            break
        elif keyboard.is_pressed('o'):
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
            ctrl.ctrl_yaw(-45)  # 左に45速度
        elif keyboard.is_pressed('right'):
            ctrl.ctrl_yaw(45)  # 右に45速度


    tello.land()
    time.sleep(0.5)
    tello.streamoff()
    print("Finish!")

except KeyboardInterrupt:
    tello.end()
    print("Interrupted by the user.")
