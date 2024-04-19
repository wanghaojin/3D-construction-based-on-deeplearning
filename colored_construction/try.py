import os
import cv2
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve
from scipy.ndimage import zoom

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

def poisson_solver(gx, gy):
    """ Solve the Poisson equation using finite difference method """
    ny, nx = gx.shape
    gxx = np.zeros_like(gx)
    gyy = np.zeros_like(gy)

    # Calculate Laplacian
    gxx[1:-1, :] = gx[2:, :] - gx[:-2, :]
    gyy[:, 1:-1] = gy[:, 2:] - gy[:, :-2]

    laplacian = gxx + gyy

    # Boundary conditions
    boundary = np.zeros((ny, nx))

    # Solve Poisson equation
    f = laplacian.ravel() + boundary.ravel()
    A = lil_matrix((nx*ny, nx*ny))

    for j in range(ny):
        for i in range(nx):
            k = i + nx*j
            A[k, k] = -4
            if i > 0:    A[k, k-1] = 1
            if i < nx-1: A[k, k+1] = 1
            if j > 0:    A[k, k-nx] = 1
            if j < ny-1: A[k, k+nx] = 1

    A = csr_matrix(A)
    result = spsolve(A, f)
    return result.reshape((ny, nx))
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
    gx = np.zeros((m, n))
    gy = np.zeros((m, n))

    # Map RGB values to normal vectors
    rgb_to_normal = {tuple(plane.RGB): np.array(plane.n) for plane in planes}

    # Process the image and calculate gradients
    for i in range(m):
        for j in range(n):
            rgb = tuple(image[i, j][::-1])  # Convert from BGR to RGB
            if rgb in rgb_to_normal:
                normal = rgb_to_normal[rgb]
                nz = normal[2] if normal[2] != 0 else 1  # Prevent division by zero
                gx[i, j] = normal[0] / nz
                gy[i, j] = normal[1] / nz

    # Solve Poisson equation to obtain the height map
    height_map = poisson_solver(gx, gy)
    
    scale_factor = (101 / height_map.shape[0], 101 / height_map.shape[1])
    height_map = zoom(height_map, scale_factor, mode='nearest')
    
    np.save('height_map.npy', height_map)
    
    
    # Plot the result
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    m, n = height_map.shape
    X, Y = np.meshgrid(np.arange(n), np.arange(m))
    ax.plot_surface(X, Y, height_map, cmap='viridis')

    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Height')
    plt.show()
else:
    print("Image file not found.")
