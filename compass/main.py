import cv2
import numpy as np
import itertools

cv2.namedWindow("img")
cap = cv2.VideoCapture(1)
M = None

history = []

while True:
    result, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.circle(frame, (frame.shape[1] // 2, frame.shape[0] // 2), 5, (0, 0, 255), -1)

    lower = np.array([0, 90, 50])
    upper = np.array([10, 255, 255])
    lower2 = np.array([170, 90, 50])
    upper2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower, upper)
    mask2 = cv2.inRange(hsv, lower, upper)
    mask = cv2.bitwise_or(mask1, mask2)

    blr = cv2.blur(mask, (5, 5))

    _, cnts, _ = cv2.findContours(blr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if cnts:
        c = max(cnts, key=cv2.contourArea)
        cv2.drawContours(frame, c, -1, (0, 255, 0), 5)

        pts = [i.reshape((-1)) for i in c]
        
        m = cv2.moments(c)
        cx = int(m["m10"] / m["m00"])
        cy = int(m["m01"] / m["m00"])
        ce = np.array([cx, cy])

        cv2.circle(frame, (cx, cy), 5, (255, 0, 255), 5, -1)
        cv2.line(frame, (cx, cy), (frame.shape[1] // 2, frame.shape[0] // 2), (0, 255, 255), 5)

        vx = frame.shape[1] // 2 - cx
        vy = cy - frame.shape[0] // 2

        ang = np.degrees(np.arctan2(vy, vx))
        history.append(ang)
        if len(history) > 5:
            del history[0]
        if max(history) - min(history) > 20:
            history = [ang]

        nang = sum(history) / len(history)
        print(nang)

        py = 100 * np.sin(np.radians(nang))
        px = 100 * np.cos(np.radians(nang))

        pointer = np.array([px, -py])
        pointer = pointer / np.linalg.norm(pointer)
        pointer = pointer * 50

        cv2.line(frame, (frame.shape[1] // 2, frame.shape[0] // 2), (frame.shape[1] // 2 + int(pointer[0]), frame.shape[0] // 2 + int(pointer[1])), (255, 100, 0), 5)
        cv2.putText(frame, "North: " + str(round(nang * 1000) / 1000) + "deg", (0, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow("img", frame)
    if (cv2.waitKey(1) == 27):
        M = c
        break

cv2.destroyAllWindows()
