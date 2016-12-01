import warnings

import cv2
import numpy as np
import qreader
from PIL import Image
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


def find_qr(image):
    # todo: FIX QR CODE DETECTION PROBLEMS - only adds one corner to the array
    # todo: error detection in message
    # todo: rotate depending on orientation

    img = image

    edges = edge_detect(img)

    _, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]  # get the actual inner list of hierarchy descriptions

    corner = 0
    corner_cnts = np.empty((1, 2), int)
    print(corner_cnts)

    indices = sorted(range(len(contours)), key=lambda i: cv2.contourArea(contours[i]))

    print(indices)

    # For each contour, find the bounding rectangle and draw it
    for i in reversed(indices):
        currentContour = contours[i]
        currentHierarchy = hierarchy[i]
        x, y, w, h = cv2.boundingRect(currentContour)

        if currentHierarchy[3] < 0:
            if 0.85 < (w / h) < 1.1:
                new = np.vstack((corner_cnts, currentContour.reshape(-1, 2)))
                # these are the outermost parent components

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                corner += 1

        if corner == 3:
            break

    print(np.delete(np.hsplit(new, 2)[0].flatten(), (0), axis=0))

    # Finally show the image
    cv2.imshow('img', cv2.resize(img, (0, 0), fx=0.2, fy=0.2))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # reshapes np array and cuts image to QR code
    x = np.delete(np.hsplit(new, 2)[0].flatten(), (0), axis=0)
    y = np.delete(np.hsplit(new, 2)[1].flatten(), (0), axis=0)
    np_qr = image[y.min():y.max(), x.min():x.max()]

    cv2.imshow("qr", np_qr)
    cv2.waitKey(0)

    np_qr = binarise_image(np_qr, type=1)
    np_qr = (255 - np_qr)  # inverts

    cv2.imshow("qr", np_qr)
    cv2.waitKey(0)

    downsize = cv2.resize(np_qr, (21, 21))  # each pixel represents one block on QR code

    cv2.imshow("qr", downsize)
    cv2.waitKey(0)

    pil_qr = Image.fromarray(downsize)  # turns into PIL image for use with qreader.read()

    data = qreader.read(pil_qr)  # should return Student_ID

    return data


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
            cnts = np.delete(cnts, c)
            break

    # crops and rotates image to match the border rectangle found above
    transformed = perspective.four_point_transform(image, border.reshape(4, 2))

    return transformed


def retrieve_answers(image):
    # todo: REWRITE SO FINDS CONTOURS OF THE BUBBLES

    answers = {}

    image = find_border(image)
    binary = binarise_image(image)

    # splits image in half to make it easier to iterate through the questions
    height_full, width_full = binary.shape
    half_one = binary[float(height_full * 0.02):float(height_full * 0.98), 0:width_full // 2]
    half_two = binary[float(height_full * 0.02):float(height_full * 0.98), width_full // 2:float(width_full)]

    # cv2.imwrite("1.jpg", half_one[0:, :-80])
    # cv2.imwrite("2.jpg", half_two[0:, 80:])

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


# print(find_qr(cv2.imread("../resources/Scans/4.jpg")))

# print(mark_answers(correct_answers, retrieve_answers(cv2.imread("../resources/Scans/2.jpg"))))
for i in range(7, 9):
    print(find_qr(cv2.imread("../resources/Scans/" + str(i) + ".jpg")))
