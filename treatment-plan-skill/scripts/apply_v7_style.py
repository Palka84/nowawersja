"""Applies the approved "v7" style to the offer HTML produced by build_offer.py:
darker text, fonts ×1.15, white background behind certificate images, no badges under the certificates,
optional replacement of photos with high-quality versions, iPhone-safe highlight style (.hl).
Usage: python3 apply_v7_style.py <offer.html> <offer_v7.html> <folder_with_photos_or_empty_folder>"""
import sys, re, os, base64
src, dst, imgdir = sys.argv[1:4]
h = open(src, encoding='utf-8').read()

# 1) photo replacement: n-th <img> in document order -> file from imgdir (if present)
REPL = {5: 'klinika_szeroka.jpg', 6: 'klinika_recepcja.jpg', 7: 'klinika_strefa.jpg',
        9: 'cert_highest_volume.jpg', 10: 'cert_diamond.jpg',
        11: 'rev_wilhelm.jpg', 12: 'rev_tomek.jpg', 13: 'rev_weronika.jpg', 14: 'rev_beata.jpg'}
k = -1
def sub(m):
    global k
    k += 1
    f = os.path.join(imgdir, REPL.get(k, '__brak__'))
    if not os.path.exists(f):
        return m.group(0)
    return 'src="data:image/jpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode() + '"'
h = re.sub(r'src="data:image/[^"]+"', sub, h)

# 2) remove the badges (JCI / Straumann / Medentika / Diamond) under the certificates
h = re.sub(r'<div class="cert-row">.*?</div>', '', h, count=1, flags=re.S)

# 3) larger fonts: every font-size in px ×1.15
def big(m):
    v = float(m.group(1)) * 1.15
    return f'font-size:{v:.1f}px'
h = re.sub(r'<style[^>]*>.*?</style>', lambda s: re.sub(r'font-size:([\d.]+)px', big, s.group(0)), h, flags=re.S)

# 4) darker text + white background for certificate images
CSS = """
<style id="v7">
:root{--muted:#3A4256;--ink:#0B1220;}
body{color:#0B1220;}
.item{color:#0B1220;}
.item small{color:var(--navy);font-size:11.5px;letter-spacing:.1em;}
.pay th{color:#3A4256;}
.rv-tx p,.rc-body p,.about p,.plan-intro,.vid-intro p,.vid .tx p{color:#0B1220;}
.rev-foot,.where-card span,.includes,.note,.sources{color:#3A4256;}
.rc-img,.rc-card.wide .rc-img{background:#fff;border-bottom:1px solid var(--line);padding:18px 0;}
.rc-img img{border-radius:10px;}
.item > div:first-child{font-weight:600;}
.hl{color:var(--navy);font-weight:700;text-decoration-line:underline;text-decoration-color:#9BF6F1;text-decoration-thickness:0.5em;text-underline-offset:-0.28em;text-decoration-skip-ink:none;-webkit-text-decoration-skip:none;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
.passport{background:#fff;border:1px solid var(--line);}
.total b{white-space:nowrap;}
@media(max-width:700px){
  .timeline{flex-direction:row;gap:0;} .timeline:before{display:block;}
  .total{gap:14px;} .total b{font-size:26px;}
  .rc-img img,.rc-card.wide .rc-img img{height:auto;max-height:420px;}
  .cover .photo{height:400px;}
  .cover .overlay{position:static;background:var(--navy);padding:22px 20px 26px;}
  .meta{grid-template-columns:1fr 1fr 1fr;row-gap:16px;}
}
</style>
"""
h = h.replace('</head>', CSS + '</head>', 1)
open(dst, 'w', encoding='utf-8').write(h)
print(dst, len(h) // 1024, 'KB, obrazki podmienione:', [v for i, v in REPL.items() if os.path.exists(os.path.join(imgdir, v))])
