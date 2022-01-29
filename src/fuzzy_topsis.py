import numpy as np
import src.punkty_odniesienia as po


#  Sortowanie rankingu:
def bubble_sort(lst1, lst2):
    if lst1 == []:
        return lst1
    n = len(lst1)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if lst2[j] > lst2[j + 1]:
                lst1[j], lst1[j + 1] = lst1[j + 1], lst1[j]
                lst2[j], lst2[j + 1] = lst2[j + 1], lst2[j]
    return lst1, lst2


# Algorytm Fuzzy-Topsis:
def topsis_fuzzy(macierz_decyzyjna, idealnyA1_nieskalowany, nadir_nieskalowany, min_max='min'):
    liczbaAlternatyw, iloscKryteriow = macierz_decyzyjna.shape
    wektorWag = [1, 1, 1, 1, 1]

    macierz_skalowana = np.copy(macierz_decyzyjna)
    idealnyA1 = np.zeros(iloscKryteriow - 1)
    nadir = np.zeros(iloscKryteriow - 1)
    idealnyA1_nieskalowany = list(idealnyA1_nieskalowany[0, :])
    nadir_nieskalowany = list(nadir_nieskalowany[0, :])
    for i in range(1, liczbaAlternatyw):  # SKALOWANIE MACIERZY DECYZJI
        for j in range(1, iloscKryteriow):
            if min_max[j - 1] == 'min':
                macierz_skalowana[i, j] = (macierz_decyzyjna[i, j] * wektorWag[j - 1]) / np.sqrt(
                    sum((macierz_decyzyjna[:, j] ** 2)))
            elif min_max[j - 1] == 'max':
                macierz_skalowana[i, j] = 1 - ((macierz_decyzyjna[i, j] * wektorWag[j - 1]) / np.sqrt(
                    sum((macierz_decyzyjna[:, j] ** 2))))
    for i in range(1, iloscKryteriow):
        if min_max[i - 1] == 'min':
            idealnyA1[i - 1] = (idealnyA1_nieskalowany[i - 1] * wektorWag[i - 1]) / np.sqrt(
                sum((macierz_decyzyjna[:, i] ** 2)))
            nadir[i - 1] = (nadir_nieskalowany[i - 1] * wektorWag[i - 1]) / np.sqrt(
                sum((macierz_decyzyjna[:, i] ** 2)))
        elif min_max[i - 1] == 'max':
            idealnyA1[i - 1] = 1 - ((idealnyA1_nieskalowany[i - 1] * wektorWag[i - 1]) / np.sqrt(
                sum((macierz_decyzyjna[:, i] ** 2))))
            nadir[i - 1] = 1 - ((nadir_nieskalowany[i - 1] * wektorWag[i - 1]) / np.sqrt(
                sum((macierz_decyzyjna[:, i] ** 2))))
    odleglosci = np.zeros((liczbaAlternatyw, 2))

    for i in range(0, liczbaAlternatyw):  # OBLICZENIE ODLEGLOSCI
        sumaIdealny = 0
        sumaAntyIdealny = 0

        for j in range(1, iloscKryteriow):
            sumaIdealny = sumaIdealny + (macierz_skalowana[i, j] - idealnyA1[j - 1]) ** 2
            sumaAntyIdealny = sumaAntyIdealny + (macierz_skalowana[i, j] - nadir[j - 1]) ** 2
            odleglosci[i, 0] = np.sqrt(sumaIdealny)
            odleglosci[i, 1] = np.sqrt(sumaAntyIdealny)

    ranking = np.zeros((liczbaAlternatyw, 2))
    for i in range(0, liczbaAlternatyw):  # RANKING
        ranking[i, 0] = i
        ranking[i, 1] = odleglosci[i, 1] / (odleglosci[i, 0] + odleglosci[i, 1])
    numer_wiersza = list(ranking[:, 0])
    wartosc_rank = list(ranking[:, 1])
    dictionary = {}
    numer_wiersza, wartosc_rank = bubble_sort(numer_wiersza, wartosc_rank)
    for elem in numer_wiersza:
        dictionary[macierz_decyzyjna[int(elem), 0]] = list(macierz_decyzyjna[int(elem), 1:])

    for i in range(len(numer_wiersza)):
        temp_list = list(macierz_decyzyjna[int(numer_wiersza[i]), 1:])
        temp_list.append(wartosc_rank[i])
        dictionary[macierz_decyzyjna[int(numer_wiersza[i]), 0]] = temp_list
    return dictionary


# Funkcja do wywołania całego algorytmu:
def run_topsis(pref, pref_qwo, lista_kryteriow):
    A0, vec_ideal, A3, vec_anty_ideal, A1, idealny_A1, A2, antyidealny_A2, M, flagi = po.wyznaczenie_zbiorow(pref,
                                                                                                             pref_qwo,
                                                                                                             lista_kryteriow)
    return topsis_fuzzy(M, idealny_A1, antyidealny_A2, flagi)

