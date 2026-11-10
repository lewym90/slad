// Pełne przejście sprawy przez interfejs (Playwright + Chrome). Użycie: node tools/e2e.mjs [url] [phone|tablet|desktop]
import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
import fs from 'fs';
const URL = process.argv[2] || 'http://localhost:8800/';
const dev = process.argv[3] || 'phone';
const VP = { phone: { width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }, tablet: { width: 820, height: 1180, isMobile: true, hasTouch: true, deviceScaleFactor: 1 }, desktop: { width: 1440, height: 900, deviceScaleFactor: 1 } }[dev];
const out = `/home/claude/audit/e2e-${dev}`; fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
const ctx = await b.newContext({ viewport: { width: VP.width, height: VP.height }, isMobile: !!VP.isMobile, hasTouch: !!VP.hasTouch, deviceScaleFactor: VP.deviceScaleFactor });
const p = await ctx.newPage(); const errs = [];
p.on('pageerror', e => errs.push('PAGE ' + e.message)); p.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE ' + m.text()); });
p.on('dialog', d => d.accept());
let n = 0; const shot = async (name, full = false) => { await p.waitForTimeout(350); await p.screenshot({ path: `${out}/${String(++n).padStart(2, '0')}-${name}.png`, fullPage: full }); };
const A = async (a, extra = '') => { const el = p.locator(`[data-a="${a}"]${extra}`).first(); await el.scrollIntoViewIfNeeded().catch(() => {}); await el.click(); await p.waitForTimeout(60); };
const closeAll = async () => { while (await p.locator('#overlay-root .ov').count()) { await p.locator('[data-a="close-all"]').first().click(); await p.waitForTimeout(150); } };
const FROM = process.env.FROM_STATE;
if (FROM) { await p.goto(URL, { waitUntil: 'networkidle' }); await p.evaluate(s => localStorage.setItem('slad.v2', s), fs.readFileSync(FROM, 'utf8')); await p.goto(URL + '#/gra/001/akta', { waitUntil: 'networkidle' }); await p.reload({ waitUntil: 'networkidle' }); }
else { await p.goto(URL, { waitUntil: 'networkidle' }); await shot('home'); await shot('home-full', true); }
const C = await p.evaluate(() => fetch('cases/001.json').then(r => r.json()));
const state = () => p.evaluate(() => JSON.parse(localStorage.getItem('slad.v2')).games['001']);
if (!FROM) {
await A('open-case', '[data-id="001"]'); await shot('intro'); await shot('intro-full', true);
await A('count', '[data-n="3"]'); await p.fill('#pn0', 'Kasia'); await p.fill('#pn1', 'Tomek'); await p.fill('#pn2', 'Ola');
await A('begin');
for (let i = 0; i < 3; i++) { if (i === 0) await shot('pass'); await A('dist-open'); if (i === 0) await shot('private'); await A('dist-next'); }
await p.waitForTimeout(400); await shot('start-msg'); await closeAll(); await shot('files');
// ujawnij wszystkie tajne akta
await A('tab', '[data-tab="analiza"]'); await A('ana', '[data-t="tajne"]'); await shot('analysis-private');
for (let i = 0; i < 3; i++) { await A('priv', `[data-i="${i}"]`); await A('priv-open'); if (i === 0) await shot('priv-open'); while (await p.locator('[data-a="share"]').count()) await A('share'); await closeAll(); }
const solvePuzzle = async pz => {
  await A('tab', '[data-tab="analiza"]'); await A('ana', '[data-t="zagadki"]');
  await A('puzzle', `[data-id="${pz.id}"]`);
  if (pz.input === 'text') { await p.fill('#pzin', pz.answers[0]); }
  else { const d = pz.answers[0].replace(/\D/g, ''); for (let i = 0; i < 4; i++) { for (let k = 0; k < +d[i]; k++) await p.locator(`[data-a="dial"][data-id="${pz.id}"][data-i="${i}"][data-d="1"]`).click(); } }
  if (pz.id === 'p-time') await shot('puzzle-dials');
  await A('solve', `[data-id="${pz.id}"]`); await shot('puzzle-' + pz.id); await closeAll();
};
// pętla śledztwa
for (let round = 0; round < 5; round++) {
  await A('tab', '[data-tab="miejsca"]'); if (round === 0) await shot('places');
  for (const l of C.locations) {
    await A('loc', `[data-id="${l.id}"]`); if (round === 0 && l.id === 'study') await shot('location-study');
    while (await p.locator('[data-a="search"]').count()) await A('search');
    if (round === 0 && l.id === 'study') await shot('location-study-searched');
    await closeAll();
  }
  await A('tab', '[data-tab="osoby"]'); if (round === 0) await shot('people');
  for (const per of C.people) {
    await A('person', `[data-id="${per.id}"]`);
    while (await p.locator('[data-a="ask"]:not([disabled])').count()) await A('ask', ':not([disabled])');
    if (round === 0 && per.id === 'wiktor') await shot('interrogation');
    await A('pmode', `[data-m="stmt"]`);
    const g = await state();
    for (const s of per.statements) {
      if (s.truth || !g.claims.includes(s.id) || g.broken.includes(s.id)) continue;
      const evid = s.contradicts.find(x => g.found.includes(x) || g.shared.includes(x)); if (!evid) continue;
      await A('confront', `[data-id="${s.id}"]`); if (s.id === 'w-l2') await shot('confront-pick');
      await A('confront-with', `[data-s="${s.id}"][data-id="${evid}"]`); await p.waitForTimeout(250);
      if (s.id === 'h-l2') await shot('confront-break');
      await A('pmode', `[data-m="stmt"]`);
    }
    await closeAll();
  }
  const g = await state();
  for (const pz of C.puzzles) { if (g.puzzles[pz.id]?.solved) continue; if (pz.requires.every(r => g.found.includes(r) || g.shared.includes(r))) await solvePuzzle(pz); }
}
fs.writeFileSync(`/tmp/state-${dev}.json`, await p.evaluate(() => localStorage.getItem('slad.v2')));
}
const g = await state();
const allEv = C.evidence.map(e => e.id); const missing = allEv.filter(id => !g.found.includes(id) && !g.shared.includes(id));
console.log(dev, 'actions', g.actions, 'par', C.par, 'broken', g.broken.length, 'missing evidence', missing.join(',') || 'none', 'puzzles', Object.keys(g.puzzles).filter(k => g.puzzles[k].solved).length);
// zrzuty sekcji
await A('tab', '[data-tab="akta"]'); await shot('files-full'); await A('ev', '[data-id="e13"]'); await shot('doc-watch'); await A('pin', '[data-key="ev:e13"]'); await closeAll();
await A('ev', '[data-id="e11"]'); await shot('doc-diary'); await A('pin', '[data-key="ev:e11"]'); await closeAll();
await A('tab', '[data-tab="osoby"]'); await A('person', '[data-id="wiktor"]'); await A('pin', '[data-key="p:wiktor"]'); await closeAll();
await A('tab', '[data-tab="analiza"]'); await A('ana', '[data-t="czas"]'); await shot('timeline'); await shot('timeline-full', true);
await A('tab', '[data-tab="tablica"]'); await A('link-mode');
await p.locator('.bitem').nth(0).click(); await p.locator('.bitem').nth(2).click(); await shot('board');
// raport
await A('tab', '[data-tab="analiza"]'); await A('tab', '[data-tab="raport"]'); await shot('report-1');
for (const q of C.report.questions) {
  if (q.type === 'single') { await A('ropt', `[data-q="${q.id}"][data-k="${q.correct}"]`); if (q.proof) { for (const id of q.proof.valid.slice(0, q.proof.count)) await A('rproof', `[data-id="${id}"]`); await shot('report-proof'); } }
  else { const st = await state(); let order = st.draft.order.slice();
    for (let target = 0; target < q.correct.length; target++) { let i = order.indexOf(q.correct[target]); while (i > target) { await p.locator(`[data-a="rord"][data-i="${i}"][data-d="-1"]`).click(); order = (await state()).draft.order; i--; } }
    await shot('report-order'); }
  await A('rstep', '[data-d="1"]');
}
await shot('report-sign'); await A('submit'); await p.waitForTimeout(500); await shot('result');
await A('decide', '[data-id="mercy"]'); await shot('result-decided', true);
const fin = await state(); console.log(dev, 'SCORE', fin.report.total, fin.report.rank, JSON.stringify(fin.report.pen.filter(x => x[1])));
console.log('ERRORS', errs.length ? errs.join('\n') : 'none');
await b.close();
