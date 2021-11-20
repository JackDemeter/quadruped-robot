from adafruit_servokit import ServoKit
from enum import IntEnum
import time
import math
import bezier
import numpy as np

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
        self.upper_leg_length = 10
        self.lower_leg_length = 10.5
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

    def set_angle(self,leg_id, degrees):
        self.kit.servo[leg_id].angle = degrees

    def test_pos(self,x,y,shoulder,elbow,right=True):
        elbow_offset = 20
        shoulder_offset = 10
        a1 = self.upper_leg_length
        a2 = self.lower_leg_length

        c2 = (x**2+y**2-a1**2-a2**2)/(2*a1*a2)
        s2 = math.sqrt(1-c2**2)
        theta2 = math.atan2(s2,c2)
        c2 = math.cos(theta2)
        s2 = math.sin(theta2)

        c1 = (x*(a1+(a2*c2)) + y*(a2*s2))/(x**2+y**2)
        s1 = (y*(a1+(a2*c2)) - x*(a2*s2))/(x**2+y**2)
        theta1 = math.atan2(s1,c1)
        # generate positions with respect to robot motors
        theta_shoulder = -theta1
        theta_elbow = theta_shoulder - theta2
        if right:
            theta_shoulder = 180 - self.rad_to_degree(theta_shoulder) + shoulder_offset
            theta_elbow = 130 - self.rad_to_degree(theta_elbow) + elbow_offset
        else:
            theta_shoulder = self.rad_to_degree(theta_shoulder) - shoulder_offset
            theta_elbow = 50 + self.rad_to_degree(theta_elbow) - elbow_offset
        self.kit.servo[shoulder].angle = theta_shoulder
        self.kit.servo[elbow].angle = theta_elbow
        # print("theta shoulder:",theta_shoulder,"\ttheta_elbow:",theta_elbow)
        return [theta_shoulder, theta_elbow]

    def test_step(self, cycles=1):
        # Generate foot tragectory
        step_nodes = np.asfortranarray([
            [-4.0, -4.0, 0.0, 0.0],
            [-15.0, -10, -10, -15.0],
        ])
        curve = bezier.Curve(step_nodes, degree=3)
        s_vals = np.linspace(0.0, 1.0, 20)
        step = curve.evaluate_multi(s_vals)

        slide_nodes = np.asfortranarray([
            [0.0, -4.0],
            [-15.0, -15.0],
        ])
        curve = bezier.Curve(slide_nodes, degree=1)
        s_vals = np.linspace(0.0, 1.0, 60)
        slide = curve.evaluate_multi(s_vals)

        foot_motion = step
        for x,y in zip(slide[0],slide[1]):
            new_x=np.append(foot_motion[0],x)
            new_y=np.append(foot_motion[1],y)
            foot_motion = [new_x,new_y]
        
        x = foot_motion[0]
        y = foot_motion[1]
        
        for cycle in range(cycles):
            for index in range(80):
                self.test_pos(x[index],y[index],Motor.FR_SHOULDER,Motor.FR_ELBOW,right=True)
                self.test_pos(x[(index+20)%80],y[(index+20)%80],Motor.BR_SHOULDER,Motor.BR_ELBOW,right=True)
                self.test_pos(x[(index+40)%80],y[(index+40)%80],Motor.FL_SHOULDER,Motor.FL_ELBOW,right=False)
                self.test_pos(x[(index+60)%80],y[(index+60)%80],Motor.BL_SHOULDER,Motor.BL_ELBOW,right=False)
                time.sleep(0.02)

    def rad_to_degree(self,rad):
        return rad*180/math.pi


if __name__ == "__main__":
    r = Quadruped()
    r.calibrate()
    time.sleep(1)
    r.test_step(5)