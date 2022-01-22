import numpy as np
import pandas as pd

# Pobieranie danych do macierzy:
def data(path):
    my_data = pd.read_csv("dane_2.csv", sep=";", encoding='latin-1')
    my_data = my_data.values 
    my_data = my_data[:,:my_data.shape[1] - 1]  
    return my_data


# Ustawianie ręczne flag czy kryterium ma dążyć do maks czy do min
def flagi_kryteriow():
    kryteria = ['min', 'min', 'min', 'min', 'min']
    return kryteria


# Ustawienie wszystkich kryteriów żeby dążyły do minimum (początkowo zmienia do minimu a po drugim wywołaniu z powrotem)
def odwrocenie_max_kryteriow(M):
    flagi = flagi_kryteriow()
    for i in range(0, len(flagi)):
        if flagi[i] == 'max':
            M[:, i] = -M[:, i]
    return M


#  Funkcja wyznacza wszystkie punkty niezdominowane, które są jednocześnie nieporównywalne (dożąc do minium)
def punkty_niezdominowe_nieporownywalne(matrix):
    # Wyznaczenie rozmiarów macierzy:
    liczba_decyzji = matrix.shape[0]
    liczba_kryteriow = matrix.shape[1]

    # Szukamy punktów nie zdominowanych, albo nie porównywalnych (kryteria -> min)
    nieporownywalne = matrix[0,:].reshape((1,liczba_kryteriow))
    nie_zdominowany = matrix[0,:]
    
    for i in range(1, liczba_decyzji):
        # wskaźnik czy punkty obecny niezdominowany dalej dominuje nad innymi punktami:
        # czy_zdominowany = 0 to niezdominowany, czy_zdominowany = liczba kryteriow to zdaminowany,
        # a pomiędzy to nieporównywalny
        czy_zdominowany = 0
        rowne = 0
        for j in range(liczba_kryteriow):
            if nie_zdominowany[j] < matrix[i,j]:
                czy_zdominowany += 1
            elif nie_zdominowany[j] > matrix[i,j]:
                czy_zdominowany += 0
            else:
                rowne += 1

        r = liczba_kryteriow - rowne
        if  r == 0 or (czy_zdominowany > 0 and czy_zdominowany < r):
            # tworzenie macierzy nieporownywalnej
            nieporownywalne = np.concatenate((nieporownywalne, matrix[i,:].reshape((1,liczba_kryteriow))),axis=0) 
        elif czy_zdominowany == 0: 
            # Zamiana punktu niezdominowanage i inicjalizacja nowej mocierzy punktów nieporównywalnych
            stare_nieporownywalne = nieporownywalne
            nie_zdominowany = matrix[i,:]
            # Porównanie czy nowy punkt dominuje nad starymi w macierzy nieporównywalne:
            if stare_nieporownywalne.shape[0] != 1:
                stare_nieporownywalne = np.concatenate((nie_zdominowany.reshape((1,liczba_kryteriow)), stare_nieporownywalne), axis=0)
                nieporownywalne = punkty_niezdominowe_nieporownywalne(stare_nieporownywalne)
            else:
                nieporownywalne = nie_zdominowany.reshape((1,liczba_kryteriow))
        elif czy_zdominowany == r:
            # nic nie rób
            continue
    return nieporownywalne


