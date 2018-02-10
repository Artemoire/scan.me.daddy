import numpy as np
from numpy.linalg import norm
import cv2

try:
    from cv2 import cv2
except ImportError:
    pass


class Line:

    def __init__(self, p1, p2):
        self.__p1 = p1
        self.__p2 = p2

    def hit_test(self, number):
        center = number.get_center()

        if center[0] > self.__p1[0] and center[0] < self.__p2[0] and center[1] < self.__p1[1] and center[1] > self.__p2[1]:
            p1 = np.array(self.__p1)
            p2 = np.array(self.__p2)
            p3 = np.array(center)
            distance = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)

            if distance < 17:
                return True

        return False

    def draw_line(self, img, color):
        cv2.line(img, self.__p1, self.__p2, color, thickness=1)