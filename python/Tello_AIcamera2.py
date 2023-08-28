import cv2
import socket
import threading
import boto3
import time

color = (0, 0, 0)

# telloへのアクセス用
tello_ip = '192.168.10.1'
tello_port = 8889
tello_address = (tello_ip, tello_port)

# telloからの受信用
VS_UDP_IP = '0.0.0.0'
VS_UDP_PORT = 11111

# VideoCapture用のオブジェクト準備
cap = None
# データ受信用のオブジェクト準備
response = None

# 通信用のソケットを作成
# ※アドレスファミリ：AF_INET（IPv4）、ソケットタイプ：SOCK_DGRAM（UDP）
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# リッスン状態にする
sock.bind(('', tello_port))

cap = cv2.VideoCapture(0)
cascade_path = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

# データ受け取り用の関数
def recv():
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break

# コマンドモードを使うため'command'というテキストを投げる
sent = sock.sendto(b'command', tello_address)


# ビデオストリーミング開始
sent = sock.sendto(b'streamon', tello_address)
print("streamon")
# time.sleep(10)qqqqq

udp_video_address = 'udp://@' + VS_UDP_IP + ':' + str(VS_UDP_PORT)
if cap is None:
    cap = cv2.VideoCapture(udp_video_address)
if not cap.isOpened():
    cap.open(udp_video_address)

# 離陸
sent = sock.sendto(b'takeoff', tello_address)
time.sleep(10)

#上に20cm
sent = sock.sendto(b'up 20', tello_address)
time.sleep(10)

#キャプチャ画面の中心点の取得
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
c_x = width//2
c_y = height//2
c_w = width//4
c_h = height//4


c_x_max = c_x + 50
c_x_min = c_x - 50

while(True):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        frame = cv2.rectangle(gray,(x,y),(x+w,y+h),color,2)

        a=x
        b=y
        c=x+w
        d=y+h

        face_area = h * w / 100

        f_x = (a+c)//2
        f_y = (b+d)//2


        print(face_area)   
        # print("center" , c_x, c_y)
        # print("face" , f_x, f_y)
        # print("width" , width)

        #追尾制御 横、前後移動
        if 0 < f_x < 370:

            #右に20cm
            sent = sock.sendto(b'left 20', tello_address)

        elif 590 < f_x < 960:

            #左に20cm
            sent = sock.sendto(b'right 20', tello_address)

        elif 100 < face_area < 200:
            #前に20cm
            sent = sock.sendto(b'forward 20', tello_address)

        elif 500 < face_area < 600:
            #後ろに20cm
            sent = sock.sendto(b'back 20', tello_address)


    cv2.imshow('frame', gray)
    # qキーを押して着陸
    if cv2.waitKey(1) & 0xFF == ord('q'):
        sent = sock.sendto(b'land', tello_address)
        break

cap.release()
cv2.destroyAllWindows()

# ビデオストリーミング停止
sent = sock.sendto(b'streamoff', tello_address)
