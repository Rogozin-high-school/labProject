import cv2
import numpy as np
import itertools

def get_red(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 90, 50])
    upper = np.array([10, 255, 255])
    lower2 = np.array([170, 90, 50])
    upper2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower, upper)
    mask2 = cv2.inRange(hsv, lower, upper)
    mask = cv2.bitwise_or(mask1, mask2)
    return mask

def get_blue(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([100, 90, 50])
    upper = np.array([150, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    return mask

_ctrx = 0
_ctry = 0
_ctrc = 0
def get_center_contour(img):
    mask = get_blue(img)
    blr = cv2.blur(mask, (5, 5))
    _, cnts, _ = cv2.findContours(blr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if cnts:
        return max(cnts, key=cv2.contourArea)
    else:
        return None

def get_center_point(img):
    global _ctrx, _ctry, _ctrc
    c = get_center_contour(img)

    if c is not None:
        cv2.drawContours(img, c, -1, (255, 0, 0), 5)
        m = cv2.moments(c)
        x = int(m["m10"] / m["m00"])
        y = int(m["m01"] / m["m00"])
        cv2.circle(img, (x, y), 7, (255, 255, 0), -1)
        _ctrc += 1
        return x, y

    else:
        return 0, 0

def get_compass_contour(img):    
    mask = get_red(img)
    blr = cv2.blur(mask, (5, 5))
    _, cnts, _ = cv2.findContours(blr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if cnts:
        return max(cnts, key=cv2.contourArea)
    else:
        return None

cap = None

def init():
    global cap
    cap = cv2.VideoCapture(2)
    # cv2.namedWindow("Compass View")
history = []

def frame():
    global cap, history

    result, frame = cap.read()
    
    f1, f0 = get_center_point(frame)
    if f1 + f0 == 0:
        return

    # cv2.circle(frame, (f1, f0), 5, (255, 0, 0), -1)

    c = get_compass_contour(frame)
    d = get_center_contour(frame)
    ang = None
    if c is not None:
        cv2.drawContours(frame, c, -1, (0, 255, 0), 5)
        
        m = cv2.moments(c)
        cx = int(m["m10"] / m["m00"])
        cy = int(m["m01"] / m["m00"])
        ce = np.array([cx, cy])

        cv2.circle(frame, (cx, cy), 5, (255, 0, 255), 5, -1)
        cv2.line(frame, (cx, cy), (f1, f0), (0, 255, 255), 5)

        vx = f1 - cx
        vy = cy - f0

        ang = np.degrees(np.arctan2(vy, vx))

        history.append(ang)
        if len(history) > 5:
            del history[0]
        if max(history) - min(history) > 20:
            history = [ang]

        nang = sum(history) / len(history)

        py = np.sin(np.radians(nang))
        px = np.cos(np.radians(nang))

        pointer = np.array([px, -py])
        pointer = pointer / np.linalg.norm(pointer)
        pointer = pointer * 75

        cv2.line(frame, (f1, f0), (f1 + int(pointer[0]), f0 + int(pointer[1])), (255, 100, 0), 5)
        cv2.putText(frame, "North: " + str(round(nang * 1000) / 1000) + "deg", (0, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    # cv2.imshow("Compass View", frame)

    return ang, frame

def close():
    # cv2.destroyWindow("Compass View")
    pass