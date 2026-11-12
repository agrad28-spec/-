const { chromium } = require('playwright');
const fs = require('fs');
const emb = 'data:image/png;base64,' + fs.readFileSync('/home/user/-/build/book/assets/emblem.png').toString('base64');
const target = process.argv[2] || 'book';
const out = { book: '/home/user/-/kitab_al_ulum_4_ibtidai.pdf', guide: '/home/user/-/dalil_ijabat_almuallim.pdf' }[target];
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('file:///home/user/-/build/book/' + target + '.html');
  await pg.evaluate(() => document.fonts.ready);
  await pg.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
