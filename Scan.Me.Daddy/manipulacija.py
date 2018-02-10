import cv2
import numpy as np

try:
    from cv2 import cv2
except ImportError:
    pass

def find_center(num):
    pixs = 0.0
    xs = []
    ys = []
    for x, row in enumerate(num):
        for y, col in enumerate(row):
            if col != 0:
                pixs = pixs + 1.0
                xs.append(x)
                ys.append(y)
    avgx = 0
    avgy = 0
    for i in range(0, int(pixs)):
        avgx += xs[i]
        avgy += ys[i]

    avgx /= pixs
    avgy /= pixs

    return avgx, avgy


def hough_find(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, 50, 1)  # todo igrati se sa parametrima

    x1_min, y2_min, x2_max, y1_max = 50000, 50000, -1, -1

    for line in lines:
        x11, y11, x22, y22 = line[0]
        if x11 < x1_min:
            x1_min = x11
        if y11 > y1_max:
            y1_max = y11
        if x22 > x2_max:
            x2_max = x22
        if y22 < y2_min:
            y2_min = y22

    return (x1_min, y1_max), (x2_max, y2_min)


def image_color_range(img, lowerb, upperb):
    mask = cv2.inRange(img, np.array(lowerb), np.array(upperb))
    return cv2.bitwise_and(img, img, mask=mask)

def image_color_range_2(img, lowerb, upperb):
    mask = cv2.inRange(img, lowerb, upperb)
    return cv2.bitwise_and(img, img, mask=mask)

def image_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def image_bin(image):
    image_gs = image_gray(image)
    ret, image_binary = cv2.threshold(image_gs, 127, 255, cv2.THRESH_BINARY)
    return image_binary

def image_bin_2(image):
    ret, image_binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    return image_binary

def invert(image):
    return 255 - image


def dilate(image, kmult):
    kernel = np.ones((kmult, kmult))  # strukturni element 3x3 blok
    return cv2.dilate(image, kernel, iterations=1)


def erode(image, kmult):
    kernel = np.ones((kmult, kmult))  # strukturni element 3x3 blok
    return cv2.erode(image, kernel, iterations=1)

def find_nw(pic):
    n = False
    w = False
    for i in range(0, pic.shape[0]):
        for j in range(0, pic.shape[1]):
            if n is False and pic[i, j] != 0.0:
                n = i
            if w is False and pic[j, i] != 0.0:
                w = i
            if n is not False and w is not False:
                break
    return n, w

def move_pic(pic):
    n, w = find_nw(pic)
    moved = np.zeros((28,28)).astype('float32')
    for i in range(0, moved.shape[0]):
        for j in range(0, moved.shape[1]):
            if 0 <= i + n < pic.shape[0] and 0 <= j + w < pic.shape[1]:
                moved[i, j] = pic[i+n, j+w]
    return moved

def copy_number(img, number):
    region = np.zeros((28, 28))
    x, y, w, h = number.get_bounds()
    x -= 3
    y -= 3
    w += 3
    h += 3
    x_off = (28 - w) / 2
    y_off = (28 - h) / 2
    for j in range(0, w):
        for k in range(0, h):
            if (not y + k >= img.shape[0]) and (not x + j >= img.shape[1]) and (not x + j < 0) and (not y+k < 0):
                col = img[y + k, x + j]
                region[y_off+k, x_off+j] = col / 255.0
    return move_pic(region)


def resize_region(img, cx, cy):
    region = np.zeros((28, 28))
    for x in range(0, 28):
        for y in range(0, 28):
            if (not y + cy >= img.shape[0]) and (not x + cx >= img.shape[1]):
                col = img[y + cy, x + cx]
                region[y, x] = col / 255.0
    return region

def re_box(bbox):
    x, y, w, h = bbox
    cx = int(x + w / 2.0)
    cy = int(y + h / 2.0)
    bbox = (cx - 14, cy - 14, 28, 28)
    return bbox


def select_roi(image_orig, image_bin):
    '''Oznaciti regione od interesa na originalnoj slici. (ROI = regions of interest)
        Za svaki region napraviti posebnu sliku dimenzija 28 x 28.
        Za oznacavanje regiona koristiti metodu cv2.boundingRect(contour).
        Kao povratnu vrednost vratiti originalnu sliku na kojoj su obelezeni regioni
        i niz slika koje predstavljaju regione sortirane po rastucoj vrednosti x ose
    '''
    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    regions_array = []
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        x, y = np.int0(rect[0])
        area = cv2.contourArea(contour)
        # kopirati [y:y+h+1, x:x+w+1] sa binarne slike i smestiti u novu sliku
        # oznaciti region pravougaonikom na originalnoj slici (image_orig) sa rectangle funkcijom
        if 10.0 < area < 784.0:
            regions_array.append([resize_region(image_bin, x - 14, y - 14), (x, y)])
            # cv2.rectangle(image_orig, (x - 14, y - 14), (x + 14, y + 14), (0, 0, 255), 1)

    # sortirati sve regione po x osi (sa leva na desno) i smestiti u promenljivu sorted_regions
    return regions_array
