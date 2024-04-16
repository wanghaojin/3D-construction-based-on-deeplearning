import numpy as np
import cv2


class Pixel:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.height = 0
        self.n = (0, 0, 0)

    def update(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n

    def get_height(self, height):
        self.height = height


path = "data"
image = cv2.imread(path)
m, n, _ = image.shape
height_map = [[Pixel() for i in range(m)] for j in range(n)]
