import cv2 
import os

def setup(cap):
    path = "videos"

    frame_width = int(cap.get(3)) 
    frame_height = int(cap.get(4)) 
    size = (frame_width, frame_height)  #set the image size only this way   

    if not os.path.exists(path): 
        os.mkdir(path)

    try:
        last_add_file = os.listdir("videos")[-1]
        last_name = last_add_file.split('.')[0]
        new_name = str(int(last_name)+1)
    except:
        new_name = "0"


    out = cv2.VideoWriter(f"videos/{new_name}.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 20.0, size)
    return out



