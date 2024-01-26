from djitellopy import Tello
import pygame
import keyboard
from time import sleep
import cv2 
import numpy as np
import controls


tel=Tello()
ctrl = controls.CTRL()
tel.connect()
sleep(0.5)
tel.streamon()

# トラックバーを作るため，まず最初にウィンドウを生成
cv2.namedWindow("OpenCV Window")

# トラックバーのコールバック関数は何もしない空の関数
def nothing(x):
    pass

# トラックバーの生成
cv2.createTrackbar("H_min", "OpenCV Window", 0, 179, nothing)
cv2.createTrackbar("H_max", "OpenCV Window", 9, 179, nothing)       # Hueの最大値は179
cv2.createTrackbar("S_min", "OpenCV Window", 128, 255, nothing)
cv2.createTrackbar("S_max", "OpenCV Window", 255, 255, nothing)
cv2.createTrackbar("V_min", "OpenCV Window", 128, 255, nothing)
cv2.createTrackbar("V_max", "OpenCV Window", 255, 255, nothing)

flag = 0
#Ctrl+cが押されるまでループ

try:
    while True:
        if keyboard.is_pressed('esc'):
            break
        else:
            frame = tel.get_frame_read().frame
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)      # OpenCV用のカラー並びに変換する
            bgr_image = cv2.resize(image, dsize=(480,360) ) # 画像サイズを半分に変更
            hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)  # BGR画像 -> HSV画像

            # トラックバーの値を取る

            h_min = cv2.getTrackbarPos("H_min", "OpenCV Window")
            h_max = cv2.getTrackbarPos("H_max", "OpenCV Window")
            s_min = cv2.getTrackbarPos("S_min", "OpenCV Window")
            s_max = cv2.getTrackbarPos("S_max", "OpenCV Window")
            v_min = cv2.getTrackbarPos("V_min", "OpenCV Window")
            v_max = cv2.getTrackbarPos("V_max", "OpenCV Window")

            # inRange関数で範囲指定２値化
            bin_image = cv2.inRange(hsv_image, (h_min, s_min, v_min), (h_max, s_max, v_max)) # HSV画像なのでタプルもHSV並び

            # bitwise_andで元画像にマスクをかける -> マスクされた部分の色だけ残る
            masked_image = cv2.bitwise_and(hsv_image, hsv_image, mask=bin_image)

            # ラベリング結果書き出し用に画像を準備
            out_image = masked_image

            # 面積・重心計算付きのラベリング処理を行う
            num_labels, label_image, stats, center = cv2.connectedComponentsWithStats(bin_image)

            # 最大のラベルは画面全体を覆う黒なので不要．データを削除
            num_labels = num_labels - 1
            stats = np.delete(stats, 0, 0)
            center = np.delete(center, 0, 0)


            if num_labels >= 1:
                # 面積最大のインデックスを取得
                max_index = np.argmax(stats[:,4])
                #print max_index

                # 面積最大のラベルのx,y,w,h,面積s,重心位置mx,myを得る
                x = stats[max_index][0]
                y = stats[max_index][1]
                w = stats[max_index][2]
                h = stats[max_index][3]
                s = stats[max_index][4]
                mx = int(center[max_index][0])
                my = int(center[max_index][1])
                #print("(x,y)=%d,%d (w,h)=%d,%d s=%d (mx,my)=%d,%d"%(x, y, w, h, s, mx, my) )

                # ラベルを囲うバウンディングボックスを描画
                cv2.rectangle(out_image, (x, y), (x+w, y+h), (255, 0, 255))

                # 重心位置の座標を表示
                #cv2.putText(out_image, "%d,%d"%(mx,my), (x-15, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
                cv2.putText(out_image, "%d"%(s), (x, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))

                if flag == 1:
                    a = b = c = d = 0

          # P制御の式(Kpゲインはとりあえず1.0)
                    dx = 1.0 * (240 - mx)       # 画面中心との差分

                    # 旋回方向の不感帯を設定
                    d = 0.0 if abs(dx) < 50.0 else dx   # ±50未満ならゼロにする

                    d = -d
                    # 旋回方向のソフトウェアリミッタ(±100を超えないように)
                    d =  100 if d >  100.0 else d
                    d = -100 if d < -100.0 else d

                    print('dx=%f'%(dx) )
                    tel.send_rc_control(int(a), int(b), int(c), int(d))

            cv2.waitKey(1)
            # (X)ウィンドウに表示
            cv2.imshow('OpenCV Window', out_image)  # ウィンドウに表示するイメージを変えれば色々表示できる

            if keyboard.is_pressed('q'):
                break
            elif keyboard.is_pressed('t'):
                tel.takeoff()                   # 離陸
            elif keyboard.is_pressed('l'):
                tel.land()                      # 着陸
            elif keyboard.is_pressed('w'):
                ctrl.ctrl_forward()             # 前進
            elif keyboard.is_pressed('s'):
                ctrl.ctrl_back()                # 後進
            elif keyboard.is_pressed('a'):
                ctrl.ctrl_left()                # 左移動
            elif keyboard.is_pressed('d'):
                ctrl.ctrl_right()               # 右移動
            elif keyboard.is_pressed('left'):
                ctrl.ctrl_yaw_left()            # 左旋回
            elif keyboard.is_pressed('right'):
                ctrl.ctrl_yaw_right()           # 右旋回
            # elif keyboard.is_pressed('w' and 'd'):  
            #     ctrl.ctrl_clock_one()           #前右
            # elif keyboard.is_pressed('w' and 'a'):
            #     ctrl.ctrl_clock_eleven()        #前左
            # elif keyboard.is_pressed('s' and 'd'):
            #     ctrl.ctrl_clock_five()          #後ろ右
            # elif keyboard.is_pressed('s' and 'a'):
            #     ctrl.ctrl_clock_seven()         #後ろ左
            elif keyboard.is_pressed('up'):
                ctrl.ctrl_up()          # 上昇
            elif keyboard.is_pressed('down'):
                ctrl.ctrl_down()        # 下降
            elif keyboard.is_pressed('1'):
                flag = 1
                sleep(0.6)
                print("Prees 1  treas ON!!")                    # 追跡モードON
            elif keyboard.is_pressed('2'):
                flag = 0                    # 追跡モードOFF
                sleep(0.9)
                print("Pressed 0 trease OFF!!")
            else:
                ctrl.ctrl_hover()


    tel.streamoff()
    tel.land()
    sleep(0.6)
    cv2.destroyAllWindows()
        
except (KeyboardInterrupt, SystemExit):
    tel.end()
    cv2.destroyAllWindows()