# Funkcja wyznaczająca zbiory A0 i A3 wraz z ich wektorami idealnymi (korzysta z funkcji 'punkty_niezdominowe_nieporownywalne')
def punkty_najlepsze(matrix, flaga='min'):
    if flaga == 'max':
        matrix = -matrix
    liczba_decyzji = matrix.shape[0]
    liczba_kryteriow = matrix.shape[1]

    # Wyznaczenie punktów nieporównywalnych i punktu niezdominowanego:
    nieporow = punkty_niezdominowe_nieporownywalne(matrix)
    nie_zdomin = nieporow[0,:]


    # Trzeba teraz wykonać powyższą funkcję dla zbioru punktów nieporównywalnych jeżeli jest ich więcej niż 2 (bez punktu niezdominowanego)
    nieporow_kol = nieporow
    nieporow = nie_zdomin.reshape((1,liczba_kryteriow))
    while nieporow_kol.shape[0] > 2:
        nieporow_kol = punkty_niezdominowe_nieporownywalne(nieporow_kol[1:,:])
        nie_zdomin_kol = nieporow_kol[0,:]
        nieporow = np.concatenate((nie_zdomin_kol.reshape((1,liczba_kryteriow)), nieporow), axis=0)


    if nieporow_kol.shape == (2,liczba_kryteriow):
        nieporow = np.concatenate((nieporow_kol[1,:].reshape((1,liczba_kryteriow)), nieporow), axis=0)

    # Utworzenie macierzy punktów najlepszych, dla flagi 'max' najgorszych
    A0 = nieporow

    # Wyznaczenie punktu idealnego --> min ze zbioru A0 nie musi należeć do A0:
    # W przypadku flagi 'max' wyznaczenie punktu antyidealnego
    lst_param = []
    for i in range(A0.shape[1]):
        lst_param.append(A0[:,i].min())
    idealny = np.array([lst_param])

    
    if flaga == 'max':
        A0 = -A0
        idealny = - idealny

    return A0, idealny


# Sprawdzenie warunku wewnętrznej niesprzeczności i związane z tym poprawienie klasy i-tej klasy A
def wewnetrzna_niesprzecznosc(A):
    liczba_kryteriow = A.shape[1]

    # Wyznaczenie punktów nieporównywalnych i punktu niezdominowanego dla macierzy (zdominowane zostają odrzucone):
    nieporow = punkty_niezdominowe_nieporownywalne(A)
    nie_zdomin = nieporow[0,:]

    # Trzeba teraz wykonać powyższą funkcję dla zbioru punktów nieporównywalnych w pętli jeżeli jest ich więcej niż 2 (bez punktu niezdominowanego - jest to pierwszy punkt w macierzy nieporównywalne)
    nieporow_kol = nieporow
    nieporow = nie_zdomin.reshape((1,liczba_kryteriow))
    while nieporow_kol.shape[0] > 2:
        nieporow_kol = punkty_niezdominowe_nieporownywalne(nieporow_kol[1:,:])
        nie_zdomin_kol = nieporow_kol[0,:]
        nieporow = np.concatenate((nie_zdomin_kol.reshape((1,liczba_kryteriow)), nieporow), axis=0)

    if nieporow_kol.shape == (2,liczba_kryteriow):
        nieporow = np.concatenate((nieporow_kol[1,:].reshape((1,liczba_kryteriow)), nieporow), axis=0)

    return nieporow


# Sprawdzenie warunku zewnętrznej niesprzeczności, a tym samym poprawa zbioru A o wyższym indeksie
def zewnetrzna_niesprzecznosc(A_wieksza, A_mniejsza):
    #  Zakładamy że liczba kryteriow A i B jest taka sama:
    liczba_kryt = A_wieksza.shape[1]
    liczba_ptkA = A_wieksza.shape[0]
    liczba_ptkB = A_mniejsza.shape[0]

    nowe_ptk_A = []
    for i in range(liczba_ptkA):
        warunek = False
        prownanie = 0
        for j in range(liczba_ptkB):
            for k in range(liczba_kryt):
                if A_wieksza[i,k] < A_mniejsza[j,k]:
                    warunek = False
                    break
                else:
                    warunek = True

            if warunek:
                porownanie = A_mniejsza[j,:]
                break
        if warunek:
            if np.equal(A_wieksza[i,:], porownanie).all():
                pass
            else:
                nowe_ptk_A.append(A_wieksza[i,:])

    nowa_A = np.array(nowe_ptk_A)
    return nowa_A


