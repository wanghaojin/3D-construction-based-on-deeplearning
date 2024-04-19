import numpy as np
import cv2
import os
from utils_col import Pixel, Plane, calcualte_height,sub_list,add_list
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
mplstyle.use('fast')

main_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(main_dir, '../data')
xlsx_source = os.path.join(data_dir, 'RGB.xlsx')
xlsx = pd.read_excel(xlsx_source)
path = os.path.join(data_dir, "image.tif")

n_ob = [1,0.83,0.97]
n_st = [0,0,1]
n_tr = sub_list(n_st,n_ob)

image = None
if os.path.exists(path):
    image = cv2.imread(path)
m, n, _ = image.shape
height_map = [[Pixel() for i in range(m)] for j in range(n)]
num = xlsx['晶面'].isnull().idxmax()

if os.path.exists('height_map.npy'):
    height_map = np.load(os.path.join(data_dir, 'height_map.npy'))
else:
    plane_list = []
    for i in range(num):
        R, G, B = xlsx['R'][i], xlsx['G'][i], xlsx['B'][i]
        xyz = xlsx['晶面'][i][1:-1].split(' ')
        x, y, z = [int(x) for x in xyz]
        plane_list.append(Plane([R, G, B], [x, y, z]))
    for i in range(m):
        for j in range(n):
            R_img = image[i][j][2]
            G_img = image[i][j][1]
            B_img = image[i][j][0]
            RGB_img = [R_img, G_img, B_img]
            for plane in plane_list:
                if plane.RGB == RGB_img:
                    height_map[i][j].update(add_list(plane.n,n_tr))
                    break
            if j == 0:
                continue
            if height_map[i][j].n == None or height_map[i][j-1].n == None: 
                height_map[i][j].update_height(height_map[i][j-1].height)
                continue
            height_map[i][j].update_height(height_map[i][j-1].height+calcualte_height(height_map[i][j-1].n, height_map[i][j].n))
    m,n = len(height_map), len(height_map[0])
    height_map = np.array([[height_map[i][j].height for j in range(n)] for i in range(m)])
    np.save(os.path.join(data_dir, 'height_map.npy'), height_map)
x = np.arange(m)
y = np.arange(n)
x,y = np.meshgrid(x,y)
# height_map = height_map.astype(int)

sampling_factor = 10
height_map_downsampled = height_map[::sampling_factor, ::sampling_factor]
x_downsampled = np.arange(0, height_map.shape[0], sampling_factor)
y_downsampled = np.arange(0, height_map.shape[1], sampling_factor)
x_downsampled, y_downsampled = np.meshgrid(x_downsampled, y_downsampled)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surface = ax.plot_surface(x_downsampled, y_downsampled, height_map_downsampled, rstride=1, cstride=1, cmap='viridis')
fig.colorbar(surface)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Height')
ax.set_title('3D Construction (Downsampled)')
plt.show()



# for i in range(m):
#     for j in range(n):
#         if(height_map[i][j].n != [1,0,1] and height_map[i][j].n!= None):
#             print(height_map[i][j].n)
