import numpy as np
import cv2
import os
from utils_col import Pixel, Divide,calcualte_height,plot_height_map
import pandas as pd

xlsx_source = '../data/RGB.xlsx'
xlsx = pd.read_excel(xlsx_source)
path = "../data/image.tif"
image = None
if os.path.exists(path):
    image = cv2.imread(path)
m, n, _ = image.shape
height_map = [[Pixel() for i in range(m)] for j in range(n)]
num = xlsx['晶面'].isnull().idxmax()
divide_list = []
for i in range(num):
    R, G, B = xlsx['R'][i], xlsx['G'][i], xlsx['B'][i]
    xyz = xlsx['晶面'][0][1:-1].split(' ')
    x, y, z = [int(x) for x in xyz]
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
