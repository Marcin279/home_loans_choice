import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple, List, Union, Optional
from copy import deepcopy
import punkty_odniesienia as po


class Point:
    def __init__(self, cor: list, name=None, skoring=None):
        self.name = name
        self.cor = deepcopy(cor)
        self.len = len(cor)
        self.skoring = skoring

    def __len__(self):
        return len(self.cor)


# crits_type = {'Marża [%]': 1, 'Prowizja [%]': 0, 'RRSO [%]': 0, 'Koszt miesięczny [PLN]': 1, 'Wkład własny [%]': 0,
#               'Opinie[pkt. Max. 5]': 1}
#
# lista_kryteriow = ['Punkt']
#
# for k, v in crits_type.items():
#     if v == 0:
#         continue
#     else:
#         lista_kryteriow.append(k)

lista_kryteriow = []

# dane = pd.read_excel("dane.xlsx", 'Arkusz3')

# pref = np.array([1700, 20, -5])
# pref_qwo = np.array([2300, 41, -1])

# W gui zmienić na ujemne oceny
# pref = np.array([1.2, 15, -6])
# pref_qwo = np.array([3.5, 42, -1])
#
# A0, vec_ideal, A3, vec_anty_ideal, A1, idealny_A1, A2, idealny_A2, B0, flagi = po.wyznaczenie_zbiorow(pref, pref_qwo,
#                                                                                                       lista_kryteriow)
#
# A1_points = []
# A2_points = []
# B0_points = []

# for i, row in enumerate(A1):
#     print(len(row))
#     if len(row) == 3:
#         A1_points.append(Point([row[1], row[2], row[3]], row[0]))
#     if len(row) == 2:
#         A1_points.append(Point([row[1], row[2]], row[0]))
#
# for i, row in enumerate(A2):
#     if len(row) == 3:
#         A1_points.append(Point([row[1], row[2], row[3]], row[0]))
#     if len(row) == 2:
#         A1_points.append(Point([row[1], row[2]], row[0]))
#
# for i, row in enumerate(B0):
#     if len(row) == 3:
#         A1_points.append(Point([row[1], row[2], row[3]], row[0]))
#     if len(row) == 2:
#         A1_points.append(Point([row[1], row[2]], row[0]))


# for i, row in enumerate(A1):
#     A1_points.append(Point([row[1], row[2], row[3]], row[0]))
#
# for i, row in enumerate(A2):
#     A2_points.append(Point([row[1], row[2], row[3]], row[0]))
#
# for i, row in enumerate(B0):
#     B0_points.append(Point([row[1], row[2], row[3]], row[0]))


# A1_points = A1_points.tolist()
# A2_points = A2_points.tolist()
# B0_points = B0_points.tolist()

def check(u, point_A1, point_A2) -> bool:
    """
    Sprawdzanie czy dana dany punkt znajduje się w prostokącie stworzonym przez punktu ze
    zbioru A1 i A2

    params: -u: Tuple(int, int)
            -A1_point: Tuple(int, int),
            -A2_point: Tuple(int, int),

    Return: bool
    """
    """ Zmienić warunki w przypadku maksymalizacji!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! """
    if len(u.cor) == 2:
        if 'Opinie[pkt. Max. 5]' not in lista_kryteriow:
            if ((u.cor[0] >= point_A1.cor[0]) and (u.cor[0] <= point_A2.cor[0])) and (
                    (u.cor[1] >= point_A1.cor[1]) and (u.cor[1] <= point_A2.cor[1])):
                return True
            else:
                return False
        else:
            if ((u.cor[0] >= point_A1.cor[0]) and (u.cor[0] <= point_A2.cor[0])) and (
                    (u.cor[1] <= point_A1.cor[1]) and (u.cor[1] >= point_A2.cor[1])):
                return True
            else:
                return False
    elif len(u.cor) == 3:
        if 'Opinie[pkt. Max. 5]' not in lista_kryteriow:
            if ((u.cor[0] >= point_A1.cor[0]) and (u.cor[0] <= point_A2.cor[0])) and (
                    (u.cor[1] >= point_A1.cor[1]) and (u.cor[1] <= point_A2.cor[1])) and (
                    (u.cor[2] >= point_A1.cor[2]) and (u.cor[2] <= point_A2.cor[2])):
                return True
            else:
                return False
        else:
            if ((u.cor[0] >= point_A1.cor[0]) and (u.cor[0] <= point_A2.cor[0])) and (
                    (u.cor[1] >= point_A1.cor[1]) and (u.cor[1] <= point_A2.cor[1])) and (
                    (u.cor[2] <= point_A1.cor[2]) and (u.cor[2] >= point_A2.cor[2])):
                return True
            else:
                return False


def oblicz_P_lub_V(A1_point: Tuple, A2_point: Tuple, u: Tuple) -> Tuple:
    """
    Funkcja obliczająca pole pomiędzy A1_point, A2_point i sprawdza czy punkt ze zbioru status-quo znajduje się w
    obrębie tego prostokąta.


    params: -A1_point: Tuple(int, int),
            -A2_point: Tuple(int, int),
            -u: Tuple(int, int)

    Return: Tuple(Optional[Union[float, int], str, str])
    """
    p1 = A1_point
    p2 = A2_point
    if len(u.cor) == 2:
        if check(u, A1_point, A2_point):
            return abs(A1_point.cor[0] - A2_point.cor[0]) * abs(A1_point.cor[1] - A2_point.cor[1]), p1, p2
        else:
            return 0, p1, p2
    elif len(u.cor) == 3:
        if check(u, A1_point, A2_point):
            return abs(A1_point.cor[0] - A2_point.cor[0]) * abs(A1_point.cor[1] - A2_point.cor[1]) * abs(
                A1_point.cor[2] - A2_point.cor[2]), p1, p2
        else:
            return 0, p1, p2


