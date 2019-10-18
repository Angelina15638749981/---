import cv2
image = cv2.imread("d.jpg")
h, w = image.shape[:2]
print(h, w)
h, w = map(int, [h/4, w/4])

# no flip
draw_0 = cv2.rectangle(image, (2*w, 2*h), (3*w, 3*h), (255, 0, 0), 2)
# vertical flip
draw_1 = cv2.rectangle(image, (2*w, 3*h), (3*w, 2*h), (255, 0, 0), 2)
# horizontal flip
draw_2 = cv2.rectangle(image, (3*w, 2*h), (2*w, 3*h), (255, 0, 0), 2)
# h & v flip
draw_3 = cv2.rectangle(image, (3*w, 3*h), (2*w, 2*h), (255, 0, 0), 2)

cv2.imwrite("origin.jpg", draw_0)
cv2.imwrite("vertical_flip.jpg", draw_1)
cv2.imwrite("horizontal_flip.jpg", draw_2)
cv2.imwrite("hv_flip.jpg", draw_3)
