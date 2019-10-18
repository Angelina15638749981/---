# -*- coding: utf-8 -*-
"""
Created on Tue May 28 19:23:19 2019
将图片按照表格框线交叉点分割成子图片（传入图片路径）
@author: hx
"""

import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'D:/softwares/tesseract/tesseract.exe'
# import urllib.request
# urllib.request.urlretrieve('https://www.tcpjw.com/img/normalize/20190613/090017531.jpg', 'd.jpg')

img = cv2.imread('c2.png', 1)
x, y = img.shape[0:2]
image = cv2.resize(img, (int(y), int(x)))


# 灰度
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 二值化
binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
# ret,binary = cv2.threshold(~gray, 127, 255, cv2.THRESH_BINARY)
# cv2.imshow("二值化图片：", binary)  # 展示图片
cv2.waitKey(0)


rows, cols = binary.shape
scale = 40
# 识别横线
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
eroded = cv2.erode(binary, kernel, iterations=1)
# cv2.imshow("Eroded Image",eroded)
dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
# cv2.imshow("表格横线展示：", dilatedcol)
cv2.waitKey(0)

# 识别竖线
scale = 20
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
eroded = cv2.erode(binary, kernel, iterations=1)
dilatedrow = cv2.dilate(eroded, kernel, iterations=1)
# cv2.imshow("表格竖线展示：", dilatedrow)
cv2.waitKey(0)

# 标识交点
bitwiseAnd = cv2.bitwise_and(dilatedcol, dilatedrow)
# cv2.imshow("表格交点展示：", bitwiseAnd)
cv2.waitKey(0)
# cv2.imwrite("my.png",bitwiseAnd) #将二值像素点生成图片保存

# 标识表格
merge = cv2.add(dilatedcol, dilatedrow)
# cv2.imshow("表格整体展示：", merge)
# cv2.imwrite('merge.png', merge, )
cv2.waitKey(0)

# 两张图片进行减法运算，去掉表格框线
merge2 = cv2.subtract(binary, merge)
# cv2.imshow("图片去掉表格框线展示：", merge2)
# cv2.imwrite('e.png', merge2, )
cv2.waitKey(0)

# 裁剪
cropImg = merge2[0:int(0.6*x), 0:int(y)]
cv2.imwrite('cut.png', cropImg, )
# cv2.imshow("表格整体展示：", cropImg)


# 开运算操作
img_f = cv2.imread('cut.png',0)
kernel = np.ones((5,5),np.uint8)
opening = cv2.morphologyEx(img_f, cv2.MORPH_OPEN, kernel)
cv2.imshow('src',img_f)
cv2.imshow('show',opening)
cv2.waitKey()



text1 = pytesseract.image_to_string(img_f, lang='chi_sim')  # 读取文字，此为默认英文
print(text1)


# # 识别黑白图中的白色交叉点，将横纵坐标取出
# ys, xs = np.where(bitwiseAnd > 0)
# # print(xs)
# # print(ys)
#
# mylisty = []  # 纵坐标
# mylistx = []  # 横坐标
#
# # 通过排序，获取跳变的x和y的值，说明是交点，否则交点会有好多像素值值相近，我只取相近值的最后一点
# # 这个10的跳变不是固定的，根据不同的图片会有微调，基本上为单元格表格的高度（y坐标跳变）和长度（x坐标跳变）
# i = 0
# myxs = np.sort(xs)
# for i in range(len(myxs) - 1):
#     if (myxs[i + 1] - myxs[i] > 10):
#         mylistx.append(myxs[i])
#     i = i + 1
# mylistx.append(myxs[i])  # 要将最后一个点加入
#
# i = 0
# myys = np.sort(ys)
# for i in range(len(myys) - 1):
#     if (myys[i + 1] - myys[i] > 10):
#         mylisty.append(myys[i])
#     i = i + 1
# mylisty.append(myys[i])  # 要将最后一个点加入
#
# # print('mylisty', mylisty)
# # print('mylistx', mylistx)
#
# # 循环y坐标，x坐标分割表格
# for i in range(len(mylisty) - 1):
#     for j in range(len(mylistx) - 1):
#         # 在分割时，第一个参数为y坐标，第二个参数为x坐标
#         ROI = image[mylisty[i] + 3:mylisty[i + 1] - 3, mylistx[j]:mylistx[j + 1] - 3]  # 减去3的原因是由于我缩小ROI范围
#         # cv2.imshow("分割后子图片展示：", ROI)
#         cv2.imwrite('%s.png' % i, ROI, )
#         cv2.waitKey(0)
#
#
#         text1 = pytesseract.image_to_string(ROI, lang='chi_sim')  # 读取文字，此为默认英文
#         # text2 = ''.join([char for char in text2 if char not in special_char_list])
#         print(text1)
#         j = j + 1
#     i = i + 1

