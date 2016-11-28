import warnings

import cv2
import numpy as np
from imutils import perspective

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

correct_answers = {0: 2, 1: 4, 2: 4, 3: 1, 4: 2, 5: 3, 6: 3, 7: 0, 8: 0, 9: 3, 10: 1, 11: 2, 12: 1, 13: 2, 14: 4, 15: 1,
                   16: 1, 17: 0, 18: 2, 19: 4}


def binarise_image(image, threshold=200, maxValue=255, type=1):
    # converts image to grey
    if type == 1:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarised, returns tuple but only the binary is used
    th, binary = cv2.threshold(image, threshold, maxValue, cv2.THRESH_BINARY_INV)

    return binary


def edge_detect(image, lower=75, upper=200):
    # converts image to black and white
    binary = binarise_image(image, type=2)

    # canny edge detect algorithm
    blurred = cv2.GaussianBlur(binary, (5, 5), 0)
    edges = cv2.Canny(blurred, lower, upper)

    return edges


def find_border(image):
    cv2.imshow("qr", image)
    cv2.waitKey(0)

    edges = edge_detect(image)

    # finds contours using edges
    _, cnts, heirachy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finds largest rectangle out of list of cnts
    for c in sorted(cnts, key=cv2.contourArea, reverse=True):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            border = approx
            break

        for c in sorted(cnts, key=cv2.contourArea, reverse=True)[1:]:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                cv2.imshow("qr", approx)
                cv2.waitKey(0)

    # crops and rotates image to match the border rectangle found above
    transformed = perspective.four_point_transform(image, border.reshape(4, 2))

    cv2.imwrite("border.jpg", transformed)

    return transformed


def retrieve_answers(image):

    answers = {}

    image = find_border(image)
    binary = binarise_image(image)

    # splits image in half to make it easier to iterate through the questions
    height_full, width_full = binary.shape
    half_one = binary[float(height_full * 0.02):float(height_full * 0.98), 0:width_full // 2]
    half_two = binary[float(height_full * 0.02):float(height_full * 0.98), width_full // 2:float(width_full)]

    cv2.imwrite("1.jpg", half_one[0:, :-80])
    cv2.imwrite("2.jpg", half_two[0:, 80:])

    # allows for the same index numbers to be used for 0-9 and then 10-19 - see use below
    half_num = 0

    for half in [half_one, half_two[0:, 80:]]:

        # y coordinate range of the answer sections to each of the questions - note that the third item is the position
        # eg. 0 is the 1st position, 1 is the 2nd etc
        question_locations = [[100, 160, 0], [300, 360, 1], [500, 560, 2], [700, 760, 3], [900, 960, 4],
                              [1080, 1140, 5], [1280, 1340, 6], [1460, 1520, 7], [1660, 1720, 8], [1860, 1920, 9]]

        # x location of the A, B, C, D, E bubbles
        answer_locations = [[150, 200], [290, 350], [430, 490], [570, 630], [710, 770]]

        for y in question_locations:
            # todo: add support for tests with less than 20 questions
            # todo: add support for tests with less than 5 options

            # stores pixel value - highest pixel value is the bubble with markings
            pixels = []

            for x in answer_locations:
                pixels.append(cv2.sumElems(half[y[0]:y[1], x[0]:x[1]])[0])

            answers[y[2] + half_num * 10] = pixels.index(max(pixels))

        half_num += 1

    print(answers)  # testing

    return answers


def mark_answers(correct_answers, answers):
    mark = 0

    for key, value in answers.items():
        if correct_answers[key] == value:
            mark += 1

    return mark


find_border(cv2.imread('C:\\Users\\Theo\\Documents\\ScansScan_20161128_114205.jpg'))
