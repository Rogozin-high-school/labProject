import cv2
import numpy as np

cv2.namedWindow("img")
cap = cv2.VideoCapture(1)

while True:
    result, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 0])
    upper = np.array([100, 255, 100])
    mask = cv2.inRange(hsv, lower, upper)
    blr = cv2.blur(mask, (5, 5))
    cv2.imshow("img", mask)
    if (cv2.waitKey(1) == 27):
        break

cv2.destroyAllWindows()
