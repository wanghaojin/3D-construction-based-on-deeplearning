import numpy as np
import cv2
import os
from utils_col import Pixel, Divide,calcualte_height,plot_height_map
import pandas as pd
sorce = 'data/RGB.xlsx'
path = "data/image.tif"
image = None
if os.path.exists(path):
    image = cv2.imread(path)
df = pd.read_excel(sorce)

m, n, _ = image.shape
height_map = [[Pixel() for i in range(m)] for j in range(n)]
num = int(input("Number of Colors: "))
divide_list = []
for i in range(num):
    R, G, B = map(int, input("R,G,B:").split())
    x, y, z = map(float, input("n: ").split())
    divide_list.append(Divide([R, G, B], [x, y, z]))
for i in range(m):
    for j in range(n):
        R_img = image[i][j][2]
        G_img = image[i][j][1]
        B_img = image[i][j][0]
        RGB_img = (R_img, G_img, B_img)
        for divide in divide_list:
            if divide.RGB == RGB_img:
                height_map[i][j].update(divide.n)
                break
        if j == 0:
            continue
        if height_map[i][j].n == None: 
            height_map[i][j].update_height(height_map[i][j-1].height)
            continue
        height_map[i][j].update_height(height_map[i][j-1].height+calcualte_height(height_map[i][j-1].n, height_map[i][j].n))
plot_height_map(height_map)
