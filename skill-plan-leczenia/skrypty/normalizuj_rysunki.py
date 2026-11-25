"""IMAGE PROPORTION KEY – prepares the tooth-image library for a system that places each image separately.

Problem: the system fitted every file into its own equal-width cell (object-fit: contain), so tightly
cropped images (incisor 230 px wide, molar 361 px) ended up at different scales and a full arch
stretched across 11 cells.

Solution (same as the Fly4Smile offer charts): every file gets a canvas of FIXED HEIGHT 940 px
(common scale 32.7 px = 1 mm, drawings are never rescaled); canvas width = TOOTH-POSITION WIDTH
(width of that tooth's zirconia crown + 4 px on each side), element centred:
  • upper jaw (1x, 2x):  occlusal edge of the crown 30 px above the bottom of the canvas (roots up),
  • lower jaw (3x, 4x):  occlusal edge 30 px below the top of the canvas (roots down),
  • implant without crown: implant platform 265 px from the occlusal line,
  • full arch:           height 940 px, width = sum of positions 16–26 (46–36),
  • missing tooth:       missing_XX.png – transparent canvas of the tooth-position width.
SYSTEM REQUIREMENT: all images in a row have the same HEIGHT and automatic width
(CSS: .row{display:flex;justify-content:center;gap:1px} .row img{height:96px;width:auto}),
not equal-width cells. Full spec: IT_SPEC_image_proportions_EN.md.

Usage: python3 normalizuj_rysunki.py <input_PNG_folder> <output_folder>
(file names unchanged; upper/lower jaw and full arches are detected from the file name;
the input folder must contain zirconia_crown_11 … zirconia_crown_48 – they define the position widths)."""
import sys, os, re, glob
from PIL import Image

CH, EDGE, IMPL_OFF, SIDE = 940, 30, 265, 4

UPR = [18,17,16,15,14,13,12,11,21,22,23,24,25,26,27,28]
LOR = [48,47,46,45,44,43,42,41,31,32,33,34,35,36,37,38]
REFW = {}   # tooth-position width = zirconia_crown_XX width + 2×SIDE

def load_ref(folder):
    for n in UPR + LOR:
        f = os.path.join(folder, f"zirconia_crown_{n}.png")
        if os.path.exists(f):
            b = Image.open(f).getbbox(); REFW[n] = (b[2]-b[0]) + 2*SIDE

def missing(folder_out):
    """missing_XX.png – transparent placeholder for a missing tooth."""
    for n, w in REFW.items():
        Image.new("RGBA", (w, CH), (0,0,0,0)).save(os.path.join(folder_out, f"missing_{n}.png"))

def upper_of(name):
    m = re.search(r"_(\d)\d\.png$", name)
    if m: return m.group(1) in "1256"          # 1x, 2x (primary 5x, 6x) = upper jaw
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
        w = max(REFW[n], im.width + 2*SIDE)    # tooth-position width
    else:
        w = im.width + 2 * SIDE
    if im.height > CH - EDGE:
        print("WARNING – does not fit, check:", name, im.size)
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
    print("done")
