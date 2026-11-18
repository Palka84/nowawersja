"""Generuje KATALOG_RYSUNKOW.md z drive_index.csv."""
import csv, sys, os, re
IDX, OUT = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(IDX, encoding='utf-8')))
byname = {}
for r in rows:
    byname.setdefault(r['title'], r)
folders = {r['title']: r for r in rows if r['mimeType'].endswith('folder')}
def flink(title):
    r = folders.get(title)
    return f"[{title}]({r['viewUrl']})" if r else title
def link(fn, label=None):
    r = byname.get(fn)
    return f"[{label or fn}]({r['viewUrl']})" if r else f"`{fn}` (brak na Drive)"

ROOT = "https://drive.google.com/drive/folders/1XEiTQqL2fuKYnrzuR0LmhzGtsLRxbgN6"
STATES = [
 # state, kiedy, plik, folder, przyklad_nr, wygląd
 ("natural", "Ząb własny pacjenta, bez zabiegu na tej wizycie (widoczny na RTG).", "natural_{n}.png", None, "01",
  "Naturalny ząb: korona w kolorze szkliwa, korzeń beżowy. Numer szary."),
 ("missing", "Zęba nie ma (brak na RTG, wcześniej usunięty, ósemki nieobecne). Także ząb usunięty na wizycie I – na schemacie wizyty II.", "—", None, "01",
  "Brak rysunku, numer szary i przekreślony."),
 ("extraction", "Ekstrakcja na danej wizycie (zwykła lub chirurgiczna).", "extraction_{n}.png", "Tooth Extraction – Ekstrakcja zęba", "10",
  "Blady zarys zęba z cienkim czerwonym X. Numer w turkusowej pigułce."),
 ("implant", "Implant wszczepiony na wizycie I, bez korony (gojenie).", "implant_{n}.png", "Dental Implant – Implant", "02",
  "Sam implant (turkusowa śruba), lekko obniżony względem linii zgryzu. Numer podświetlony."),
 ("implant_crown", "Korona cyrkonowa Amann Girrbach lub Ivoclar na implancie (zwykle wizyta II).", "zirconia_crown_on_implant_{n}.png", "Zirconia Crown on Implant – Korona cyrkonowa na implancie", "03",
  "Turkusowa korona na jednolitym implancie."),
 ("temp_implant", "Tymczasowa korona na implancie / filar stałej tymczasowej pracy na implantach (wizyta I).", "temporary_crown_on_implant_{n}.png", "Temporary Crown on Implant – Korona tymczasowa na implancie", "04",
  "Bursztynowa korona na implancie."),
 ("crown", "Korona cyrkonowa Amann Girrbach lub Ivoclar na własnym zębie; także filar mostu na własnych zębach.", "zirconia_crown_{n}.png", "Zirconia Crown – Korona cyrkonowa", "05",
  "Turkusowa korona na naturalnym korzeniu."),
 ("pontic", "Przęsło mostu na własnych zębach (ząb brakujący zastąpiony koroną bez korzenia).", "bridge_pontic_{n}.png", "Bridge on Natural Teeth – Most na własnych zębach", "06",
  "Sama turkusowa korona, bez korzenia; łącznik mostu za koronami."),
 ("implant_pontic", "Przęsło mostu na implantach.", "implant_bridge_pontic_{n}.png", "Implant Bridge – Most na implantach", "07",
  "Turkusowa korona bez korzenia między koronami na implantach; łącznik w kolorze korony."),
 ("temp_pontic", "Przęsło stałej tymczasowej pracy na implantach.", "temp_pontic_{n}.png (generowany – patrz uwaga)", "Implant Bridge – Most na implantach", "08",
  "Bursztynowa korona bez korzenia; łącznik bursztynowy (bridge_color [226,170,90])."),
 ("veneer", "Licówka porcelanowa Laminate Veneer (rysunki tylko dla zębów 11–15, 21–25, 31–35, 41–45).", "veneer_{n}.png", "Veneer – Licówka", "09",
  "Cienka turkusowa łuska na przedniej powierzchni zęba."),
]

