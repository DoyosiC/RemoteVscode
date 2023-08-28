#
# Tello Python3 Control Demo 
#
# http://www.ryzerobotics.com/
#
# 1/1/2018

import threading 
import socket
import cv2
import sys
import time


host = ''
port = 9000
VS_UDO_IP = '0.0.0.0'
VS_UDP_PROT = 11111
TELLO_CAMERA_ADDRESS = 'udp://@0.0.0.0:11111'
locaddr = (host,port) 


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ('192.168.10.1', 8889)

sock.bind(locaddr)

def recv():
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break


print ('\r\n\r\nTello Python3 Demo.\r\n')

print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

print ('end -- quit demo.\r\n')


#recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()

while True: 

    try:
        msg = input("");

        if not msg:
            break  

        if 'end' in msg:
            print ('...')
            sock.close()  
            break

        # Send data
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()  
        break


import threading 
import socket


# Telloからのレスポンス受信
def udp_receiver():
    count = 0
    while True: 
        try:
            # クライアントからのメッセージの受信を受付開始(コネクションレス型)
            data, server = sock.recvfrom(1518)
        except Exception:
            print ('\nExit . . .\n')
            break

# Tello側のローカルIPアドレス(デフォルト)、宛先ポート番号(コマンドモード用)
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

# UDP通信ソケットの作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 自ホストで使用するIPアドレスとポート番号を設定
sock.bind(('', TELLO_PORT))

# 受信用スレッドの作成
thread  = threading.Thread(target=udp_receiver)
thread.daemon = True
thread .start()

while True: 

    try:
        msg = input("")

        # メッセージがなければ何もしない
        if not msg:
            break  

        # 「q」でソケット通信終了
        if 'q' in msg:
            print ('QUIT...')
            sock.close()  
            break

        # データを送信
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, TELLO_ADDRESS)

    except KeyboardInterrupt:
        sock.close()  
        break




