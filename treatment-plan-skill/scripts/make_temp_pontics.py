"""Creates pontics of a fixed temporary prosthesis (temp_pontic_XX.png) – amber crowns without root –
from implant_bridge_pontic_XX.png (Drive › Implant Bridge – Most na implantach)
by recolouring by luminance to the amber palette (same as PMMA temporary work).
Usage: python3 make_temp_pontics.py <folder_with_implant_bridge_pontic> <output_folder>"""
import sys, glob, os
from PIL import Image
SRC, OUT = sys.argv[1], sys.argv[2]
LUT = [(40,(150,88,25)),(120,(214,140,52)),(190,(240,190,105)),(235,(252,228,170)),(255,(255,248,225))]
def lut(v):
    for (a,ca),(b,cb) in zip(LUT, LUT[1:]):
        if v <= b:
            t = max(0, (v-a)/(b-a)); return tuple(round(ca[i]+(cb[i]-ca[i])*t) for i in range(3))
    return LUT[-1][1]
os.makedirs(OUT, exist_ok=True)
for fn in sorted(glob.glob(os.path.join(SRC, "implant_bridge_pontic_[1-4][1-8].png"))):
    im = Image.open(fn).convert("RGBA"); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r,g,b,a = px[x,y]
            if a:
                c = lut(int(0.299*r+0.587*g+0.114*b)); px[x,y] = (*c, a)
    im.save(os.path.join(OUT, "temp_pontic_" + fn.split("_")[-1]))
print("done")
