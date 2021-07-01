#This is a python project to control brightness using gesture control

import cv2
import numpy as np
import time
import handtrackingmodule as htm
import math
import screen_brightness_control as sbc

#Video left at 3:10:07

############################
wCam,hCam=1200,1200
############################

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
cTime=0

detector = htm.handDetector(detectionCon=0.7)


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) != 0:
        #print(lmList[4],lmList[8])

        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)

        brightness = np.interp(length,[30,250],[0,100])
        print(int(length),brightness)
        sbc.set_brightness(int(brightness))

        if length<30:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}',(10,20),cv2.FONT_HERSHEY_COMPLEX,
                0.8,(255,255,255),1)

    cv2.imshow("Image",img)
    cv2.waitKey(1)