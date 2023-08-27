from djitellopy import Tello
import time

class CTRL:
    MAX_HEIGHT = 200  # cm (Max_2m)
    MIN_HEIGHT = 15   # cm (Min_15cm)

    def __init__(self) -> None:
        self.tello = Tello()
        self.tello.connect()

    def input_key(self, x: str):
        pass

    def ctrl_forward(self):  # forward 50cm/s
        self.tello.send_rc_control(0, 50, 0, 0)

    def ctrl_back(self):  # back 50cm/s
        self.tello.send_rc_control(0, -50, 0, 0)

    def ctrl_left(self):  # left
        self.tello.send_rc_control(-50, 0, 0, 0)

    def ctrl_right(self):  # right
        self.tello.send_rc_control(50, 0, 0, 0)

    def ctrl_up(self):
        height = self.tello.get_height()
        if 20 <= height <= self.MAX_HEIGHT:
            self.tello.send_rc_control(0, 0, 20, 0)
            time.sleep(1)
        else:
            print("Cannot go higher! Already at maximum height.")

    def ctrl_down(self):
        height = self.tello.get_height()
        if 20 <= height <= self.MIN_HEIGHT:
            self.tello.send_rc_control(0, 0, -15, 0)
            time.sleep(1)
        else:
            print("Cannot go lower! Already at minimum height.")

    def ctrl_yaw(self, yaw):  # Specify yaw angle in degrees
        self.tello.send_rc_control(0, 0, 0, yaw)

    def ctrl_hover(self):
        self.tello.send_rc_control(0, 0, 0, 0)

if __name__ == "__main__":
    ctrl = CTRL()
