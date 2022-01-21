# Tu powninny się znaleźć takie funkcje jak
# * wczytywanie danych z excela
# * wzynacznie zbiorów A0, A1, A2, A3
from copy import deepcopy

class Point:
    def __init__(self, cor: list,name = None,skoring = None):
        self.name = name
        self.cor = deepcopy(cor)
        self.len = len(cor)
        self.skoring = skoring

    def __len__(self):
        return len(self.cor)