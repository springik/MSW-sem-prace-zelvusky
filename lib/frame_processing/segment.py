import cv2
import numpy as np

MIN_AREA = 1500
MIN_SOLIDITY = 0.50
BORDER_MARGIN = 2


def segment(img_path):
    image = cv2.imread(img_path)
    output_image = image.copy()
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8,8))
    gray_image = clahe.apply(gray_image)

    blur = cv2.GaussianBlur(gray_image, (11,11), 0)
    ret, _ = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    forgiving_treshold = ret * 0.80
    _, thresh = cv2.threshold(blur, forgiving_treshold, 255, cv2.THRESH_BINARY)

    kernel = np.ones((3,3), np.uint8)

    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=3)

    sure_background = cv2.dilate(closing, kernel, iterations=1)

    distance_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 5)
    ret, sure_foreground = cv2.threshold(
        distance_transform,
        0.3 * distance_transform.max(),
        255,
        0
    )
    sure_foreground = np.uint8(sure_foreground)

    unknown_area = cv2.subtract(sure_background, sure_foreground)

    ret, markers = cv2.connectedComponents(sure_foreground)
    markers = markers + 1
    markers[unknown_area == 255] = 0

    markers = cv2.watershed(image, markers)

    raw_mask = np.zeros_like(gray_image)
    raw_mask[markers > 1] = 255

    # image[markers == -1] = [0, 0, 255]

    final_mask = np.zeros_like(gray_image)
    contours, _ = cv2.findContours(raw_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # final_mask[markers > 1] = 255

    img_h, img_w = gray_image.shape

    for contour in contours:
        area = cv2.contourArea(contour)
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        if hull_area > 0:
            solidity = float(area) / hull_area
        else:
            solidity = 0

        x, y, w, h = cv2.boundingRect(contour)

        touches_border = (
            x <= BORDER_MARGIN
            or y <= BORDER_MARGIN
            or x + w >= img_w - BORDER_MARGIN
            or y + h >= img_h - BORDER_MARGIN
        )

        if area > MIN_AREA and solidity > MIN_SOLIDITY and not touches_border:
            cv2.drawContours(final_mask, [contour], -1, 255, thickness=cv2.FILLED)
            cv2.drawContours(output_image, [contour], -1, [0, 0, 255], 1)

    return output_image, final_mask
