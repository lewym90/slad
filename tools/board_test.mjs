// Test tablicy śledczej (karty z treścią, fragmenty, układanie, migracja starych zapisów, prywatność).
// Użycie: node tools/board_test.mjs [url] [phone|tablet|desktop]   (CASE=001|002|003, MODE=table|phones)
import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
import fs from 'fs';
const URL = process.argv[2] || 'http://localhost:8800/';
const dev = process.argv[3] || 'phone';
const MODE = process.env.MODE || 'table';
const CID = process.env.CASE || '001';
const VP = { phone: { width: 390, height: 844, isMobile: true, hasTouch: true }, tablet: { width: 820, height: 1180, isMobile: true, hasTouch: true }, desktop: { width: 1440, height: 900 } }[dev];
const out = `/home/claude/audit/board-${CID}-${dev}-${MODE}`; fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
const ctx = await b.newContext({ viewport: { width: VP.width, height: VP.height }, isMobile: !!VP.isMobile, hasTouch: !!VP.hasTouch });
const p = await ctx.newPage(); const errs = []; const fails = [];
p.on('pageerror', e => errs.push('PAGE ' + e.message)); p.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE ' + m.text()); });
p.on('dialog', d => d.accept(d.type() === 'prompt' ? 'Zmieniona notatka' : undefined));
const ok = (cond, msg) => { console.log((cond ? 'OK   ' : 'FAIL ') + msg); if (!cond) fails.push(msg); };
let n = 0; const shot = async (name) => { await p.waitForTimeout(300); await p.screenshot({ path: `${out}/${String(++n).padStart(2, '0')}-${name}.png` }); };
const A = async (a, extra = '') => { const el = p.locator(`[data-a="${a}"]${extra}`).first(); await el.scrollIntoViewIfNeeded().catch(() => {}); await el.click({ timeout: 5000 }); await p.waitForTimeout(150); };
const state = () => p.evaluate(cid => JSON.parse(localStorage.getItem('slad.v2')).games[cid], CID);
const closeAll = async () => { let k = 0; while (await p.locator('#overlay-root [data-a="close-all"]').count() && k++ < 4) { await p.locator('#overlay-root [data-a="close-all"]').first().click(); await p.waitForTimeout(150); } };

await p.goto(URL, { waitUntil: 'networkidle' });
const C = await p.evaluate(cid => fetch(`cases/${cid}.json`).then(r => r.json()), CID);
await A('open-case', `[data-id="${CID}"]`); await A('mode', `[data-m="${MODE}"]`); await A('count', '[data-n="3"]');
await p.fill('#pn0', 'Kasia'); await p.fill('#pn1', 'Tomek'); await p.fill('#pn2', 'Ola'); await A('begin'); await p.waitForTimeout(500);
{ let k = 0; while (await p.locator('.g-nav .btn:not(.ghost)[data-a="guide-go"]').count() && k++ < 15) { await p.locator('.g-nav .btn:not(.ghost)[data-a="guide-go"]').click(); await p.waitForTimeout(100); } await p.locator('.g-nav [data-a="guide-end"]').click(); await p.waitForTimeout(300); }
if (MODE === 'phones') { await p.waitForTimeout(400); await A('qr-done'); await p.waitForTimeout(400); }
await p.waitForTimeout(400); await closeAll();

