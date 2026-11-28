# Przekazanie: dostosowanie rysunków zębów do systemu ofert (stan na 28.11.2026)

Kontynuacja pracy z sesji „ofert Esnan”. Paulina (koordynatorka Fly4Smile) pisze po polsku; wszystko dla IT ma być po angielsku (nazwy plików, folderów, opisy, klucze JSON).

## Problem
System ofert (IT) generuje plan leczenia z rysunkami zębów i zaburza proporcje: wkleja każdy obrazek do równego pola (16 pól w rzędzie, object-fit: contain), więc każdy ząb ma inną skalę, a pełny łuk (All-on-6) jest ogromny. Przykład z systemu: Drive › folder „IT – Tooth chart image proportions (2026-11-25)” › `01_current_system_output_WRONG.png`.

## Rozwiązanie (klucz v3 – ustalony i przetestowany)
- Wspólna skala biblioteki: 32,7 px = 1 mm; rysunków nie skalujemy.
- Każdy plik: płótno o stałej wysokości **940 px**; szerokość = **szerokość miejsca zęba** (szerokość korony cyrkonowej tego zęba + 4 px z boków), element na środku.
- Szczęka: krawędź zgryzowa 30 px nad dolną krawędzią; żuchwa: 30 px pod górną; sam implant: platforma 265 px od krawędzi zgryzowej.
- Pełny łuk: wysokość 940 px, szerokość = suma miejsc 16–26 / 46–36. Zatoka: bez zmian (nie jest w rzędzie).
- Nowe pliki: `natural_XX` (ząb naturalny), `temp_pontic_XX` (przęsło tymczasowe), `missing_XX` (przezroczyste miejsce po braku).
- System (IT): rząd flex, wszystkie obrazki tej samej wysokości, szerokość automatyczna (`.row img{height:96px;width:auto}`); system dorysowuje łącznik mostu, przekreślony numer brakującego zęba, numery nad pełnym łukiem wg szerokości.
- Pełna specyfikacja po angielsku: `IMAGE_PROPORTIONS_SPEC.md`.

## Co jest zrobione
- Skrypt: `scripts/normalize_images.py` (+ `make_natural_teeth.py`, `make_temp_pontics.py`).
- Test krzyżowy na 8 planach (oferta vs układ z samych obrazków w HTML) – zgodne. Drive: `03_cross_check_offer_vs_system_6_plans.jpg`, `06_cross_check_full_new_library_8_plans.jpg`.
- Cała biblioteka (474 rysunki z Drive „New Common Dental Procedures 2026-11-08”) przerobiona → 570 plików (+ natural, temp_pontic, missing). Spakowana jako `library_for_system_2026-11-25.zip` (80 MB) i wysłana Paulinie w czacie, bo upload z sesji na Dysk ma limit ok. 3 MB na wywołanie. **Paulina ma ją sama rozpakować i przeciągnąć na Dysk** do folderu „IT – Tooth chart image proportions (2026-11-25)” (https://drive.google.com/drive/folders/1dXW8p5hUMjujChU0zczYVGSgP3846RFV).
- Zbiorczy indeks: `library/PROCEDURES_AND_FILES_INDEX.xlsx` (+ `PROCEDURES_INDEX.csv`, `FILES_INDEX.csv`) – wszystkie procedury z cennikiem → folder, wzór nazwy, przykładowy plik; wszystkie 570 plików (ścieżki względne).
- Pakiet dla IT po angielsku w tym folderze: `README.md`, `TREATMENT_PLAN_RULES.md`, `DRAWING_CATALOG.md`, `IMAGE_PROPORTIONS_SPEC.md`, `system_example/tooth_chart_example.html`.
- Do czatu „Ujednolicenie grafik stomatologicznych” (session_01Fqf55GTSNXTS9hP7EKz6dW, na Macu Pauliny, rozłączony) wysłano klucz v3 – ta praca jest już zrobiona tutaj, więc tamten czat nie musi jej powtarzać.

## Co zostało / następne kroki
1. Po wgraniu biblioteki przez Paulinę na Dysk: uzupełnić w `PROCEDURES_AND_FILES_INDEX.xlsx` kolumnę z linkami Drive do plików (wyszukać pliki w nowym folderze i dopisać viewUrl) i wgrać arkusz (mały plik) na Dysk.
2. Odpowiadać na pytania IT / Pauliny, poprawki w specyfikacji.
3. Jeśli trzeba odtworzyć bibliotekę: pobrać 474 pliki z Drive (lista z id: `library/drive_index.csv`; najszybciej kilku agentów równolegle, każdy `mcp__Google_Drive__download_file_content` i `cp` z podanej ścieżki), potem `make_temp_pontics.py` + skopiować `library/natural_teeth/*` + `normalize_images.py`.

## Ograniczenia, o których trzeba pamiętać
- Upload na Dysk z sesji: maks. ok. 3 MB na jedno wywołanie – duże paczki wysyłać Paulinie przez czat (SendUserFile), ona wrzuca na Dysk.
- Paulina nie chce klikać zgód: `.claude/settings.json` w repo zezwala na narzędzia Google Drive bez pytania.
- Zasady ofert (ceny, koordynator, nazewnictwo itd.) – `CLAUDE.md` i `SKILL.md`; starszych planów nie zmieniać bez prośby.
