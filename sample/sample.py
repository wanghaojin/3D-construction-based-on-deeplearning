import numpy as np
import matplotlib.pyplot as plt


def rectangle_(xl,yl,h,sample_position,sample_space,dl):#dl is dx,h in m  
    ###########矩形区域x方向宽度xl（m）y方向宽度（m），升高h(m),sample_position:中心位置[x,y]，sample_space：给定尺寸的0矩阵。dl是xy平面格点间距，
    xl_half = int(np.round(xl / (2 * dl)))
    yl_half = int(np.round(yl / (2 * dl)))
    x_center, y_center = np.round(np.array(sample_position) / dl).astype(int)
    
    x_start = max(x_center - xl_half, 0)
    x_end = min(x_center + xl_half, sample_space.shape[0])
    y_start = max(y_center - yl_half, 0)
    y_end = min(y_center + yl_half, sample_space.shape[1])
    sample_space[x_start:x_end, y_start:y_end] += h


def lean_tower(xl1,xl2,lean_angle,sample_position,sample_space,dl):#四棱柱金字塔结构，xl1：棱柱塔底宽度，xl2：棱柱顶宽度，lean_angle斜面倾斜角度，
    xl1r=round(xl1/dl)
    xl2r=round(xl2/dl)
    #print (xl1r)
    for i in np.arange(xl2,xl1,2*dl):
        height = dl * np.tan(lean_angle)
    for i in np.arange(xl2, xl1, 2 * dl):
        rectangle_(i, i, height, sample_position, sample_space, dl)


# #flight above sample
# sample_l=100 #样品尺寸/格点间距
# dl=0.3e-6
# sample_space= np.zeros((sample_l+1, sample_l+1), dtype=float)#sample_space：给定尺寸的0矩阵
# sample_position=[15e-6,15e-6]
# #三层棱柱堆叠
# sample_space=lean_tower(20.28e-6,17.81e-6,1/6*np.pi,sample_position,sample_space,dl)
# sample_space=lean_tower(13.15e-6,10.66e-6,1/6*np.pi,sample_position,sample_space,dl)
# sample_space=lean_tower(6.205e-6,3.53e-6,1/6*np.pi,sample_position,sample_space,dl)

# name='sample.npy'
# np.save(name,sample_space)  ###### S A V E


# #PLOT SAMPLE HIGHT
# sample_space=np.load(name)
# plt.figure()
# xlplot=dl*sample_l#样品尺寸
# sample_space_show=sample_space.T
# plt.imshow(sample_space_show,origin='lower',extent=[0, xlplot, 0, xlplot] )

# plt.colorbar(label='hight')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Sample')
# plt.show()
sample_l = 100
dl = 0.3e-6
sample_space = np.zeros((sample_l + 1, sample_l + 1), dtype=float)
sample_position = [15e-6, 15e-6]
towers = [
    (20.28e-6, 17.81e-6),
    (13.15e-6, 10.66e-6),
    (6.205e-6, 3.53e-6)
]
for base, top in towers:
    lean_tower(base, top, 1/6*np.pi, sample_position, sample_space, dl)

np.save('sample1.npy', sample_space)  
sample_space = np.load('sample1.npy') 

plt.figure()
xlplot = dl * sample_l
plt.imshow(sample_space.T, origin='lower', extent=[0, xlplot, 0, xlplot])
plt.colorbar(label='Height (m)')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('Sample Structure')
plt.show()