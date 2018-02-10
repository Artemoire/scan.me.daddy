import cv2
import numpy as np
from timer import Timer
from keras.datasets import mnist


def test_num(img):
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    # timer = Timer().start()
    test = img.reshape(1, 784)
    test = test.astype('float32')
    test /= 255
    return np.int8(knn.findNearest(test, k=1)[0])
    # timer.stop('Predicted ' + str(res) + ' in')


if __name__ == '__main__':
    pass

timer = Timer().start()
print 'Loading MNIST data set...'
# the data, shuffled and split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()
timer.stop('Data set loaded in')

x_train = x_train.reshape(60000, 784)
x_train = (x_train) > 180
x_train = x_train.astype('float32')
y_train = y_train.astype('float32')

timer.start()
print 'Training...'
knn = cv2.ml.KNearest_create()
knn.train(x_train, cv2.ml.ROW_SAMPLE, y_train)
timer.stop('Finished training in')

correct = 0

timer.start()
print 'Evaluating...'
for i, x in enumerate(x_test):
    if y_test[i] == test_num(x):
        correct += 1
timer.stop('Evaluation done in')
print str(float(correct)/10000.0 * 100.0)+'% correct'