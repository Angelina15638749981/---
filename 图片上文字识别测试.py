import cv2
import numpy as np
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'D:/softwares/tesseract/tesseract.exe'


# img = cv2.imread('gray_ROI_d1.png')
img = cv2.imread('d1gray1_full_name_1.png')

# 全称1
x, y = img.shape[0:2]
img = cv2.resize(img, (int(2 * y), int(2 * x)))
cv2.imshow("全称1", img)
cv2.waitKey(0)


full_name_1 = pytesseract.image_to_string(img, lang='chi_sim')  # 读取文字，此为默认英文
print("出票人全称：%s" % full_name_1.replace("  ", "").replace("”", "").replace("“", "").replace("。", ""))

