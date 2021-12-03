import numpy as np
import time
import os
import bezier
import curses

def main(win):
    win.nodelay(True)
    key=""
    win.clear()                
    momentum = np.asarray([0,0,1],dtype=np.float)
    string =  "forward: " + str(momentum[0]) + "sideways: " + str(momentum[1])
    win.addstr(string)
    key = None
    step_size = 0.05
    index = 1
    while True:
        try:
            key = win.getkey()
        except:
            key = None      
        win.clear()
        if key == 'w':
            if momentum[0] < 1:
                momentum[0]+= step_size
        elif key == 's':
            if momentum[0] > -1:
                momentum[0]-= step_size
        else:
            if momentum[0] > step_size:
                momentum[0] -= step_size
            elif momentum[0] < -step_size:
                momentum[0] += step_size
            else:
                momentum[0] = 0
        if key == 'a':
            if momentum[1] < 1:
                momentum[1]+= step_size
        elif key == 'd':
            if momentum[1] > -1:
                momentum[1]-= step_size
        else:
            if momentum[1] > step_size:
                momentum[-1] -= step_size
            elif momentum[1] < -step_size:
                momentum[1] += step_size
            else:
                momentum[1] = 0
        string =  "forward: " + str(round(momentum[0],2)) + "   sideways: " + str(round(momentum[1],2))
        win.addstr(string)
        if key == os.linesep:
            break 
        # # Generate footstep
        # s_vals = np.linspace(0.0, 1.0, 20)
        
        # step_nodes = np.asfortranarray([
        #     [-2.0, -2.0, 2.0, 2.0],
        #     [-2.0, -2.0, 2.0, 2.0],
        #     [-15.0, -10, -10, -15.0],
        # ])
        # curve = bezier.Curve(step_nodes, degree=3)
        # step = curve.evaluate_multi(s_vals)

        # slide_nodes = np.asfortranarray([
        #     [2.0, -2.0],
        #     [2.0, -2.0],
        #     [-15.0, -15],
        # ])
        # curve = bezier.Curve(slide_nodes, degree=1)
        # slide = curve.evaluate_multi(s_vals)

        # motion = np.concatenate((step,slide), axis=1)
        # tragectory = motion * momentum[:, None]
        # x,z,y = tragectory
        # # 
        # i1 = index%40
        # i2 = (index+20)%40 
        # Apply movement
        # self.test_pos(Motor.FR_SHOULDER,Motor.FR_ELBOW,x[i1],y[i1],z=z[i1],hip=Motor.FR_HIP,right=True)
        # self.test_pos(Motor.BR_SHOULDER,Motor.BR_ELBOW,x[i2],y[i2],right=True)
        # self.test_pos(Motor.FL_SHOULDER,Motor.FL_ELBOW,x[i2],y[i2],z=-z[i2],hip=Motor.FL_HIP,right=False)
        # self.test_pos(Motor.BL_SHOULDER,Motor.BL_ELBOW,x[i1],y[i1],right=False)

        index += 1
        time.sleep(0.05)
curses.wrapper(main)     