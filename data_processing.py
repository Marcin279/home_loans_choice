# Tu powninny się znaleźć takie funkcje jak
# * wczytywanie danych z excela
# * wzynacznie zbiorów A0, A1, A2, A3
from copy import deepcopy

class Point:
    def __init__(self, cor: list):
        self.cor = deepcopy(cor)
        self.len = len(cor)