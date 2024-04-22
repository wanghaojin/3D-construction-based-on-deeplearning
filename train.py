import torch
import torch.nn as nn
import numpy as np
from utils import *
from model import ShadowConstruction
import torch.nn.functional as F
path = "data"
num_images = 10
train_epoch = 1000
iters = 5
shadows, heights = data_loader(path, num_images, num_ignore=6)
layers = [
    shadows[0].shape[0],
    1024,
    2048,
    1024,
    512,
    256,
    128,
    256,
    512,
    heights[0].shape[0]
    ]
shadowconstruction = ShadowConstruction(layers)
optimizer = torch.optim.Adam(shadowconstruction.parameters(), lr=0.001)
for iter in range(iters):
    print(f"Iteration: {iter}------------------------------------------")
    for epoch in range(train_epoch):
        total_loss = 0
        for i in range(0, len(shadows), 4):
            img1, img2, img3, img4 = [torch.tensor(shadows[j]).float() for j in range(i, i+4)]
            height = torch.tensor(heights[i]).float() 

            optimizer.zero_grad()
            height1, height2, height3, height4 = shadowconstruction(img1, img2, img3, img4)
            height_hat = (height1 + height2 + height3 + height4) / 4
            loss1 = F.mseloss(height_hat, height)
            loss2 = F.mseloss(height1, height2)
            loss3 = F.mseloss(height1, height3)
            loss4 = F.mseloss(height1, height4)
            loss = loss1 + loss2 + loss3 + loss4
            total_loss += loss.item()
            loss.backward()
            optimizer.step()
        average_loss = total_loss / (len(shadows) // 4)
        if epoch % 200 == 0:
            print(f"Epoch: {epoch}, Average Loss: {average_loss}")
    print("---------------------------------------------------------")