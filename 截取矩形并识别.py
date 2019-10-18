import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'D:/softwares/tesseract/tesseract.exe'
import urllib.request
import time
# https://www.tcpjw.com/Content/Images/201908141842014385955.jpg
# urllib.request.urlretrieve('https://www.tcpjw.com/Content/Images/201908191542170013083.jpg', 'c21.png')
# time.sleep(3)
# photo_name=str(input("请输入测试的图片名字："))
image = cv2.imread('gray.png', 1)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # 色彩空间转换为hsv，便于分离
cv2.imshow("hsv", hsv)
cv2.waitKey(0)
lower_hsv = np.array([0, 0, 0])  # 提取颜色的低值
high_hsv = np.array([180, 255, 46])  # 提取颜色的高值
mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=high_hsv)
cv2.imshow("mask", mask)
cv2.waitKey(0)



#二值化
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray image", gray)
cv2.waitKey(0)

binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
#ret,binary = cv2.threshold(~gray, 127, 255, cv2.THRESH_BINARY)
cv2.imshow("cell", binary)
# cv2.imwrite('binary.png', binary, )

cv2.waitKey(0)

rows, cols = binary.shape
scale = 40
#识别横线
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(cols//scale,1))
eroded = cv2.erode(binary,kernel,iterations = 1)
# cv2.imshow("Eroded Image",eroded)
dilatedcol = cv2.dilate(eroded,kernel,iterations = 1)
# cv2.imshow("Dilated Image",dilatedcol)
# cv2.waitKey(0)

#识别竖线
scale = 20
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,rows//scale))
eroded = cv2.erode(binary,kernel,iterations = 1)
dilatedrow = cv2.dilate(eroded,kernel,iterations = 1)
# cv2.imshow("Dilated Image",dilatedrow)
# cv2.waitKey(0)

#标识交点
bitwiseAnd = cv2.bitwise_and(dilatedcol, dilatedrow)
# cv2.imshow("bitwiseAnd Image", bitwiseAnd)
cv2.imwrite('biaodian.png', bitwiseAnd, )

# cv2.waitKey(0)
# cv2.imwrite("my.png",bitwiseAnd)

#标识表格
merge = cv2.add(dilatedcol, dilatedrow)
# cv2.imshow("add Image",merge)
# cv2.imwrite('biaoge.png', merge, )

cv2.waitKey(0)

#识别黑白图中的白色点
ws, hs = np.where(bitwiseAnd>0)
# print('------------------------ws-------------------------')
# print(ws, len(ws))
# print('------------------------hs-------------------------')
# print(hs, len(hs))
mylistw = []
mylisth = []

#通过排序，获取跳变的x和y的值，说明是交点，否则交点会有好多像素值，我只取最后一点
i = 0
myxs = np.sort(hs)
for i in range(len(myxs)-1):
    if(myxs[i+1]-myxs[i]>10):
        mylisth.append(myxs[i])
    i = i+1
mylisth.append(myxs[i])


i = 0
myys = np.sort(ws)
# print(mylistx)
# print(mylisty)

for i in range(len(myys)-1):
    if(myys[i+1]-myys[i]>10):
        mylistw.append(myys[i])
    i = i+1
mylistw.append(myys[i])
# 高度
print(mylistw, len(mylistw))
# 宽度
print(mylisth, len(mylisth))

# c规格的图片
# 情形1 c1
if len(mylistw) == 13 and len(mylisth) == 7:
    ROI = image[mylistw[0]:mylistw[4], mylisth[0]:mylisth[-1]]
    print(mylistw[0], mylistw[4], mylisth[0], mylisth[-1])

    photo_name = str(input("请输入保存图片名字："))
    cv2.imwrite('ROI_%s.png' % photo_name, ROI, )
    cv2.waitKey(0)

    # 全称1
    full_name_1 = image[mylistw[1]:mylistw[2], mylisth[2]:mylisth[3]]
    # 全称 2
    full_name_2 = image[mylistw[1]:mylistw[2], mylisth[5]:mylisth[6]]

    # 全称1
    x, y = full_name_1.shape[0:2]
    full_name_1 = cv2.resize(full_name_1, (int(2 * y), int(2 * x)))
    cv2.imshow("全称1", full_name_1)

    # 全称2
    x, y = full_name_2.shape[0:2]
    full_name_2 = cv2.resize(full_name_2, (int(2 * y), int(2 * x)))

    cv2.imwrite('%s_full_name_1.png' % photo_name, full_name_1)
    cv2.imwrite('%s_full_name_2.png' % photo_name, full_name_2)

    full_name_1 = pytesseract.image_to_string(full_name_1, lang='chi_sim')  # 读取文字，此为默认英文
    print("出票人全称：%s" % full_name_1)
    full_name_2 = pytesseract.image_to_string(full_name_2, lang='chi_sim')  # 读取文字，此为默认英文
    print("收款人全称：%s" % full_name_2)


# 情形2
elif len(mylistw) == 13 and len(mylisth) == 6:
    ROI = image[mylistw[0]:mylistw[4], mylisth[0]:mylisth[-1]]
    print(mylistw[0], mylistw[4], mylisth[0], mylisth[-1])

    photo_name = str(input("请输入保存图片名字："))
    cv2.imwrite('ROI_%s.png' % photo_name, ROI, )
    cv2.waitKey(0)

    # 全称1
    full_name_1 = image[mylistw[1]:mylistw[2], mylisth[1]:mylisth[2]]
    # 全称 2
    full_name_2 = image[mylistw[1]:mylistw[2], mylisth[4]:mylisth[5]]

    # 全称1
    x, y = full_name_1.shape[0:2]
    full_name_1 = cv2.resize(full_name_1, (int(2 * y), int(2 * x)))
    cv2.imshow("全称1", full_name_1)

    # 全称2
    x, y = full_name_2.shape[0:2]
    full_name_2 = cv2.resize(full_name_2, (int(2 * y), int(2 * x)))

    cv2.imwrite('%s_full_name_1.png' % photo_name, full_name_1)
    cv2.imwrite('%s_full_name_2.png' % photo_name, full_name_2)

    full_name_1 = pytesseract.image_to_string(full_name_1, lang='chi_sim')  # 读取文字，此为默认英文
    print("出票人全称：%s" % full_name_1)
    full_name_2 = pytesseract.image_to_string(full_name_2, lang='chi_sim')  # 读取文字，此为默认英文
    print("收款人全称：%s" % full_name_2)



# d规格的图片
# 情形3 d1
elif len(mylistw) ==14 and len(mylisth) ==21:
    ROI = image[mylistw[1]:mylistw[4], mylisth[0]:mylisth[19]]
    print(mylistw[1], mylistw[4], mylisth[0], mylisth[19])

    photo_name = str(input("请输入保存图片名字："))
    cv2.imwrite('ROI_%s.png' % photo_name, ROI, )
    cv2.waitKey(0)

    # 全称1
    full_name_1 = image[mylistw[1]:mylistw[2], mylisth[2]:mylisth[4]]
    # 全称 2
    full_name_2 = image[mylistw[1]:mylistw[2], mylisth[6]:mylisth[19]]

    # 全称1
    x, y = full_name_1.shape[0:2]
    full_name_1 = cv2.resize(full_name_1, (int(2 * y), int(2 * x)))
    cv2.imshow("全称1", full_name_1)

    # 全称2
    x, y = full_name_2.shape[0:2]
    full_name_2 = cv2.resize(full_name_2, (int(2 * y), int(2 * x)))

    cv2.imwrite('%s_full_name_1.png' % photo_name, full_name_1)
    cv2.imwrite('%s_full_name_2.png' % photo_name, full_name_2)

    full_name_1 = pytesseract.image_to_string(full_name_1, lang='chi_sim')  # 读取文字，此为默认英文
    print("出票人全称：%s" % full_name_1)
    full_name_2 = pytesseract.image_to_string(full_name_2, lang='chi_sim')  # 读取文字，此为默认英文
    print("收款人全称：%s" % full_name_2)

# 情形3 d2
elif len(mylistw) ==14 and len(mylisth) ==9:
    ROI = image[mylistw[0]:mylistw[3], mylisth[0]:mylisth[-1]]
    print(mylistw[0], mylistw[3], mylisth[0], mylisth[-1])

    photo_name = str(input("请输入保存图片名字："))
    cv2.imwrite('ROI_%s.png' % photo_name, ROI, )
    cv2.waitKey(0)

    # 全称1
    full_name_1 = image[mylistw[0]:mylistw[1], mylisth[2]:mylisth[4]]
    # 全称 2
    full_name_2 = image[mylistw[0]:mylistw[1], mylisth[6]:mylisth[-1]]

    # 全称1
    x, y = full_name_1.shape[0:2]
    full_name_1 = cv2.resize(full_name_1, (int(2 * y), int(2 * x)))
    cv2.imshow("全称1", full_name_1)

    # 全称2
    x, y = full_name_2.shape[0:2]
    full_name_2 = cv2.resize(full_name_2, (int(2 * y), int(2 * x)))

    cv2.imwrite('%s_full_name_1.png' % photo_name, full_name_1)
    cv2.imwrite('%s_full_name_2.png' % photo_name, full_name_2)

    full_name_1 = pytesseract.image_to_string(full_name_1, lang='chi_sim')  # 读取文字，此为默认英文
    print("出票人全称：%s" % full_name_1)
    full_name_2 = pytesseract.image_to_string(full_name_2, lang='chi_sim')  # 读取文字，此为默认英文
    print("收款人全称：%s" % full_name_2)

# 情形 d3
elif len(mylistw) == 15 and len(mylisth) == 20:
    ROI = image[mylistw[1]:mylistw[4], mylisth[1]:mylisth[-2]]
    print(mylistw[1], mylistw[4], mylisth[1], mylisth[-2])

    photo_name = str(input("请输入保存图片名字："))
    cv2.imwrite('ROI_%s.png' % photo_name, ROI, )
    cv2.waitKey(0)

    # 全称1
    full_name_1 = image[mylistw[1]:mylistw[2], mylisth[2]:mylisth[4]]
    # 全称 2
    full_name_2 = image[mylistw[1]:mylistw[2], mylisth[6]:mylisth[-2]]

    # 全称1
    x, y = full_name_1.shape[0:2]
    full_name_1 = cv2.resize(full_name_1, (int(2 * y), int(2 * x)))
    cv2.imshow("全称1", full_name_1)
    cv2.waitKey(0)


    # 全称2
    x, y = full_name_2.shape[0:2]
    full_name_2 = cv2.resize(full_name_2, (int(2 * y), int(2 * x)))

    cv2.imwrite('%s_full_name_1.png' % photo_name, full_name_1)
    cv2.imwrite('%s_full_name_2.png' % photo_name, full_name_2)

    full_name_1 = pytesseract.image_to_string(full_name_1, lang='chi_sim')  # 读取文字，此为默认英文
    print("出票人全称：%s" % full_name_1)
    full_name_2 = pytesseract.image_to_string(full_name_2, lang='chi_sim')  # 读取文字，此为默认英文
    print("收款人全称：%s" % full_name_2)





