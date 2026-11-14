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
let BT = 0, EVN = 0; const dismissBt = async () => { let k = 0; while (await p.locator('.bt').count() && k++ < 5) { BT++; if (BT <= 3) await shot('breakthrough-' + BT); await p.locator('.bt .btn[data-a="bt-close"]').click({ timeout: 5000 }).catch(() => {}); await p.waitForTimeout(250); }
  k = 0; while (await p.locator('#overlay-root .clock-ev').count() && k++ < 4) { EVN++; if (EVN <= 2) await shot('clock-event-' + EVN); await p.locator('#overlay-root .ov-body > .btn[data-a="close"]').last().click({ timeout: 4000 }).catch(() => {}); await p.waitForTimeout(250); } };
const A = async (a, extra = '') => { if (await p.locator('#overlay-root .clock-ev').count() === 0 && C0clock) await p.waitForTimeout(0); await dismissBt(); const el = p.locator(`[data-a="${a}"]${extra}`).first(); await el.scrollIntoViewIfNeeded().catch(() => {}); try { await el.click({ timeout: 4000 }); } catch (e) { await p.waitForTimeout(800); await dismissBt(); await el.scrollIntoViewIfNeeded().catch(() => {}); await el.click(); } await p.waitForTimeout(60); };
const closeAll = async () => { await dismissBt(); if (await p.locator('#zoom').count()) { await p.locator('#zoom [data-a="close"]').click(); await p.waitForTimeout(200); console.log('zoom closed', !(await p.locator('#zoom').count())); } while (await p.locator('#overlay-root .ov').count()) { await p.locator('[data-a="close-all"]').first().click({ timeout: 4000 }).catch(() => {}); await p.waitForTimeout(150); await dismissBt(); } };
let C0clock = false;
const FROM = process.env.FROM_STATE;
if (FROM) { await p.goto(URL, { waitUntil: 'networkidle' }); await p.evaluate(s => localStorage.setItem('slad.v2', s), fs.readFileSync(FROM, 'utf8')); await p.goto(URL + `#/gra/${CID}/akta`, { waitUntil: 'networkidle' }); await p.reload({ waitUntil: 'networkidle' }); }
else { await p.goto(URL, { waitUntil: 'networkidle' }); await shot('home'); await shot('home-full', true); }
const C = await p.evaluate(cid => fetch(`cases/${cid}.json`).then(r => r.json()), CID); C0clock = !!C.clock;
const hasT = (g, t) => t.startsWith('lie:') ? g.broken.includes(t.slice(4)) : t.startsWith('st:') ? g.claims.includes(t.slice(3)) : t.startsWith('show:') ? (g.showsDone || []).includes(t.slice(5)) : (g.found.includes(t) || g.shared.includes(t) || !!(g.puzzles[t] && g.puzzles[t].solved) || g.spots.includes(t) || g.asked.includes(t));
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
  await A('qr-done'); await p.waitForTimeout(400); if (await p.locator('[data-a="unlock-ok"]').count()) { await p.locator('[data-a="unlock-ok"]').click(); await p.waitForTimeout(500); console.log('unlock screen ok'); } await closeAll();
  await A('tab', '[data-tab="analiza"]'); await A('ana', '[data-t="tajne"]'); await shot('analysis-private');
  for (const [k, code] of codes.entries()) { await A('reveal'); await p.fill('#revcode', code); if (k === 0) await shot('reveal'); await A('reveal-go'); await p.waitForTimeout(300); await closeAll(); }
  await A('reveal'); await p.fill('#revcode', 'ZZZZ'); await A('reveal-go'); const bad = await p.locator('.result-bad').count(); console.log('wrong code rejected', bad === 1); await closeAll();
} else {
  await p.waitForTimeout(400); if (await p.locator('[data-a="unlock-ok"]').count()) { await shot('unlocks'); await p.locator('[data-a="unlock-ok"]').click(); await p.waitForTimeout(500); console.log('unlock screen ok'); }
  await shot('start-msg'); await closeAll(); await shot('files');
}
// zdolność roli + powiększenie zdjęcia
await A('tab', '[data-tab="analiza"]'); await A('ana', '[data-t="zespol"]'); await A('power'); await shot('power-armed'); console.log('armed', (await state()).armed, 'used', JSON.stringify((await state()).used));
await A('tab', '[data-tab="akta"]'); await A('ev'); await p.waitForTimeout(200);
if (await p.locator('[data-a="pzoom"]').count()) { await A('pzoom'); await p.waitForTimeout(300); await shot('zoom'); console.log('zoom open', await p.locator('#zoom').count()); }
await closeAll();
const solvePuzzle = async pz => {
  await A('tab', '[data-tab="analiza"]'); await A('ana', '[data-t="zagadki"]');
  await A('puzzle', `[data-id="${pz.id}"]`);
  if (pz.input === 'grid') { const sol = pz.answers[0]; for (const r of pz.grid.rows) for (const cl of pz.grid.cols) await p.selectOption(`[data-gc="${pz.id}|${r.id}|${cl.id}"]`, sol[r.id][cl.id]); }
  else if (pz.input === 'torn') {
    await p.waitForTimeout(300); const t = await p.evaluate(id => window.__tornTest(id), pz.id);
    if (t) { await p.mouse.move(t.from[0], t.from[1]); await p.mouse.down(); await p.mouse.move((t.from[0] + t.to[0]) / 2, (t.from[1] + t.to[1]) / 2, { steps: 6 }); await p.mouse.move(t.to[0], t.to[1], { steps: 6 }); await p.mouse.up(); await p.waitForTimeout(250);
      const st = await state(); console.log('torn drag placed', JSON.stringify((st.puzzles[pz.id] || {}).placed || [])); }
    await shot('puzzle-torn-' + pz.id); await p.evaluate(id => window.__tornTest(id, true), pz.id); await p.waitForTimeout(300); await shot('puzzle-' + pz.id); await closeAll(); return;
  }
  else if (pz.input === 'text') { await p.fill('#pzin', pz.answers[0]); }
  else if (pz.input === 'number') { const [lo, hi] = pz.answers[0].split('-').map(Number); await p.fill('#pzin', String(Math.round((lo + (hi || lo)) / 2))); }
  else { const d = pz.answers[0].replace(/\D/g, ''); for (let i = 0; i < 4; i++) { for (let k = 0; k < +d[i]; k++) await p.locator(`[data-a="dial"][data-id="${pz.id}"][data-i="${i}"][data-d="1"]`).click(); } }
  await shot('puzzle-input-' + pz.id);
  await A('solve', `[data-id="${pz.id}"]`); await shot('puzzle-' + pz.id); await closeAll();
};
// pętla śledztwa
const goTo = async at => { if (!C.map || !at) return; const g0 = await state(); if ((g0.pos || C.map.start) === at) return; await closeAll(); const m = await p.evaluate(id => window.__travelTest(id), at); await p.waitForTimeout(700); await dismissBt(); await closeAll(); if (!globalThis.travelLog) globalThis.travelLog = []; globalThis.travelLog.push(at + ':' + m); };
if (C.clock) { await A('clock'); await shot('clock'); await closeAll(); }
for (let round = 0; round < 5; round++) {
  if (C.clock && round === 2) { const t = await p.evaluate(() => window.__waitAll()); await p.waitForTimeout(700); await dismissBt(); if (!globalThis.evShot) { globalThis.evShot = true; await shot('clock-events'); } await closeAll(); console.log('waited until', t); }
  await A('tab', '[data-tab="miejsca"]'); if (round === 0) { await shot('places'); if (C.map) await shot('places-full', true); }
  for (const l of (MODE === 'table' ? [...C.locations, ...C.tableMode.locations] : C.locations)) {
    if (C.map && round > 0 && !(await p.evaluate(lid => { const { c, g } = ctx(); const l = c.loc[lid]; return l.spots.some(s => spotState(c, g, s) === 'open'); }, l.id))) continue;
    await goTo(l.at); await A('tab', '[data-tab="miejsca"]');
    await A('loc', `.loc[data-id="${l.id}"]`); if (round === 0 && l.id === 'study') await shot('location-study');
    while (await p.locator('[data-a="search"]').count()) await A('search');
    if (l.search) { await A('look-open', `[data-id="${l.id}"]`); await p.waitForTimeout(300); if (!globalThis.lookShot) { globalThis.lookShot = true; await shot('look'); }
      const miss = await p.evaluate(() => { const { c, g } = ctx(); return JSON.stringify(lookTap(c, g, c.loc[route().id ? Object.keys(c.loc).find(k => c.loc[k].search) : ''], 0.001, 0.001, 3)); }); if (round === 0) console.log('look miss', miss);
      const low = await p.evaluate(lid => { const { c, g } = ctx(); const l = c.loc[lid]; const [x, y] = Object.values(l.search.spots)[0]; return JSON.stringify(lookTap(c, g, l, x, y, 1)); }, l.id); if (round === 0) console.log('look no-zoom', low);
      for (const sid of Object.keys(l.search.spots)) { const r = await p.evaluate(([lid, s]) => JSON.stringify(window.__lookTest(lid, s)), [l.id, sid]); if (r.includes('hit')) console.log('look hit', sid); }
      await closeAll(); }
    if (round === 0 && l.id === 'study') await shot('location-study-searched');
    await closeAll();
  }
  for (const e of C.evidence.filter(e => e.audio)) { const g = await state(); if (!hasT(g, e.id) || e.audio.marks.every(m => (g.marks || []).includes(m.id))) continue;
    await A('tab', '[data-tab="akta"]'); await A('ev', `[data-id="${e.id}"]`); await A('listen', `[data-id="${e.id}"]`); await p.waitForTimeout(400); await shot('listen-' + e.id);
    const miss = await p.evaluate(id => JSON.stringify(listenPick(ctx().c, ctx().g, id, 'Kaszel', 3.0)), e.id); console.log('listen miss', miss);
    for (const m of e.audio.marks) { const r = await p.evaluate(([id, mid]) => JSON.stringify(window.__listenTest(id, mid)), [e.id, m.id]); console.log('listen', m.id, r.includes('hit')); }
    await A('lplay'); await p.waitForTimeout(1200); await p.evaluate(() => { renderOv(); }); await p.waitForTimeout(300); await shot('listen-done-' + e.id); await closeAll(); }
  await A('tab', '[data-tab="osoby"]'); if (round === 0) await shot('people');
  for (const per of C.people) {
    if (C.map && !(await p.evaluate(pid => { const { c, g } = ctx(); const P = c.person[pid]; const hasT = t => has(g, c, t);
      return availableQs(c, g, P).some(q => !g.asked.includes(q.id)) || (P.shows || []).some(x => !(g.showsDone || []).includes(x.id) && hasT(x.ev) && (x.requires || []).every(hasT))
        || P.statements.some(s => !s.truth && g.claims.includes(s.id) && !g.broken.includes(s.id) && (s.contradicts || []).some(hasT)); }, per.id))) continue;
    await goTo(per.at); await A('tab', '[data-tab="osoby"]');
    await A('person', `[data-id="${per.id}"]`);
    while (await p.locator('[data-a="ask"]:not([disabled])').count()) await A('ask', ':not([disabled])');
    if (round === 0 && per.id === 'wiktor') await shot('interrogation');
    if (per.showDefault) for (const x of per.shows || []) { const g = await state(); if ((g.showsDone || []).includes(x.id)) continue; if (!(hasT(g, x.ev) && (x.requires || []).every(t => hasT(g, t)))) continue;
      await A('pmode', '[data-m="show"]'); if (!globalThis.showShot) { globalThis.showShot = true; await shot('show-tab'); } await A('show', `[data-p="${per.id}"][data-id="${x.ev}"]`); await p.waitForTimeout(250); if (!(await state()).showsDone.includes(x.id)) errs.push('show failed ' + x.id); }
    await A('pmode', `[data-m="stmt"]`);
    const g = await state();
    for (const s of per.statements) {
      if (s.truth || !g.claims.includes(s.id) || g.broken.includes(s.id)) continue;
      const evid = s.contradicts.find(x => x.startsWith('st:') ? g.claims.includes(x.slice(3)) : (g.found.includes(x) || g.shared.includes(x))); if (!evid) continue;
      await A('confront', `[data-id="${s.id}"]`); if (s.id === 'w-l2') await shot('confront-pick');
      if (!globalThis.cfChecked && !evid.startsWith('st:')) { globalThis.cfChecked = true;
        const vis = () => p.evaluate(() => [...document.querySelectorAll('.cf-item')].filter(x => !x.hidden && x.offsetParent).length);
        const all = await vis(); await A('cf-tab', '[data-k="doc"]'); const d = await vis(); await A('cf-tab', '[data-k="all"]'); const back = await vis();
        console.log('confront ui: all', all, 'docs', d, 'sticky', await p.locator('.cf-sticky').count()); if (!(d >= 1 && d < all && back === all)) errs.push('confront tab filter');
        await A('cf-preview', `[data-id="${evid}"]`); await shot('confront-preview'); await A('confront-with', `[data-s="${s.id}"][data-id="${evid}"]`); await p.waitForTimeout(250);
      } else await A('confront-with', `[data-s="${s.id}"][data-id="${evid}"]`); await p.waitForTimeout(250);
      if (s.id === 'h-l2') await shot('confront-break');
      await A('pmode', `[data-m="stmt"]`);
    }
    await closeAll();
  }
  for (let rep = 0; rep < 2; rep++) { const g = await state();
  for (const pz of C.puzzles) { if ((await state()).puzzles[pz.id]?.solved) continue; if (pz.requires.every(r => hasT(g, r))) await solvePuzzle(pz); } }
  if (C.db) { if (!globalThis.baseOf) globalThis.baseOf = await p.evaluate(() => loadDB().then(d => d.baseOf));
    await A('tab', '[data-tab="bazy"]');
    if (round === 0) { await shot('bazy');
      await A('db-base', '[data-b="pojazdy"]'); await p.fill('.term-form input[name="nr"]', 'ZS7PR04'); await A('db-search'); const none = await p.locator('.term-none').count();
      await A('db-base', '[data-b="osoby"]'); await p.fill('.term-form input[name="nazwisko"]', 'Kowalski'); await A('db-search'); const many = await p.locator('.term-row').count() + await p.locator('.term-none').count();
      await p.fill('.term-form input[name="nazwisko"]', 'kowalski'); await p.fill('.term-form input[name="imie"]', 'jan'); await A('db-search'); const jan = await p.locator('.term-row').count(); const janOk = await p.$$eval('.term-row b', els => els.every(e => /^Kowalski Jan/.test(e.textContent)));
      await shot('bazy-results'); console.log('db: no-space plate rejected', none === 1, '| Kowalski results', many, '| Jan Kowalski', jan, janOk); if (none !== 1 || !janOk) errs.push('db search semantics'); }
    for (const a of C.db.attach) { const g = await state(); if (g.found.includes(a.ev)) continue; const pt = a.paths.find(x => x.from.every(t => hasT(g, t))); if (!pt) continue;
      const base = globalThis.baseOf[a.rec]; await A('db-base', `[data-b="${base}"]`);
      for (const inp of await p.$$('.term-form input')) await inp.fill('');
      for (const [k, v] of Object.entries(pt.q)) await p.fill(`.term-form input[name="${k}"]`, v);
      await A('db-search'); await A('db-rec', `[data-id="${a.rec}"]`); if (!globalThis.recShot) { globalThis.recShot = true; await shot('db-record'); } await A('db-attach', `[data-id="${a.rec}"]`); await p.waitForTimeout(200); await closeAll();
      if (!(await state()).found.includes(a.ev)) errs.push('attach failed ' + a.ev); } }
}
fs.writeFileSync(`/tmp/state-${CID}-${dev}-${MODE}.json`, await p.evaluate(() => localStorage.getItem('slad.v2')));
}
const g = await state();
const allEv = C.evidence.map(e => e.id); const missing = allEv.filter(id => !g.found.includes(id) && !g.shared.includes(id));
if (C.clock) console.log('clock', g.mins, 'min, travel', (globalThis.travelLog || []).join(' '));
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
await A('tab', '[data-tab="analiza"]'); await A('ana', '[data-t="podejrzani"]'); await p.locator('[data-mx]').first().fill('motyw: zemsta'); await p.waitForTimeout(500); await shot('suspects');
console.log('matrix saved', JSON.stringify((await state()).matrix).includes('zemsta'));
await A('ana', '[data-t="zespol"]'); await shot('team');
if (MODE === 'phones') { await A('to-report'); await shot('vote-ask'); await p.locator('#overlay-root [data-a="vote"]').click(); await p.waitForTimeout(200); await shot('vote-0'); await A('vote-go'); await p.waitForTimeout(3300); await shot('vote-2'); await A('vote-res', '[data-v="zgodni"]'); await p.waitForTimeout(500); }
else await A('to-report');
await p.waitForTimeout(300); await shot('report-1');
for (const q of C.report.questions) {
  if (q.type === 'single') { await A('ropt', `[data-q="${q.id}"][data-k="${q.correct}"]`); if (q.proof) { for (const id of q.proof.valid.slice(0, q.proof.count)) await A('rproof', `[data-id="${id}"]`); await shot('report-proof'); } }
  else if (q.type === 'multi') { for (const k of q.correct) await A('rmulti', `[data-q="${q.id}"][data-k="${k}"]`); }
  else { const st = await state(); let order = st.draft.order.slice();
    for (let target = 0; target < q.correct.length; target++) { let i = order.indexOf(q.correct[target]); while (i > target) { await p.locator(`[data-a="rord"][data-i="${i}"][data-d="-1"]`).click(); order = (await state()).draft.order; i--; } }
    await shot('report-order'); }
  await A('rstep', '[data-d="1"]');
}
await shot('report-sign'); await A('submit'); await p.waitForTimeout(500); await shot('result');
await A('decide', `[data-id="${C.endings.correct.decision.options[1].id}"]`); await shot('result-decided', true);
if (await p.locator('.bt').count()) console.log('breakthrough left open');
await A('chronicle'); await p.waitForTimeout(400); await shot('chronicle', true); console.log('chronicle entries', await p.locator('.chron-item').count());
const fin = await state(); console.log(dev, 'SCORE', fin.report.total, fin.report.rank, JSON.stringify(fin.report.pen.filter(x => x[1])));
console.log('breakthroughs seen', BT, '/', (C.breakthroughs || []).length);
console.log('ERRORS', errs.length ? errs.join('\n') : 'none');
await b.close();
