import cv2
import numpy as np

try:
    from cv2 import cv2
except ImportError:
    pass


class Number:

    def __init__(self, bounds):
        self.__bounds = bounds
        self.__hit_green = False
        self.__hit_blue = False

    def set_bounds(self, bounds):
        self.__bounds = bounds

    def get_bounds(self):
        return self.__bounds

    def get_center(self):
        x, y, w, h = self.__bounds
        x = int(x + (w / 2.0))
        y = int(y + (h / 2.0))
        return (x, y)

    def draw_rect(self, img):
        x, y = self.get_center()
        cv2.rectangle(img, (x - 14, y - 14), (x + 14, y + 14), (0, 255, 255), 1)

    def draw_number(self, img, n):
        x, y = self.get_center()
        cv2.putText(img, str(n), (x+14, y-14), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    def has_hit_green(self):
        return self.__hit_green

    def has_hit_blue(self):
        return self.__hit_blue

    def hit_green(self):
        self.__hit_green = True

    def hit_blue(self):
        self.__hit_blue = True
