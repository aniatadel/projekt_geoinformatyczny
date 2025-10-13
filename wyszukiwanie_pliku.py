from pathlib import Path

def sciezka_do_katalogu_gl_projektu(szukana_nazwa_pliku =".git"):
    """
    Funkcja służąca do znajdywania katalogu głównego projektu, szukając określonego pliku lub katalogu
    :param szukana_nazwa_pliku: Nazwa pliku lub katalogu, który ma być wyszukany, aby zidentyfikować katalog główny projektu
    :return: Absolutna ścieżka do katalogu głównego projektu.
    """
    obecna_sciezka = Path(__file__).resolve()

    for parent in obecna_sciezka.parents:
        if (parent / szukana_nazwa_pliku).exists():
            return parent

    raise FileNotFoundError(f"Nie można znaleźć katalogu głównego projektu o nazwie: {szukana_nazwa_pliku}")