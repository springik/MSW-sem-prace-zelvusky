import cv2
import numpy as np


def segment(img_path):
    image = cv2.imread(img_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray_image, (9,9), 0)

    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((5,5), np.uint8)

    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    sure_background = cv2.dilate(closing, kernel, iterations=3)

    distance_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 5)
    ret, sure_foreground = cv2.threshold(
        distance_transform,
        0.5 * distance_transform.max(),
        255,
        0
    )

    sure_foreground = np.uint8(sure_foreground)
    unknown_area = cv2.subtract(sure_background, sure_foreground)

    ret, markers = cv2.connectedComponents(sure_foreground)
    markers = markers + 1
    markers[unknown_area == 255] = 0

    markers = cv2.watershed(image, markers)

    image[markers == -1] = [0, 0, 255]

    final_mask = np.zeros_like(gray_image)
    final_mask[markers > 1] = 255

    return image, final_mask
