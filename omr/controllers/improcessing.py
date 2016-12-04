import warnings
from collections import Counter

import cv2
import numpy as np
import qreader
from PIL import Image

# todo: TURN INTO A CLASS

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


def find_qr(image):
    # todo: error detection in message

    image = rotate(image)

    edges = binarise_image(rotate(image))

    _, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]  # get the actual inner list of hierarchy descriptions

    corner = 0
    corner_cnts = np.zeros((1, 2), dtype=np.float64)

    # For each contour, find the bounding rectangle and draw it
    for i in reversed(sorted(range(len(contours)), key=lambda i: cv2.contourArea(contours[i]))):
        current_contour = contours[i]
        current_hierarchy = hierarchy[i]
        x, y, w, h = cv2.boundingRect(current_contour)

        if current_hierarchy[3] < 0:
            if 0.85 < (w / h) < 1.1:
                x = np.hsplit(current_contour.reshape(-1, 2), 2)[0]
                y = np.hsplit(current_contour.reshape(-1, 2), 2)[1]
                corner_cnts = np.vstack((corner_cnts, np.hstack((x, y))))

                corner += 1

        if corner == 3:
            break

    corner_cnts = np.delete(corner_cnts, 0, axis=0)

    # reshapes np array and cuts image to QR code
    x = np.delete(np.hsplit(corner_cnts, 2)[0].flatten(), (0), axis=0)
    y = np.delete(np.hsplit(corner_cnts, 2)[1].flatten(), (0), axis=0)
    np_qr = image[y.min():y.max(), x.min():x.max()]

    np_qr = binarise_image(np_qr, type=1)
    np_qr = (255 - np_qr)  # inverts

    downsize = cv2.resize(np_qr, (21, 21))  # each pixel represents one block on QR code
    pil_qr = Image.fromarray(downsize)  # turns into PIL image for use with qreader.read()
    data = qreader.read(pil_qr)  # should return Student_ID

    return data


def rotate(image):
    # todo: optimize

    edges = edge_detect(image)

    # finds contours using edges
    _, cnts, heirachy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finds largest rectangle out of list of cnts
    for c in sorted(cnts, key=cv2.contourArea, reverse=True):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            rect = cv2.minAreaRect(c)
            if rect[2] > -45:
                angle = rect[2]
            else:
                angle = rect[2] + 90
            break

    M = cv2.getRotationMatrix2D((image.shape[1] / 2, image.shape[0] / 2), angle, 1)
    img = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    return img


def find_border(image):
    image = rotate(image)
    edges = edge_detect(image)

    # finds contours using edges
    _, cnts, heirachy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finds largest rectangle out of list of cnts
    for c in sorted(cnts, key=cv2.contourArea, reverse=True):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(c)
            return image[y:y + h, x:x + w]


def retrieve_answers(image):
    # todo: optimise

    answers = {}
    image = find_border(image)
    binary = binarise_image(image, threshold=200)

    _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    hierarchy = hierarchy[0]  # get the actual inner list of hierarchy descriptions

    # list of potential contours
    bubbles = []
    areas = []
    xpositions = []
    ypositions = []

    # For each contour, see if it is approximately square
    for component in zip(contours, hierarchy):
        current_contour = component[0]
        current_hierarchy = component[1]
        x, y, w, h = cv2.boundingRect(current_contour)
        if current_hierarchy[2] < 0:

            if 0.9 < w / h < 1.1:
                bubbles.append(current_contour)
                areas.append(w * h)

    mode = [i[0] for i in Counter(areas).most_common()][0]  # find modal area which is probably the bubbles

    # find start of each question
    for c in bubbles:
        x, y, w, h = cv2.boundingRect(c)

        if mode - mode * 0.1 < w * h < mode + mode * 0.1:
            xpositions.append(round(x, -1))
            ypositions.append(round(y, -1))

    # todo: add support for less than 20 questions and less than 20 answers (probably by merging similar numbers)
    xpos = sorted([i[0] for i in Counter(xpositions).most_common()][0:10])
    ypos = [i[0] for i in Counter(ypositions).most_common()][0:10]

    binary = binarise_image(image)

    for y in ypos:
        xcount = 0
        for x in xpos:
            # todo: automatically calculate threshold for sum of pixels                      VVVVVV
            if cv2.sumElems(binary[y:y + binary.shape[0] * 0.03, x:x + binary.shape[1] * 0.03])[0] > 190000:
                question = (x // (image.shape[1] // 2)) * 10 + y // (image.shape[0] * 0.09)
                answers[question] = xcount % 5

            xcount += 1

    return answers


def mark_answers(correct_answers, answers):
    mark = 0

    for key, value in answers.items():
        if correct_answers[key] == value:
            mark += 1

    return mark


for i in range(1, 8):
    retrieve_answers(cv2.imread("../resources/Scans/" + str(i) + ".jpg"))
