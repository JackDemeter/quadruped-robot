# run this program on the Mac to display image streams from multiple RPis
import cv2
import imagezmq
image_hub = imagezmq.ImageHub()
vid_cod = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter("cam_video.avi", vid_cod, 5.0, (640,480))
count = 0
while True:  # show streamed images until Ctrl-C
    rpi_name, image = image_hub.recv_image()
    cv2.imshow(rpi_name, image) # 1 window for each RPi
    key = cv2.waitKey(1)
    image_hub.send_reply(b'OK')
    if key == ord('q'):
        break
    if rpi_name:
        if count %100 ==0:
            print('reading')
        count += 1
        output.write(image)
        

output.release()

