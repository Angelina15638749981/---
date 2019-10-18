from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'D:/softwares/tesseract/tesseract.exe'

# image = Image.open('1.1_full_name_2.png')


import cv2


image = cv2.imread("1.1_full_name_1.png")

full_name_1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("new image", full_name_1)
cv2.imwrite("cut1.png", full_name_1)
cv2.waitKey(0)

# imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
#
# print(imageVar)
# 全称1
x, y = full_name_1.shape[0:2]
full_name_1 = cv2.resize(full_name_1, (int(2 * y), int(2 * x)))
cv2.imshow("全称1", full_name_1)
cv2.imwrite("cut2.png", full_name_1)

cv2.waitKey(0)

full_name_1 = pytesseract.image_to_string(full_name_1, lang='chi_sim')  # 读取文字，此为默认英文
print("出票人全称：%s" % full_name_1)
# 5380201910100041