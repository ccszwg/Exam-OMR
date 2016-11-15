import warnings

import cv2
import numpy as np
from imutils import perspective

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

correct_answers = {0: 2, 1: 4, 2: 4, 3: 1, 4: 2, 5: 3, 6: 3, 7: 0, 8: 0, 9: 3, 10: 1, 11: 2, 12: 1, 13: 2, 14: 4, 15: 1,
                   16: 1, 17: 0, 18: 2, 19: 4}


def binarise_image(image, threshold=200, maxValue=255):
    # converts image to grey
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarised, returns tuple but only the binary is used
    th, binary = cv2.threshold(gray_image, threshold, maxValue, cv2.THRESH_BINARY_INV)

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
    _, cnts, heirachy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finds largest rectangle out of list of cnts
    for c in sorted(cnts, key=cv2.contourArea, reverse=True):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            border = approx
            break

    # cv2.drawContours(image, [border], -1, (0, 255, 0), 2)

    # crops and rotates image to match the border rectangle found above
    transformed = perspective.four_point_transform(image, border.reshape(4, 2))

    return transformed


def retrieve_answers(image):
    answers = {}

    # todo: PRIORITY refactor this

    image = find_border(image)

    binary = binarise_image(image)

    # splits image in half
    height_full, width_full = binary.shape
    half_one = binary[float(height_full * 0.02):float(height_full * 0.98), 0:width_full // 2]
    cv2.imwrite("test2.jpeg", half_one)

    half_two = binary[float(height_full * 0.02):float(height_full * 0.98), width_full // 2:float(width_full)]
    # halves = [half_one, half_two]
    halves = [half_one]

    for half in halves:

        _, cnts, heirachy = cv2.findContours(half, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        answer_cnts = []

        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour, then use the
            # bounding box to derive the aspect ratio
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)

            # in order to label the contour as a question, region
            # should be sufficiently wide, sufficiently tall, and
            # have an aspect ratio approximately equal to 1
            if w >= 5 and h >= 5 and 0.9 <= ar <= 1.1:
                print(c)
            answer_cnts.append(c)

        cv2.drawContours(half, answer_cnts, -1, (0, 255, 0), 3)
        cv2.imwrite("test.jpeg", half)

        # todo: currently finds marks, need to order marks from top-to-bottom,
        # todo: work out what question they correspond to
        # todo: return script's answers


def mark_answers(correct_answers, answers):
    mark = 0

    for key, value in answers.items():
        if correct_answers[key] == value:
            mark += 1

    return mark


im = cv2.imread("resources/Scan_20161115_203418.jpg")
retrieve_answers(im)