// dowody początkowe (widoczne od startu)
const starts = C.evidence.filter(e => e.start && !e.private);
ok(starts.length >= 2, `są co najmniej 2 dowody początkowe (${starts.length})`);
await A('tab', '[data-tab="akta"]');
// 1) fragmenty w widoku akt, a brak pinezek w widoku teczki (compact)
const e0 = starts[0];
await A('ev', `[data-id="${e0.id}"]`);
const nPins = await p.locator('#overlay-root .fpin').count();
const expected = e0.body.reduce((s, x) => s + (typeof x === 'string' ? 1 : x.kv ? x.kv.length : x.log ? x.log.length : (x.quote || x.note) ? 1 : 0), 0);
ok(nPins === expected && nPins > 0, `dokument ${e0.id}: pinezek przy fragmentach ${nPins} = fragmentów ${expected}`);
await shot('doc-with-fragment-pins');
await p.locator('#overlay-root .fpin').first().click(); await p.waitForTimeout(200);
await p.locator('#overlay-root .fpin').first().click(); await p.waitForTimeout(200); // drugi raz: „Już na tablicy”
let st = await state();
ok(st.board.items.filter(x => x.key.startsWith('f:')).length === 1, 'ten sam fragment przypięty tylko raz');
if (nPins > 1) { await p.locator('#overlay-root .fpin').nth(nPins - 1).click(); await p.waitForTimeout(200); }
await A('pin', `[data-key="ev:${e0.id}"]`); await closeAll();
for (const e of starts.slice(1, 4)) { await A('ev', `[data-id="${e.id}"]`); await A('pin', `[data-key="ev:${e.id}"]`); await closeAll(); }
await A('tab', '[data-tab="osoby"]'); const per = C.people[0].id; await A('person', `[data-id="${per}"]`); await A('pin', `[data-key="p:${per}"]`); await closeAll();
await A('tab', '[data-tab="tablica"]'); await p.waitForTimeout(400);
st = await state();
const nEv = st.board.items.filter(x => x.key.startsWith('ev:')).length, nF = st.board.items.filter(x => x.key.startsWith('f:')).length;
ok(nEv === Math.min(4, starts.length), `przypięte dowody: ${nEv}`); ok(nF >= 1, `przypięte fragmenty: ${nF}`);
await shot('board-preview');

// 2) treść widoczna na karcie bez otwierania akt
const txt = await p.locator('.bitem.prev').first().innerText();
const firstWords = (e => { const s = e.body.find(x => typeof x === 'string'); return s ? s.slice(0, 18) : null; })(starts[0]);
ok(!firstWords || txt.replace(/\s+/g, ' ').includes(firstWords.replace(/\s+/g, ' ').slice(0, 12)), 'karta dowodu na tablicy pokazuje początek treści');
ok(await p.locator('.bitem.frag .ft').first().innerText().then(t => t.trim().length > 0), 'karta fragmentu ma tekst');
ok(await p.locator('.bitem.frag small').first().innerText().then(t => /Z:/.test(t)), 'fragment podaje źródło');

// 3) brak nakładania po przypięciu
const overlaps = () => p.evaluate(() => { const r = [...document.querySelectorAll('.bitem')].map(el => [parseFloat(el.style.left), parseFloat(el.style.top), el.offsetWidth, el.offsetHeight]); let c = 0; r.forEach((a, i) => r.forEach((d, j) => { if (j > i && a[0] < d[0] + d[2] - 6 && a[0] + a[2] > d[0] + 6 && a[1] < d[1] + d[3] - 6 && a[1] + a[3] > d[1] + 6) c++; })); return c; });
ok(await overlaps() === 0, 'karty po przypięciu nie nakładają się');

// 4) rozwijanie / zwijanie
const h0 = await p.locator('.bitem.prev').first().evaluate(el => el.offsetHeight);
await p.locator('.bitem.prev .bbtn[data-bx="toggle"]').first().click(); await p.waitForTimeout(300);
ok(await p.locator('.bitem.open').count() === 1, 'przycisk „Rozwiń” otwiera kartę');
const h1 = await p.locator('.bitem.open').first().evaluate(el => el.offsetHeight);
ok(h1 >= h0, `rozwinięta karta nie jest niższa (${h0}px → ${h1}px)`);
st = await state(); ok(st.board.items.some(x => x.open), 'stan „rozwinięta” zapisany w grze');
await shot('board-open');
await A('board-fold'); ok(await p.locator('.bitem.prev').count() === 0, '„Rozwiń wszystko” otwiera wszystkie dowody');
await A('board-fold'); ok(await p.locator('.bitem.open').count() === 0, '„Zwiń wszystko” zwija wszystkie dowody');
// przycisk „Akta” na karcie
await p.locator('.bitem.prev .bbtn[data-bx="open"]').first().click(); await p.waitForTimeout(300);
ok(await p.locator('#overlay-root .doc').count() === 1, 'przycisk „Akta” otwiera dokument');
await closeAll();

