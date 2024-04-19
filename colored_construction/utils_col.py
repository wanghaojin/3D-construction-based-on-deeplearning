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
class Divide:
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
    