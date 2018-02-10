import cv2
import manipulacija as mp
import sys
from tracker import NumberTracker
from region import find_regions
from line import Line
import eval_results as e
from knn import KNN
from timer import Timer

try:
    from cv2 import cv2
except ImportError:
    pass


def dt(img, blue_line, green_line, nn, tracker):
    white = mp.image_color_range(img, [127, 127, 127], [255, 255, 255])
    # white = mp.dilate(white, 1)
    white_bin = mp.image_bin(white)
    regions = find_regions(white_bin)
    numbers = tracker.update(regions)
    is_hit = False
    res = 0
    for number in numbers:
        if not number.has_hit_blue() and blue_line.hit_test(number):
            is_hit = True
            number.hit_blue()
            number.draw_rect(img)
            nimg = mp.copy_number(white_bin, number)
            x = nn.predict(nimg)
            number.draw_number(img, x)
            res += x
            # cv2.imshow('res=' + str(res), nimg)
        if not number.has_hit_green() and green_line.hit_test(number):
            is_hit = True
            number.hit_green()
            number.draw_rect(img)
            nimg = mp.copy_number(white_bin, number)
            x = nn.predict(nimg)
            number.draw_number(img, x)
            res -= x
            # cv2.imshow('res=' + str(res), nimg)

    if not is_hit:
        return None
    return res

def scan_video(file_name, pausable, verbose):
    print 'Opening file: '+file_name+'...'
    video = cv2.VideoCapture(file_name)
    ok, frame = video.read()

    if not ok:
        print 'Can not load video '+file_name
        sys.exit()

    blue = mp.image_color_range(frame, [90, 0, 0], [255, 70, 70])
    green = mp.image_color_range(frame, [0, 90, 0], [70, 255, 70])
    green = mp.erode(green, 2)
    green = mp.dilate(green, 2)
    bp1, bp2 = mp.hough_find(blue)
    gp1, gp2 = mp.hough_find(green)
    blue_line = Line(bp1, bp2)
    green_line = Line(gp1, gp2)

    nn = KNN()

    tracker = NumberTracker()
    res = 0
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        dres = dt(frame, blue_line, green_line, nn, tracker)
        if verbose:
            green_line.draw_line(frame, [0, 0, 255])
            blue_line.draw_line(frame, [255, 0, 255])
            cv2.imshow(wname, frame)
        if dres is not None:
            res += dres
            if pausable:
                cv2.waitKey(0)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    print res
    video.release()
    return res


def test():
    with open('out.txt', 'w') as file:
        file.write('RA 209/2014 Dejan Tot\n')
        file.write('File\tsum\t\n')

    for i in range(0, 10):
        fname = 'videos/video-' + str(i) + '.avi'
        res = scan_video(fname, False, False)
        with open('out.txt', 'a') as file:
            file.write(str(i) + '\t' + str(res) + '\n')

def test_single(n):
    res = scan_video('videos/video-'+str(n)+'.avi', True, True)
    e.eval_single(res, e.read_correct_single(n), str(n))

if __name__ == '__main__':
    pass

wname = 'Projekat'

nn = KNN()

timer = Timer().start('Analysis start...')
# test_single(6)
test()
e.eval_all()
timer.stop('Analysis took')

#results = []
#timer = Timer().start('Starting optimization process..')
#for i in range(15,26):
    #timer_2 = Timer().start('Analyzing videos...')
    #Line.Dst = i
    #test()
    #results.append(e.eval_all())
    #timer_2.stop('Analysis took')
#for i, r in enumerate(results):
    #print str(15+i)+':', r
#timer.stop('Optimization took')

