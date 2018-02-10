import cv2
import numpy as np

try:
    from cv2 import cv2
except ImportError:
    pass


def find_regions(image_bin):
    '''Oznaciti regione od interesa na originalnoj slici. (ROI = regions of interest)
        Za svaki region napraviti posebnu sliku dimenzija 28 x 28.
        Za oznacavanje regiona koristiti metodu cv2.boundingRect(contour).
        Kao povratnu vrednost vratiti originalnu sliku na kojoj su obelezeni regioni
        i niz slika koje predstavljaju regione sortirane po rastucoj vrednosti x ose
    '''
    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    regions_array = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour) #koordinate i velicina granicnog pravougaonika
        area = cv2.contourArea(contour)
        # kopirati [y:y+h+1, x:x+w+1] sa binarne slike i smestiti u novu sliku
        # oznaciti region pravougaonikom na originalnoj slici (image_orig) sa rectangle funkcijom
        # if 10.0 < area < 784.0:
        if h > 8 and h < 30:
            regions_array.append(Region(None, (x, y, w, h)))

    return regions_array


class Region:

    def __init__(self, img, bounds):
        self.__img = img
        self.__bounds = bounds

    def get_bounds(self):
        return self.__bounds

    def get_center(self):
        x, y, w, h = self.__bounds
        x = int(x + (w / 2.0))
        y = int(y + (h / 2.0))
        return (x, y)

    def get_img(self):
        return self.__img