L = []
A = L.append
A("# Katalog rysunków – co rysujemy w jakiej sytuacji\n")
A(f"Biblioteka rysunków na Google Drive: **[New Common Dental Procedures 2026-11-08]({ROOT})** "
  "(foldery „English – Polski”, pliki `<zabieg>_<numer FDI>.png`, przezroczyste tło, jedna skala 32,7 px = 1 mm). "
  "Pełna lista plików z linkami: `biblioteka/drive_index.csv`. Arkusz procedur: "
  "[New Common Dental Procedures 2026-11-08 (arkusz)](https://docs.google.com/spreadsheets/d/18YDUc4iizkf9e4tz5rfCG9JWz-FZioEGAqs0Y-0EIsQ/edit) "
  "(eksport: `biblioteka/arkusz_procedur.csv`).\n")
A("Zęby naturalne (`natural_11.png` … `natural_48.png`) **nie są na Drive** – są w `biblioteka/natural/` "
  "(powstały z koron cyrkonowych przez przemalowanie korony na kolor szkliwa: `skrypty/zrob_zeby_naturalne.py`).\n")
A("## 1. Jak powstaje schemat\n")
A("1. Z RTG i schematu kliniki ustal stan **każdego** z 32 zębów na koniec danej wizyty.\n"
  "2. Zapisz go w pliku JSON: `{\"state\": {\"<numer>\": \"<stan>\", …}, \"bridges\": [[od, do], …], \"bridge_color\": [r,g,b]}`. "
  "Zęby nie wpisane = `natural`.\n"
  "3. `python3 skrypty/schemat_zebow.py <folder_PNG_z_Drive> biblioteka/natural wynik.png config.json` – skrypt dla każdego zęba bierze plik wg tabeli poniżej, "
  "skaluje wszystkie zęby jednym współczynnikiem (szerokość 2400 px), ustawia je obok siebie wzdłuż linii zgryzu, rysuje numery.\n"
  "4. Jeśli jest podniesienie zatoki: `skrypty/dodaj_zatoki.py` (rysunek nad 16 i/lub 26).\n"
  "5. Zmniejsz do 1500 px (JPG, jakość ~74) i podaj w JSON pacjenta jako `schemat` wizyty.\n")
A("**Zasady rysowania (wspólne):**\n")
A("- Górny łuk: 18 … 11 | 21 … 28, korzenie do góry; dolny: 48 … 41 | 31 … 38, korzenie w dół. Prawa strona pacjenta = lewa strona obrazka.\n"
  "- Numer zęba leczonego na tej wizycie (każdy stan inny niż `natural`/`missing`) – w turkusowej pigułce (#31F1E8) z granatowym tekstem.\n"
  "- `missing` – brak rysunku, numer jasnoszary przekreślony. `natural` – rysunek naturalnego zęba, numer szary.\n"
  "- Most: `bridges: [[45,47]]` – zaokrąglony łącznik między skrajnymi zębami mostu, za koronami (turkus; dla prac tymczasowych bursztyn `[226,170,90]`).\n"
  "- Implant bez korony (`implant`) jest przesunięty o 30% wysokości od linii zgryzu (widać, że nie ma korony).\n"
  "- Kolory: korony stałe – turkus/aqua; prace tymczasowe (PMMA, korony tymczasowe, proteza tymczasowa) – bursztyn; pełne łuki z koronami – biel; dziąsło protezy hybrydowej – róż; implant – turkusowa śruba z tytanową szyjką.\n")
A("## 2. Stany pojedynczych zębów\n")
A("| Stan w JSON | Kiedy | Plik (n = numer FDI) | Folder na Drive | Jak wygląda | Przykład |")
A("|---|---|---|---|---|---|")
for st, when, fn, folder, ex, look in STATES:
    exfile = [f for f in sorted(os.listdir(os.path.join(os.path.dirname(OUT), 'katalog'))) if f.startswith(ex) and f.endswith('.jpg')][0]
    A(f"| `{st}` | {when} | `{fn}` | {flink(folder) if folder else '—'} | {look} | [{exfile}](katalog/{exfile}) |")
