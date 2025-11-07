from komiwojazer import Komiwojazer
from graf import Graf
from wyszukiwanie_pliku import sciezka_do_katalogu_gl_projektu
import pandas as pd
import json

def pobieranie_danych_od_uzytkownika():
    """
    Metoda służąca do pobierania danych od użytkownika dot. miasta skąd chcą zacząc wycieczkę i jakie miasta odwiedzić
    :return miasto_startowe: zwraca miasto startowe podróży
    :return miasta_do_odwiedzenia: zwraca miasta do odwiedzenia podczas podróży
    """
    miasto_startowe = int(input("Podaj miasto początkowe podróży po Europie (1-20): "))  # pobieranie danych od użytkownika
    miasta_do_odwiedzenia = input("Podaj jakie miasta europejskie chcesz odwiedzić (1-20): ")
    miasta_do_odwiedzenia = list(map(int, miasta_do_odwiedzenia.split(',')))  # int - tylko liczby całkowite, dzielenie łańcucha znaków na podłańcuchy używając przecinka jako separator, np.: lista: 1,2,3 -> '1','2','3'
    return miasto_startowe, miasta_do_odwiedzenia

komiwojazer = Komiwojazer()
graf = Graf()

projekt = sciezka_do_katalogu_gl_projektu()
plik = open(projekt/ "macierz_sasiedztwa_grafu.json")
macierz_sasiedztwa_grafu = json.load(plik)


miasto_startowe, miasta_do_odwiedzenia = pobieranie_danych_od_uzytkownika()

# podgraf
_, podgraf = graf.tworzenie_grafu(macierz_sasiedztwa_grafu, miasto_startowe, miasta_do_odwiedzenia) # _ używane do oznaczania zmiennych, które nie będą używane
macierz, oryginalne_wierzcholki, oryginalne_wierzcholki_konwersja = graf.konwersja(podgraf)

# graf
graf_pelny, _ = graf.tworzenie_grafu(macierz_sasiedztwa_grafu, miasto_startowe, [i for i in range(1, miasto_startowe)] + [i for i in range(miasto_startowe + 1, 21)])
macierz_pelna, org_wierzch_peln, org_wierzch_konw_peln = graf.konwersja(graf_pelny)



# Kruksal
trasa_kr, dystans_kr = komiwojazer.tsp(macierz, oryginalne_wierzcholki[miasto_startowe])
for i in range(len(trasa_kr)):
    trasa_kr[i] = oryginalne_wierzcholki_konwersja[trasa_kr[i]]

# Najbliższy sąsiad
trasa_nb, dystans_nb = komiwojazer.najblizszy_sasiad(macierz, oryginalne_wierzcholki[miasto_startowe])
for i in range(len(trasa_nb)):
    trasa_nb[i] = oryginalne_wierzcholki_konwersja[trasa_nb[i]]

# Held-Karp
trasa_hk, dystans_hk, opt = komiwojazer.held_karp(macierz, oryginalne_wierzcholki[miasto_startowe])
for i in range(len(trasa_hk)):
    trasa_hk[i] = oryginalne_wierzcholki_konwersja[trasa_hk[i]]

# Naiwny
trasa_naiw, dystans_naiw = komiwojazer.naiwny(macierz, oryginalne_wierzcholki[miasto_startowe])
for i in range(len(trasa_naiw)):
    trasa_naiw[i] = oryginalne_wierzcholki_konwersja[trasa_naiw[i]]

# tworzenie tabeli
wyniki = {
"Algorytm": ["Kruksal", "Najbliższy Sąsiad", "Held-Karp", "Naiwny"],
"Trasa": [trasa_kr, trasa_nb, trasa_hk, trasa_naiw],
"Dystans [km]": [dystans_kr, dystans_nb, dystans_hk, dystans_naiw]
}

df = pd.DataFrame(wyniki)

df.index = range(1, len(df) + 1) # ustawienie indeksowania od 1

# ustawienie stylu tabeli
styl_df = df.style.set_properties(**{
    'border': '1px solid pink',
    'color': '#FF1493',
    'font-size': '14px'
}).format({'Dystans [km]': '{:.2f}'})  # dystans do dwóch miejsc po przecinku

# Wyświetlenie tabeli
print("\n")
print("Tabela wyników:")
display(styl_df)

print("\n")
rysowanie_podgrafu = graf.rysowanie_grafu(macierz, oryginalne_wierzcholki[miasto_startowe], oryginalne_wierzcholki_konwersja)

print("\n")
rysowanie_grafu = graf.rysowanie_grafu(macierz_pelna, org_wierzch_peln[miasto_startowe], org_wierzch_konw_peln)