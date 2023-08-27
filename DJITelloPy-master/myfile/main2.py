from djitellopy import Tello
import time, keyboard

tello = Tello()
tello.connect()
battary = tello.get_battery()
temp = tello.get_temperature()
print(f"バッテリー残量：{battary}%")
print(f"温度：{temp}%")
time.sleep(2)
tello.takeoff()
# tello.set_speed(30)
try:

    tello.send_rc_control(0,50,0,0)
    time.sleep(3)
    tello.send_rc_control(0,0,0,0)
    time.sleep(5)
    tello.send_rc_control(0,-50,0,0)
    time.sleep(3)
    tello.send_rc_control(0,0,0,0)
    time.sleep(4)
    tello.land()
    tello.end()
    # if keyboard.read_event('esc'):
    #         tello.land()
    # else:
    #     tello.send_rc_control(0, 50, 0, 0)
    #     tello.land()
    
except KeyboardInterrupt:
    tello.end()
    print("main2ユーザーによって中断されました.")
