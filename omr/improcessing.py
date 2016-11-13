import cv2

def binarise_image(image, threshold=200, maxValue = 255):
    """
    :param image: actual image data, not location of image - use cv2.imread()
    :param threshold: adjust for appropriate binarization - between 200 and 210 works well
    :param maxValue: leave at 255
    :return: binarized image
    """

    # converts image to grey
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarised
    th, dst = cv2.threshold(gray_image, threshold, maxValue, cv2.THRESH_BINARY);

    return dst

