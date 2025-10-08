```mermaid
gantt
    title Harmonogram projektu – Planer podróży europejskich
    dateFormat  YYYY-MM-DD
    excludes    weekends

    section Etap I – Przygotowanie danych
    Stworzenie bazy danych (Łucja)                         :a1, 2025-10-08, 5d
    Kod do wyznaczania macierzy sąsiedztwa oraz utworzenie pliku JSON (Ania) :a2, 2025-10-08, 5d

    section Etap II – Implementacja algorytmów
    Algorytm najbliższego sąsiada i naiwny (Ania)          :b1, after a2, 7d
    Algorytm Kruskala i Held-Karpa (Łucja)                 :b2, after a1, 7d

    section Etap III – Tworzenie i wizualizacja grafu
    Budowa grafu i podgrafu (Ania)                         :c1, after b1, 7d
    Wizualizacja tras na grafie i podgrafie (Łucja)        :c2, after b2, 7d

    section Etap IV – Integracja ze środowiskiem GIS
    Integracja środowiska ArcGIS z Pythonem (Ania)         :d1, after c1, 7d
    Kod rysujący trasę na mapie GIS (Łucja)                :d2, after c2, 7d

    section Etap V – Testy i podsumowanie
    Testy aplikacji (Ania i Łucja)                         :e1, after d1, 7d
    Utworzenie pliku README oraz analiza wyników (Ania i Łucja) :e2, after e1, 3d

    section Etap VI – Prezentacja projektu
    Prezentacja projektu na zajęciach                      :f1, 2025-11-13, 1d
