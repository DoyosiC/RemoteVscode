#!/usr/bin/env python
# -*- coding: utf-8 -*-

from djitellopy import Tello
import cv2
import time
import keyboard  # キーボード入力のためのライブラリ

# メイン関数
def main():
    # Telloクラスを使って，droneというインスタンス(実体)を作る
    drone = Tello()

    current_time = time.time()  # 現在時刻の保存変数
    pre_time = current_time     # 5秒ごとの'command'送信のための時刻変数

    time.sleep(0.5)     # 通信が安定するまでちょっと待つ

    #Ctrl+cが押されるまでループ
    try:
        while True:
            # (A)画像取得
            frame = drone.get_frame_read().frame
            if frame is None or frame.size == 0:    # 中身がおかしかったら無視
                continue 

            # (B)ここから画像処理
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)      # OpenCV用のカラー並びに変換する
            bgr_image = cv2.resize(image, dsize=(480, 360))     # 画像サイズを半分に変更

            hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)  # BGR画像 -> HSV画像

            # (X)ウィンドウに表示
            cv2.imshow('BGR Color', bgr_image)  # 2つのウィンドウを作る
            cv2.imshow('HSV Color', hsv_image)

            # (Y)OpenCVウィンドウでキー入力を1ms待つ
            key = cv2.waitKey(1)
            if key == 27:                   # k が27(ESC)だったらwhileループを脱出，プログラム終了
                break
            elif key == ord('t'):
                drone.takeoff()             # 離陸
            elif key == ord('l'):
                drone.land()                # 着陸
            elif key == ord('w'):
                drone.move_forward(30)      # 前進（速度30 cm/s）
            elif key == ord('s'):
                drone.move_back(30)         # 後退（速度30 cm/s）
            elif key == ord('a'):
                drone.move_left(30)         # 左移動（速度30 cm/s）
            elif key == ord('d'):
                drone.move_right(30)        # 右移動（速度30 cm/s）
            elif key == ord('q'):
                drone.rotate_counter_clockwise(30)  # 左旋回（速度30°/s）
            elif key == ord('e'):
                drone.rotate_clockwise(30)   # 右旋回（速度30°/s）
            elif key == ord('r'):
                drone.move_up(30)           # 上昇（速度30 cm/s）
            elif key == ord('f'):
                drone.move_down(30)         # 下降（速度30 cm/s）

            # (Z)5秒おきに'command'を送って、死活チェックを通す
            current_time = time.time()  # 現在時刻を取得
            if current_time - pre_time > 5.0 :  # 前回時刻から5秒以上経過しているか？
                drone.send_command('command')   # 'command'送信
                pre_time = current_time         # 前回時刻を更新

    except (KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
        print("SIGINTを検知")

    # telloクラスを削除
    del drone

# "python main.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":      # importされると"__main__"は入らないので，実行かimportかを判断できる．
    main()    # メイン関数を実行
