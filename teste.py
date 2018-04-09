import cv2
import numpy as np

img = np.zeros((2, 2, 3), dtype=np.int)
print img
img[0][0] = [0, 111, 1]
img[0][1] = [0, 210, 2]
img[1][0] = [1, 111, 3]
img[1][1] = [1, 149, 4]
print "============"
print img
cv2.imwrite('block.png',img)

img1 = cv2.imread("block.png")
print "lida ======"
print img1
