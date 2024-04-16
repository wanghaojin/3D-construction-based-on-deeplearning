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
