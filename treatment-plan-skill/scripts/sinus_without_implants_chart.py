import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
A, out = sys.argv[1]+"/", sys.argv[2]
W=2400; M=60
F="/usr/share/fonts/opentype/inter/"; fb=ImageFont.truetype(F+"Inter-SemiBold.otf",40)
NAVY=(19,37,68); LINE=(214,220,226)
U=Image.open(A+"temp_upper_noimpl.png"); L=Image.open(A+"temp_lower_noimpl.png")
s=(W-2*M)/max(U.width,L.width)
U=U.resize((round(U.width*s),round(U.height*s)),Image.LANCZOS); L=L.resize((round(L.width*s),round(L.height*s)),Image.LANCZOS)
SL=Image.open(A+"sinus_lift_one_side.png").convert("RGBA"); SL=SL.crop(SL.getbbox())
sw=540; SL=SL.resize((sw,round(SL.height*sw/SL.width)),Image.LANCZOS); SR=ImageOps.mirror(SL)
top=30; lab=60; gap=30
y_sin=top+lab
y_up=y_sin+SL.height+gap
H=y_up+U.height+40+L.height+90
c=Image.new("RGBA",(W,H),(255,255,255,255)); d=ImageDraw.Draw(c)
ux=(W-U.width)//2
cxR=ux+int(U.width*0.12); cxL=ux+int(U.width*0.88)
for cx,img,t in ((cxR,SL,"Podniesienie zatoki — prawa strona"),(cxL,SR,"Podniesienie zatoki — lewa strona")):
    c.alpha_composite(img,(cx-img.width//2,y_sin))
    w=d.textlength(t,font=fb); tx=min(max(cx-w/2,M),W-M-w); d.text((tx,top),t,font=fb,fill=NAVY)
    # dotted guide from sinus to molars
c.alpha_composite(U,(ux,y_up))
t='Szczęka górna — proteza tymczasowa ruchoma'; fm=ImageFont.truetype(F+'Inter-Medium.otf',34); w=d.textlength(t,font=fm); d.text(((W-w)/2,y_sin+SL.height//2-20),t,font=fm,fill=(110,120,135))
yo=y_up+U.height+20; d.line((M,yo,W-M,yo),fill=LINE,width=3)
c.alpha_composite(L,((W-L.width)//2,yo+20))
t='Żuchwa — proteza tymczasowa ruchoma'; w=d.textlength(t,font=fm); d.text(((W-w)/2,yo+20+L.height+14),t,font=fm,fill=(110,120,135))
c.convert("RGB").save(out,quality=86,optimize=True,progressive=True); print(c.size)
