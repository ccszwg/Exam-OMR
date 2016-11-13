import cv2


def binarise_image(image, threshold=200, maxValue=255):
    # converts image to grey
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarised
    th, dst = cv2.threshold(gray_image, threshold, maxValue, cv2.THRESH_BINARY);

    return dst


def edge_detect(image, lower=75, upper=200):
    # converts image to black and white
    binary = binarise_image(image)

    # canny edge detect algorithm
    blurred = cv2.GaussianBlur(binary, (5, 5), 0)
    edges = cv2.Canny(blurred, lower, upper)

    return edges

# todo: have program detect border of question paper and rotate and crop appropriately
