from djitellopy import Tello
import time, keyboard
import cv2
from controls import CTRL  # 自作モジュールをインポート

tello = Tello()
tello.connect()
ctrl = CTRL()

tello.streamoff()
tello.streamon()
frame_read = tello.get_frame_read()

try:
    while True:
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (480, 360))
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow("drone", image)

        if keyboard.is_pressed('esc'):
            break

        # 制御キーの設定
        for key, control_func in {
            't': tello.takeoff,
            'l': tello.land,
            'w': ctrl.ctrl_forward,
            's': ctrl.ctrl_back,
            'a': ctrl.ctrl_left,
            'd': ctrl.ctrl_right,
            'up': ctrl.ctrl_up,
            'down': ctrl.ctrl_down,
            'left': ctrl.ctrl_yaw_left,  # 左に回転
            'right': ctrl.ctrl_yaw_right,  # 右に回転
        }.items():
            if keyboard.is_pressed(key):
                control_func()

        # 何もキーが押されていない場合はホバー
        if not any(keyboard.is_pressed(key) for key in ['w', 's', 'a', 'd', 'up', 'down', 'left', 'right']):
            ctrl.ctrl_hover()

        cv2.waitKey(1)

    tello.land()
    time.sleep(0.5)
    cv2.destroyAllWindows()
    print("Finish!")

except KeyboardInterrupt:
    tello.end()
    cv2.destroyAllWindows()
    print("Interrupted by the user.")
