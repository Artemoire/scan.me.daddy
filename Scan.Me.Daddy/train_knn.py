import cv2
import numpy as np
# from keras.datasets import mnist
from timer import Timer
import manipulacija as mp
import os


def train_knn():
    if os.path.isfile('data.npz'):
        # x_train, y_train = load_original_data()
        x_train, y_train = load_data()
    # else:
    #     x_train, y_train = morph_data()

    timer = Timer().start('Training...')
    knn = cv2.ml.KNearest_create()
    knn.train(x_train, cv2.ml.ROW_SAMPLE, y_train)
    timer.stop('Finished training in')

    return knn

# def load_original_data():
#     timer = Timer().start('Loading MNIST data set...')
#     (x_train, y_train), (x_text, y_test) = mnist.load_data()
#     timer.stop('Data set loaded in')
#
#     return x_train, y_train

def load_data():
    timer = Timer().start('Loading MNIST data set from file..')
    with np.load('data.npz') as fd:
        x_train = fd['x_train']
        y_train = fd['y_train']
        timer.stop('Finished loading in')
    return x_train, y_train

# def morph_data():
#     timer = Timer().start('Loading MNIST data set...')
#     (x_train, y_train), (x_text, y_test) = mnist.load_data()
#     timer.stop('Data set loaded in')
#
#     timer.start('Manipulating data...')
#     y_train = y_train.astype('float32')
#     x_train = x_train.astype('float32')
#     x_train = np.array([mp.move_pic(x) for x in x_train])
#     x_train = x_train.reshape(60000, 784)
#     x_train /= 255
#     timer.stop('Finished in')
#
#     timer.start('Saving data...')
#     np.savez('data.npz', x_train=x_train, y_train=y_train)
#     timer.stop('Saved in')
#
#     return x_train, y_train

if __name__ == '__main__':
    knn = train_knn()