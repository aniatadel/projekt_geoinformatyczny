import itertools
from itertools import permutations

class Komiwojazer:
    """
    Klasa reprezentująca algorytmy rozwiązujące problem komiwojażera
    """

    def najblizszy_sasiad(self, macierz: list, start: int) -> tuple:
        """
        Metoda do wyznaczania najkrótszej ścieżki przy użyciu algorytmu najbliższego sąsiada
        :param macierz: macierz sąsiedztwa
        :return trasa: zwraca najkrótszą wyznaczoną drogę
        :return dystans: zwraca całkowity dystans trasy
        """
        n = len(macierz) # liczba miast
        nieodwiedzone = set(range(n)) # ustawienie wszystkich miast jako nieodwiedzone
        obecne_miasto = start
        nieodwiedzone.remove(obecne_miasto) # usuwanie ze zbioru miast nieodwiedzonych miasta startowego
        trasa = [obecne_miasto]
        dystans = 0

        # iteracyjne przechodzenie przez nieodwiedzone miasta
        while nieodwiedzone:
            najblizsze_miasto = min([(i, macierz[obecne_miasto][i]) for i in range(n) if i in nieodwiedzone and macierz[obecne_miasto][i] != 0], key=lambda x: x[1])[0] # znalezienie miasta, które jest najbliższej miasta poprzedniego
            trasa.append(najblizsze_miasto) # dodanie znalezionego najbliższego miasta do trasy
            nieodwiedzone.remove(najblizsze_miasto) # usuwanie ze zbioru miast nieodwiedzonych  najbliższego miasta, które zostało dodane do trasy
            dystans += macierz[obecne_miasto][najblizsze_miasto] # zwiększenie dystansu o odległość między dwoma miastami
            obecne_miasto = najblizsze_miasto # ustawienie obecnego miasta na znalezione miasto najbliższe
        end = len(trasa)-1 # ostatnie miasto w trasie
        trasa.append(start)

        def naiwny(self, macierz_odleglosci, start):
            """
            Znajduje najkrótszą możliwą trasę, która odwiedza każdy węzeł i wraca do punktu początkowego.

            :param macierz_odleglosci: macierz odległości
            :param start: opcjonalny parametr startowy wierzchołka wprowadzony przez użytkownika

            :return: słownik zawierający najkrótszą trasę i jej długość.
            """
            liczba_miast = len(macierz_odleglosci)
            miasta = list(range(liczba_miast))
            miasta.remove(start)

            dystans = float(
                'inf')  # dystans jest inicjalizowany jako nieskończoność w pierwszym kroku algorytmu każda znaleziona trasa będzie miała najkrótszy dystans.
            trasa = None

            for perm in permutations(miasta):  # Generuje wszystkie permutacje wierzchołków bez wierzchołka startowego.
                obecna_trasa = [start] + list(
                    perm)  # obecna_trasa zaczyna się od wierzchołka start i zawiera kolejne wierzchołki z permutacji.
                obecny_dystans = self.oblicz_dystans_naiwny(obecna_trasa,
                                                            macierz_odleglosci)  # obliczany przy użyciu metody oblicz_dystans_naiwny sumuje odległości między kolejnymi wierzchołkami trasy
                if obecny_dystans < dystans:  # jesli obecny_dystans jest mniejszy niż minimalny_dystans, to minimalny_dystans i najlepsza_trasa są aktualizowane.

                    dystans = obecny_dystans
                    trasa = obecna_trasa

            # Powrót do punktu początkowego
            trasa.append(start)
            return trasa, dystans

        def tsp(self, macierz, start):
            """
            Symuluje rozwiązanie problemu komiwojażera (TSP) na MST, wykonując przeszukiwanie w głąb (DFS).
            Odwiedza wszystkie wierzchołki zaczynając od wierzchołka 'start' i powraca do punktu startowego.
            Zlicza całkowitą wagę odwiedzonych krawędzi.

            :param macierz: macierz odległości
            :param start: Wierzchołek początkowy.
            :return: Lista odwiedzonych wierzchołków (trasa) oraz całkowita waga trasy.
            """