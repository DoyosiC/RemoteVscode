from djitellopy import Tello
from controls import CTRL
import time, keyboard

tello = Tello()
tello.connect()
ctrl = CTRL()  # Tools クラスのインスタンスを作成

try:
    while True:
        battary = tello.get_battery()
        temp = tello.get_temperature()
        if battary <= 40 :
            print('\033[31m'+"Row battary!! Can Not flying!!"+'\033[0m')
            break
        else:
            print(f"バッテリー残量：{battary}%")
            print(f"温度：{temp}%")
            time.sleep(2)
            tello.takeoff()

        if keyboard.is_pressed('esc'):
            break
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
            ctrl.ctrl_yaw(-45)  # 左に 45速度
        elif keyboard.is_pressed('right'):
            ctrl.ctrl_yaw(45)  # 右に 45速度 
        else:
            ctrl.ctrl_hover()
    tello.end()
    print("finish!!")
            
except KeyboardInterrupt:
    tello.end()
    print("main2ユーザーによって中断されました.")
