const { chromium } = require('playwright'); const fs=require('fs');
(async () => {
  const [,, html, pdf, W] = process.argv; const w=parseInt(W||'900');
  let h=fs.readFileSync(html,'utf8');
  if (w<700) h=h.split('@media(max-width:700px)').join('@media all');
  h=h.replace('</body>','<style>html{background:#162447}*,*::before,*::after{box-shadow:none !important;text-shadow:none !important;filter:none !important}</style></body>');
  const tmp=html.replace(/\.html$/,'.print.html'); fs.writeFileSync(tmp,h);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: w, height: 1200 } });
  await p.goto('file://' + tmp, { waitUntil: 'networkidle', timeout: 60000 });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
  const cw = await p.evaluate(() => document.documentElement.clientWidth);
  const ch = await p.evaluate(() => Math.ceil(document.documentElement.scrollHeight)+4);
  await p.pdf({ path: pdf, width: cw+'px', height: ch+'px', printBackground: true, margin:{top:0,bottom:0,left:0,right:0} });
  console.log(cw, ch); await b.close(); fs.unlinkSync(tmp);
})();
