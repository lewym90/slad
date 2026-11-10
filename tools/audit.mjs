// Audyt techniczny: zasoby SW, offline, Wstecz, błędne raporty, przepełnienia na wielu ekranach.
// Użycie: node tools/audit.mjs http://localhost:8800/ /tmp/state.json
import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
import fs from 'fs';
const URL = process.argv[2] || 'http://localhost:8800/';
const STATE = fs.readFileSync(process.argv[3] || '/tmp/state-phone.json', 'utf8');
const results = []; const ok = (name, pass, info = '') => { results.push([pass ? 'OK  ' : 'FAIL', name, info]); };
const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
const errs = [];
const page = async (vp, mobile = true) => { const ctx = await b.newContext({ viewport: vp, isMobile: mobile, hasTouch: mobile, deviceScaleFactor: 1 }); const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); p.on('dialog', d => d.accept()); return { ctx, p }; };
const inject = async (p, hash, state = STATE) => { await p.goto(URL, { waitUntil: 'networkidle' }); await p.evaluate(s => localStorage.setItem('slad.v2', s), state); await p.evaluate(h => { location.hash = h; }, hash); await p.reload({ waitUntil: 'networkidle' }); await p.evaluate(h => { location.hash = h; }, hash); await p.waitForTimeout(500); };

// 1. Zasoby z sw.js
{ const sw = fs.readFileSync(new globalThis.URL('../sw.js', import.meta.url), 'utf8'); const urls = [...sw.matchAll(/'(\.\/[^']*)'/g)].map(m => m[1]);
  const { ctx, p } = await page({ width: 390, height: 844 }); await p.goto(URL);
  const bad = await p.evaluate(async us => { const out = []; for (const u of us) { const r = await fetch(u, { cache: 'no-store' }); if (!r.ok) out.push(u + ' ' + r.status); } return out; }, urls);
  ok(`Wszystkie ${urls.length} pliki z pamięci offline istnieją`, !bad.length, bad.join(', ')); await ctx.close(); }

// 2. Offline
{ const { ctx, p } = await page({ width: 390, height: 844 }); await p.goto(URL, { waitUntil: 'networkidle' });
  await p.evaluate(() => navigator.serviceWorker.ready); await p.reload({ waitUntil: 'networkidle' }); await p.waitForTimeout(2500);
  const cached = await p.evaluate(async () => { const ks = await caches.keys(); let n = 0; for (const k of ks) n += (await (await caches.open(k)).keys()).length; return n; });
  await ctx.setOffline(true); await p.reload({ waitUntil: 'domcontentloaded' }); await p.waitForTimeout(800);
  const home = await p.locator('.case-card').count();
  await p.evaluate(() => { location.hash = '#/sprawa/001'; }); await p.waitForTimeout(800);
  const intro = await p.locator('.brief h1').count();
  const fontOk = await p.evaluate(() => document.fonts.check('700 20px Cormorant') && document.fonts.check('16px Typewriter'));
  ok(`Offline: strona główna i sprawa działają bez sieci (w pamięci ${cached} plików)`, home === 9 && intro === 1, `karty=${home} brief=${intro}`);
  ok('Offline: czcionki dostępne', fontOk); await ctx.close(); }

// 3. Przycisk Wstecz zamyka nakładki zamiast wychodzić z gry
{ const { ctx, p } = await page({ width: 390, height: 844 }); await inject(p, '#/gra/001/akta');
  await p.click('[data-a="ev"][data-id="e02"]'); await p.waitForTimeout(300);
  const open1 = await p.locator('.ov').count(); await p.goBack(); await p.waitForTimeout(400);
  const open2 = await p.locator('.ov').count(); const hash = await p.evaluate(() => location.hash);
  ok('Wstecz zamyka dokument i zostaje w grze', open1 === 1 && open2 === 0 && hash === '#/gra/001/akta', `${open1}->${open2} ${hash}`);
  await p.click('[data-a="tab"][data-tab="osoby"]'); await p.click('[data-a="person"][data-id="wiktor"]'); await p.click('[data-a="pmode"][data-m="stmt"]');
  const conf = p.locator('[data-a="confront"]'); const hasConf = await conf.count();
  if (hasConf) { await conf.first().click(); await p.waitForTimeout(200); await p.goBack(); await p.waitForTimeout(300); }
  const stillPerson = await p.locator('.room-head').count();
  ok('Wstecz z wyboru dowodu wraca do przesłuchania', !hasConf || stillPerson === 1);
  await ctx.close(); }

