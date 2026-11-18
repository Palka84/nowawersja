"""Dodaje nad schematem zębów (z schemat_zebow.py) pasek z rysunkiem podniesienia zatoki
i podpisem „Podniesienie zatoki — prawa/lewa strona”.
Rysunek zatoki stoi nad zębem 16 (prawa strona pacjenta = lewa strona obrazka) i/lub 26.
Użycie:
  python3 dodaj_zatoki.py <schemat.jpg|png> <sinus_lift_one_side.png> <wynik.jpg> prawa|lewa|obie [pl|en]
Rysunek zatoki: Drive › Sinus Lift – Podniesienie zatoki › sinus_lift_one_side.png
(szerokie podniesienie: wide_sinus_lift_one_side.png)."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

chart, sinus, out, side = sys.argv[1:5]
lang = sys.argv[5] if len(sys.argv) > 5 else "pl"
LAB = {"pl": ("Podniesienie zatoki — prawa strona", "Podniesienie zatoki — lewa strona"),
       "en": ("Sinus lift — right side", "Sinus lift — left side")}[lang]
ch = Image.open(chart).convert("RGB")
SL = Image.open(sinus).convert("RGBA"); SL = SL.crop(SL.getbbox())
W = ch.width; k = W / 2400                      # skrypt liczony dla szerokości 2400 px
sw = round(380 * k); SL = SL.resize((sw, round(SL.height * sw / SL.width)), Image.LANCZOS)
F = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", max(14, round(34 * k)))
bh = SL.height + round(70 * k)
c = Image.new("RGB", (W, bh + ch.height), "white"); c.paste(ch, (0, bh)); d = ImageDraw.Draw(c)
sides = []
if side in ("prawa", "obie"): sides.append((int(W * 0.19), ImageOps.mirror(SL), LAB[0]))   # nad zębem 16
if side in ("lewa", "obie"):  sides.append((int(W * 0.81), SL, LAB[1]))                     # nad zębem 26
for cx, img, t in sides:
    w = d.textlength(t, font=F)
    d.text((min(max(cx - w / 2, 40 * k), W - 40 * k - w), round(10 * k)), t, font=F, fill=(19, 37, 68))
    c.paste(img, (cx - img.width // 2, round(60 * k)), img)
c.save(out, quality=86, optimize=True, progressive=True); print(out, c.size)
