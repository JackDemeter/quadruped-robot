# Note that this library requires sudo privileges

import keyboard

def controller(momentum, accel=0.01, bound=4):
    """
    Update the momentum of the robot based on keyboard presses.
    :param momentum: the existing momentum parameter
    :param accel: how quickly the robot starts walking in a given direction
    :param bound: the max/min magnitude that the robot can walk at
    :returns: updated momentum array
    """
    if keyboard.is_pressed('w'):
        momentum[0] = min(momentum[0]+accel, bound)
        print('THIS')
    if keyboard.is_pressed('s'):
        momentum[0] = max(momentum[0]-accel, -bound)
    if keyboard.is_pressed('a'):
        momentum[1] = max(momentum[1]-accel, -bound)
    if keyboard.is_pressed('d'):
        momentum[1] = min(momentum[1]+accel, bound)
    return momentum

if __name__ == "__main__":
    import numpy as np

    momentum = np.asarray([0,0,1],dtype=np.float32)
    while True:
        momentum = controller(momentum)
        print(momentum)