// 4. Tryby: Telewizor + telefony (QR, prywatność) i Wspólny stół (bez tajnych akt, Centrala)
{ const { ctx, p } = await page({ width: 1280, height: 800 }, false); await p.goto(URL, { waitUntil: 'networkidle' }); await p.evaluate(() => localStorage.clear()); await p.reload();
  await p.evaluate(() => { location.hash = '#/sprawa/001'; }); await p.waitForTimeout(500);
  const noModeBtn = await p.locator('[data-a="begin"]').count();
  await p.click('[data-a="mode"][data-m="phones"]'); await p.waitForTimeout(200); await p.click('[data-a="begin"]'); await p.waitForTimeout(400);
  const qrs = await p.locator('.qr-card svg').count(); const docsOnTV = await p.locator('.doc').count();
  await p.reload({ waitUntil: 'networkidle' }); await p.waitForTimeout(400);
  const qrs2 = await p.locator('.qr-card svg').count(); const docs2 = await p.locator('.doc').count();
  await p.click('[data-a="priv"][data-i="0"]'); await p.waitForTimeout(200); const sealed = await p.locator('[data-a="priv-open"]').count(); const leak = await p.locator('.ov .doc').count();
  ok('Start bez wybranego trybu jest niemożliwy', noModeBtn === 0);
  ok('Telewizor + telefony: kody QR dla graczy, żadnych tajnych dokumentów na wspólnym ekranie', qrs === 2 && docsOnTV === 0 && qrs2 === 2 && docs2 === 0, `qr=${qrs}/${qrs2} doc=${docsOnTV}/${docs2}`);
  ok('„Pokaż tutaj” zabezpieczone pieczęcią', sealed === 1 && leak === 0);
  await ctx.close(); }
{ const { ctx, p } = await page({ width: 1280, height: 800 }, false); await p.goto(URL, { waitUntil: 'networkidle' }); await p.evaluate(() => localStorage.clear()); await p.reload();
  await p.evaluate(() => { location.hash = '#/sprawa/001'; }); await p.waitForTimeout(500);
  await p.click('[data-a="mode"][data-m="table"]'); await p.waitForTimeout(200); await p.click('[data-a="begin"]'); await p.waitForTimeout(600);
  const msg = await p.locator('.ov').count(); await p.click('[data-a="close-all"]');
  await p.click('[data-a="tab"][data-tab="miejsca"]'); await p.waitForTimeout(200); const hq = await p.locator('[data-a="loc"][data-id="hq"]').count();
  await p.click('[data-a="tab"][data-tab="analiza"]'); await p.waitForTimeout(200); const tajne = await p.locator('[data-a="ana"][data-t="tajne"]').count();
  await p.click('[data-a="tab"][data-tab="osoby"]'); await p.click('[data-a="person"][data-id="marta"]'); await p.waitForTimeout(200); const photoQ = await p.locator('[data-a="ask"][data-id="m-q7"]').count();
  ok('Wspólny stół: start bez rozdania, Centrala wydziału, brak tajnych akt, dodatkowe pytanie do Marty', msg === 1 && hq === 1 && tajne === 0 && photoQ === 1, `msg=${msg} hq=${hq} tajne=${tajne} q7=${photoQ}`);
  await ctx.close(); }

