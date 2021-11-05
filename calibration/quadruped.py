# test test

from adafruit_servokit import ServoKit
from enum import IntEnum
import time


class Motor(IntEnum):
    # may be useful for tuning specific motors
    FR_SHOULDER = 0
    FR_ELBOW = 1
    FR_HIP = 2
    FL_SHOULDER = 3
    FL_ELBOW = 4
    FL_HIP = 5
    BR_SHOULDER = 6
    BR_ELBOW = 7
    BL_SHOULDER = 8
    BL_ELBOW = 9

class Quadruped:
    def __init__(self):
        self.kit = ServoKit(channels=16)
        for i in range(10):
            self.kit.servo[i].set_pulse_width_range(500,2500)
        
    def calibrate(self):
        # set the robot into the default "middle position" use this for attaching legs in right location
        self.kit.servo[Motor.FR_SHOULDER].angle = 60
        self.kit.servo[Motor.FR_ELBOW].angle = 90
        self.kit.servo[Motor.FR_HIP].angle = 90
        self.kit.servo[Motor.FL_SHOULDER].angle = 120
        self.kit.servo[Motor.FL_ELBOW].angle = 90
        self.kit.servo[Motor.FL_HIP].angle = 90
        self.kit.servo[Motor.BR_SHOULDER].angle = 60
        self.kit.servo[Motor.BR_ELBOW].angle = 90
        self.kit.servo[Motor.BL_SHOULDER].angle = 120
        self.kit.servo[Motor.BL_ELBOW].angle = 90
            

    def set_shoulders(self, offset, anti=[]):
        #TODO ADD MIN MAX POSITIONS!!!
        if not Motor.FR_SHOULDER in anti:
            self.kit.servo[Motor.FR_SHOULDER].angle = self.kit.servo[Motor.FR_SHOULDER].angle - offset
        if not Motor.BR_SHOULDER in anti:
            self.kit.servo[Motor.BR_SHOULDER].angle = self.kit.servo[Motor.BR_SHOULDER].angle - offset
        if not Motor.FL_SHOULDER in anti:
            self.kit.servo[Motor.FL_SHOULDER].angle = self.kit.servo[Motor.FL_SHOULDER].angle + offset
        if not Motor.BL_SHOULDER in anti:
            self.kit.servo[Motor.BL_SHOULDER].angle = self.kit.servo[Motor.BL_SHOULDER].angle + offset

    def forward_cycle(self, num_cycles=1):
        self.calibrate()
        time.sleep(3)
        self.set_shoulders(8)
        time.sleep(2)
        for i in range(num_cycles):  
            self.set_angle(Motor.FL_ELBOW,80)
            time.sleep(0.2)
            self.set_angle(Motor.FL_SHOULDER,110)
            time.sleep(0.2)
            self.set_shoulders(10,anti=[Motor.FL_SHOULDER])
            time.sleep(0.2)
            self.set_angle(Motor.FL_ELBOW,90)
            time.sleep(0.2)
            
            # BR
            self.set_angle(Motor.BR_ELBOW,100)
            time.sleep(0.2)
            self.set_angle(Motor.BR_SHOULDER,70)
            time.sleep(0.2)
            self.set_shoulders(10,anti=[Motor.BR_SHOULDER])
            time.sleep(0.2)
            self.set_angle(Motor.BR_ELBOW,90)
            time.sleep(0.2)
                
            # FR
            self.set_angle(Motor.FR_ELBOW,100)
            time.sleep(0.2)
            self.set_angle(Motor.FR_SHOULDER,70)
            time.sleep(0.2)
            self.set_shoulders(10,anti=[Motor.FR_SHOULDER])
            time.sleep(0.2)
            self.set_angle(Motor.FR_ELBOW,90)
            time.sleep(0.2)
        
            # BL
            self.set_angle(Motor.BL_ELBOW,80)
            time.sleep(0.2)
            self.set_angle(Motor.BL_SHOULDER,1100)
            time.sleep(0.2)
            self.set_shoulders(10,anti=[Motor.BL_SHOULDER])
            time.sleep(0.2)
            self.set_angle(Motor.BL_ELBOW,90)
            time.sleep(0.2)
            

    def set_angle(self,leg_id, degrees):
        self.kit.servo[leg_id].angle = degrees

if __name__ == "__main__":
    r = Quadruped()
    r.forward_cycle()



