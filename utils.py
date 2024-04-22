import numpy as np
import os


def data_loader(path, num_images,size, num_ignore=None):
    shadow_list = []
    height_list = []
    for image in range(1, num_images + 1):
        if num_ignore is not None and image in num_ignore:
            continue
        height_path = path + "/Label" + "/" + str(image) + ".npy"
        height = np.load(height_path)
        size = height.shape
        height_list.append(height)
        for index in range(4):
            angle = index * 90
            shadow_path = path + "/Shadow/" + str(image) + "_" + str(angle) + ".npy"
            shadow = np.load(shadow_path)
            shadow = np.resize(shadow, size)
            shadow_list.append(shadow)
        
    return shadow_list, height_list
