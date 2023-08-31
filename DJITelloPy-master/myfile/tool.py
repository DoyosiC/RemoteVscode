from djitellopy import Tello
import time
import keyboard
import threading

class Tools:
    def __init__(self):
        self.tello = Tello()
# クラス Tools を追加し、
# Tello インスタンスの作成をクラスのコンストラクタで行うようにしました。
# クラスメソッド status_check を追加し、
# Tello の接続処理をクラス内で行うようにしました。
# __name__ の確認を追加して、このスクリプトが直接実行された場合にのみ 
# Tools クラスのインスタンスを作成して実行するようにしました。
# これにより、コードはよりモジュール化され、再利用しやすくなりました。
# また、スクリプトが実行されると Tools クラスのインスタンスを作成して 
# status_check メソッドを呼び出すようになります。
    5
    def display_height_periodically(self, interval=3):
        while True:
            height = self.tello.get_height()
            print(f"Current Height: {height} cm")
            time.sleep(interval)
    
    def display_hight(self):
        self.height_display_thread = threading.Thread(target=self.display_height_periodically)
        self.height_display_thread.daemon = True
        self.height_display_thread.start()

    def status_check(self):
        """
        バッテリーと高度を3秒ごとにprint表示する。
        'esc'で終了 また、ショートカットによる中断も可能。
        """
        try:
            while True:
                battery = self.tello.get_battery()
                altitude = self.tello.get_height()

                if keyboard.is_pressed('esc'):
                    self.tello.end()
                    print("[escキーが押されました]")
                    break
                else:
                    print(f"バッテリー残量: {battery}%")
                    print(f"高度: {altitude}%")
                    time.sleep(3)
        except KeyboardInterrupt:
            self.tello.end()
            print("toolsユーザーによって中断されました。")
    

if __name__ == "__main__":
    tools = Tools()
    tools.status_check()

