import numpy as np
import socket
from utils.ip_helper import create_socket_connection

s = create_socket_connection()

def controller(momentum):
    try:
        s.settimeout(0.00001)
        data, addr = s.recvfrom(1024)
        if data: 
            momentum = np.frombuffer(data)
    except:
        pass
    return momentum

if __name__ == "__main__":
    import numpy as np

    momentum = np.asarray([0,0,1,0],dtype=np.float32)
    lm = momentum
    while True:
        momentum = controller(momentum)
        if (lm != momentum).any():
            print(momentum)
            lm=momentum