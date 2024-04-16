import torch
import torch.nn as nn


class Linear(nn.Module):
    def __init__(self, input_size, output_size, before=None, after=None):
        super(Linear, self).__init__()
        self.fc = nn.Linear(input_size, output_size)
        if before == None:
            self.before = None
        elif before == "Relu":
            self.before = nn.ReLU()
        elif before == "Sigmoid":
            self.before = nn.Sigmoid()
        elif before == "Tanh":
            self.before = nn.Tanh()
        if after == None:
            self.after = None
        elif after == "Relu":
            self.after = nn.ReLU()
        elif after == "Sigmoid":
            self.after = nn.Sigmoid()
        elif after == "Tanh":
            self.after = nn.Tanh()

    def forward(self, x):
        x = self.before(x)
        return self.after(self.fc(x))


class Constructor(nn.Module):
    def __init__(self, layers):
        super(Constructor, self).__init__()
        self.layers = []
        for i in range(len(layers) - 1):
            if i == 0:
                self.layers.append(
                    Linear(layers[i], layers[i + 1], before=None, after="Relu")
                )
            if i == len(layers) - 2:
                self.layers.append(
                    Linear(layers[i], layers[i + 1], before="Relu", after=None)
                )
            self.layers.append(
                Linear(layers[i], layers[i + 1], before="Relu", after="Relu")
            )
        self.layers = nn.ModuleList(self.layers)

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x


class ShadowConstruction(nn.Module):
    def __init__(self, layers):
        super(ShadowConstruction, self).__init__()
        self.mlp1 = Constructor(layers)
        self.mlp2 = Constructor(layers)
        self.mlp3 = Constructor(layers)

    def forward(self, img1, img2, img3):
        height1 = self.mlp1(img1)
        height2 = self.mlp2(img2)
        height3 = self.mlp3(img3)
        return height1, height2, height3
