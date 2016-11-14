import cv2
from imutils import perspective


def binarise_image(image, threshold=200, maxValue=255):
    # converts image to grey
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarised, returns tuple but only the binary is used
    th, binary = cv2.threshold(gray_image, threshold, maxValue, cv2.THRESH_BINARY)

    return binary


def edge_detect(image, lower=75, upper=200):
    # converts image to black and white
    binary = binarise_image(image)

    # canny edge detect algorithm
    blurred = cv2.GaussianBlur(binary, (5, 5), 0)
    edges = cv2.Canny(blurred, lower, upper)

    return edges


def find_border(image):
    edges = edge_detect(image)

    # finds contours using edges
    _, contours, heirachy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finds largest rectangle out of list of contours
    for c in sorted(contours, key=cv2.contourArea, reverse=True):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            border = approx
            break

    # cv2.drawContours(image, [border], -1, (0, 255, 0), 2)

    # crops and rotates image to match the border rectangle found above
    transformed = perspective.four_point_transform(image, border.reshape(4, 2))

    return transformed


find_border(cv2.imread("test/Scan_20161113_221737.jpg"))
