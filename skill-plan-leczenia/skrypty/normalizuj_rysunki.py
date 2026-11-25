"""KLUCZ PROPORCJI – przygotowanie rysunków pod system, który wkleja każdy obrazek
osobno do pola (object-fit: contain).

Problem: system skaluje każdy plik do swojego pola niezależnie, więc ząb przycięty
ciasno (np. siekacz 230 px szerokości) i trzonowiec (361 px) wychodzą w różnej skali,
a pełny łuk (2991 px szerokości) rozciąga się na całą szerokość 11 pól.

Rozwiązanie (tak jak w schematach Fly4Smile): każdy plik dostaje płótno o STAŁEJ WYSOKOŚCI 940 px
(wspólna skala 32,7 px = 1 mm), a szerokość płótna = szerokość MIEJSCA zęba (= szerokość korony cyrkonowej tego zęba + 4 px z boków), element na środku:
  • szczęka (1x, 2x):   krawędź zgryzowa korony 30 px nad dolną krawędzią płótna (korzenie w górę),
  • żuchwa (3x, 4x):    krawędź zgryzowa korony 30 px pod górną krawędzią płótna (korzenie w dół),
  • sam implant (bez korony): platforma implantu 265 px od krawędzi zgryzowej,
  • pełny łuk:          ta sama wysokość 940 px, szerokość = suma szerokości miejsc 16–26 (46–36),
  • brak zęba:          missing_XX.png – przezroczyste miejsce o szerokości zęba.
WARUNEK PO STRONIE SYSTEMU: obrazki w rzędzie mają tę samą WYSOKOŚĆ i szerokość automatyczną
(np. CSS: .row{display:flex;justify-content:center;gap:2px} .row img{height:116px;width:auto}),
a nie równe pola. Wtedy każdy ząb ma swoją naturalną szerokość, zęby stykają się jak w naturze,
a pełny łuk zajmuje dokładnie miejsce zębów, które zastępuje. Numer zęba – w tej samej kolumnie co obrazek.

Użycie: python3 normalizuj_rysunki.py <folder_wejściowy_PNG> <folder_wyjściowy>
(nazwy plików bez zmian; rozpoznaje szczękę/żuchwę i pełne łuki po nazwie)."""
import sys, os, re, glob
from PIL import Image

CH, EDGE, IMPL_OFF, SIDE = 940, 30, 265, 4

UPR = [18,17,16,15,14,13,12,11,21,22,23,24,25,26,27,28]
LOR = [48,47,46,45,44,43,42,41,31,32,33,34,35,36,37,38]
REFW = {}   # szerokość miejsca każdego zęba = szerokość zirconia_crown_XX + 2×SIDE

def load_ref(folder):
    for n in UPR + LOR:
        f = os.path.join(folder, f"zirconia_crown_{n}.png")
        if os.path.exists(f):
            b = Image.open(f).getbbox(); REFW[n] = (b[2]-b[0]) + 2*SIDE

def missing(folder_out):
    """missing_XX.png – przezroczyste miejsce po brakującym zębie (system wstawia je w miejsce braku)."""
    for n, w in REFW.items():
        Image.new("RGBA", (w, CH), (0,0,0,0)).save(os.path.join(folder_out, f"missing_{n}.png"))

def upper_of(name):
    m = re.search(r"_(\d)\d\.png$", name)
    if m: return m.group(1) in "1256"          # 1x, 2x (mleczne 5x, 6x) = szczęka
    return "upper" in name

def norm(src, dst):
    name = os.path.basename(src)
    im = Image.open(src).convert("RGBA"); im = im.crop(im.getbbox())
    up = upper_of(name)
    arch = "all-on" in name
    m = re.search(r"_(\d\d)\.png$", name)
    n = int(m.group(1)) if m else None
    if arch:
        row = UPR if up else LOR
        w = sum(REFW[t] for t in row[row.index(16 if up else 46):row.index(26 if up else 36)+1]) if REFW else im.width + 2*SIDE
    elif n in REFW:
        w = max(REFW[n], im.width + 2*SIDE)    # szerokość miejsca zęba (jak korona cyrkonowa tego zęba)
    else:
        w = im.width + 2 * SIDE
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
    load_ref(a); missing(b)
    for f in sorted(glob.glob(os.path.join(a, "*.png"))):
        if "sinus" in f: continue
        norm(f, os.path.join(b, os.path.basename(f)))
    print("gotowe")
