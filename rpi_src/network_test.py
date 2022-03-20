import socket
import numpy as np
from array import array

def Main():

    host='192.168.2.115' #client ip
    port = 5561
    
    server = ('192.168.2.135', 5014)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    
    message = input("-> ")
    while message !='q':
        l = [float(i) for i in message.split(" ")]
        float_array = np.array(l)
        s.sendto(float_array.tobytes(), server)
        message = input("-> ")
    s.close()

if __name__=='__main__':
    Main()