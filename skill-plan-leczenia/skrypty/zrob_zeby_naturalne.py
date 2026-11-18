"""Tworzy rysunki zębów naturalnych (natural_XX.png) z biblioteki koron cyrkonowych:
piksele turkusowe (korona) są przemalowane na kolor szkliwa (kość słoniowa) wg luminancji.
Korzeń zostaje bez zmian. Wynik: biblioteka/natural/ (32 pliki, 11–48).
Użycie: python3 zrob_zeby_naturalne.py <folder_z_zirconia_crown_XX.png> <folder_wyjściowy>"""
import sys, glob, os, colorsys
from PIL import Image
SRC, OUT = sys.argv[1], sys.argv[2]
LUT = [(40,(150,132,110)),(120,(214,204,186)),(190,(240,234,220)),(235,(250,247,238)),(255,(255,255,252))]
def lut(v):
    for (a,ca),(b,cb) in zip(LUT, LUT[1:]):
        if v <= b:
            t = max(0, (v-a)/(b-a)); return tuple(round(ca[i]+(cb[i]-ca[i])*t) for i in range(3))
    return LUT[-1][1]
os.makedirs(OUT, exist_ok=True)
for fn in sorted(glob.glob(os.path.join(SRC, "zirconia_crown_[1-4][1-8].png"))):
    im = Image.open(fn).convert("RGBA"); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r,g,b,a = px[x,y]
            if a == 0: continue
            h,s,v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            if 0.40 < h < 0.58 and s > 0.12:
                L = int(0.299*r+0.587*g+0.114*b); L = min(255, int(L*1.08)+8)
                c = lut(L); px[x,y] = (c[0],c[1],c[2],a)
    im.save(os.path.join(OUT, "natural_" + fn.split("_")[-1]))
print("gotowe:", len(os.listdir(OUT)))
