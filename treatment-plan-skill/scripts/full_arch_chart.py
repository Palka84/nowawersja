import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
up, lo, out = sys.argv[1:4]; sinus = sys.argv[4] if len(sys.argv) > 4 else ""; both = len(sys.argv) > 5 and sys.argv[5] == "both"
W=2400; M=60; GAP=40
F="/usr/share/fonts/opentype/inter/"; fb=ImageFont.truetype(F+"Inter-SemiBold.otf",40)
U=Image.open(up).convert("RGBA"); U=U.crop(U.getbbox()); L=Image.open(lo).convert("RGBA"); L=L.crop(L.getbbox())
s=(W-2*M)/max(U.width,L.width)
U=U.resize((round(U.width*s),round(U.height*s)),Image.LANCZOS); L=L.resize((round(L.width*s),round(L.height*s)),Image.LANCZOS)
top=40; SL=None
if sinus:
    SL=Image.open(sinus).convert("RGBA"); SL=SL.crop(SL.getbbox()); sw=480; SL=SL.resize((sw,round(SL.height*sw/SL.width)),Image.LANCZOS); SL=ImageOps.mirror(SL)
    top=40+60+SL.height-150
H=top+U.height+GAP+L.height+40
c=Image.new("RGBA",(W,H),(255,255,255,255)); d=ImageDraw.Draw(c)
ux=(W-U.width)//2
if SL:
    sides=[(min(ux+int(U.width*0.955), W-SL.width//2-12), SL, "Podniesienie zatoki — lewa strona")]
    if both: sides.append((max(ux+int(U.width*0.045), SL.width//2+12), ImageOps.mirror(SL), "Podniesienie zatoki — prawa strona"))
    for cx,img,t in sides:
        w=d.textlength(t,font=fb); d.text((min(max(cx-w/2,M),W-M-w),40),t,font=fb,fill=(19,37,68)); c.alpha_composite(img,(cx-img.width//2,100))
c.alpha_composite(U,(ux,top)); y=top+U.height+GAP//2
d.line((M,y,W-M,y),fill=(214,220,226),width=3)
c.alpha_composite(L,((W-L.width)//2,top+U.height+GAP))
c.convert("RGB").save(out,quality=86,optimize=True,progressive=True); print(out.split("/")[-1], c.size)