# Funkcja do wyznaczania zbiorów A1, A2:
def nieporownywalne_dla_preferencji(preferencja, matrix):
    liczba_kryteriow = matrix.shape[1]
    liczba_decyzji = matrix.shape[0]

    nieporownywalne = preferencja.reshape((1,liczba_kryteriow))
    for i in range(1, liczba_decyzji):
        # wskaźnik czy punkty obecny niezdominowany dalej dominuje nad innymi punktami:
        # czy_zdominowany = 0 to niezdominowany, czy_zdominowany = liczba kryteriow to zdaminowany,
        # a pomiędzy to nieporównywalny
        czy_zdominowany = 0
        rowne = 0
        for j in range(liczba_kryteriow):
            if preferencja[j] < matrix[i,j]:
                czy_zdominowany += 1
            elif preferencja[j] > matrix[i,j]:
                czy_zdominowany += 0
            else:
                rowne += 1

        r = liczba_kryteriow - rowne
        if r == 0 or ( czy_zdominowany > 0 and czy_zdominowany < r):
            # tworzenie macierzy nieporownywalnej
            nieporownywalne = np.concatenate((nieporownywalne, matrix[i,:].reshape((1,liczba_kryteriow))),axis=0) 
        elif czy_zdominowany == r:
            # nic nie rób
            continue
        elif czy_zdominowany == 0:
            # nic nie rób
            continue
    return nieporownywalne


#  Wyznaczenie wektora idealnego dla Klas A1, A2:
def punkt_idealny_dla_klasy_preferencji(A, flaga = 'min'):
    # Wyznaczenie punktu idealnego --> min ze zbioru A1 nie musi należeć do A1:
    # W przypadku flagi 'max' wyznaczenie punktu antyidealnego dla A2, nie musi należeć do A2
    if flaga == 'max':
        A = -A

    lst_param = []
    for i in range(A.shape[1]):
        lst_param.append(A[:,i].min())
    idealny = np.array([lst_param])
    
    if flaga == 'max':
        idealny = -idealny
    return idealny


# Wyznaczenie decyzji między zbiorem A1 i A2 do stworzenia rankingu (jeżeli pomiędzy jest zbiór pusty to rozważamy zbiór A2)
def wyznaczanie_zbioru_mozliwych_decyzji(A1, A2, D):
    liczba_kryteriów = D.shape[1]
    liczba_decyzji = D.shape[0]

    liczba_alternatyw_A1 = A1.shape[0]
    liczba_alternatyw_A2 = A2.shape[0]

    M1 = []
    for i in range(liczba_decyzji):
        warunek = False
        for a in range(liczba_alternatyw_A1):
            for j in range(liczba_kryteriów):
                if D[i,j] >= A1[a,j]:
                    warunek = True
                else:
                    warunek = False
                    break
        if warunek:
            wpisuj = True
            for k in range(liczba_alternatyw_A1):
                if np.equal(A1[k,:], D[i,:]).all():
                    wpisuj = False
                    break
            if wpisuj:
                M1.append(D[i,:])
    M1 = np.array(M1)
    liczba_alt_M1 = M1.shape[0]

    M2 = []
    for i in range(liczba_alt_M1):
        warunek = False
        for a in range(liczba_alternatyw_A2):
            for j in range(liczba_kryteriów):
                if M1[i,j] <= A2[a,j]:
                    warunek = True
                else:
                    warunek = False
                    break
        if warunek:
            wpisuj = True
            for k in range(liczba_alternatyw_A2):
                if np.equal(A2[k,:], M1[i,:]).all():
                    wpisuj = False
                    break
            if wpisuj:
                M2.append(M1[i,:])

    if M2 == []:
        M2 = A2
    else:
        M2 = np.array(M2)
    return M2


