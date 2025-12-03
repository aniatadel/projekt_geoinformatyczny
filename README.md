# Planer podróży europejskich

Celem projektu jest rozwiązywanie problemu komiwojażera z wykorzystaniem 4 algorytmów: 
- Kruksala - algorytm zachłanny
- Najbliższego Sąsiada - algorytm zachłanny
- Helda-Karpa - algorytm dokładny
- Naiwny - algorytm dokładny

Wyniki zostaną zwizualizowane na grafie oraz interaktywnej mapie.

# Funkcjonalności
- Wyznaczanie tras komiwojażera
- Porównanie czasu pracy działania algorytmów - Monte Carlo
- Tworzenie i rysowanie grafu
- Implementacja interaktywnej mapy

# Użyte biblioteki
Spis wszystkich użytych bibliotek znajduje się w pliku "requirements.txt"

# Wymagania
- Python 3.1
- Biblioteki wymienione w "requirements.txt"
- Jupyter Notebook
- Interpreter python'a z ArcGIS PRO API

# Uruchamianie
Projekt można uruchomić na dwa sposoby:
1) W środowisku Jupyter Notebook
- Otworzyć plik "caly_projekt.ipynb"
- Po uruchomieniu wszystkich komórek, użytkownik zostanie poproszony o podanie miasta początkowego podróży oraz miasta jakie chce podczas niej odwiedzić. Następnie zostaną wyznaczone 4 trasy przez 4 różne algorytmy oraz zostanie obliczony ich dystans podany w kilometrach.
Wyniki zostaną zwizualizowane na grafie oraz interaktywnej mapie.

2) W środowisku PyCharm
- Otworzyć plik o nazwie "caly_projekt.py"
- Po uruchomieniu, użytkownik żytkownik zostanie poproszony o podanie miasta początkowego podróży oraz miasta jakie chce podczas niej odwiedzić. Następnie zostaną wyznaczone 4 trasy przez 4 różne algorytmy oraz zostanie obliczony ich dystans podany w kilometrach.
Wyniki zostaną zwizualizowane tylko na grafie, ponieważ środowisko PyCharm nie obsługuje interaktywnych widżetów jakim jest mapa.Z tego powodu dla pełnej wizualizacji wyników zalecane jest otworzenie pliku w środowisku Jupyter Notebook.

# Autorki
Anna Tądel, nr. indeksu: 273776,
Łucja Wesołowska, nr. indeksu: 273773