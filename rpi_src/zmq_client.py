# run this program on each RPi to send a labelled image stream
import socket
import time
from imutils.video import VideoStream
import imagezmq
import numpy as np

sender = imagezmq.ImageSender(connect_to='tcp://192.168.2.47:5555')

rpi_name = socket.gethostname()
cam = VideoStream('/dev/video0').start()
time.sleep(2.0)     # allow pi camera sensor to warm up
while True:         # send images as stream until Ctrl-C
    image = cam.read()
    data = sender.send_image(rpi_name, image)
    data = np.frombuffer(data, dtype="int32")  # Numpy interprets buffer as a 1D array - reshape with two columns
    np.reshape(data, (int(data.size/2),2))
