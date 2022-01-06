from mpl_toolkits import mplot3d
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm
import math
from data_processing import *

A1_point = Point(2,1,1)
u = Point(5,5,5)
A2_point = Point(11,11,9)

class SP_CS:
    def __init__(self):
        self.set_A0 = []
        self.set_A1 = []
        self.set_A2 = []
        self.set_A3 = []
        self.set_B0 = []
    
def oblicz_d(A1_point,A2_point):
    d = []
    for i in range(A1_point.len):
        d_ = (A2_point.cor[i] - A1_point.cor[i])/2
        d.append(d_)
    return min(d)

def krzywa_woronoya(A1_point,A2_point):
    d = oblicz_d(A1_point,A2_point)
    f1 = []
    f2 = []
    for i in range(A1_point.len):
        f1.append(A1_point.cor[i]+d)
        f2.append(A2_point.cor[i]-d)
    f1 = Point(*f1)
    f2 = Point(*f2)
    return (A1_point,f1,f2,A2_point)

def odleglosc_od_prostej(u,A1_odc, A2_odc):
    p = np.asarray(u.cor)
    a = np.asarray(A1_odc.cor)
    b = np.asarray(A2_odc.cor)

    # normalized tangent vector
    d = np.divide(b - a, np.linalg.norm(b - a))

    # signed parallel distance components
    s = np.dot(a - p, d)
    t = np.dot(p - b, d)

    # clamped parallel distance
    h = np.maximum.reduce([s, t, 0])

    # perpendicular distance component
    c = np.cross(p - a, d)

    return np.hypot(h, np.linalg.norm(c))

def oblicz_dlugosc_odcinka(point_1, point_2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(point_1.cor, point_2.cor)]))

def sprawdz_czy_punkt_u_w_odcinku_AB(u, point_1, point_2):
    odc_u_point_1 = oblicz_dlugosc_odcinka(u, point_1) # c
    odc_u_point_2 = oblicz_dlugosc_odcinka(u, point_2) # b
    odc_point_1_point_2 = oblicz_dlugosc_odcinka(point_1, point_2) # a
    result = False
    lst_odcinek = [odc_u_point_1, odc_point_1_point_2, odc_u_point_2]

    a_idx = lst_odcinek.index(max(lst_odcinek))
    a = lst_odcinek[a_idx]

    czy_trojkat_rozw = False
    if odc_point_1_point_2+odc_u_point_2 > odc_u_point_1 and odc_point_1_point_2+odc_u_point_1>odc_u_point_2 and odc_u_point_2+odc_u_point_1>odc_point_1_point_2:
        if odc_point_1_point_2**2+odc_u_point_2**2<odc_u_point_1**2 or odc_point_1_point_2**2+odc_u_point_1**2 < odc_u_point_2**2 or odc_u_point_2**2+odc_u_point_1**2<odc_point_1_point_2**2:
            czy_trojkat_rozw = True
        else:
            czy_trojkat_rozw = False
    
    if czy_trojkat_rozw and odc_point_1_point_2 != a:
        result = False
        
    else:
        result = True
    
    return result

def point_on_line(u, a, b):
    # au = u.cor - a.cor
    # ab = b.cor - a.cor
    # t = np.dot(au, ab) / np.dot(ab, ab)
    # # if you need the the closest point belonging to the segment
    # t = max(0, min(1, t))
    # # print('ab', ab, 'au', au, 't', t)
    # result = a.cor + t * ab
    # return result
    pass

ob = krzywa_woronoya(A1_point,A2_point)
x = []
y = []
z = []
for el in ob:
    print(el.cor)
    x.append(el.cor[0])
    y.append(el.cor[1])
    z.append(el.cor[2])

print(x)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(x, y, z, 'gray')
ax.scatter3D(x, y, z, c=z, cmap='brg')
plt.show()

# a = Point(1,1,1,1)
# b = Point(7,1,1,1)
# c = Point(4,5,1,1)
a = Point(1,1,1)
b = Point(7,1,1)
c = Point(4,4,1)

print(odleglosc_od_prostej(c,a,b))

print(oblicz_dlugosc_odcinka(a,b))

print(sprawdz_czy_punkt_u_w_odcinku_AB(c,a,b))

print(point_on_line(c,a,b))