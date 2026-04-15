const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  const htmlPath = path.join(__dirname, 'papers/LAGRANGIAN_FROM_GEOMETRY_v4.1.1.html');
  const pdfPath = path.join(__dirname, 'papers/LAGRANGIAN_FROM_GEOMETRY_v4.1.1.pdf');

  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle0' });

  await page.pdf({
    path: pdfPath,
    format: 'Letter',
    margin: {
      top: '0.6in',
      right: '0.6in',
      bottom: '0.6in',
      left: '0.6in'
    },
    printBackground: true,
    displayHeaderFooter: false,
    preferCSSPageSize: true
  });

  console.log('PDF generated: ' + pdfPath);
  await browser.close();
})();
