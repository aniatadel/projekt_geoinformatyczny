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
        # powrót do miasta startowego
        # while end>start:
        # # sprawdzanie czy istnieje bezpośrednie połączenie z miasta końcowego do miasta startowego
        #     if macierz[start][trasa[end]] != 0: # jeżeli tak, to miasto startowe jest dodawane na koniec trasy
        #         trasa.append(start)
        #         dystans += macierz[start][trasa[end]] # zwiększenie dystansu
        #         break
        #     else: # jeżeli nie, następuje powrót to poprzedeniego miasta i na nowo jest sprawdzane czy istnieje połączenie z miastem startowym
        #         end -= 1
        #         trasa.append(trasa[end])
        dystans += macierz[start][trasa[end]] # zwiększanie dystanu o odległość między ostatnim a poprzedzającym go miastem

        return trasa, dystans

    def held_karp(self, macierz, start) -> tuple:
        """
        Implementacja algorytmu Held-Karp, który rozwiązuje problem komiwojażera
        używając programowania dynamicznego z memoizacją (algorytm zapamiętuje najkrótsze drogi do pozbiorów węzłów (miast).
        Mamy n węzłów. Algorytm musi rozważyć przejście przez wszystkie miasta z początkowego

        :param macierz: macierz odległości
        :param start: indeks miasta początkowego

        :return: najkrótsza droga i jej dystans.
        """
        n = len(macierz) # liczba węzłów
        C = {} # C przechowuje minimalny dystans dotarcia do podzbiorów węzłów

        for k in range(n): # Inicjalizacja: dystans przejścia z początkowego stanu do innych węzłów
            if k != start:
                C[(1 << k, k)] = (macierz[start][k], start) #tworzy klucz w c reprezentujacy odwiedzenie tylko k. zapisuje bitowo nr miasta

        for rozmiar_podzbioru in range(2, n):   #iteracja po podzbiorach o rosnącej długości i przechowywanie wyników pośrednich
            for podzbior in itertools.combinations(range(n), rozmiar_podzbioru): #generuje i ieruje po kombinacjach rozmiaru rozmiar_podzbioru z wierzchołków od 1 do n-1
                if start in podzbior:
                    continue
                bits = 0 #bity dla wszystkich węzłów w tym podzbiorze, przechowuja informacje o wierzcholkach w  tym podzbiorze
                for bit in podzbior: #przechodzimy przez kazdy wezel w podzbiorze
                    bits |= 1 << bit #1 czyli to miasto jest czescia biezacego podzbioru

                for k in podzbior: #obliczenie minimalnego kosztu dotarcia do danego węzła z określonego podzbioru węzłów.
                    prev = bits & ~(1 << k) #usuwa ten węzeł k z bieżącego rozpatrywanego podzbioru
                    res = [] # poprzednie miasta i ich wagi
                    for m in podzbior:
                        if m == start or m == k: #jak są takie to pomijamy
                            continue
                        res.append((C[(prev, m)][0] + macierz[m][k], m)) #Dodaje do listy res koszt dojścia do węzła k z węzła m
                    C[(bits, k)] = min(res) # Znajduje minimalny koszt dojścia do węzła k z dowolnego węzła m w podzbiorze i zapisuje go w słowniku C.

        bits = (1 << n) - 1 - (1 << start) #oblicza wartość bits, która jest maską bitową. n oznacza całkowitą liczbę węzłów w grafie, a start jest indeksem węzła początkowego
        res = [] #powrót do węzła początkowego z każdego innego węzła
        for k in range(n):
            if k != start:
                res.append((C[(bits, k)][0] + macierz[k][start], k)) # Dla każdego węzła k (z wyjątkiem startowego), obliczamy koszt powrotu do węzła początkowego
        opt, parent = min(res)  # minimalny koszt powrotu

        trasa = [start] #cofa się aby znaleźć pełną ścieżkę i zapisuje w trasie
        for i in range(n - 1):
            trasa.append(parent) #Dodajemy do trasa kolejny węzeł, który jest rodzicem węzła poprzedniego na ścieżce powrotnej
            new_bits = bits & ~(1 << parent) #usuwa bieżący węzeł wskazywany przez parent z bits z bitów
            next_bits, parent = C[(bits, parent)] # Aktualizujemy parent na jego rodzica, odczytując informacje z C
            bits = new_bits

        trasa.append(start) # dodajemy węzeł początkowy na końcu
        dystans = 0
        for i in range(len(trasa) - 1):
            dystans += macierz[trasa[i]][trasa[i + 1]] #Przechodzimy przez wszystkie elementy listy trasa (poza ostatnim), dodając do dystans koszt przejścia między każdą parą sąsiednich węzłów zapisanych w macierzy macierz

        return trasa, dystans, opt

    def oblicz_dystans_naiwny(self, trasa, macierz_odleglosci):
        """
        Oblicza całkowity dystans dla danej trasy.

        :param trasa: permutacja węzłów reprezentująca trasę
        :param macierz_odleglosci: macierz odległości

        :return: całkowity dystans trasy.
        """
        calkowity_dystans = 0
        for i in range(len(trasa) - 1): #Iterujemy przez wszystkie węzły w trasie dodając dystanse między kolejnymi węzłami
            calkowity_dystans += macierz_odleglosci[trasa[i]][trasa[i + 1]]
        calkowity_dystans += macierz_odleglosci[trasa[-1]][trasa[0]]  #Powrót do punktu startowego
        return calkowity_dystans

    def istnieje_krotsza(self, dlugosc, macierz_odleglosci):
        """
        Sprawdza, czy istnieje trasa krótsza niż podana długość.

        :param dlugosc: długość trasy
        :param macierz_odleglosci: macierz odległości

        :return: słownik zawierający informację, czy istnieje taka trasa, jej długość i przebieg.
        """
        liczba_miast = len(macierz_odleglosci)
        miasta = list(range(liczba_miast))
        for perm in permutations(miasta): #Iterujemy przez wszystkie permutacje miast
            obecny_dystans = self.oblicz_dystans_naiwny(perm, macierz_odleglosci) #Obliczamy całkowity dystans dla aktualnej permutacji
            if obecny_dystans < dlugosc:  #Jeśli obecny dystans jest mniejszy niż podana długość to zwracamy informację o znalezionej trasie
                return {'istnieje': True, 'trasa': perm, 'dystans': obecny_dystans}
        return {'istnieje': False}   # Jeśli nie znaleziono trasy krótszej niż podana długość to zwracamy informację o jej braku


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

        dystans = float('inf') #dystans jest inicjalizowany jako nieskończoność w pierwszym kroku algorytmu każda znaleziona trasa będzie miała najkrótszy dystans.
        trasa = None

        for perm in permutations(miasta): #Generuje wszystkie permutacje wierzchołków bez wierzchołka startowego.
            obecna_trasa = [start] + list(perm) #obecna_trasa zaczyna się od wierzchołka start i zawiera kolejne wierzchołki z permutacji.
            obecny_dystans = self.oblicz_dystans_naiwny(obecna_trasa, macierz_odleglosci) #obliczany przy użyciu metody oblicz_dystans_naiwny sumuje odległości między kolejnymi wierzchołkami trasy
            if obecny_dystans < dystans: #jesli obecny_dystans jest mniejszy niż minimalny_dystans, to minimalny_dystans i najlepsza_trasa są aktualizowane.

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

        def kruskal(macierz):
            """
            Implementacja algorytmu Kruskala do wyznaczania minimalnego drzewa rozpinającego (MST).

            :param macierz: macierz odległości
            :return: minimalne drzewo rozpinające jako lista krawędzi.
            """

            def znajdz(rodzic, i): #znajduje korzeń zbioru
                if rodzic[i] == i: #oznacza to, że i jest korzeniem.
                    return i
                return znajdz(rodzic, rodzic[i])

            def union(rodzic, rank, x, y): #łaczy korzenie zbiorów
                root_x = znajdz(rodzic, x) #znajduje korzeń zbioru zawierającego x i y analogicznie
                root_y = znajdz(rodzic, y)

                if rank[root_x] < rank[root_y]:
                    rodzic[root_x] = root_y #laczy mniejszy  zbior z większym zbiorem
                elif rank[root_x] > rank[root_y]:
                    rodzic[root_y] = root_x #laczy mniejszy zbior z większym zbiorem
                else:
                    rodzic[root_y] = root_x #łączy oba zbiory
                    rank[root_x] += 1 #zwieksza rangę zbioru

            n = len(macierz)
            parent = [i for i in range(n)] # Inicjalizacja tablicy rodziców
            rank = [0] * n # Inicjalizacja tablicy rank (ranga każdego z korzeni)

            krawedzie = []
            for i in range(n): #iteruje po wszystkich wierzchołkach
                for j in range(i + 1, n): # Iteracja po wierzchołkach poza bieżącym, aby uniknąć powtórzeń
                    if macierz[i][j] != 0: #czy istnieje krawędź między wierzchołkami i oraz j
                        krawedzie.append((i, j, macierz[i][j])) #dodanie krawedzi do listy

            krawedzie.sort(key=lambda x: x[2]) # Sortowanie krawędzi względem wagi

            mst = []
            for krawedz in krawedzie:
                u, v, wagi = krawedz
                if znajdz(parent, u) != znajdz(parent, v): # Sprawdzenie, czy krawędź nie robi cyklu
                    union(parent, rank, u, v) #połączenie zbiorów
                    mst.append((u, v, wagi)) #dodanie krawedzi do MST

            return mst

        def konwertuj_na_liste_adj(mst, n):
            """
            Konwertuje listę krawędzi MST na listę sąsiedztwa.

            :param mst: Lista krawędzi tworzących MST.
            :param n: Liczba wierzchołków w grafie.
            :return: Lista sąsiedztwa reprezentująca MST.
            """
            lista_adj = [[] for _ in range(n)] #lista sasiedztwa

            for krawedz in mst: #iteruje po krawedziach MST
                u, v, waga = krawedz
                lista_adj[u].append((v, waga)) #dodanie krawedzi do listy siasiedztwa dla wierzcholka v
                lista_adj[v].append((u, waga))

            return lista_adj

        def dfs(v, odwiedzone, droga):
            odwiedzone[v] = True #wierzchołek v jako odwiedzony
            droga.append(v) #dodaj do trasy

            for sasiad, _ in lista_adj[v]: #po sasiadach wierzchołka v
                if not odwiedzone[sasiad]: #jesli sasiad nie był  jeszcze odwiedzony
                    dfs(sasiad, odwiedzone, droga)

        n = len(macierz) # Liczba wierzchołków w macierzy
        mst = kruskal(macierz)  # Obliczenie minimalnego drzewa rozpinającego (MST) przy użyciu algorytmu Kruskala
        lista_adj = konwertuj_na_liste_adj(mst, n) # Konwersja MST na listę sąsiedztwa

        odwiedzone = [False] * n # Tablica odwiedzonych wierzchołków
        trasa = []  # Lista przechowująca trasę komiwojażera
        dfs(start, odwiedzone, trasa)  # Wywołanie przeszukiwania w głąb (DFS) z wierzchołkiem startowym

        trasa.append(start) #powrót do punktu startowego

        dystans = 0
        for i in range(len(trasa) - 1):
            dystans += macierz[trasa[i]][trasa[i + 1]]  # Sumowanie wag krawędzi na trasie

        return trasa, dystans