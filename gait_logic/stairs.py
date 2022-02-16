from adafruit_servokit import ServoKit
from enum import IntEnum
import time
import math
import bezier
import numpy as np
import curses
import os

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

    def test_pos(self,shoulder,elbow,x,y,z=0,hip=None,right=True):
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
        self.kit.servo[shoulder].angle = theta_shoulder
        self.kit.servo[elbow].angle = theta_elbow
        if hip:
            self.kit.servo[hip].angle = theta_hip
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
        s_vals = np.linspace(0.0, 1.0, 20)
        slide = curve.evaluate_multi(s_vals)

        foot_motion = step
        for x,y in zip(slide[0],slide[1]):
            new_x=np.append(foot_motion[0],x)
            new_y=np.append(foot_motion[1],y)
            foot_motion = [new_x,new_y]
        
        x = foot_motion[0]
        y = foot_motion[1]
        
        for cycle in range(cycles):
            for index in range(40):
                self.test_pos(x[index],y[index],Motor.FR_SHOULDER,Motor.FR_ELBOW,right=True)
                self.test_pos(x[(index+20)%40],y[(index+20)%40],Motor.BR_SHOULDER,Motor.BR_ELBOW,right=True)
                self.test_pos(x[(index+20)%40],y[(index+20)%40],Motor.FL_SHOULDER,Motor.FL_ELBOW,right=False)
                self.test_pos(x[index],y[index],Motor.BL_SHOULDER,Motor.BL_ELBOW,right=False)
                time.sleep(0.01)

    def rad_to_degree(self,rad):
        return rad*180/math.pi

    def test_turn(self,cycles=1):
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
        s_vals = np.linspace(0.0, 1.0, 20)
        slide = curve.evaluate_multi(s_vals)

        turn_motion = step
        for x,y,z in zip(slide[0],slide[1],slide[2]):
            new_x=np.append(turn_motion[0],x)
            new_y=np.append(turn_motion[1],y)
            turn_motion = [new_x,new_y]

        z = turn_motion[0]
        y = turn_motion[1]
        for cycle in range(cycles):
            for index in range(40):
                    self.test_pos(Motor.FR_SHOULDER,Motor.FR_ELBOW,0,y[index],z=z[index],hip=Motor.FR_HIP,right=True)
                    self.test_pos(Motor.BR_SHOULDER,Motor.BR_ELBOW,0,y[(index+20)%40],right=True)
                    self.test_pos(Motor.FL_SHOULDER,Motor.FL_ELBOW,0,y[(index+20)%40],z=-z[(index+20)%40],hip=Motor.FL_HIP,right=False)
                    self.test_pos(Motor.BL_SHOULDER,Motor.BL_ELBOW,0,y[(index)%40],right=False)


    def WASD(self):
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
                [-2.0, -2.0, 2.0, 2.0],
                [-2.0, -2.0, 2.0, 2.0],
                [-18.0, -6, -6, -18.0],
            ])
            curve = bezier.Curve(step_nodes, degree=3)
            step = curve.evaluate_multi(s_vals)

            slide_nodes = np.asfortranarray([
                [2.0, -2.0],
                [2.0, -2.0],
                [-18.0, -18],
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
                self.test_pos(Motor.FR_SHOULDER,Motor.FR_ELBOW,x[i1],y[i1],z=z[i1],hip=Motor.FR_HIP,right=True)
                self.test_pos(Motor.BR_SHOULDER,Motor.BR_ELBOW,x[i2]-2,y[i2],right=True)
                self.test_pos(Motor.FL_SHOULDER,Motor.FL_ELBOW,x[i2]-4,y[i2],z=-z[i2],hip=Motor.FL_HIP,right=False)
                self.test_pos(Motor.BL_SHOULDER,Motor.BL_ELBOW,x[i1]-3,y[i1],right=False)
                index += 1
                time.sleep(0.003)
                
        curses.wrapper(main)  

    def stair(self):
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
                [-10.0, -3.0, -3.0, -10.0],
            ])
            curve = bezier.Curve(step_nodes, degree=3)
            step = curve.evaluate_multi(s_vals)


            s_vals = np.linspace(0.0, 1.0, 60)
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
                i1 = index%80
                i2 = (index+20)%80 
                i3 = (index+40)%80 
                i4 = (index+60)%80 
                # Apply movement based movement
                self.test_pos(Motor.FR_SHOULDER,Motor.FR_ELBOW,x[i1],y[i1],z=z[i1],hip=Motor.FR_HIP,right=True)
                self.test_pos(Motor.BR_SHOULDER,Motor.BR_ELBOW,x[i2],y[i2]-1,right=True)
                self.test_pos(Motor.FL_SHOULDER,Motor.FL_ELBOW,x[i3],y[i3],z=-z[i3],hip=Motor.FL_HIP,right=False)
                self.test_pos(Motor.BL_SHOULDER,Motor.BL_ELBOW,x[i4],y[i4]-1,right=False)
                index += 1
                time.sleep(0.01)
        curses.wrapper(main)   


if __name__ == "__main__":
    r = Quadruped()
    r.calibrate()
    r.WASD()
    # r.stair()
