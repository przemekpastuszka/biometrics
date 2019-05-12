import cv2

im_gray = cv2.imread("images/right3.jpg", 2)
(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = 127
im_binary = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

cv2.imwrite("images/right3_binary.jpg", im_bw)
