"""KLUCZ PROPORCJI – przygotowanie rysunków pod system, który wkleja każdy obrazek
osobno do pola (object-fit: contain).

Problem: system skaluje każdy plik do swojego pola niezależnie, więc ząb przycięty
ciasno (np. siekacz 230 px szerokości) i trzonowiec (361 px) wychodzą w różnej skali,
a pełny łuk (2991 px szerokości) rozciąga się na całą szerokość 11 pól.

Rozwiązanie (tak jak w schematach Fly4Smile): każdy plik dostaje płótno o STAŁEJ WYSOKOŚCI 940 px
(wspólna skala 32,7 px = 1 mm), a szerokość płótna = szerokość zęba + 4 px z każdej strony:
  • szczęka (1x, 2x):   krawędź zgryzowa korony 30 px nad dolną krawędzią płótna (korzenie w górę),
  • żuchwa (3x, 4x):    krawędź zgryzowa korony 30 px pod górną krawędzią płótna (korzenie w dół),
  • sam implant (bez korony): platforma implantu 265 px od krawędzi zgryzowej,
  • pełny łuk:          ta sama wysokość 940 px, szerokość = szerokość łuku.
WARUNEK PO STRONIE SYSTEMU: obrazki w rzędzie mają tę samą WYSOKOŚĆ i szerokość automatyczną
(np. CSS: .row{display:flex;justify-content:center;gap:2px} .row img{height:116px;width:auto}),
a nie równe pola. Wtedy każdy ząb ma swoją naturalną szerokość, zęby stykają się jak w naturze,
a pełny łuk zajmuje dokładnie miejsce zębów, które zastępuje. Numer zęba – w tej samej kolumnie co obrazek.

Użycie: python3 normalizuj_rysunki.py <folder_wejściowy_PNG> <folder_wyjściowy>
(nazwy plików bez zmian; rozpoznaje szczękę/żuchwę i pełne łuki po nazwie)."""
import sys, os, re, glob
from PIL import Image

CH, EDGE, IMPL_OFF, SIDE = 940, 30, 265, 4

def upper_of(name):
    m = re.search(r"_(\d)\d\.png$", name)
    if m: return m.group(1) in "1256"          # 1x, 2x (mleczne 5x, 6x) = szczęka
    return "upper" in name

def norm(src, dst):
    name = os.path.basename(src)
    im = Image.open(src).convert("RGBA"); im = im.crop(im.getbbox())
    up = upper_of(name)
    arch = "all-on" in name
    w = im.width + 2 * SIDE                    # szerokość = szerokość zęba (bez pustych pól po bokach)
    if im.height > CH - EDGE:
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
