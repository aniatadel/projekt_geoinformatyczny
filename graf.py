import math
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from wyszukiwanie_pliku import sciezka_do_katalogu_gl_projektu
from komiwojazer import Komiwojazer

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

    def tworzenie_grafu(self, macierz_sasiedztwa_grafu: list, miasto_startowe: int, miasta_do_odwiedzenia: list) -> tuple:
        """
        Metoda służąca do tworzenia grafu i podgrafu (który zawiera tylko miasta wybrane przez użytkownika).
        :param macierz_sasiedztwa_grafu: macierz sąsiedztwa grafu (lista list)
        :param miasto_startowe: miasto, w którym zaczyna się podróż
        :param miasta_do_odwiedzenia: miasta do odwiedzenia podczas podróży
        :return: tuple zawierający pełny graf oraz podgraf zawierający tylko miasta podane przez użytkownika
        """

        graf_pelny = nx.Graph()  # inicjalizacja pełnego grafu
        n = len(macierz_sasiedztwa_grafu)  # liczba wszystkich wierzchołków

        # Przechodzenie iteracyjnie przez wierzchołki w grafie
        for i in range(1, n + 1):  # iteracja od 1 (nie od 0)
            graf_pelny.add_node(i)  # dodawanie wierzchołków

        # Dodawanie krawędzi między miastami
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):  # nie dodaje dwa razy takich samych krawędzi (i, j) i (j, i)
                if macierz_sasiedztwa_grafu[i - 1][j - 1] != 0:  # jeżeli odległość od miasta1 do miasta2 jest różna od 0
                    graf_pelny.add_edge(i, j, weight=macierz_sasiedztwa_grafu[i - 1][j - 1])  # dodanie krawędzi o danej wadze do grafu

        # Tworzenie podgrafu
        wybrane_wierzcholki = [miasto_startowe] + miasta_do_odwiedzenia  # ustalanie wybranych wierzchołków
        podgraf = graf_pelny.subgraph(wybrane_wierzcholki)  # tworzenie podgrafu na podstawie pełnego grafu

        return graf_pelny, podgraf

    def konwersja(self, graf: nx) -> tuple:
        """
        Metoda służąca do tworzenia macierzy sąsiedztwa na podstawie grafu oraz przypisywania oryginalnych wierzchołków w podgrafie
        :param graf: graf lub podgraf
        :return: zwracana jest macierz sąsiedztwa miast, oryginalne wierzchołki i ich konwersja
        """
        oryginalne_wierzcholki = {} # słownik do przechowywania orygnialnych wierzchołków
        oryginalne_wierzcholki_konwersja = {} # słownik do przechowywania odwzorowania indeksów na oryginalne wierzchołki
        n = len(graf.nodes) # liczba wierzchołków w grafie
        macierz_sasiedztwa = np.zeros((n, n))  # tworzenie macierzy sąsiedztwa, która na początku wypełniona jest samymi zerami

        # iteracyjne przechodzenie przez węzły w grafie
        for i, u in enumerate(graf.nodes()):  # funkcja enumerate dodaje numer do każdego elementu listy
            oryginalne_wierzcholki[u] = i  # mapowanie wierzchołka na indeks
            oryginalne_wierzcholki_konwersja[i] = u
            for j, v in enumerate(graf.nodes()):  # iteracja po węzłach grafu
                if graf.has_edge(u, v):  # jeżeli istnieje połączenie (krawędź) między dwoma węzłami
                    macierz_sasiedztwa[i][j] = graf[u][v]['weight']  # to waga krawędzi zostaje przypisana w odpowiednie miejsce w macierzy sąsiedztwa

        return macierz_sasiedztwa, oryginalne_wierzcholki, oryginalne_wierzcholki_konwersja

    def polaczenia_w_grafie_i_trasie(self, macierz_sasiedztwa_grafu: list, start: int, oryginalne={}) -> tuple:
        """
        Metoda służąca do wyznaczania połączeń w grafie oraz drogi komiwojażera wyznaczonej przez algorytmy.
        :param macierz_sasiedztwa_grafu: ścieżka do pliku, w której znajduje się macierz sąsiedztwa grafu (json).
        :param start: miasto początkowe podróży wybrane przez użytkownika.
        :return: zwracane są wszystkie połączenia w grafie oraz połączenia w najkrótszej trasie wyznaczonej przez algorytm
        """
        def polaczenia_w_calym_grafie(self, macierz_sasiedztwa: list, oryginalne = {}) -> list:
            """
            Metoda służąca do pobierania wszystkich połączeń w grafie na podstawie macierzy sąsiedztwa
            :param macierz_sasiedztwa: macierz sąsiedztwa
            :return: zwracana jest lista zawierająca połączenia w całym grafie
            """
            polaczenia_w_calym_grafie = []  # pusta lista, do której zostaną dodane połączenia w grafie

            # interacja po wszystkich wierszach macierzy
            if oryginalne:
                for i in range(len(macierz_sasiedztwa)):
                    # iteracja po wszystkich kolumnach w bieżącym wierszu
                    for j in range(len(macierz_sasiedztwa[0])):
                        if macierz_sasiedztwa[i][j] != 0:  # Jeśli istnieje połączenie między wierzchołkami
                            # to pobierane są nazwy miast dla indeksów wierzchołków z bazy danych
                            miasto1 = self.kursor.execute(f"SELECT miasto FROM lotniska WHERE ID = {oryginalne[i]}").fetchone()
                            miasto2 = self.kursor.execute(f"SELECT miasto FROM lotniska WHERE ID = {oryginalne[j]}").fetchone()
                            polaczenia_w_calym_grafie.append((miasto1[0], miasto2[0]))  # dodawanie połączenia między miastami do listy połączeń w grafie

                return polaczenia_w_calym_grafie

            else:

                for i in range(len(macierz_sasiedztwa)):
                    # iteracja po wszystkich kolumnach w bieżącym wierszu
                    for j in range(len(macierz_sasiedztwa[0])):
                        if macierz_sasiedztwa[i][j] != 0:  # Jeśli istnieje połączenie między wierzchołkami
                            # to pobierane są nazwy miast dla ideneksów wierzchołków z bazy danych
                            miasto1 = self.kursor.execute(f"SELECT miasto FROM lotniska WHERE ID = {i + 1}").fetchone()
                            miasto2 = self.kursor.execute(f"SELECT miasto FROM lotniska WHERE ID = {j + 1}").fetchone()
                            polaczenia_w_calym_grafie.append((miasto1[0], miasto2[0]))  # dodawanie połączenia między miastami do listy połączeń w grafie

            return polaczenia_w_calym_grafie

        def polaczenia_w_trasie(self, trasa: list, oryginalne = {}) -> list:
            """
            Metoda służąca do pobierania połączeń w trasie komiwojażera na podstawie listy odwiedzanych miast
            :param trasa: trasa wyznaczona przez algorytmy rozwiązujace problem komiwojażera
            :return: zwracana jest lista zawierająca połączenia trasy w grafie
            """
            polaczenia_w_trasie = []  # pusta lista, do której zostaną dodane połączenia w trasie

            if oryginalne:
                # iteracja po wszystkich miastach z trasy
                for i in range(len(trasa) - 1):
                    miasto1 = self.kursor.execute(f"SELECT miasto FROM lotniska WHERE ID = {oryginalne[trasa[i]]}").fetchone()  # pobieranie nazwy miast dla indeksów wierzchołków z bazy danych
                    miasto2 = self.kursor.execute(f"SELECT miasto FROM lotniska WHERE ID = {oryginalne[trasa[i + 1]]}").fetchone()
                    polaczenia_w_trasie.append((miasto1[0], miasto2[0]))  # dodawanie połączeń między tymi miastami do listy połączeń w trasie

                return polaczenia_w_trasie

            else:
                for i in range(len(trasa) - 1):
                    miasto1 = self.kursor.execute(f"SELECT miasto FROM lotniska WHERE ID = {trasa[i] + 1}").fetchone()  # pobieranie nazwy miast dla indeksów wierzchołków z bazy danych
                    miasto2 = self.kursor.execute(f"SELECT miasto FROM lotniska WHERE ID = {trasa[i + 1] + 1}").fetchone()
                    polaczenia_w_trasie.append((miasto1[0], miasto2[0]))  # dodawanie połączeń między tymi miastami do listy połączeń w trasie

                return polaczenia_w_trasie

        komiwojazer = Komiwojazer()

        najkrotsza_droga_kruksal = komiwojazer.tsp(macierz_sasiedztwa_grafu, start)[0]

        najkrotsza_droga_held_karp = komiwojazer.held_karp(macierz_sasiedztwa_grafu, start)[0]

        if oryginalne:
            polaczenia_w_calym_grafie = polaczenia_w_calym_grafie(self, macierz_sasiedztwa_grafu, oryginalne)
            polaczenia_w_trasie_kruksal = polaczenia_w_trasie(self, najkrotsza_droga_kruksal, oryginalne)
            polaczenia_w_trasie_hk = polaczenia_w_trasie(self, najkrotsza_droga_held_karp, oryginalne)
        else:
            polaczenia_w_calym_grafie = polaczenia_w_calym_grafie(self, macierz_sasiedztwa_grafu)
            polaczenia_w_trasie_kruksal = polaczenia_w_trasie(self, najkrotsza_droga_kruksal)
            polaczenia_w_trasie_hk = polaczenia_w_trasie(self, najkrotsza_droga_held_karp)

        return polaczenia_w_calym_grafie, polaczenia_w_trasie_kruksal, polaczenia_w_trasie_hk