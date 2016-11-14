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


def retrieve_answers(image):
    answers = {}

    # todo: PRIORITY refactor this

    binary = binarise_image(image)

    height_full, width_full = binary.shape

    # crops image to half
    for half in range(0, 2):

        cropped = binary[height_full * 0.02:height_full,
                  (width_full * 0.05) + ((width_full // 2 + width_full * 0.06) * half):(width_full // 2) + (
                                                                                                               width_full // 2) * half]

        # cv2.imshow("test", cropped)
        # cv2.waitKey(0)

        for q in range(0, 10):
            # todo: fix visible deprecation warnings

            # crops image suitably mutliple times to find each distint answer
            question_shape = (height_full // 1.28) * 0.095

            question = cropped[question_shape * q:question_shape * (q + 1), width_full * 0.01:width_full // 2]

            height_question, width_question = question.shape

            answer_shape = width_question // 6.1

            inputs = {}

            for a in range(0, 5):
                answer = question[height_question // 2:height_question, answer_shape * a:answer_shape * (a + 1)]

                # saves all pixel sum vales in dictionary - lowest value equals answer that has been inputted
                inputs[a] = cv2.sumElems(answer)[0]

                # cv2.imshow("test", answer)
                # cv2.waitKey(0)

            answers[int(half * 10 + q)] = min(inputs, key=inputs.get)

    return answers


def mark_answers(correct_answers, answers):
    mark = 0

    for key, value in answers.items():
        if correct_answers[key] == value:
            mark += 1

    return mark


print(mark_answers(correct_answers, retrieve_answers(cv2.imread("cropped.png"))))
