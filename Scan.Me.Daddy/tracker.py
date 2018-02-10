import vec
import numpy as np
from number import Number


class NumberTracker:

    def __init__(self):
        self.__numbers = []

    def update(self, regions):
        for region in regions:
            self.__update_region(region)
        return self.__numbers

    def __update_region(self, region):
        center = region.get_center()
        bounds = region.get_bounds()

        if self.__numbers.__len__() == 0:
            number = Number(bounds)
            self.__numbers.append(number)
            return number

        distances = []

        for number in self.__numbers:
            distances.append(vec.distance(center, number.get_center()))

        number = None

        i = np.argmin(distances)

        if distances[i] < 20:
            number = self.__numbers[i]

        if number is None:
            number = Number(bounds)
            self.__numbers.append(number)
        else:
            number.set_bounds(bounds)

        return number
