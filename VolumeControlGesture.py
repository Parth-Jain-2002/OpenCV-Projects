import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    cv2.imshow("Image",img)
    cv2.waitKey(1)