def wagi(A1, A2, u) -> List:
    """
    Funkcja obliczająca wagi na podstawie punktów A1, A2, u
    Wewnętrznie sprawdzany jest warunek czy dany punkt u znajduje się w prostokącie A1, A2

    params: -A1: List[Tuple(int, int)],
            -A2: List[Tuple(int, int)],
            -u: Tuple(int, int)

    Return: List[Tuple(float, str, str)]
    """
    suma = 0
    pola = []
    wagi_ = []

    for A1_point in A1:
        for A2_point in A2:
            p1 = A1_point
            p2 = A2_point
            pole = oblicz_P_lub_V(A1_point, A2_point, u)[0]
            suma += pole
            pola.append((pole, p1, p2))

    for pole_ in pola:
        pole, p1, p2 = pole_
        if suma != 0:
            waga = pole / suma
        else:
            waga = 0
        wagi_.append((waga, p1, p2))

    return wagi_


def check_if_weight_sum_to_1(A1, A2, u):
    """
    Funkcja sprawdzająca czy obliczone wagi z danego punktu u sumują się do 1
    """
    x = wagi(A1, A2, u)
    suma = 0
    for i in x:
        suma += i[0]
    return suma


# A1_point = Point([10,10,10])
# u = Point([10,10,10])
# A2_point = Point([30,30,30])


# suma = check_if_weight_sum_to_1([A1_point], [A2_point], u)
# print("Sprawdzenie czy suma ", suma)


# print(check(dct['N21'],dct['N11'],dct['N16']))
def distance(u: Tuple, A: Tuple) -> float:
    """
    Funkcja obliczająca dystans z punktu u do A
    params: u - Tuple(int, int)
            A - Tuple(int, int)

    return: float
    """
    if len(u.cor) == 2:
        d = np.sqrt((u.cor[0] - A.cor[0]) ** 2 + (u.cor[1] - A.cor[1]) ** 2)
    elif len(u.cor) == 3:
        d = np.sqrt((u.cor[0] - A.cor[0]) ** 2 + (u.cor[1] - A.cor[1]) ** 2 + (u.cor[2] - A.cor[2]) ** 2)
    return d


def skoring(u, A1, A2) -> Tuple:
    """
    Funkcja wyliczajaca wartość funkcji skoringowej dla danego
    punktu u ze zbioru status quo

    params:
    u - Tuple(int, int)
    A1 - List[Tuple(int, int)]
    A2 - List[Tuple(int, int)]

    """
    wagi_ = wagi(A1, A2, u)
    F = 0
    for waga, A1_point, A2_point in wagi_:
        d_idealny = distance(u, A1_point)
        d_anty = distance(u, A2_point)
        f = d_anty / (d_anty + d_idealny)
        F += waga * f
    u_ = u.name
    return F


def fill_points(A1, A2, B0):
    A1_points = []
    A2_points = []
    B0_points = []

    for i, row in enumerate(A1):
        if len(row) == 3:
            A1_points.append(Point([row[1], row[2]], row[0]))
        if len(row) == 4:
            A1_points.append(Point([row[1], row[2], row[3]], row[0]))

    for i, row in enumerate(A2):
        if len(row) == 3:
            A2_points.append(Point([row[1], row[2]], row[0]))
        if len(row) == 4:
            A2_points.append(Point([row[1], row[2], row[3]], row[0]))

    for i, row in enumerate(B0):
        if len(row) == 3:
            B0_points.append(Point([row[1], row[2]], row[0]))
        if len(row) == 4:
            B0_points.append(Point([row[1], row[2], row[3]], row[0]))

    return A1_points, A2_points, B0_points


# Poniższa częśc kodu odpowiada za tworzenie rankingu
# ranking jest zwracany w postaci List[Tuple(float, str')]
# listy punktów od najlepszego do najgorszego
def run_rsm(criteria):
    #
    global lista_kryteriow
    lista_kryteriow = criteria
    # pref = np.array([1.2, 15, -6])
    # pref_qwo = np.array([3.5, 42, -1])
    pref = np.array([1.2, -6])
    pref_qwo = np.array([3.5, -1])
    # C_2_6 + C_3_6
    A0, vec_ideal, A3, vec_anty_ideal, A1, idealny_A1, A2, idealny_A2, B0, flagi = po.wyznaczenie_zbiorow(pref,
                                                                                                          pref_qwo,
                                                                                                          criteria)

    A1_points, A2_points, B0_points = fill_points(A1, A2, B0)

    dct_out = {}
    for point in B0_points:
        dct_out[point] = skoring(point, A1_points, A2_points)

    dct_out = dict(sorted(dct_out.items(), key=lambda item: item[1], reverse=True))

    dct_out1 = {}

    for key in dct_out:
        if len(key.cor) == 2:
            dct_out1[key.name] = [key.cor[0], key.cor[1]]
        if len(key.cor) == 3:
            dct_out1[key.name] = [key.cor[0], key.cor[1], key.cor[2]]

    return dct_out1


# print(run_rsm(lista_kryteriow))
# kryteria = ['Punkt','Marża [%]','Wkład własny [%]','Opinie[pkt. Max. 5]']

# print(run_rsm(kryteria))
