from djitellopy import Tello
import time
import keyboard
import threading
class TelloController:
    MAX_HEIGHT = 200  # cm (Max_2m)
    MIN_HEIGHT = 15   # cm (Min_15cm)

    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.tello.takeoff()  # プログラム開始時に離陸

    def move_up(self):
        height = self.tello.get_height()
        if 15 <= height <= self.MAX_HEIGHT:
            self.tello.send_rc_control(0, 0, 20, 0)
        else:
            print("Cannot go higher! Already at maximum height.")

    def move_down(self):
        height = self.tello.get_height()
        if 15 <= height <= self.MIN_HEIGHT:
            self.tello.send_rc_control(0, 0, -15, 0)
        else:
            print("Cannot go lower! Already at minimum height.")

    def display_height_periodically(self, interval=3):
        while True:
            height = self.tello.get_height()
            print(f"Current Height: {height} cm")
            time.sleep(interval)

    def run(self):
        try:
            height_display_thread = threading.Thread(target=self.display_height_periodically)
            height_display_thread.daemon = True
            height_display_thread.start()

            while True:
                if keyboard.is_pressed('esc'):
                    break
                elif keyboard.is_pressed('up'):
                    self.move_up()
                elif keyboard.is_pressed('down'):
                    self.move_down()
            
            self.tello.land()
        
        except KeyboardInterrupt:
            self.tello.end()
            print("ユーザーによって中断されました.")

if __name__ == "__main__":
    controller = TelloController()
    controller.run()