A("")
A("Przykładowe pliki na Drive (ząb 36 lub 11): " + ", ".join(link(f) for f in [
  "implant_36.png", "zirconia_crown_36.png", "zirconia_crown_on_implant_36.png", "temporary_crown_on_implant_36.png",
  "temporary_crown_pmma_36.png", "bridge_pontic_36.png", "bridge_abutment_36.png", "implant_bridge_pontic_36.png",
  "implant_bridge_abutment_36.png", "extraction_36.png", "veneer_11.png", "root_canal_36.png", "filling_36.png", "zirconia_implant_36.png"]) + ".\n")
A("> Uwaga: rysunków `temp_pontic_{n}.png` (przęsło stałej pracy tymczasowej) **nie ma na Drive** – generuje je "
  "`skrypty/zrob_przesla_tymczasowe.py` z `implant_bridge_pontic_{n}.png` (przemalowanie na bursztyn PMMA). "
  "Zęby naturalne `natural_{n}.png` – podobnie, z `zirconia_crown_{n}.png` (`skrypty/zrob_zeby_naturalne.py`, gotowe w `biblioteka/natural/`). "
  "Wszystkie PNG z Drive pobieramy do **jednego płaskiego folderu** i podajemy go jako pierwszy argument `schemat_zebow.py`.\n")
A("## 3. Jak przełożyć zabieg z PDF kliniki na stan zęba\n")
A("| Pozycja w PDF kliniki | Schemat wizyty I | Schemat wizyty II |")
A("|---|---|---|")
for a,b,c in [
 ("Implant (Medentika / Straumann)", "`implant`", "zależnie od korony: `implant_crown` / `implant_pontic`"),
 ("Implant + tymczasowa korona na implancie (55 EUR)", "`temp_implant`", "`implant_crown`"),
 ("Implanty + stała tymczasowa praca protetyczna (1 łuk, 421 EUR)", "filary `temp_implant`, przęsła `temp_pontic`, łącznik bursztynowy; przy całym łuku – rysunek pełnego łuku (rozdz. 4)", "korony / most / proteza hybrydowa"),
 ("Korona cyrkonowa na własnym zębie", "`natural` (ząb jeszcze nieoszlifowany)", "`crown`"),
 ("Most na własnych zębach (np. 45–47)", "`natural` filary, `missing` w miejscu przęsła", "filary `crown`, przęsło `pontic`, `bridges: [[45,47]]`"),
 ("Most na implantach (np. 24–26)", "`implant` na filarach, `missing` w przęśle", "`implant_crown` + `implant_pontic`, `bridges: [[24,26]]`"),
 ("Licówka Laminate Veneer", "`natural`", "`veneer`"),
 ("Korona porcelanowa Empress", "`natural`", "`crown` (ten sam rysunek co cyrkon – opis w tekście)"),
 ("Ekstrakcja / ekstrakcja chirurgiczna", "`extraction`", "`missing` (albo implant/przęsło, jeśli tak w planie)"),
 ("Podniesienie zatoki", "rysunek zatoki nad 16 i/lub 26 (`dodaj_zatoki.py`)", "bez zatoki"),
 ("Leczenie kanałowe", "nie rysujemy osobno (ząb pod koronę)", "`crown`"),
 ("Ząb istniejący na RTG, bez zabiegu (też ósemki)", "`natural`", "`natural`"),
 ("Brak zęba na RTG", "`missing`", "`missing`"),
]:
    A(f"| {a} | {b} | {c} |")
