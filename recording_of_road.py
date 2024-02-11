import cv2 
import os


path = "videos"

video = cv2.VideoCapture(0)

frame_width = int(video.get(3)) 
frame_height = int(video.get(4)) 
size = (frame_width, frame_height)  #set the image size only this way   

if not os.path.exists(path): 
    os.mkdir(path)

try:
    last_add_file = os.listdir("videos")[-1]
    last_name = last_add_file.split('.')[0]
    new_name = str(int(last_name)+1)
except:
    new_name = "0"


out = cv2.VideoWriter(f"videos/{new_name}.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 60.0, size)

while True:
    ret, frame = video.read()
    if not ret:
        break

    out.write(frame)  #adding a frame to a stream
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

out.release()