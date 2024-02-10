import cv2 
import numpy as np
import pigpio
import os
import time

cap = cv2.VideoCapture(0)


angle = 1400
esc = 1540
prev_error = 0
crazy_turn = False
count_for_turn = 0

os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(2)


ESC = 17 
STEER = 18 

pi = pigpio.pi()
time.sleep(2)

print("podau signal")

pi.set_servo_pulsewidth(ESC, 1000)#2400 left , 800
time.sleep(2)
pi.set_servo_pulsewidth(ESC, 1500)#2400 left , 800
time.sleep(2)

# pi.set_servo_pulsewidth(STEER, 1800)
# time.sleep(2)

pi.set_servo_pulsewidth(STEER, 1400) #1700 1100 
time.sleep(2)

SIZE = [200, 360]
src = np.float32([[5, 200], 
                  [350, 200],
                  [300, 120], #top right
                  [55, 120]])

src_draw = np.array(src, dtype=np.int32)

dst = np.float32([[0, SIZE[0]], 
                  [SIZE[1], SIZE[0]],
                  [SIZE[1], 0],
                  [0, 0]])


while True:
    ret, frame = cap.read()
    if not ret:
        break
#frame = cv2.imread("foto/2.jpg")
    try:
        resized = cv2.resize(frame, (SIZE[1], SIZE[0]))

        r_channel = resized[:,:,2]
        binary = np.zeros_like(r_channel)
        binary[(r_channel > 200)] = 1

        hls = cv2.cvtColor(resized, cv2.COLOR_BGR2HLS)
        s_channel = resized[:,:,2]
        binary2 = np.zeros_like(s_channel)
        binary2[(r_channel > 250)] = 1 #if road light we above 

        allBinary = np.zeros_like(binary)
        allBinary[(binary==1) | (binary2==1)] =255
        

        allBinary_visual = allBinary.copy()
        cv2.polylines(allBinary_visual, [src_draw], True, (255, 0,255))
        

        M = cv2.getPerspectiveTransform(src, dst)
        warped = cv2.warpPerspective(allBinary, M, (SIZE[1], SIZE[0]), flags=cv2.INTER_LINEAR)

    

        histogram = np.sum(warped[warped.shape[0]//2:, :],axis=0)
        midpoint = histogram.shape[0]//2
        IndWhitestColumnL = np.argmax(histogram[:midpoint])
        IndWhitestColumnR = np.argmax(histogram[midpoint:]) + midpoint
        warped_visual = warped.copy()
        cv2.line(warped_visual, (IndWhitestColumnL, 0), (IndWhitestColumnL, warped_visual.shape[0]), 110, 2)
        cv2.line(warped_visual, (IndWhitestColumnR, 0), (IndWhitestColumnR, warped_visual.shape[0]), 110, 2)
        

        nwindows = 9
        window_height = int(warped.shape[0]/nwindows)
        window_half_width = 25

        XcenterLeftWindow = IndWhitestColumnL
        XcenterRightWindow = IndWhitestColumnR

        left_lane_inds = np.array([], dtype= np.int16)
        right_lane_inds = np.array([], dtype= np.int16)

        out_img = np.dstack((warped, warped, warped))

        nonzero = warped.nonzero()
        WhitePixelIndY = np.array(nonzero[0])
        WhitePixelIndX = np.array(nonzero[1])


        for window in range(nwindows):

            win_y1 = warped.shape[0] - (window+1) * window_height
            win_y2 = warped.shape[0] - (window) * window_height

            left_win_x1 = XcenterLeftWindow - window_half_width
            left_win_x2 = XcenterLeftWindow + window_half_width

            right_win_x1 = XcenterRightWindow - window_half_width
            right_win_x2 = XcenterRightWindow + window_half_width

            cv2.rectangle(out_img, (left_win_x1, win_y1), (left_win_x2, win_y2), (50 + window *21,0,0),2)
            cv2.rectangle(out_img, (right_win_x1, win_y1), (right_win_x2, win_y2), (0 ,0 ,50 + window * 21), 2)
            

            good_left_inds = ((WhitePixelIndY>=win_y1) & (WhitePixelIndY<=win_y2) & 
            (WhitePixelIndX>=left_win_x1) & (WhitePixelIndX<=left_win_x2)).nonzero()[0]

            good_right_inds = ((WhitePixelIndY>=win_y1) & (WhitePixelIndY<=win_y2) & 
            (WhitePixelIndX>=right_win_x1) & (WhitePixelIndX<=right_win_x2)).nonzero()[0]

            left_lane_inds = np.concatenate((left_lane_inds, good_left_inds))
            right_lane_inds = np.concatenate((right_lane_inds, good_right_inds))

            if len(good_left_inds) > 50:
                XcenterLeftWindow = int(np.mean(WhitePixelIndX[good_left_inds]))
            if len(good_right_inds) > 50:
                XcenterRightWindow = int(np.mean(WhitePixelIndX[good_right_inds]))

        out_img[WhitePixelIndY[left_lane_inds], WhitePixelIndX[left_lane_inds]] = [255, 0,0]
        out_img[WhitePixelIndY[right_lane_inds], WhitePixelIndX[right_lane_inds]] = [0,0,255]
        #cv2.imshow("Lane", out_img) 

        leftx = WhitePixelIndX[left_lane_inds]
        lefty = WhitePixelIndY[left_lane_inds]
        rightx = WhitePixelIndX[right_lane_inds]
        righty = WhitePixelIndY[right_lane_inds]


        left_fit = np.polyfit(lefty, leftx, 2)
        right_fit = np.polyfit(righty, rightx, 2)

        center_fit = ((left_fit+right_fit)/2)

        #print(out_img.shape[0])

        high_point = 50
        low_point = 150

        low_gor_ind = ((center_fit[0]) * (low_point ** 2)+ center_fit[1] * low_point + center_fit[2])
        high_gor_ind = ((center_fit[0]) * (high_point ** 2)+ center_fit[1] * high_point + center_fit[2])

        # for ver_ind in range(out_img.shape[0]):
        #     gor_ind = ((center_fit[0]) * (ver_ind ** 2)+
        #             center_fit[1] * ver_ind +
        #             center_fit[2])
            
        #     high_point = 50
        #     low_point = 150

        #     if ver_ind == low_point:
        #         #cv2.circle(out_img, (int(gor_ind), int(ver_ind)), 2, (0,0,255), 5)
        #         low_gor_ind = int(gor_ind)
        #     elif ver_ind == high_point:
        #         #cv2.circle(out_img, (int(gor_ind), int(ver_ind)), 2, (0,0,255), 5)
        #         high_gor_ind = int(gor_ind)
        #     else:
        #         cv2.circle(out_img, (int(gor_ind), int(ver_ind)), 2, (255,0,255), 1)


        #print(low_gor_ind, high_gor_ind)
        cur_error = int(high_gor_ind - low_gor_ind)
        print("cur_error", cur_error)

        if abs(cur_error) > 30: #crazy turn
            count_for_turn+=1
            if count_for_turn > 5:
                TURN = True
            # if not crazy_turn:
            #     start = time.time()
            # crazy_turn = True

        # if abs(cur_error - prev_error) > 2:

        #     if cur_error > 0 and angle > 1100:
        #         angle-=20
        #     elif cur_error < 0 and angle < 1700:
        #         angle+=20

        prev_error = cur_error
        #print(angle)
        
        pi.set_servo_pulsewidth(STEER, angle)
        #time.sleep(0.1)
        
        

        pi.set_servo_pulsewidth(ESC, esc)
        #time.sleep(0.2)

        #cv2.imshow("frame", frame)
        # cv2.imshow("binary", allBinary)
        # cv2.imshow("polygon", allBinary_visual)
        # # cv2.imshow("warped", warped)
        # # cv2.imshow("WhitestColumn", warped_visual)
        # # cv2.imshow("windows", out_img)
        # cv2.imshow("CenterLine", out_img)

        # k = cv2.waitKey(1)
        # if k == ord("q"):
        #     os.system("sudo killall pigpiod")
        #     break

        # elif k == ord("w"):
        #     angle+=100

        # elif k == ord("s"):
        #     angle-=100

        # elif k == ord("d"):
        #     angle+=10
        # elif k == ord("a"):
        #     angle-=10
        


        # elif k == ord("i"):
        #     esc+=100

        # elif k == ord("k"):
        #     esc-=100

        # elif k == ord("l"):
        #     esc+=10
        # elif k == ord("j"):
        #     esc-=10
        #print(esc)
        print(angle)

    except:
        pass


        

