import cv2
import mediapipe as mp
import time
import os
import handtrackingmodule as htm

wCam , hCam = 640 ,480

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

folderPath = "FingerImages"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    #print(f'{folderPath}/{imPath}')
    overlayList.append(image)
    
print(len(overlayList))
pTime=0
cTime=0

detector=htm.handDetector(detectionCon=0.75)

tipIds  = [4,8,12,16,20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    #print(lmList)

    if len(lmList)!=0:
        fingers=[]

        #Thumb
        if lmList[1][1] > lmList[17][1]:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(0)
            else:
                fingers.append(1)


        #4 Fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-1][2]<lmList[tipIds[id]-2][2]<lmList[tipIds[id]-3][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        #print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        img[0:200,0:200] = cv2.resize(overlayList[totalFingers],(200,200))

        cv2.rectangle(img,(20,255),(170,425),(255,255,0),cv2.FILLED)
        cv2.putText(img,str(totalFingers),(45,395),cv2.FONT_HERSHEY_PLAIN,
                    10,(0,0,0),25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}', (500,30),cv2.FONT_HERSHEY_COMPLEX,
                1,(255,0,0),2)

    cv2.imshow("Image",img)
    cv2.waitKey(1)