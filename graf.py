import math
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from wyszukiwanie_pliku import sciezka_do_katalogu_gl_projektu

class Graf:
    """
    Klasa reprezentująca algorytmy tworzące połączenie z bazą danych
    oraz obliczające dystans między miastami, tworzenie macierzy sąsiedztwa
    i rysowanie grafu z naniesioną trasą komiwojażera
    """
    def __init__(self):
        """
        Metoda służąca do połączenia z bazą danych zawierająca
        informacje dot. lotnisk, miejscowości gdzie się znajudją oraz ich współrzędnych
        """
        projekt = sciezka_do_katalogu_gl_projektu()
        self.polaczenie = sqlite3.connect(projekt / 'baza.db') # połączenie z naszą bazą danych
        self.kursor = self.polaczenie.cursor() # kursor do wykonywania operacji na danych zawartych w bazie
        self.kursor.execute("SELECT ID, x, y, miasto FROM lotniska") # za pomocą kursora wybranie kolumn z bazy danych
        self.miasta = self.kursor.fetchall() # przy użyciu fetchall pobierane są dane z określonej kolumny z wszytskich wierszy

    def obliczanie_dystansu(self, miasto1: list, miasto2:list)  -> float:
        """
        Metoda służąca do obliczania dystansu między miastami na podstawie ich współrzędnych z uwzględnieniem zakrzywienia Ziemi
        :param miasto1: pierwsze miasto między którym będzie obliczana odległość
        :param miasto2: drugie miasto między którym będzie obliczana odległość
        :return: zwracana jest odległość między dwoma miastami
        """
        szer1, dl1 = miasto1[2], miasto1[1]  # indeks 1 - x, indeks 2 - y (w geodezji wsp. są na odwrót)
        szer2, dl2 = miasto2[2], miasto2[1]
        promien_ziemi = 6371  # Promień Ziemi w kilometrach

        # wzór Haversin'a, uwzględnieniający zakrzywienie Ziemi:  R ⋅ sin -¹(√[sin²((θ₂ - θ₁) / 2) + cosθ₁ ⋅ cosθ₂ ⋅ sin²((φ₂ - φ₁) / 2)])
        d_szer = math.radians(szer2 - szer1) # różnica w szer i dł geog. (linia prosta)
        d_dl = math.radians(dl2 - dl1)
        a = math.sin(d_szer / 2) ** 2 + math.cos(math.radians(szer1)) * math.cos(math.radians(szer2)) * math.sin(d_dl / 2) ** 2
        b = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        odleglosc = promien_ziemi * b

        return odleglosc

    def macierz_odleglosci(self):
        """
        Metoda służąca do wyznaczania macierzy odległości między wszystkimi miastami w bazie danych
        :return: zwracana jest macierz odległości między miastami
        """
        n = len(self.miasta) # liczba miast
        odleglosci = np.zeros((n, n)) # macierz sąsiedztwa wypełniona zerami

        # iteracja po każdym mieście
        for i in range(n):
            for j in range(i + 1, n):
                odl = self.obliczanie_dystansu(self.miasta[i], self.miasta[j]) # obliczanie dystansu między dwoma miastami
                odleglosci[i][j] = int(odl) # dystans z pierwszego miasta do drugiego jest taki sam jak dystans z drugiego do pierwszego
                odleglosci[j][i] = int(odl)

        return odleglosci