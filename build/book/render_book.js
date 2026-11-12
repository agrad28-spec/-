const { chromium } = require('playwright');
const target = process.argv[2] || 'book';
const out = { book: '/home/user/-/kitab_al_ulum_4_ibtidai.pdf', guide: '/home/user/-/dalil_ijabat_almuallim.pdf' }[target];
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('file:///home/user/-/build/book/' + target + '.html');
  await pg.evaluate(() => document.fonts.ready);
  await pg.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:10px;width:100%;text-align:center;font-family:LoewNA,FreeSerif"><span dir="ltr"><span class="pageNumber"></span></span></div>',
    preferCSSPageSize: true });
  await b.close();
})();
