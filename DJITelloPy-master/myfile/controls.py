from djitellopy import Tello

#from tool import Tools
#import time

class CTRL:

    DRONE_SPEED = 50
    MAX_HEIGHT = 200  # cm (Max_2m)
    MIN_HEIGHT = 15   # cm (Min_15cm)
    s = DRONE_SPEED
    yaw = s
    u = s-30  #20
    d = s-35  #15
    def __init__(self) -> None:
        self.tello = Tello()
        self.tello.connect()

    def input_key(self, x: str):
        pass

    def ctrl_forward(self):  # forward 50cm/s
        self.tello.send_rc_control(0, self.s, 0, 0)

    def ctrl_back(self):  # back 50cm/s
        self.tello.send_rc_control(0, -self.s, 0, 0)

    def ctrl_left(self):  # left
        self.tello.send_rc_control(-self.s, 0, 0, 0)

    def ctrl_right(self):  # right
        self.tello.send_rc_control(self.s, 0, 0, 0)

    def ctrl_clock_one(self):
        self.tello.go_xyz_speed(self.s, self.s, 0, 0)

    def ctrl_clock_five(self):
        self.tello.go_xyz_speed(self.s, -self.s, 0, 0)

    def ctrl_clock_seven(self):
        self.tello.go_xyz_speed(-self.s, -self.s, 0, 0)

    def ctrl_clock_eleven(self):
        self.tello.go_xyz_speed(-self.s, self.s, 0, 0)

    def ctrl_up(self):
        height = self.tello.get_height()
        if 15 <= height <= self.MAX_HEIGHT:
            self.tello.send_rc_control(0, 0, self.u, 0)
        else:
            print("Cannot go higher! Already at maximum height.")
    
    def ctrl_down(self):
        height = self.tello.get_height()
        if 15 <= height <= self.MIN_HEIGHT:
            self.tello.send_rc_control(0, 0, -self.d, 0)
        else:
            print("Cannot go lower! Already at minimum height.")

    def ctrl_yaw_left(self):  # Specify yaw angle in degrees
        self.tello.send_rc_control(0, 0, 0, -self.yaw)
    
    def ctrl_yaw_right(self):  # Specify yaw angle in degrees
        self.tello.send_rc_control(0, 0, 0, self.yaw)

    def ctrl_hover(self):
        self.tello.send_rc_control(0, 0, 0, 0)

if __name__ == "__main__":
    ctrl = CTRL()
