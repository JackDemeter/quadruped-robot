from adafruit_servokit import ServoKit
from enum import IntEnum
import time
import math
import bezier
import numpy as np
import curses
import os

class Motor(IntEnum):
    # identifies the corresponding pin location with the motor location
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

    def set_angle(self,motor_id, degrees):
        """
        set the angle of a specific motor to a given angle
        :param motor_id: the motor id
        :param degrees: the angle to put the motor to
        :returns: void
        """
        self.kit.servo[motor_id].angle = degrees

    def rad_to_degree(self,rad):
        """
        Converts radians to degrees
        :param rad: radians
        :returns: the corresponding degrees as a float
        """
        return rad*180/math.pi

    def calibrate(self):
        """
        sets the robot into the default "middle position" use this for attaching legs in right location
        :returns: void
        """
        self.set_angle(Motor.FR_SHOULDER, 60)
        self.set_angle(Motor.FR_ELBOW, 90)
        self.set_angle(Motor.FR_HIP, 90)
        self.set_angle(Motor.FL_SHOULDER, 120)
        self.set_angle(Motor.FL_ELBOW, 90)
        self.set_angle(Motor.FL_HIP, 90)
        self.set_angle(Motor.BR_SHOULDER, 60)
        self.set_angle(Motor.BR_ELBOW, 90)
        self.set_angle(Motor.BL_SHOULDER, 120)
        self.set_angle(Motor.BL_ELBOW, 90)    

    def inverse_positioning(self, shoulder, elbow, x, y, z=0, hip=None, right=True):
        '''
        Positions the end effector at a given position based on cartesian coordinates in 
        centimeter units and with respect to the should motor of the
        :param shoulder: motor id used for the shoulder
        :param elbow: motor id used for the elbow
        :param x: cartesian x with respect to shoulder motor (forward/back)
        :param y: cartesian y with respect to shoulder motor (up/down)
        :param z: cartesian z with respect to shoulder motor (left/right)
        :param hip: motor id used for the hip
        :param right: a boolean that flips the logic for left and right side to properly map "forward direction"
        :return: a list containing the appropriate angle for the shoulder and elbow
        '''
        L=2
        y_prime = -math.sqrt((z+L)**2 + y**2)
        thetaz = math.atan2(z+L,abs(y))-math.atan2(L,abs(y_prime))
        print(thetaz/math.pi*180)

        elbow_offset = 20
        shoulder_offset = 10
        a1 = self.upper_leg_length
        a2 = self.lower_leg_length

        c2 = (x**2+y_prime**2-a1**2-a2**2)/(2*a1*a2)
        s2 = math.sqrt(1-c2**2)
        theta2 = math.atan2(s2,c2)
        c2 = math.cos(theta2)
        s2 = math.sin(theta2)

        c1 = (x*(a1+(a2*c2)) + y_prime*(a2*s2))/(x**2+y_prime**2)
        s1 = (y_prime*(a1+(a2*c2)) - x*(a2*s2))/(x**2+y_prime**2)
        theta1 = math.atan2(s1,c1)
        # generate positions with respect to robot motors
        theta_shoulder = -theta1
        theta_elbow = theta_shoulder - theta2
        theta_hip = 0
        if right:
            theta_shoulder = 180 - self.rad_to_degree(theta_shoulder) + shoulder_offset
            theta_elbow = 130 - self.rad_to_degree(theta_elbow) + elbow_offset
            if hip:
                theta_hip = 90 - self.rad_to_degree(thetaz)
        else:
            theta_shoulder = self.rad_to_degree(theta_shoulder) - shoulder_offset
            theta_elbow = 50 + self.rad_to_degree(theta_elbow) - elbow_offset
            if hip:
                theta_hip = 90 + self.rad_to_degree(thetaz)
        self.set_angle(shoulder, theta_shoulder)
        self.set_angle(elbow, theta_elbow)
        if hip:
            self.set_angle(hip, theta_hip)
        # print("theta shoulder:",theta_shoulder,"\ttheta_elbow:",theta_elbow)
        return [theta_shoulder, theta_elbow]

    def leg_position(self, leg_id, x, y, z=0):
        """
        wrapper for inverse position that makes it easier to control each leg for making fixed paths
        :param led_id: string for the leg to be manipulated
        :param x: cartesian x with respect to shoulder motor (forward/back)
        :param y: cartesian y with respect to shoulder motor (up/down)
        :param z: cartesian z with respect to shoulder motor (left/right)
        """
        if leg_id == 'FL':
            self.inverse_positioning(Motor.FL_SHOULDER, Motor.FL_ELBOW, x, y, z=z, hip=Motor.FL_HIP, right=False)
        if leg_id == 'FR':
            self.inverse_positioning(Motor.FR_SHOULDER, Motor.FR_ELBOW, x, y, z=z, hip=Motor.FR_HIP, right=True)
        if leg_id == 'BL':
            self.inverse_positioning(Motor.BL_SHOULDER, Motor.BL_ELBOW, x, y, right=False)
        if leg_id == 'BR':
            self.inverse_positioning(Motor.BR_SHOULDER, Motor.BR_ELBOW, x, y, right=True)

    def move(self, controller=None):
        """
        Walks around based on the controller inputed momentum.
        :param controller: the controller that is called to determine the robot momentum
        """
        def main(win):
            win.nodelay(True)
            key=""
            win.clear()                
            momentum = np.asarray([0,0,1],dtype=np.float32)
            string =  "forward: " + str(momentum[0]) + "sideways: " + str(momentum[1])
            win.addstr(string)
            key = None
            step_size = 1
            index = 1
            # Generate footstep
            s_vals = np.linspace(0.0, 1.0, 20)
            
            step_nodes = np.asfortranarray([
                [-1.0, -1.0, 1.0, 1.0],
                [-1.0, -1.0, 1.0, 1.0],
                [-15.0, -10, -10, -15.0],
            ])
            curve = bezier.Curve(step_nodes, degree=3)
            step = curve.evaluate_multi(s_vals)

            slide_nodes = np.asfortranarray([
                [1.0, -1.0],
                [1.0, -1.0],
                [-15.0, -15],
            ])
            curve = bezier.Curve(slide_nodes, degree=1)
            slide = curve.evaluate_multi(s_vals)

            motion = np.concatenate((step,slide), axis=1)
            x_range = 4
            z_range = 4
            while True:
                try:
                    key = win.getkey()
                    curses.flushinp()
                except:
                    key = None      
                win.clear()
                if key == 'w':
                    if momentum[0] < x_range:
                        momentum[0]+= step_size
                elif key == 's':
                    if momentum[0] > -x_range:
                        momentum[0]-= step_size
                if key == 'a':
                    if momentum[1] > -z_range:
                        momentum[1]-= step_size
                elif key == 'd':
                    if momentum[1] < z_range:
                        momentum[1]+= step_size

                string =  "x: " + str(round(momentum[0],2)) + "   y: " + str(round(momentum[1],2))
                win.addstr(string)
                if key == os.linesep:
                    break 
                
                tragectory = motion * momentum[:, None]
                x,z,y = tragectory
                # 
                i1 = index%40
                i2 = (index+20)%40 
                # Apply movement based movement
                self.inverse_positioning(Motor.FR_SHOULDER,Motor.FR_ELBOW,x[i1],y[i1],z=z[i1],hip=Motor.FR_HIP,right=True)
                self.inverse_positioning(Motor.BR_SHOULDER,Motor.BR_ELBOW,x[i2],y[i2],right=True)
                self.inverse_positioning(Motor.FL_SHOULDER,Motor.FL_ELBOW,x[i2],y[i2],z=-z[i2],hip=Motor.FL_HIP,right=False)
                self.inverse_positioning(Motor.BL_SHOULDER,Motor.BL_ELBOW,x[i1],y[i1],right=False)
                index += 1
        curses.wrapper(main) 

if __name__ == "__main__":
    r = Quadruped()
    r.calibrate()
    r.move()
