"""Diagram 32 zębów w stylu formatki Fly4Smile, z grafik z biblioteki (2x rozdzielczość).
state: crown | pontic | natural | missing ; treated = podświetlony numer"""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont
TEETH, NAT, OUT, CFG = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
cfg = json.load(open(CFG))
st = {int(k): v for k, v in cfg["state"].items()}
bridges = cfg.get("bridges", [])
BRC = tuple(cfg.get("bridge_color", [104,204,198]))
W = 2400
NAVY=(19,37,68); CYAN=(49,241,232); CYAN_D=(10,120,135); GREY=(120,128,140); LINE=(214,220,226); TEAL=(104,204,198)
F = "/usr/share/fonts/opentype/inter/"
fb = ImageFont.truetype(F+"Inter-Bold.otf", 28); fm = ImageFont.truetype(F+"Inter-Medium.otf", 28)
UP = [18,17,16,15,14,13,12,11,21,22,23,24,25,26,27,28]
LO = [48,47,46,45,44,43,42,41,31,32,33,34,35,36,37,38]
def load(n):
    s = st.get(n, "natural")
    if s == "missing": return None
    fn = {"crown": f"{TEETH}/zirconia_crown_{n}.png", "pontic": f"{TEETH}/bridge_pontic_{n}.png",
          "natural": f"{NAT}/natural_{n}.png",
          "implant_crown": f"{TEETH}/zirconia_crown_on_implant_{n}.png", "implant_pontic": f"{TEETH}/implant_bridge_pontic_{n}.png",
          "temp_implant": f"{TEETH}/temporary_crown_on_implant_{n}.png", "temp_pontic": f"{TEETH}/temp_pontic_{n}.png",
          "implant": f"{TEETH}/implant_{n}.png", "extraction": f"{TEETH}/extraction_{n}.png",
          "veneer": f"{TEETH}/veneer_{n}.png" if os.path.exists(f"{TEETH}/veneer_{n}.png") else f"{NAT}/natural_{n}.png"}[s]
    im = Image.open(fn).convert("RGBA"); return im.crop(im.getbbox())
# proportional layout: teeth side by side (anatomical widths), rows centred on midline
M = 56
ref = {n: load(n) for n in UP + LO}
base = {n: Image.open(f"{TEETH}/zirconia_crown_{n}.png").getbbox() for n in UP + LO}
bw = {n: base[n][2]-base[n][0] for n in UP + LO}
GAPPX = 10
s = (W - 2*M - GAPPX*15) / max(sum(bw[n] for n in UP), sum(bw[n] for n in LO))
hmax = max(base[n][3]-base[n][1] for n in UP+LO) * s
def centers(row):
    tot = sum(bw[n]*s for n in row) + GAPPX*(len(row)-1); x = (W - tot)/2; out = {}
    for n in row:
        out[n] = x + bw[n]*s/2; x += bw[n]*s + GAPPX
    return out
CU, CL = centers(UP), centers(LO)
PILL = 48; GAP = 18
top_lab = 20; up_occ = top_lab + PILL + GAP + hmax; occ = up_occ + 18
lo_top = occ + 18; lo_lab = lo_top + hmax + GAP
H = int(lo_lab + PILL + 20)
c = Image.new("RGBA", (W, H), (255,255,255,255)); d = ImageDraw.Draw(c)
# divider lines
d.line((M, occ, W-M, occ), fill=LINE, width=3)
d.line((W/2, top_lab+PILL+8, W/2, lo_lab-8), fill=LINE, width=3)
def pill(x, y, n):
    t = str(n); treated = st.get(n) in ("crown", "pontic", "implant_crown", "implant_pontic", "temp_implant", "temp_pontic", "veneer", "implant", "extraction")
    w = d.textlength(t, font=fb)
    if treated:
        d.rounded_rectangle((x-33, y, x+33, y+PILL), radius=10, fill=CYAN)
        d.text((x-w/2, y+8), t, font=fb, fill=NAVY)
    elif st.get(n) == "missing":
        w2 = d.textlength(t, font=fm); c2 = (196,202,210)
        d.text((x-w2/2, y+8), t, font=fm, fill=c2)
        d.line((x-w2/2-6, y+PILL/2+1, x+w2/2+6, y+PILL/2+1), fill=c2, width=3)
    else:
        d.text((x-d.textlength(t,font=fm)/2, y+8), t, font=fm, fill=GREY)
# bridge connectors (behind crowns, lower jaw crown zone)
pos = {**CU, **CL}
for a, b in bridges:
    x1, x2 = sorted((pos[a], pos[b]))
    if a // 10 in (1, 2):
        d.rounded_rectangle((x1, up_occ-76, x2, up_occ-36), radius=20, fill=BRC)
    else:
        d.rounded_rectangle((x1, lo_top+36, x2, lo_top+76), radius=20, fill=BRC)
for row, y_edge, up in ((UP, up_occ, True), (LO, lo_top, False)):
    for i, n in enumerate(row):
        im = ref[n]; x = (CU if up else CL)[n]
        pill(x, top_lab if up else lo_lab, n)
        if im is None: continue
        im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
        off = round(hmax*0.30) if st.get(n)=="implant" else 0
        y = y_edge - im.height - off if up else y_edge + off
        c.alpha_composite(im, (round(x - im.width/2), round(y)))
c.convert("RGB").save(OUT, quality=86, optimize=True, progressive=True)
print(c.size, s)
