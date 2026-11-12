const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('file:///home/user/-/build/living.html');
  await pg.evaluate(() => document.fonts.ready);
  await pg.pdf({ path: '/home/user/-/takseef_alkaenat_alhaya.pdf', format: 'A4', printBackground: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:9px;width:100%;text-align:center;font-family:LoewNA,FreeSerif"><span dir="ltr"><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    margin: { top: '13mm', bottom: '14mm', left: '14mm', right: '14mm' } });
  await b.close();
})();