A("")
A("## 4. Pełne łuki i zatoki\n")
A(f"Folder: {flink('Full Arch – Pełny łuk')}, {flink('Sinus Lift – Podniesienie zatoki')}. Skrypty: `schemat_pelny_luk.py <górny.png> <dolny.png> <wynik> [zatoka.png] [both]`, `schemat_zatoki_bez_implantow.py`.\n")
A("| Sytuacja | Rysunek | Plik(i) na Drive | Przykład |")
A("|---|---|---|---|")
for sit, look, files, ex in [
 ("Stała tymczasowa praca na implantach – cały łuk (All-on-6 / All-on-4)", "bursztynowy łuk koron na 6 (lub 4) implantach", ["temporary_prosthesis_upper_all-on-6.png","temporary_prosthesis_lower_all-on-6.png","temporary_prosthesis_upper_all-on-4.png","temporary_prosthesis_lower_all-on-4.png"], "11"),
 ("Wizyta II: proteza hybrydowa na implantach", "białe zęby z różowym dziąsłem na implantach", ["hybrid_prosthesis_upper_all-on-6.png","hybrid_prosthesis_lower_all-on-6.png","hybrid_prosthesis_upper_all-on-4.png","hybrid_prosthesis_lower_all-on-4.png"], "12"),
 ("Wizyta II: 12 koron cyrkonowych na implantach w łuku", "białe korony na implantach, bez dziąsła", ["12_zirconia_crowns_upper_all-on-6.png","12_zirconia_crowns_lower_all-on-6.png","12_zirconia_crowns_upper_all-on-4.png","12_zirconia_crowns_lower_all-on-4.png"], "13"),
 ("Proteza Toronto (z belką tytanową)", "białe zęby + dziąsło + szara belka", ["toronto_prosthesis_upper_all-on-6.png","toronto_prosthesis_lower_all-on-6.png"], None),
 ("Podniesienie zatoki przy pełnym łuku (obie strony)", "rysunki zatok nad trzonowcami, podpis „Podniesienie zatoki — prawa/lewa strona”", ["sinus_lift_one_side.png","wide_sinus_lift_one_side.png"], "14"),
 ("Podniesienie zatoki przy pojedynczych implantach", "schemat zębów + pasek z rysunkiem zatoki nad 16/26", ["sinus_lift_one_side.png"], "16"),
 ("Bez implantów na wizycie I (proteza ruchoma) + zatoki", "łuki tymczasowe bez implantów + zatoki", ["sinus_lift_one_side.png"], "15"),
]:
    ex_s = ""
    if ex:
        exfile = [f for f in sorted(os.listdir(os.path.join(os.path.dirname(OUT), 'katalog'))) if f.startswith(ex) and f.endswith('.jpg')][0]
        ex_s = f"[{exfile}](katalog/{exfile})"
    A(f"| {sit} | {look} | " + ", ".join(link(f) for f in files) + f" | {ex_s} |")
A("")
A("Implanty w pełnych łukach: All-on-6 – proste w 16/14/12/22/24/26 i 46/44/42/32/34/36; All-on-4 – proste 12/22 i 42/32, pochylone 35° w 15/25 i 45/35.\n")
A("## 5. Przykłady (podgląd)\n")
for f in sorted(os.listdir(os.path.join(os.path.dirname(OUT), 'katalog'))):
    if f.endswith('.jpg'):
        cfg = f[:-4] + '.json'
        has = os.path.exists(os.path.join(os.path.dirname(OUT), 'katalog', cfg))
        A(f"### {f[:-4].replace('_', ' ')}\n")
        if has: A(f"Konfiguracja: [`katalog/{cfg}`](katalog/{cfg})\n")
        A(f"![{f}](katalog/{f})\n")
A("## 6. Wszystkie foldery biblioteki na Drive\n")
A("| Folder | Liczba plików |")
A("|---|---|")
cnt = {}
for r in rows:
    if not r['mimeType'].endswith('folder'):
        top = r['folder_path'].split(' / ')
        key = top[1] if len(top) > 1 else top[0]
        cnt[key] = cnt.get(key, 0) + 1
for t, r in sorted(folders.items()):
    if t.startswith('New Common'): continue
    A(f"| [{t}]({r['viewUrl']}) | {cnt.get(t, '')} |")
open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('ok', len(rows))
