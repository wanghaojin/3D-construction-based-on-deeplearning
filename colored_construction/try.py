import os
import cv2
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Pixel:
    def __init__(self):
        self.height = 0
        self.n = None

    def update(self, n):
        self.n = n

    def update_height(self, height):
        self.height = height

class Plane:
    def __init__(self, RGB, n):
        self.RGB = RGB
        self.n = n

def sub_list(list1, list2):
    return [a - b for a, b in zip(list1, list2)]

# Define paths
main_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(main_dir, '../data')
xlsx_source = os.path.join(data_dir, 'RGB.xlsx')
image_path = os.path.join(data_dir, "image.tif")

# Read the Excel file with RGB and normal vectors
xlsx = pd.read_excel(xlsx_source)
# for index, row in xlsx.iterrows() :
#     if pd.isnull(row['晶面']):
#         continue
#     print(index, '%%%', row)
planes = [Plane([row['R'], row['G'], row['B']], list(map(int, xlsx['晶面'][index][1:-1].split(' ')))) for index, row in xlsx.iterrows() if not pd.isnull(row['晶面'])]

# Load the image
image = cv2.imread(image_path)
if image is not None:
    m, n, _ = image.shape
    height_map = np.zeros((m, n))

    # Map RGB values to normal vectors
    rgb_to_normal = {tuple(plane.RGB): plane.n for plane in planes}

    # Process the image
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(m):
        for j in range(n):
            rgb = tuple(image[i, j][::-1])  # OpenCV reads in BGR
            if rgb in rgb_to_normal:
                # Placeholder: Height calculation logic here
                z = np.linalg.norm(rgb_to_normal[rgb]) * 100  # Just an example height calculation
                height_map[i, j] = z
                ax.scatter(i, j, z, color=np.array(rgb)/255, marker='o')

    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Height')
    plt.show()
else:
    print("Image file not found.")
