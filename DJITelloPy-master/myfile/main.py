import cv2
from djitellopy import Tello
import time,keyboard

# Telloドローンとの通信を確立
tello = Tello()
tello.connect()

# カメラストリーミングを有効にする
tello.streamon()

# カメラ画像を受信し、表示
while True:
    frame = tello.get_frame_read().frame
    cv2.imshow("Tello Camera", frame)

    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 後片付け
tello.streamoff()
tello.end()
cv2.destroyAllWindows()