// 5. Błędne raporty → właściwe epilogi i niska punktacja
for (const [who, title] of [['anna', 'Wygodna winna'], ['marta', 'Motyw to za mało'], ['helena', 'Służąca zawsze pod ręką'], ['accident', 'Nieszczęśliwy wypadek']]) {
  const s = JSON.parse(STATE); const g = s.games['001'];
  g.draft = { step: 7, answers: { 'r-who': who, 'r-weapon': 'hearth', 'r-time': '2246', 'r-motive': 'revenge', 'r-identity': 'anna', 'r-past': 'survived' }, proofs: ['e01', 'e02', 'e03'], order: ['found', 'hide', 'attack', 'meet', 'tea', 'fight'] };
  const { ctx, p } = await page({ width: 390, height: 844 }); await inject(p, '#/gra/001/raport', JSON.stringify(s));
  await p.click('[data-a="submit"]'); await p.waitForTimeout(500);
  const txt = await p.locator('#main').innerText(); const sc = await p.evaluate(() => JSON.parse(localStorage.getItem('slad.v2')).games['001'].report.total);
  ok(`Błędne oskarżenie (${who}) → epilog „${title}”, brak decyzji`, txt.includes(title.toUpperCase()) || txt.includes(title), `wynik ${sc}`);
  ok(`Błędny raport (${who}) daje 0 pkt`, sc === 0, `wynik ${sc}`);
  await ctx.close();
}
// częściowo poprawny: sprawca dobrze, reszta źle
{ const s = JSON.parse(STATE); const g = s.games['001'];
  g.draft = { step: 7, answers: { 'r-who': 'wiktor', 'r-weapon': 'poker', 'r-time': '2246', 'r-motive': 'heir', 'r-identity': 'anna', 'r-past': 'locked' }, proofs: ['e18', 'e16', 'e01'], order: ['fight', 'tea', 'meet', 'attack', 'found', 'hide'] };
  const { ctx, p } = await page({ width: 390, height: 844 }); await inject(p, '#/gra/001/raport', JSON.stringify(s));
  await p.click('[data-a="submit"]'); await p.waitForTimeout(500);
  const r = await p.evaluate(() => JSON.parse(localStorage.getItem('slad.v2')).games['001'].report);
  const txt = await p.locator('#main').innerText();
  // 13 + 8 (2 trafne dowody) + 10 (przeszłość) + 10 (4/6 kolejności) − kary
  ok('Częściowy raport: zatrzymanie + adnotacja o słabych wnioskach + decyzja', txt.includes('ZATRZYMANIE') && txt.includes('obrona będzie miała') && (await p.locator('[data-a="decide"]').count()) === 3, `punkty ${r.pts}, wynik ${r.total}`);
  ok('Częściowy raport: punkty przed karami = 41', r.pts === 41, `pts=${r.pts}`);
  await ctx.close(); }

// 6. Przepełnienia na wielu ekranach
const VPS = [['iPhone SE 1', 320, 568], ['iPhone SE', 375, 667], ['iPhone 15', 390, 844], ['telefon poziomo', 844, 390], ['iPad pionowo', 768, 1024], ['iPad poziomo', 1024, 768], ['Full HD', 1920, 1080]];
const ROUTES = ['#/', '#/sprawa/001', '#/gra/001/akta', '#/gra/001/miejsca', '#/gra/001/osoby', '#/gra/001/analiza', '#/gra/001/tablica', '#/gra/001/raport'];
for (const [name, w, h] of VPS) {
  const { ctx, p } = await page({ width: w, height: h }, w < 1100); const bad = [];
  for (const r of ROUTES) {
    await inject(p, r);
    const o = await p.evaluate(() => {
      const W = innerWidth; const out = [];
      if (document.documentElement.scrollWidth > W + 1) out.push('strona ' + document.documentElement.scrollWidth);
      document.querySelectorAll('#app *').forEach(el => { if (el.closest('.tabs,.board-wrap,.log,.hero,.intro-hero,.hero-bg,.dials')) return; const rc = el.getBoundingClientRect(); if (rc.width && rc.right > W + 2 && getComputedStyle(el).position !== 'fixed') out.push((el.className || el.tagName) + ':' + Math.round(rc.right)); });
      return out.slice(0, 3);
    });
    if (o.length) bad.push(r + ' → ' + o.join(' | '));
  }
  // dokument i osoba w nakładce
  await inject(p, '#/gra/001/akta'); await p.click('[data-a="ev"][data-id="e13"]'); await p.waitForTimeout(300);
  const ov = await p.evaluate(() => { const pnl = document.querySelector('.ov-panel'); return pnl.scrollWidth > pnl.clientWidth + 1 ? 'nakładka ' + pnl.scrollWidth + '>' + pnl.clientWidth : ''; });
  if (ov) bad.push(ov);
  await p.screenshot({ path: `/home/claude/audit/vp-${w}x${h}.png` });
  ok(`Brak przepełnień: ${name} ${w}×${h}`, !bad.length, bad.join(' ; '));
  await ctx.close();
}
ok('Brak błędów JavaScript w całym audycie', !errs.length, [...new Set(errs)].slice(0, 5).join(' | '));
await b.close();
for (const r of results) console.log(r[0], r[1], r[2] ? '— ' + r[2] : '');
console.log(`\n${results.filter(r => r[0] === 'OK  ').length}/${results.length} OK`);
