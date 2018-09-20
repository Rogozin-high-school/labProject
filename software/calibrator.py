import json
import numpy as np 
import cv2

with open("log.json", "r") as f:
    history = json.loads(f.read())

min_x = min(history, key=lambda c: c[0])[0]
max_x = max(history, key=lambda c: c[0])[0]
min_y = min(history, key=lambda c: c[1])[1]
max_y = max(history, key=lambda c: c[1])[1]

# Maor/Nir 20.9.2018
# After Yotam's calibration:
# The ratio between the ellipse's height to width is approx. 5:2
# So let's multiply the width by 2.5.
horizontal_stretch = 1.9

earth_b = 40 # micro Tesla

bias_x = (min_x + max_x) / 2
bias_y = (min_y + max_y) / 2

diam_x = (max_x - min_x)
diam_y = (max_y - min_y)

scalef_x = (2 * earth_b) / diam_x
scalef_y = (2 * earth_b) / diam_y

newpts = [[(c[0] - bias_x) * horizontal_stretch / scalef_x, (c[1] - bias_y) / scalef_y] for c in history]

print("Min x: " + str(min_x))
print("Max x: " + str(max_x))
print("Min y: " + str(min_y))
print("Max y: " + str(max_y))
print("Bias x: " + str(bias_x))
print("Bias y: " + str(bias_y))
print("SF x: " + str(scalef_x))
print("SF y: " + str(scalef_y))

img = np.zeros([800, 800, 3], np.uint8)
cv2.line(img, (0, 400), (800, 400), (255, 255, 255), 3)
cv2.line(img, (400, 0), (400, 800), (255, 255, 255), 3)

for pt in history:
    cv2.circle(img, (400 +  int(pt[0]) * 3, 400 - int(pt[1]) * 3), 3, (0, 0, 255), -1)

for pt in newpts:
    cv2.circle(img, (400 +  int(pt[0]) * 3, 400 - int(pt[1]) * 3), 3, (0, 255, 0), -1)

# x, y = 100, 0

# cv2.circle(img, (400 + x, 400 - y), 3, (255, 0, 255), -1)

cv2.imshow("a", img)
cv2.waitKey(0)
cv2.destroyAllWindows()