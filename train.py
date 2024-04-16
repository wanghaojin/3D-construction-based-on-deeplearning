import torch
import torch.nn as nn
import numpy as np
from utils import *
from model import ShadowConstruction

path = "data"
num_images = 10
shadows, heights = data_loader(path, num_images, num_ignore=6)
layers = [
    shadows[0].shape[0],
    8192,
    4096,
    2048,
    1024,
    512,
    256,
    128,
    256,
    512,
    heights[0].shape[0],
]
shadowconstruction = ShadowConstruction(layers)
optimizer = torch.optim.Adam(shadowconstruction.parameters(), lr=0.001)
