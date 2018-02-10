import numpy as np
from train_knn import train_knn


def copy_image(frame, cx, cy):
    img = np.zeros((28, 28))
    for x in range(0, 28):
        for y in range(0, 28):
            if (not y + cy >= frame.shape[0]) and (not x + cx >= frame.shape[1]):
                col = frame[y + cy, x + cx]
                col = (col[0] / 255.0 + col[1] / 255.0 + col[2] / 255.0) / 3.0
                img[y, x] = col
    return img


class KNN:
    model = None

    def __init__(self):
        self.load_model()

    def load_model(self):
        if KNN.model is None:
            KNN.model = train_knn()

    def predict(self, target):
        target = target.reshape(1, 784).astype('float32')
        return int(self.model.findNearest(target, k=1)[0])
