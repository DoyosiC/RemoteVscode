from djitellopy import Tello
import cv2
import keyboard

# # Telloドローンのインスタンスを作成
# tello = Tello()

# # Telloドローンに接続
# tello.connect()

# # ビデオストリームを開始
# tello.streamon()

# # OpenCVのビデオキャプチャオブジェクトを作成
# cap = cv2.VideoCapture(tello.get_udp_video_address())

# while True:
#     # フレームをキャプチャ
#     ret, frame = cap.read()

#     if ret:
#         # フレームを表示
#         cv2.imshow('Tello Video Stream', frame)

#     # 'q'キーを押すとループを終了
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # キャプチャとTelloドローンへの接続を解除
# cap.release()
# cv2.destroyAllWindows()
# tello.streamoff()

# Telloドローンのインスタンスを作成
tello = Tello()

# ドローンのビデオストリームを受信するBackgroundFrameReadオブジェクトを作成
frame_reader = tello.get_frame_read()

# フレーム読み取りを開始
frame_reader.start()

# メインループでビデオフレームを処理
while True:
    frame = frame_reader.frame  # 最新のビデオフレームを取得
    # ここでフレームを処理する（例：表示、保存、オブジェクト検出）
    if keyboard.is_pressed('q'):
        break

# プログラムの終了時にフレーム読み取りを停止
frame_reader.stop()

