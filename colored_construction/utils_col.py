import matplotlib.pyplot as plt
import numpy as np
import math
class Pixel:
    def __init__(self):
        self.height = 0
        self.n = None

    def update(self, n):
        self.n = n

    def update_height(self, height):
        self.height = height
class Plane:
    def __init__(self,RGB,n):
        self.RGB = RGB
        self.n = n

def calcualte_height(n0,n1):
    a0 = n0[0]
    b0 = n0[1]
    c0 = n0[2]
    a1 = n1[0]
    b1 = n1[1]
    c1 = n1[2]
    if n0 != n1:
        delta_h = math.sqrt(1-((a0*a1 + b0*b1 + c0*c1) / (math.sqrt(a0**2 + b0**2 + c0**2) * math.sqrt(a1**2 + b1**2 + c1**2)))**2)
    if n0 == n1:
        c1 = 0
        delta_h = (a0*a1 + b0*b1 + c0*c1) / (math.sqrt(a0**2 + b0**2 + c0**2) * math.sqrt(a1**2 + b1**2 + c1**2))

    return delta_h

def sub_list(a,b):
    return [a[i]-b[i] for i in range(len(a))]
def add_list(a,b):
    return [a[i]+b[i] for i in range(len(a))]
    
def plot_3D_height_map(height_map, sampling_factor=10):
    """
    Function to plot the 3D structure of the height map.
    """
    # Sampling the height map to make the plot less dense and easier to view
    height_map_downsampled = height_map[::sampling_factor, ::sampling_factor]
    x = np.arange(0, height_map.shape[0], sampling_factor)
    y = np.arange(0, height_map.shape[1], sampling_factor)
    x, y = np.meshgrid(x, y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Plotting the surface
    ax.plot_surface(x, y, height_map_downsampled, cmap='viridis')

    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_zlabel('Height')
    plt.title('3D Height Map Visualization')
    plt.show()