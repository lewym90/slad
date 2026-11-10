// Pełne przejście sprawy przez interfejs (Playwright + Chrome). Użycie: node tools/e2e.mjs [url] [phone|tablet|desktop]
import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
import fs from 'fs';
const URL = process.argv[2] || 'http://localhost:8800/';
const dev = process.argv[3] || 'phone';
const MODE = process.env.MODE || 'table';
const CID = process.env.CASE || '001';
const VP = { phone: { width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }, tablet: { width: 820, height: 1180, isMobile: true, hasTouch: true, deviceScaleFactor: 1 }, desktop: { width: 1440, height: 900, deviceScaleFactor: 1 } }[dev];
const out = `/home/claude/audit/e2e-${CID}-${dev}-${MODE}`; fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
const ctx = await b.newContext({ viewport: { width: VP.width, height: VP.height }, isMobile: !!VP.isMobile, hasTouch: !!VP.hasTouch, deviceScaleFactor: VP.deviceScaleFactor });
const p = await ctx.newPage(); const errs = [];
p.on('pageerror', e => errs.push('PAGE ' + e.message)); p.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE ' + m.text()); });
p.on('dialog', d => d.accept());
let n = 0; const shot = async (name, full = false) => { await p.waitForTimeout(350); await p.screenshot({ path: `${out}/${String(++n).padStart(2, '0')}-${name}.png`, fullPage: full }); };
const A = async (a, extra = '') => { const el = p.locator(`[data-a="${a}"]${extra}`).first(); await el.scrollIntoViewIfNeeded().catch(() => {}); await el.click(); await p.waitForTimeout(60); };
const closeAll = async () => { while (await p.locator('#overlay-root .ov').count()) { await p.locator('[data-a="close-all"]').first().click(); await p.waitForTimeout(150); } };
const FROM = process.env.FROM_STATE;
if (FROM) { await p.goto(URL, { waitUntil: 'networkidle' }); await p.evaluate(s => localStorage.setItem('slad.v2', s), fs.readFileSync(FROM, 'utf8')); await p.goto(URL + `#/gra/${CID}/akta`, { waitUntil: 'networkidle' }); await p.reload({ waitUntil: 'networkidle' }); }
else { await p.goto(URL, { waitUntil: 'networkidle' }); await shot('home'); await shot('home-full', true); }
const C = await p.evaluate(cid => fetch(`cases/${cid}.json`).then(r => r.json()), CID);
const state = async () => { await p.evaluate(c => { window.__cid = c; }, CID); return p.evaluate(() => JSON.parse(localStorage.getItem('slad.v2')).games[window.__cid]); };
if (!FROM) {
await A('open-case', `[data-id="${CID}"]`); await shot('intro'); await shot('intro-full', true);
await A('mode', `[data-m="${MODE}"]`); await shot('modes'); await shot('modes-full', true);
await A('count', '[data-n="3"]'); await p.fill('#pn0', 'Kasia'); await p.fill('#pn1', 'Tomek'); await p.fill('#pn2', 'Ola');
await A('begin');
await p.waitForTimeout(500);
{ let k = 0; while (await p.locator('.g-nav .btn:not(.ghost)[data-a="guide-go"]').count() && k < 15) { await shot(`guide-${k}`); await p.locator('.g-nav .btn:not(.ghost)[data-a="guide-go"]').click(); await p.waitForTimeout(120); k++; }
  await shot(`guide-${k}`); console.log('guide cards', k + 1); await p.locator('.g-nav [data-a="guide-end"]').click(); await p.waitForTimeout(300); }
if (MODE === 'phones') {
  await p.waitForTimeout(400); await shot('qr-screen'); await shot('qr-screen-full', true);
  const nQR = await p.locator('.qr-card svg').count(); console.log('QR codes', nQR);
  const urls = await p.evaluate(cid => [0, 1, 2].map(i => folderURL(caseFor(cid), G(cid), i)), CID);
  const phone = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  const codes = [];
  for (const [i, u] of urls.entries()) { const pp = await phone.newPage(); pp.on('pageerror', e => errs.push('PHONE ' + e.message)); await pp.goto(u, { waitUntil: 'networkidle' }); await pp.waitForTimeout(400);
    if (i === 0) await pp.screenshot({ path: `${out}/phone-folder.png`, fullPage: false });
    codes.push(...await pp.$$eval('.code-tag b', els => els.map(e => e.textContent.trim()))); await pp.close(); }
  console.log('folder codes', codes.join(','));
  await A('qr-done'); await p.waitForTimeout(400); await closeAll();
  await A('tab', '[data-tab="analiza"]'); await A('ana', '[data-t="tajne"]'); await shot('analysis-private');
  for (const [k, code] of codes.entries()) { await A('reveal'); await p.fill('#revcode', code); if (k === 0) await shot('reveal'); await A('reveal-go'); await p.waitForTimeout(300); await closeAll(); }
  await A('reveal'); await p.fill('#revcode', 'ZZZZ'); await A('reveal-go'); const bad = await p.locator('.result-bad').count(); console.log('wrong code rejected', bad === 1); await closeAll();
} else {
  await p.waitForTimeout(400); await shot('start-msg'); await closeAll(); await shot('files');
}
const solvePuzzle = async pz => {
  await A('tab', '[data-tab="analiza"]'); await A('ana', '[data-t="zagadki"]');
  await A('puzzle', `[data-id="${pz.id}"]`);
  if (pz.input === 'text') { await p.fill('#pzin', pz.answers[0]); }
  else if (pz.input === 'number') { const [lo, hi] = pz.answers[0].split('-').map(Number); await p.fill('#pzin', String(Math.round((lo + (hi || lo)) / 2))); }
  else { const d = pz.answers[0].replace(/\D/g, ''); for (let i = 0; i < 4; i++) { for (let k = 0; k < +d[i]; k++) await p.locator(`[data-a="dial"][data-id="${pz.id}"][data-i="${i}"][data-d="1"]`).click(); } }
  await shot('puzzle-input-' + pz.id);
  await A('solve', `[data-id="${pz.id}"]`); await shot('puzzle-' + pz.id); await closeAll();
};
// pętla śledztwa
for (let round = 0; round < 5; round++) {
  await A('tab', '[data-tab="miejsca"]'); if (round === 0) await shot('places');
  for (const l of (MODE === 'table' ? [...C.locations, ...C.tableMode.locations] : C.locations)) {
    await A('loc', `.loc[data-id="${l.id}"]`); if (round === 0 && l.id === 'study') await shot('location-study');
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
fs.writeFileSync(`/tmp/state-${CID}-${dev}-${MODE}.json`, await p.evaluate(() => localStorage.getItem('slad.v2')));
}
const g = await state();
const allEv = C.evidence.map(e => e.id); const missing = allEv.filter(id => !g.found.includes(id) && !g.shared.includes(id));
console.log(dev, 'actions', g.actions, 'par', C.par, 'broken', g.broken.length, 'missing evidence', missing.join(',') || 'none', 'puzzles', Object.keys(g.puzzles).filter(k => g.puzzles[k].solved).length);
// zrzuty sekcji
const evA = C.evidence[12].id, evB = C.evidence[10].id, perA = C.people[2].id;
await A('tab', '[data-tab="akta"]'); await shot('files-full'); await A('ev', `[data-id="${evA}"]`); await shot('doc-a'); await A('pin', `[data-key="ev:${evA}"]`); await closeAll();
await A('ev', `[data-id="${evB}"]`); await shot('doc-b'); await A('pin', `[data-key="ev:${evB}"]`); await closeAll();
await A('tab', '[data-tab="osoby"]'); await A('person', `[data-id="${perA}"]`); await A('pin', `[data-key="p:${perA}"]`); await closeAll();
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
await A('decide', `[data-id="${C.endings.correct.decision.options[1].id}"]`); await shot('result-decided', true);
const fin = await state(); console.log(dev, 'SCORE', fin.report.total, fin.report.rank, JSON.stringify(fin.report.pen.filter(x => x[1])));
console.log('ERRORS', errs.length ? errs.join('\n') : 'none');
await b.close();
