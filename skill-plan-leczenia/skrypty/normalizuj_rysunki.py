"""KLUCZ PROPORCJI – przygotowanie rysunków pod system, który wkleja każdy obrazek
osobno do pola (object-fit: contain).

Problem: system skaluje każdy plik do swojego pola niezależnie, więc ząb przycięty
ciasno (np. siekacz 230 px szerokości) i trzonowiec (361 px) wychodzą w różnej skali,
a pełny łuk (2991 px szerokości) rozciąga się na całą szerokość 11 pól.

Rozwiązanie: każdy plik dostaje płótno o STAŁEJ WYSOKOŚCI (wspólna skala 32,7 px = 1 mm):
  • pojedynczy ząb:     płótno 380 × 940 px (11,6 × 28,7 mm), ząb na środku w poziomie,
  • szczęka (1x, 2x):   krawędź zgryzowa korony 30 px nad dolną krawędzią płótna (korzenie w górę),
  • żuchwa (3x, 4x):    krawędź zgryzowa korony 30 px pod górną krawędzią płótna (korzenie w dół),
  • sam implant (bez korony): platforma implantu 265 px od krawędzi zgryzowej (tam, gdzie zaczyna się korzeń),
  • pełny łuk:          płótno n × 380 px szerokości (n = liczba zębów, które łuk zastępuje, np. 16–26 → 11)
                        i ta sama wysokość 940 px; łuk na środku, krawędź zgryzowa jak wyżej.
Ponieważ WSZYSTKIE płótna mają tę samą wysokość, a system dopasowuje je do pól o tej samej wysokości,
każdy element dostaje ten sam współczynnik skali → proporcje się zgadzają.
Warunek po stronie systemu: pole jednego zęba musi mieć proporcje 380:940 (np. 47 × 116 px),
a pole łuku = n pól obok siebie i ta sama wysokość.

Użycie: python3 normalizuj_rysunki.py <folder_wejściowy_PNG> <folder_wyjściowy>
(nazwy plików bez zmian; rozpoznaje szczękę/żuchwę i pełne łuki po nazwie)."""
import sys, os, re, glob
from PIL import Image

CW, CH, EDGE, IMPL_OFF = 380, 940, 30, 265
SPAN = {"upper": 11, "lower": 11}   # 16–26 i 46–36

def upper_of(name):
    m = re.search(r"_(\d)\d\.png$", name)
    if m: return m.group(1) in "1256"          # 1x, 2x (mleczne 5x, 6x) = szczęka
    return "upper" in name

def norm(src, dst):
    name = os.path.basename(src)
    im = Image.open(src).convert("RGBA"); im = im.crop(im.getbbox())
    up = upper_of(name)
    arch = "all-on" in name
    w = CW * (SPAN["upper" if up else "lower"] if arch else 1)
    if im.width > w or im.height > CH - EDGE:
        print("UWAGA – nie mieści się, sprawdź:", name, im.size)
    c = Image.new("RGBA", (w, CH), (0, 0, 0, 0))
    off = IMPL_OFF if re.match(r"(zirconia_)?implant_\d\d\.png$", name) else 0
    x = (w - im.width) // 2
    y = (CH - EDGE - im.height - off) if up else (EDGE + off)
    c.alpha_composite(im, (x, max(0, y)))
    c.save(dst)

if __name__ == "__main__":
    a, b = sys.argv[1], sys.argv[2]; os.makedirs(b, exist_ok=True)
    for f in sorted(glob.glob(os.path.join(a, "*.png"))):
        if "sinus" in f: continue
        norm(f, os.path.join(b, os.path.basename(f)))
    print("gotowe")
