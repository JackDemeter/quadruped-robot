import socket
import numpy as np
import argparse
import keyboard

from utils.ip_helper import create_socket_connection 

def controller(pi_ip, pi_port, accel = 0.002, bound=4, return_to_zero=False):

    s = create_socket_connection()

    server = (pi_ip, pi_port)
    momentum = np.array([0.,0.,1.,0.]) # Control [x,z,y,quit] telemetry
    close = False
    while not close:
        moved = False
        if keyboard.is_pressed('w'):
            momentum[0] = min(momentum[0]+accel, bound)
            moved = True
        if keyboard.is_pressed('s'):
            momentum[0] = max(momentum[0]-accel, -bound)
            moved = True
        if keyboard.is_pressed('a'):
            momentum[1] = max(momentum[1]-accel, -bound)
            moved = True
        if keyboard.is_pressed('d'):
            momentum[1] = min(momentum[1]+accel, bound)
            moved = True
        if keyboard.is_pressed('p'):
            momentum[3] = 1
            close = True
            moved = True
        
        # Not controlling the robot will slowly come to a stop
        if return_to_zero and not moved:
            moved = True
            if momentum[0] > 0:
                momentum[0] = momentum[0]-accel
            elif momentum[0] < 0:
                momentum[0] = momentum[0]+accel
            if momentum[1] > 0:
                momentum[1] = momentum[1]-accel
            elif momentum[1] < 0:
                momentum[1] = momentum[1]+accel
        if moved:
            s.sendto(momentum.tobytes(), server)
            print(momentum)
    s.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pi_ip')
    parser.add_argument('pi_port', type=int) 
    parser.add_argument('--accel', type=float, default=0.002)
    parser.add_argument('--bound', type=int, default=4)
    parser.add_argument('--return_to_zero', action='store_true')
    args = parser.parse_args()

    controller(args.pi_ip, args.pi_port, args.accel, args.bound, args.return_to_zero)