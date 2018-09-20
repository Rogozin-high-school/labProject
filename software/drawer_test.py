from module.datahub.listener import init, get_value 
import cv2
import numpy as np
import json

# Width
w = 800
# Height
h = 800

init()
img = np.zeros([w, h, 3], np.uint8)
cv2.line(img, (0, (int)(h/2)), (w, (int)(h/2)), (255, 255, 255), 3)
cv2.line(img, ((int)(w/2), 0), ((int)(w/2), h), (255, 255, 255), 3)

history = []


while True:
    cv2.imshow("a", img)
    x = get_value("sat_mag")
    if x is not None:
        pt = x[0][:2]
        if not pt in history:
            history.append(pt)
        print(pt[0])
        cv2.circle(img, ((int)(w/2) +  int(pt[1]) * 3, (int)(h/2) - int(pt[0]) * 3), 3, (0, 0, 255), -1)
    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

with open("log.json", "w") as f:
    f.write(json.dumps(history))

cv2.destroyAllWindows()