// 5) notatka: dodanie, edycja
await A('note-add'); await p.waitForTimeout(200);
await p.locator('.bitem .bcard.note').first().click(); await p.waitForTimeout(200);
await A('note-edit'); await p.waitForTimeout(200);
st = await state(); ok(st.board.items.some(x => x.key.startsWith('n:') && x.text === 'Zmieniona notatka'), 'notatkę można edytować');
// 6) uporządkuj + nitka
await A('link-mode'); await p.locator('.bitem').nth(0).click(); await p.locator('.bitem').nth(1).click(); await p.waitForTimeout(200);
st = await state(); ok(st.board.links.length === 1, 'nitka łączy dwie karty');
await A('board-arrange'); await p.waitForTimeout(300);
ok(await overlaps() === 0, 'po „Uporządkuj” karty się nie nakładają'); await shot('board-arranged');
const path = await p.locator('#strings path').first().getAttribute('d'); ok(/^M[\d.]+,[\d.]+ Q/.test(path || ''), 'nitka narysowana poprawnie');

// 7) migracja starego zapisu (karty w siatce 220×230 bez pola v)
await p.evaluate(cid => { const s = JSON.parse(localStorage.getItem('slad.v2')); const g = s.games[cid]; g.board = { items: g.board.items.filter(x => x.key.startsWith('ev:')).map((x, i) => ({ key: x.key, x: 40 + (i % 7) * 220, y: 40 + Math.floor(i / 7) * 230 })), links: [], zoom: 1 }; localStorage.setItem('slad.v2', JSON.stringify(s)); }, CID);
await p.reload({ waitUntil: 'networkidle' }); await p.waitForTimeout(600);
await A('tab', '[data-tab="tablica"]'); await p.waitForTimeout(900);
st = await state(); ok(st.board.v === 2, 'stary zapis oznaczony jako zmigrowany'); ok(await overlaps() === 0, 'stara tablica po migracji bez nakładania');
await shot('board-migrated');

// 8) prywatność (tryb telefonów): w teczce tajnych akt nie ma pinezek fragmentów
if (MODE === 'phones') {
  const html = await p.evaluate(cid => { const c = caseFor(cid), g = G(cid); return (g.priv[0] || []).map(id => docHTML(c, c.ev[id], true)).join(''); }, CID);
  ok(html.length > 0 && !html.includes('fpin'), 'teczka tajnych akt (widok zwarty) nie ma pinezek');
  const priv = await p.evaluate(cid => { const c = caseFor(cid), g = G(cid); return Object.values(g.priv).flat().filter(id => !g.shared.includes(id) && !g.found.includes(id)).slice(0, 1)[0]; }, CID);
  if (priv) { const r = await p.evaluate(({ cid, id }) => { const c = caseFor(cid), g = G(cid); const before = g.board.items.length; pinToBoard(g, 'f:' + id + ':0:-1', 'x', { src: id, fmt: 'p' }); const L = boardLabel(c, g, 'ev:' + id); return { e: L.e }; }, { cid: CID, id: priv }); ok(r.e === null, 'nieujawnione tajne akta nie wyświetlą treści na tablicy'); }
}
ok(errs.length === 0, 'brak błędów w konsoli: ' + JSON.stringify(errs.slice(0, 3)));
await b.close();
console.log(fails.length ? `\nNIEUDANE: ${fails.length}` : '\nWSZYSTKO OK'); process.exit(fails.length ? 1 : 0);
