import cv2
import numpy as np
 
img = cv2.imread("road.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 600,600)

lines = cv2.HoughLinesP(edges,1, np.pi/180,50, maxLineGap=100)

for line in lines:
    print(line)

    cv2.circle(img,(line[0][0],line[0][1]), 20,(255,255,0), -1)

    
    x1, y1, x2 ,y2 = line[0]
    cv2.line(img, (x1,y1), (x2, y2), (0,255,0), 3)

cv2.imshow("lines", img)
cv2.imshow("canny", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()