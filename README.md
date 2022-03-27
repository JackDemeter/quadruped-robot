# quadruped-robot
![quadruped](https://user-images.githubusercontent.com/24850401/160302298-203e922e-81ea-4b7f-a4e0-efc720e2eb74.JPG)

A quadruped robot for a university capstone project. The associated CAD files can be found on [GrabCad](https://grabcad.com/library/quadruped-robot-w-code-1)

## Installation
To use this code simply download the repository onto the raspberry pi, install the requirements, set up the pi for camera and the servo library usage, and run `python3 control-quadruped`. This will start the walking motion and print out the pi's IP and port. Run the controller on your computer, setting the IP and port given by the pi and the robot will start taking momentum data from the controller.

### Computer vision controller
The computer vision controller has a few extra steps that can seen here.
Specific to the computer-vision controller you will also need to run `python3 image-sender/rpi_send_video.py` to pass camera data to you computer, in this case make sure to change the IP and Port to the ones used by the controller.

## Project Info
### Intro
This project was created with the intention of developing a robot that can follow users as a proof of concept for a larger assistant quadruped. The associated code allows for keyboard based control or computer-vision-based control and was structured such that new controllers can easily be implemented by sending momentum packets to the raspberry pi.

### Robot Control
The robot uses an inverse kinematic model to determine how to position the foot in the requested location. Some of the math for this can be seen in the model directory with the jupyter notebook 

#TODO: clean up jupyter notebook (and probably all other files)
#TODO: add set up instructions for initial robot building
#TODO: consistent file/folder naming
#TODO: add wiki? and finish readme
