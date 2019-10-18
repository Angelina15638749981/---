
#! /usr/bin/env python
# -*- coding:utf-8 -*-
import cv2
src = cv2.imread("d1.png")
gray_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
cv2.imshow("input image", src)
cv2.waitKey(0)

cv2.imshow("gray image", gray_src)
cv2.imwrite("gray.png", gray_src)
cv2.waitKey(0)

gray_src = cv2.bitwise_not(gray_src)
binary_src = cv2.adaptiveThreshold(gray_src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
cv2.namedWindow("result image", cv2.WINDOW_AUTOSIZE)
cv2.imshow("result image", binary_src)
cv2.waitKey(0)

# 提取水平线
hline = cv2.getStructuringElement(cv2.MORPH_RECT, ((src.shape[1] / 16), 1), (-1, -1))
# 提取垂直线
vline = cv2.getStructuringElement(cv2.MORPH_RECT, (1, (src.shape[0] / 16)), (-1, -1))
# 这两步就是形态学的开操作——先腐蚀再膨胀
# temp = cv2.erode(binary_src, hline)
# dst = cv2.dilate(temp, hline)
dst = cv2.morphologyEx(binary_src, cv2.MORPH_OPEN, vline)
dst = cv2.bitwise_not(dst)
cv2.imshow("Final image", dst)
cv2.waitKey(0)
