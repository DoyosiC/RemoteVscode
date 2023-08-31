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
print('0')
sleep(0.5)
print('0.5')
tel.streamon()
sleep(0.5)


# トラックバーを作るため，まず最初にウィンドウを生成
cv2.namedWindow("OpenCV Window")

# トラックバーのコールバック関数は何もしない空の関数
def nothing(x):
    pass        # passは何もしないという命令

# トラックバーの生成
    
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
            flag = None
            frame_read = tel.get_frame_read()
            img = frame_read.frame
            cv2.waitKey(1)


            image = cv2.resize(img,dsize=(480,360))

            hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

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

            cv2.imshow("drone",out_image)

            if keyboard.is_pressed('q'):
                break
            elif keyboard.is_pressed('t'):
                flag = 0
                tel.takeoff()             # 離陸
            elif keyboard.is_pressed('l'):
                tel.land()                # 着陸
            elif keyboard.is_pressed('w'):
                ctrl.ctrl_forward()     # 前進
            elif keyboard.is_pressed('s'):
                ctrl.ctrl_back()    # 後進
            elif keyboard.is_pressed('a'):
                ctrl.ctrl_left()        # 左移動
            elif keyboard.is_pressed('d'):
                ctrl.ctrl_right()       # 右移動
            elif keyboard.is_pressed('q'):
                ctrl.ctrl_yaw_left()        # 左旋回
            elif keyboard.is_pressed('e'):
                ctrl.ctrl_yaw_right()        # 右旋回
            elif keyboard.is_pressed('r'):
                ctrl.ctrl_up(0.3)          # 上昇
            elif keyboard.is_pressed('f'):
                ctrl.ctrl_down(0.3)        # 下降
            elif keyboard.is_pressed('1'):
                flag = 1                    # 追跡モードON
            elif keyboard.is_pressed('2'):
                flag = 0                    # 追跡モードOFF

    tel.streamoff()
    tel.end()
    cv2.destroyAllWindows()
        
except (KeyboardInterrupt, SystemExit):
    tel.end()
    cv2.destroyAllWindows()


