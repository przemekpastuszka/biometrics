import cv2

im_gray = cv2.imread("image\rthumb.png", 2)
(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = 190
im_binary = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

cv2.imwrite("image\rthumb_binary.png", im_bw)