# Wyznaczenie zbiorów A0, A1, A2, A3 na gotowo wraz z ich wektorami idealnymi oraz zbioru decyzji dopuszczalnych pomiędzy A1 i A2:
def wyznaczenie_zbiorow(pref, pref_qwo):
    #  pref - to preferencje do wyznaczenia zbioru A1 (nieosiągalnego dla kljenta), 
    #  pref_qwo - to preferencje minimalne do wyznaczenia zbioru A2 (klijent chce coś więcej niż to)

    # Pobierz dane z pliku csv i utwórz macierz decyzji:
    D =  data("Decyzje_prb.csv")

    # Przemnóż maksymalne kryteria przez -1:
    Dmin = odwrocenie_max_kryteriow(D)
    # print(Dmin)
    # pref = odwrocenie_max_kryteriow(pref)
    # pref_qwo = odwrocenie_max_kryteriow(pref_qwo)

    #  Wyznaczanie zbiru A0 i wektora idealne:
    A0, vec_ideal = punkty_najlepsze(Dmin)

    #  Wyznaczanie zbioru A3 i wektora antyidealnego:
    A3, vec_anty_ideal = punkty_najlepsze(Dmin, 'max')

    #  Wyznaczanie zbioru A1  i sprawdzenie wewnętrznej niesprzeczności:
    A1 = nieporownywalne_dla_preferencji(pref,Dmin)
    A1 = wewnetrzna_niesprzecznosc(A1)

    # Sprawdzenie zewnętrznej niesprzeczności dla zbiorów A1 i A0:
    A1 = zewnetrzna_niesprzecznosc(A1,A0)
    if A1.shape == (0,):
        A1 = A0

    # Wyznaczenie wektora idealnego dla A1:
    idealny_A1 = punkt_idealny_dla_klasy_preferencji(A1, 'min')
    
    #  Wyznaczenie zbioru A2:
    A2 = nieporownywalne_dla_preferencji(pref_qwo,Dmin)
    A2 = wewnetrzna_niesprzecznosc(A2)
    # print()
    # print(A2)
    # print()
    # print(A1)

   # Sprawdzenie zewnętrznej niesprzeczności dla zbiorów A2 i A1
    A2 = zewnetrzna_niesprzecznosc(A2,A1)
    if A2.shape == (0,):
        A2 = A1
        idealny_A2 = punkt_idealny_dla_klasy_preferencji(A2, 'maks')
        M = A1
    else:
        # Wyznaczenie wektora idealnego dla A2:
        idealny_A2 = punkt_idealny_dla_klasy_preferencji(A2, 'maks')

        # Wyznaczenie zbioru decyzji między A1 i A2:
        M = wyznaczanie_zbioru_mozliwych_decyzji(A1, A2, Dmin)
    kryteria = flagi_kryteriow()
    if 'max' in kryteria:
        M = odwrocenie_max_kryteriow(M)
        A0 = odwrocenie_max_kryteriow(A0)
        vec_ideal = odwrocenie_max_kryteriow(vec_ideal)
        vec_anty_ideal = odwrocenie_max_kryteriow(vec_anty_ideal)
        A3 = odwrocenie_max_kryteriow(A3)
        A2 = odwrocenie_max_kryteriow(A2)
        A1 = odwrocenie_max_kryteriow(A1)
        idealny_A1 = odwrocenie_max_kryteriow(idealny_A1)
        idealny_A2 = odwrocenie_max_kryteriow(idealny_A2)
    
    return (A0, vec_ideal, A1, idealny_A1, A2, idealny_A2, A3, vec_anty_ideal, M)




def main():
    pref = np.array([1.4, 0, 4.5, 631000, 1900])
    pref_qwo = np.array([1.8, 2, 5.1, 681000, 2300])
    A0, A0_vec, A1, A1_vec, A2, A2_vec, A3, A3_vec, M = wyznaczenie_zbiorow(pref, pref_qwo)

    print('Punkty najlepsze')
    print(A0)
    print()
    print('Wektor idealny', A0_vec)
    print()
    print('Punkty najgorzsze')
    print(A3)
    print()
    print('Wektor antyidealny', A3_vec)
    print()
    print('Punkty preferencji nieosiągalnych:')
    print(A1)
    print()
    print('Wektor idealny z A1:', A1_vec)
    print()
    print('Punkty status QWO:')
    print(A2)
    print()
    print('Wektor nadir z A2:',  A2_vec)
    print()
    print('Pomiędzy A1 a A2:')
    print(M)
main()