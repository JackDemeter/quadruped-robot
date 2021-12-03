import curses
import os
import time
import bezier
import numpy as np

def main(win):
    win.nodelay(True)
    key=""
    win.clear()                
    momentum = [0,0]
    string =  "forward: " + str(momentum[0]) + "sideways: " + str(momentum[1])
    win.addstr(string)
    key = None
    step_size = 0.05
    while True:
        # Read WASD keys and increase our momentum based on those
        try:
            key = win.getkey()
            curses.flushinp()
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
        string =  "forward: " + str(round(momentum[0],2)) + "\tsideways: " + str(round(momentum[1],2))
        win.addstr(string)

        # exit on enter key
        if key == os.linesep:
            break
        # Generate foot tragectory
        step_nodes = np.asfortranarray([
            [-2.0*momentum[0], -2.0, 2.0, 2.0],
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


curses.wrapper(main)