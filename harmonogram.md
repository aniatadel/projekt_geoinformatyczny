```mermaid
gantt
    title Harmonogram projektu – Planer podróży europejskich
    dateFormat  YYYY-MM-DD
    excludes    weekends

    section Etap I – Przygotowanie danych
    Baza danych (A)                         :a1, 2025-10-08, 5d
    Macierz sąsiedztwa i JSON (Ł)           :a2, 2025-10-08, 5d

    section Etap II – Implementacja algorytmów
    Algorytm NS i naiwny (A)                :b1, after a2, 7d
    Algorytm Kruskala i Held-Karpa (Ł)      :b2, after a1, 7d

    section Etap III – Tworzenie i wizualizacja grafu
    Budowa grafu i podgrafu (A)             :c1, after b1, 7d
    Wizualizacja tras na grafie i podgrafie (Ł) :c2, after b2, 7d

    section Etap IV – Integracja ze środowiskiem GIS
    Integracja środowiska ArcGIS z Pythonem (A) :d1, after c1, 7d
    Kod rysujący trasę na mapie GIS (Ł)          :d2, after c2, 7d

    section Etap V – Testy i podsumowanie
    Testy aplikacji (A&Ł)                  :e1, 2025-11-10, 1d
    Plik README (A&Ł)                      :e2, after e1, 1d

    section Etap VI – Oddanie projektu
    Analiza wyników (A&Ł)                  :f1, 2025-11-13, 1d
    Prezentacja projektu (A&Ł)             :f2, after f1, 1d
