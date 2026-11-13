#!/usr/bin/env node
/* Walidator logiki spraw ŚLAD. Użycie: node tools/validate.js [cases/001.json ...] */
'use strict';
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const files = process.argv.slice(2).length ? process.argv.slice(2) : JSON.parse(fs.readFileSync(path.join(root, 'cases/index.json'), 'utf8')).cases.filter(c => c.ready).map(c => `cases/${c.id}.json`);
const norm = s => String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ł/g, 'l').replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();
const digits = s => String(s).replace(/\D/g, '');
let failures = 0;
/* ---------- baza danych: wczytanie i kontrola globalna ---------- */
const DBK = ['osoby', 'pojazdy', 'firmy', 'ksiegi'];
let DBX = null;
function loadDB() {
  if (DBX) return DBX; const dir = path.join(root, 'data/baza'); if (!fs.existsSync(path.join(dir, 'index.json'))) return null;
  const d = { byId: {}, baseOf: {} }; DBK.forEach(k => { d[k] = []; });
  JSON.parse(fs.readFileSync(path.join(dir, 'index.json'), 'utf8')).files.forEach(f => { const pt = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')); DBK.forEach(k => (pt[k] || []).forEach(r => { d[k].push(r); if (d.byId[r.id]) dbErr.push(`baza: duplikat id ${r.id}`); d.byId[r.id] = r; d.baseOf[r.id] = k; })); });
  DBX = d; return d;
}
const dbErr = [];
const peselOk = p => /^\d{11}$/.test(p) && (10 - [1, 3, 7, 9, 1, 3, 7, 9, 1, 3].reduce((a, w, i) => a + w * +p[i], 0) % 10) % 10 === +p[10];
const nipOk = n => /^\d{10}$/.test(n) && [6, 5, 7, 2, 3, 4, 5, 6, 7].reduce((a, w, i) => a + w * +n[i], 0) % 11 === +n[9];
const KWV = { X: 10, A: 11, B: 12, C: 13, D: 14, E: 15, F: 16, G: 17, H: 18, I: 19, J: 20, K: 21, L: 22, M: 23, N: 24, O: 25, P: 26, R: 27, S: 28, T: 29, U: 30, W: 31, Y: 32, Z: 33 };
const kwOk = s => { const m = /^([A-Z0-9]{4})\/(\d{8})\/(\d)$/.exec(s); if (!m) return false; const b = m[1] + m[2]; return [...b].reduce((a, ch, i) => a + (/\d/.test(ch) ? +ch : KWV[ch]) * [1, 3, 7][i % 3], 0) % 10 === +m[3]; };
const dowOk = s => { const m = /^([A-Z]{3}) (\d)(\d{5})$/.exec(s); if (!m) return false; const v = [...m[1]].map(ch => ch.charCodeAt(0) - 55).concat([...m[3]].map(Number)); return v.reduce((a, x, i) => a + x * [7, 3, 1, 7, 3, 1, 7, 3][i], 0) % 10 === +m[2]; };
function checkDB() {
  const d = loadDB(); if (!d) return;
  const uniq = (list, f, name) => { const seen = new Map(); list.forEach(r => { const v = f(r); if (v == null) return; if (seen.has(v)) dbErr.push(`baza: powtórzony ${name} ${v} (${seen.get(v)}, ${r.id})`); seen.set(v, r.id); }); };
  uniq(d.osoby, r => r.pesel, 'PESEL'); uniq(d.osoby, r => r.dowod && r.dowod.nr, 'nr dowodu'); uniq(d.pojazdy, r => r.nr, 'nr rejestracyjny'); uniq(d.pojazdy, r => r.vin, 'VIN');
  uniq(d.firmy, r => r.krs, 'KRS'); uniq(d.firmy, r => r.nip, 'NIP'); uniq(d.ksiegi, r => r.nr, 'nr księgi');
  const P = new Map(d.osoby.map(r => [r.pesel, r])), K = new Map(d.firmy.map(r => [r.krs, r]));
  d.osoby.forEach(r => { if (!peselOk(r.pesel)) dbErr.push(`baza ${r.id}: zła suma PESEL`); if (r.dowod && !dowOk(r.dowod.nr)) dbErr.push(`baza ${r.id}: zła suma nr dowodu ${r.dowod.nr}`);
    const born = `${+r.pesel.slice(2, 4) > 20 ? '20' : '19'}${r.pesel.slice(0, 2)}-${String(+r.pesel.slice(2, 4) % 20).padStart(2, '0')}-${r.pesel.slice(4, 6)}`; if (born !== r.urodzony) dbErr.push(`baza ${r.id}: PESEL nie zgadza się z datą urodzenia`);
    if ((+r.pesel[9] % 2 ? 'M' : 'K') !== r.plec) dbErr.push(`baza ${r.id}: PESEL nie zgadza się z płcią`);
    if (r.malzonek) { const m = P.get(r.malzonek.pesel); if (!m) dbErr.push(`baza ${r.id}: małżonek ${r.malzonek.pesel} nie istnieje`); else if (!m.malzonek || m.malzonek.pesel !== r.pesel) dbErr.push(`baza ${r.id}: małżeństwo niesymetryczne`); else if (m.nazwisko !== r.malzonek.nazwisko || !m.imiona.includes(r.malzonek.imie)) dbErr.push(`baza ${r.id}: dane małżonka niezgodne z jego rekordem`); } });
  d.firmy.forEach(r => { if (!nipOk(r.nip)) dbErr.push(`baza ${r.id}: zła suma NIP`); r.zarzad.forEach(z => { const o = P.get(z.pesel); if (!o) dbErr.push(`baza ${r.id}: członek zarządu ${z.pesel} nie istnieje w ewidencji`); else if (o.nazwisko.toUpperCase() !== z.nazwisko) dbErr.push(`baza ${r.id}: nazwisko w zarządzie niezgodne z ewidencją (${z.nazwisko})`); }); });
  d.pojazdy.forEach(r => { const w = r.wlasciciel; if (w.pesel && !P.get(w.pesel)) dbErr.push(`baza ${r.id}: właściciel ${w.pesel} nie istnieje`); if (w.krs && !K.get(w.krs)) dbErr.push(`baza ${r.id}: firma ${w.krs} nie istnieje`); if (w.krs && K.get(w.krs) && K.get(w.krs).nazwa !== w.nazwa) dbErr.push(`baza ${r.id}: nazwa właściciela niezgodna z KRS`); });
  d.ksiegi.forEach(r => { if (!kwOk(r.nr)) dbErr.push(`baza ${r.id}: zła cyfra kontrolna KW ${r.nr}`); r.wlasciciele.forEach(w => { if (w.pesel && !P.get(w.pesel)) dbErr.push(`baza ${r.id}: właściciel ${w.pesel} nie istnieje`); if (w.krs && !K.get(w.krs)) dbErr.push(`baza ${r.id}: firma ${w.krs} nie istnieje`); }); });
}
checkDB();
if (DBX) { console.log(`\nBaza danych: osoby ${DBX.osoby.length} · pojazdy ${DBX.pojazdy.length} · firmy ${DBX.firmy.length} · księgi ${DBX.ksiegi.length}`); dbErr.forEach(e => console.log('  BŁĄD   ' + e)); if (!dbErr.length) console.log('  OK — sumy kontrolne, unikalność i powiązania'); failures += dbErr.length; }
const lcx = v => String(v || '').trim().toLocaleLowerCase('pl');
const FORMS = [[/\bsp\.\s*z\s*o\.\s*o\.?/g, 'spółka z ograniczoną odpowiedzialnością'], [/\bs\.\s*a\./g, 'spółka akcyjna'], [/\bsp\.\s*j\./g, 'spółka jawna'], [/\bsp\.\s*k\./g, 'spółka komandytowa']];
const ntok = v => { let t = lcx(v); FORMS.forEach(([re, f]) => { t = t.replace(re, f); }); return t.split(/\s+/).filter(Boolean); };
const DBMATCH = {
  osoby: (r, f) => (!f.nazwisko || lcx(r.nazwisko) === lcx(f.nazwisko)) && (!f.imie || r.imiona.some(n => lcx(n) === lcx(f.imie))) && (!f.pesel || r.pesel === f.pesel.trim()),
  pojazdy: (r, f) => (!f.nr || lcx(r.nr) === lcx(f.nr)) && (!f.vin || lcx(r.vin) === lcx(f.vin)),
  firmy: (r, f) => (!f.krs || r.krs === f.krs.trim()) && (!f.nip || r.nip === f.nip.trim()) && (!f.nazwa || (t => ntok(f.nazwa).every(w => t.includes(w)))(ntok(r.nazwa))),
  ksiegi: (r, f) => lcx(r.nr) === lcx(f.nr) };
const dbVis = (r, c) => !(r.from && r.from > c.db.date) && !(r.to && r.to <= c.db.date) && !r.afterSolved && !(r.case && !r.neutral && r.case !== c.id);
const recText = r => JSON.stringify(r);

function applyTable(raw) {
  const t = raw.tableMode || {}; const c = JSON.parse(JSON.stringify(raw));
  c.evidence = c.evidence.map(e => e.private ? { ...e, private: false } : e);
  c.locations = [...c.locations, ...(t.locations || [])];
  c.people = c.people.map(p => (t.questions || {})[p.id] ? { ...p, questions: [...p.questions, ...t.questions[p.id]] } : p);
  c.privateClues = []; return c;
}
const runs = [];
for (const f of files) { const raw = JSON.parse(fs.readFileSync(path.join(root, f), 'utf8')); runs.push([f + ' [Telewizor + telefony]', raw]); if (raw.tableMode) runs.push([f + ' [Wspólny stół]', applyTable(raw)]); else { console.log(f + ': BŁĄD brak wariantu tableMode'); failures++; } }
for (const [f, c] of runs) {
  const errs = [], warns = [];
  const E = id => errs.push(id);
  if (c.plan) {
    const W = m => warns.push(m);
    const locIds = new Set(c.locations.map(l => l.id)); const spotIds = new Set(c.locations.flatMap(l => l.spots.map(s => s.id)));
    const placed = new Set();
    c.plan.views.forEach(v => {
      v.items.forEach(it => { if (it.loc && !locIds.has(it.loc)) E(`plan ${v.id}: nieznane miejsce ${it.loc}`); if (it.t === 'body' && !(spotIds.has(it.req) || c.evidence.some(e => e.id === it.req))) E(`plan ${v.id}: zły warunek ciała ${it.req}`); });
      Object.keys(v.spots || {}).forEach(s => { if (!spotIds.has(s)) E(`plan ${v.id}: nieznany punkt ${s}`); placed.add(s); });
    });
    c.locations.filter(l => l.id !== 'hq').forEach(l => { if (!c.plan.views.some(v => v.items.some(it => it.loc === l.id))) W(`plan: miejsce ${l.id} nie ma pomieszczenia na szkicu`); l.spots.forEach(s => { if (!placed.has(s.id)) W(`plan: punkt ${s.id} bez znacznika`); }); });
  }
  if (c.intro && (!c.intro.modeRules || !c.intro.modeRules.table || !c.intro.modeRules.phones)) E('brak zasad zależnych od trybu (intro.modeRules)');
  const ev = new Map(c.evidence.map(e => [e.id, e]));
  const spots = new Map(); c.locations.forEach(l => l.spots.forEach(s => { if (spots.has(s.id)) E(`duplikat punktu ${s.id}`); spots.set(s.id, s); }));
  const qs = new Map(), st = new Map();
  c.people.forEach(p => { p.questions.forEach(q => { if (qs.has(q.id)) E(`duplikat pytania ${q.id}`); qs.set(q.id, { ...q, person: p.id }); }); p.statements.forEach(s => { if (st.has(s.id)) E(`duplikat zeznania ${s.id}`); st.set(s.id, { ...s, person: p.id }); }); });
  const pz = new Map(c.puzzles.map(p => [p.id, p]));
  if (ev.size !== c.evidence.length) E('powtórzone ID dowodów');
  const sh = new Map(); c.people.forEach(p => (p.shows || []).forEach(x => { if (sh.has(x.id) || qs.has(x.id) || st.has(x.id)) E(`duplikat id reakcji ${x.id}`); sh.set(x.id, { ...x, person: p.id }); }));
  const isTok = t => t.startsWith('show:') ? sh.has(t.slice(5)) : t.startsWith('lie:') || t.startsWith('st:') ? st.has(t.slice(t.indexOf(':') + 1)) : ev.has(t) || spots.has(t) || qs.has(t) || pz.has(t);
  const needEv = (id, where) => { if (!ev.has(id)) E(`${where}: brak dowodu ${id}`); };

  // 1. Referencje
  for (const [id, s] of spots) { (s.gives || []).forEach(x => needEv(x, `punkt ${id}`)); if (s.requires && s.requires.puzzle && !pz.has(s.requires.puzzle)) E(`punkt ${id}: brak zagadki ${s.requires.puzzle}`); if (s.requires && s.requires.all) s.requires.all.forEach(t => { if (!isTok(t)) E(`punkt ${id}: nieznany wymóg ${t}`); }); if (s.requires && !s.lockedText) E(`punkt ${id}: brak tekstu blokady`); }
  for (const [id, q] of qs) { (q.requiresAny || []).forEach(x => { if (!isTok(x)) E(`pytanie ${id}: nieznany wymóg ${x}`); }); (q.requires || []).forEach(x => { if (!isTok(x)) E(`pytanie ${id}: nieznany wymóg ${x}`); }); (q.gives || []).forEach(x => needEv(x, `pytanie ${id}`)); (q.claims || []).forEach(x => { if (!st.has(x)) E(`pytanie ${id}: brak zeznania ${x}`); }); }
  for (const [id, s] of st) {
    if (s.truth && s.contradicts && s.contradicts.length) E(`zeznanie ${id}: prawdziwe, a ma sprzeczne dowody`);
    if (!s.truth && !s.unbreakable && !(s.contradicts || []).length) E(`zeznanie ${id}: kłamstwo bez dowodu, który mu przeczy`);
    if (!s.truth && !s.response) E(`zeznanie ${id}: brak reakcji po konfrontacji`);
    (s.contradicts || []).filter(x => !x.startsWith('st:')).forEach(x => needEv(x, `zeznanie ${id}`)); (s.gives || []).forEach(x => needEv(x, `zeznanie ${id}`)); (s.reveals || []).forEach(x => { if (!st.has(x)) E(`zeznanie ${id}: ujawnia nieznane ${x}`); });
  }
  for (const [id, x] of sh) { needEv(x.ev, `reakcja ${id}`); (x.requires || []).forEach(t => { if (!isTok(t)) E(`reakcja ${id}: nieznany wymóg ${t}`); }); (x.gives || []).forEach(t => needEv(t, `reakcja ${id}`)); (x.claims || []).forEach(t => { if (!st.has(t)) E(`reakcja ${id}: nieznane zeznanie ${t}`); }); if (!x.a) E(`reakcja ${id}: brak tekstu`); }
  c.people.forEach(p => { if ((p.shows || []).length && !(p.showDefault || []).length) E(`osoba ${p.id}: reakcje bez domyślnych odpowiedzi`); });
  for (const [id, p] of pz) {
    p.requires.forEach(x => { if (!isTok(x)) E(`zagadka ${id}: nieznany wymóg ${x}`); });
    ((p.reward || {}).spots || []).forEach(x => { if (!spots.has(x)) E(`zagadka ${id}: nagroda — brak punktu ${x}`); });
    if (!p.answers.length) E(`zagadka ${id}: brak odpowiedzi`);
    if (!p.hints || p.hints.length !== 3) E(`zagadka ${id}: wymagane 3 stopnie podpowiedzi`);
    // 5. Brak przecieku odpowiedzi
    const text = [p.prompt, p.title].join(' ');
    if (p.input !== 'grid') p.answers.forEach(a => {
      if (p.input === 'text') { if (norm(text).includes(norm(a)) && norm(a).length > 3) E(`zagadka ${id}: odpowiedź „${a}” występuje w treści`); }
      else if (p.input === 'number') { const [lo, hi] = String(a).split('-').map(Number); if (isNaN(lo) || (hi !== undefined && !isNaN(hi) && hi < lo)) E(`zagadka ${id}: zły przedział ${a}`); const nums = (text.match(/\d+/g) || []).map(Number); if (nums.some(n => n >= lo && n <= (isNaN(hi) ? lo : hi))) E(`zagadka ${id}: liczba z przedziału odpowiedzi występuje w treści`); }
      else { if (digits(text).includes(digits(a))) E(`zagadka ${id}: cyfry odpowiedzi ${a} występują w treści`); }
    });
    if (p.input === 'digits4' || p.input === 'time') { const reqText = p.requires.map(r => JSON.stringify((ev.get(r) || {}).body || '')).join(' '); p.answers.forEach(a => { if (reqText.includes(a)) warns.push(`zagadka ${id}: odpowiedź ${a} dosłownie w wymaganym dowodzie — upewnij się, że wymaga przekształcenia`); }); }
  }
  for (const [id, p] of pz) if (p.input === 'grid') {
    const gd = p.grid || {}; const W = m => E(`zagadka ${id}: ${m}`);
    const rows = (gd.rows || []).map(r => r.id), cols = (gd.cols || []).map(r => r.id), opts = (gd.options || []).map(o => o.id);
    if (!rows.length || !cols.length || opts.length < 2) { W('macierz wymaga wierszy, kolumn i co najmniej 2 opcji'); continue; }
    [rows, cols, opts].forEach(a => { if (new Set(a).size !== a.length) W('powtórzone identyfikatory w macierzy'); });
    const sol = p.answers[0] || {};
    rows.forEach(r => cols.forEach(cl => { if (!opts.includes((sol[r] || {})[cl])) W(`odpowiedź nie wypełnia komórki ${r}/${cl}`); }));
    if (p.answers.length !== 1) W('macierz musi mieć dokładnie jedno rozwiązanie wzorcowe');
    const cons = gd.constraints || []; if (cons.length < rows.length) W('za mało warunków logicznych');
    const cells = []; rows.forEach(r => cols.forEach(cl => cells.push([r, cl])));
    const refs = k => ({ is: [[k.r, k.c]], not: [[k.r, k.c]], same: [[k.r1, k.c], [k.r2, k.c]], diff: [[k.r1, k.c], [k.r2, k.c]], forbid: [[k.r, k.c1], [k.r, k.c2]], exactly: rows.map(r => [r, k.c]), in: [[k.r, k.c]] }[k.t]);
    cons.forEach((k, i) => {
      const R = refs(k); if (!R) { W(`warunek ${i}: nieznany typ ${k.t}`); return; }
      R.forEach(([r, cl]) => { if (!rows.includes(r) || !cols.includes(cl)) W(`warunek ${i}: nieznana komórka ${r}/${cl}`); });
      [k.v, k.v1, k.v2, ...(k.vs || [])].filter(v => v !== undefined).forEach(v => { if (!opts.includes(v)) W(`warunek ${i}: nieznane miejsce ${v}`); });
      if (!k.src || !k.src.length) W(`warunek ${i}: brak dokumentu źródłowego`); else k.src.forEach(x => { if (!ev.has(x) && !isTok(x)) W(`warunek ${i}: brak dowodu ${x}`); else if (!p.requires.includes(x)) W(`warunek ${i}: dowód ${x} nie jest na liście wymaganych materiałów zagadki`); });
      if (!k.why) W(`warunek ${i}: brak opisu (pole why)`);
    });
    p.requires.forEach(x => { if (ev.has(x) && !cons.some(k => (k.src || []).includes(x))) warns.push(`zagadka ${id}: wymagany dowód ${x} nie jest źródłem żadnego warunku`); });
    const okCons = (A, k) => { const g = (r, cl) => A[r + '|' + cl];
      if (k.t === 'is') return g(k.r, k.c) === k.v; if (k.t === 'not') return g(k.r, k.c) !== k.v;
      if (k.t === 'same') return g(k.r1, k.c) === g(k.r2, k.c); if (k.t === 'diff') return g(k.r1, k.c) !== g(k.r2, k.c);
      if (k.t === 'forbid') return !(g(k.r, k.c1) === k.v1 && g(k.r, k.c2) === k.v2);
      if (k.t === 'in') return (k.vs || []).includes(g(k.r, k.c));
      if (k.t === 'exactly') return rows.filter(r => g(r, k.c) === k.v).length === k.n; return false; };
    const A = {}; let nsol = 0, firstSol = null;
    const ready = k => (refs(k) || []).every(([r, cl]) => A[r + '|' + cl] !== undefined);
    const dfs = i => {
      if (nsol > 1) return;
      if (i === cells.length) { nsol++; if (!firstSol) firstSol = { ...A }; return; }
      const [r, cl] = cells[i];
      for (const v of opts) { A[r + '|' + cl] = v; if (cons.every(k => !ready(k) || okCons(A, k))) dfs(i + 1); }
      delete A[r + '|' + cl];
    };
    dfs(0);
    if (nsol === 0) W('warunki logiczne nie mają żadnego rozwiązania');
    else if (nsol > 1) W('warunki logiczne dopuszczają więcej niż jedno rozwiązanie — macierz nie jest jednoznaczna');
    else rows.forEach(r => cols.forEach(cl => { if (firstSol[r + '|' + cl] !== (sol[r] || {})[cl]) W(`rozwiązanie z warunków różni się od odpowiedzi w komórce ${r}/${cl}`); }));
  }
  (c.privateClues || []).forEach(x => { needEv(x, 'tajne akta'); if (ev.get(x) && !ev.get(x).private) E(`tajny dokument ${x} bez flagi private`); });
  c.evidence.filter(e => e.private).forEach(e => { if (!c.privateClues.includes(e.id)) E(`dowód ${e.id} oznaczony jako tajny, ale nie rozdawany`); });
  c.people.forEach(p => (p.revealOn || []).forEach(x => { if (!st.has(x)) E(`${p.id}: revealOn wskazuje nieznane ${x}`); }));
  (c.hintTrail || []).forEach((h, i) => [...(h.when || []), ...(h.unless || [])].forEach(t => { if (!isTok(t)) E(`trop ${i}: nieznany token ${t}`); }));
  const timeRe = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/;
  const chkTime = (arr, w) => (arr || []).forEach(t => { if (!timeRe.test(t[0]) || !t[1] || !t[2]) E(`${w}: zły wpis czasu ${JSON.stringify(t)}`); });
  c.evidence.forEach(e => chkTime(e.time, e.id)); qs.forEach((q, id) => chkTime(q.time, id)); st.forEach((s, id) => chkTime(s.time, id)); pz.forEach((p, id) => chkTime((p.reward || {}).time, id));
  // źródła pozyskania
  const sources = new Map(); const addSrc = (id, s) => { if (!sources.has(id)) sources.set(id, []); sources.get(id).push(s); };
  c.evidence.filter(e => e.start).forEach(e => addSrc(e.id, 'start'));
  (c.privateClues || []).forEach(id => addSrc(id, 'tajne'));
  spots.forEach((s, sid) => (s.gives || []).forEach(id => addSrc(id, sid)));
  qs.forEach((q, qid) => (q.gives || []).forEach(id => addSrc(id, qid)));
  st.forEach((s, sid) => (s.gives || []).forEach(id => addSrc(id, sid)));
  sh.forEach((x, xid) => (x.gives || []).forEach(id => addSrc(id, xid)));
  ((c.db && c.db.attach) || []).forEach(a => addSrc(a.ev, 'baza:' + a.rec));
  c.evidence.forEach(e => { if (!sources.has(e.id)) E(`dowód ${e.id} nie ma źródła — nie da się go zdobyć`); });

  // 2. Symulacja osiągalności (zespół ujawnia wszystkie tajne akta)
  const K = new Set([...c.evidence.filter(e => e.start).map(e => e.id), ...(c.privateClues || [])]);
  const done = new Set(), claims = new Set(), broken = new Set(), solved = new Set();
  const has = t => t.startsWith('show:') ? done.has(t) : t.startsWith('lie:') ? broken.has(t.slice(4)) : t.startsWith('st:') ? claims.has(t.slice(3)) : pz.has(t) ? solved.has(t) : spots.has(t) || qs.has(t) ? done.has(t) : K.has(t);
  let changed = true, rounds = 0;
  while (changed && rounds++ < 200) {
    changed = false;
    for (const [id, s] of spots) if (!done.has(id) && (!s.requires || ((!s.requires.puzzle || solved.has(s.requires.puzzle)) && (!s.requires.all || s.requires.all.every(has))))) { done.add(id); (s.gives || []).forEach(x => K.add(x)); changed = true; }
    for (const [id, q] of qs) if (!done.has(id) && (q.requires || []).every(has) && (!q.requiresAny || q.requiresAny.some(has))) { done.add(id); (q.gives || []).forEach(x => K.add(x)); (q.claims || []).forEach(x => claims.add(x)); changed = true; }
    for (const [id, p] of pz) if (!solved.has(id) && p.requires.every(has)) { solved.add(id); if (p.reward && p.reward.search) (p.reward.spots || []).forEach(s => { done.add(s); (spots.get(s).gives || []).forEach(x => K.add(x)); }); changed = true; }
    for (const [id, x] of sh) if (!done.has('show:' + id) && K.has(x.ev) && (x.requires || []).every(has)) { done.add('show:' + id); (x.gives || []).forEach(t => K.add(t)); (x.claims || []).forEach(t => claims.add(t)); changed = true; }
    ((c.db && c.db.attach) || []).forEach(a => { if (!K.has(a.ev) && a.paths.some(pt => pt.from.every(t => K.has(t)))) { K.add(a.ev); changed = true; } });
    for (const id of claims) { const s = st.get(id); if (!broken.has(id) && !s.truth && (s.contradicts || []).some(x => x.startsWith('st:') ? claims.has(x.slice(3)) : K.has(x))) { broken.add(id); (s.gives || []).forEach(x => K.add(x)); (s.reveals || []).forEach(x => claims.add(x)); changed = true; } }
  }
  c.evidence.forEach(e => { if (!K.has(e.id)) E(`dowód ${e.id} nieosiągalny w pełnym przejściu`); });
  spots.forEach((_, id) => { if (!done.has(id)) E(`punkt ${id} nieosiągalny`); });
  qs.forEach((_, id) => { if (!done.has(id)) E(`pytanie ${id} nigdy się nie pojawi`); });
  pz.forEach((_, id) => { if (!solved.has(id)) E(`zagadka ${id} nigdy się nie odblokuje`); });
  st.forEach((s, id) => { if (!claims.has(id)) E(`zeznanie ${id} nigdy nie padnie`); else if (!s.truth && !s.unbreakable && !broken.has(id)) E(`kłamstwa ${id} nie da się podważyć`); });

  sh.forEach((x, id) => { if (!done.has('show:' + id)) E(`reakcja ${id} nigdy nie padnie`); });
  // 5a. Baza danych w sprawie
  if (c.db) { const d = loadDB(); if (!d) E('sprawa korzysta z bazy, a brak data/baza');
    else {
      const evText = id => { const e = ev.get(id); if (!e) return ''; if (e.db) return recText(d.byId[e.db] || {}); return JSON.stringify(e.body) + ' ' + e.title; };
      (c.db.bases || []).forEach(b => { if (!DBK.includes(b)) E(`baza: nieznany rejestr ${b}`); });
      (c.db.attach || []).forEach(a => { const r = d.byId[a.rec]; const e = ev.get(a.ev);
        if (!r) { E(`baza: brak rekordu ${a.rec}`); return; } if (!e) E(`baza: brak dowodu ${a.ev}`); else if (e.db !== a.rec) E(`baza: dowód ${a.ev} nie wskazuje rekordu ${a.rec}`);
        if (!dbVis(r, c)) E(`baza: rekord ${a.rec} niewidoczny w dacie sprawy`); const base = d.baseOf[a.rec]; if (!(c.db.bases || []).includes(base)) E(`baza: rejestr ${base} niedostępny w sprawie`);
        a.paths.forEach((pt, i) => { const res = d[base].filter(x => dbVis(x, c) && DBMATCH[base](x, pt.q)); if (!res.some(x => x.id === a.rec)) E(`baza ${a.ev} ścieżka ${i}: zapytanie nie zwraca rekordu`); if (res.length > 30) E(`baza ${a.ev} ścieżka ${i}: ponad 30 wyników — gracz nie zobaczy listy`);
          const txt = lcx(pt.from.map(evText).join(' ')); Object.values(pt.q).forEach(v => { if (!txt.includes(lcx(v))) E(`baza ${a.ev} ścieżka ${i}: „${v}” nie występuje w ${pt.from.join(', ')} w tej formie`); });
          if (base === 'osoby' && pt.q.nazwisko) { const same = res.filter(x => x.id !== a.rec && x.urodzony.slice(0, 4) === r.urodzony.slice(0, 4) && x.adres.split(' ').pop() === r.adres.split(' ').pop()); if (same.length) E(`baza ${a.ev}: imiennik z tym samym rokiem urodzenia i miastem — nie da się rozróżnić`); } }); });
      // każdy identyfikator w tekstach sprawy musi istnieć w bazie dokładnie w tej formie
      const vis = { nr: new Set(), pesel: new Set(), krs: new Set(), nip: new Set(), kw: new Set(), dow: new Set() };
      d.pojazdy.filter(x => dbVis(x, c)).forEach(x => vis.nr.add(x.nr)); d.osoby.filter(x => dbVis(x, c)).forEach(x => { vis.pesel.add(x.pesel); vis.dow.add(x.dowod.nr); });
      d.firmy.filter(x => dbVis(x, c)).forEach(x => { vis.krs.add(x.krs); vis.nip.add(x.nip); }); d.ksiegi.filter(x => dbVis(x, c)).forEach(x => vis.kw.add(x.nr));
      const ign = new Set(c.db.ignore || []);
      const texts = []; c.evidence.filter(e => !e.db).forEach(e => texts.push([e.id, JSON.stringify(e.body) + ' ' + e.title + ' ' + e.summary]));
      c.people.forEach(p => { p.questions.forEach(q => texts.push([q.id, q.q + ' ' + q.a])); p.statements.forEach(x => texts.push([x.id, x.text + ' ' + (x.response || '')])); (p.shows || []).forEach(x => texts.push([x.id, x.a])); });
      texts.push(['intro', JSON.stringify(c.intro)]); texts.push(['raport', JSON.stringify(c.report) + JSON.stringify(c.solution) + JSON.stringify(c.endings)]);
      const RX = [['nr', /\b[A-Z]{2,3} [0-9][0-9A-Z]{3,4}\b|\b[A-Z]{2,3} [0-9A-Z]{3,4}[0-9]\b/g], ['pesel', /(?<![\d ])\d{11}(?!\d)/g], ['krs', /\b0000\d{6}\b/g], ['nip', /(?<!\d)(?!0000)\d{10}(?!\d)/g], ['kw', /\b[A-Z]{2}\d[A-Z]\/\d{8}\/\d\b/g], ['dow', /\b[A-Z]{3} \d{6}\b/g]];
      texts.forEach(([w, t]) => RX.forEach(([k, re]) => (t.match(re) || []).forEach(m => { if (k === 'nr' && /^[A-Z]{3} \d{6}$/.test(m)) return; if (!ign.has(m) && !vis[k].has(m)) E(`${w}: identyfikator „${m}” nie istnieje w bazie w tej formie`); })));
    } }
  // 5b. Przełomy, pieczęcie archiwisty, sprzeczności zeznań
  (c.breakthroughs || []).forEach(b => { if (!b.id || !b.title || !b.text) E(`przełom ${b.id}: brak pól`); if (!isTok(b.when)) E(`przełom ${b.id}: nieznany token ${b.when}`); else if (!has(b.when)) E(`przełom ${b.id}: nieosiągalny`); });
  c.evidence.forEach(e => { if (e.mark && !/^[A-ZĄĆĘŁŃÓŚŹŻ]$/.test(e.mark)) E(`dowód ${e.id}: zła pieczęć ${e.mark}`); });
  st.forEach((s, id) => (s.contradicts || []).forEach(x => { if (!isTok(x) && !ev.has(x)) E(`zeznanie ${id}: nieznana sprzeczność ${x}`); if (x.startsWith('st:') && !st.get(x.slice(3)).truth) E(`zeznanie ${id}: ${x} nie jest prawdą`); }));

  // 5c. Pliki multimediów
  const fsx = require('fs'), pathx = require('path');
  if (c.voiceDir) c.people.forEach(p => { [...p.questions, ...((c.tableMode && c.tableMode.questions && c.tableMode.questions[p.id]) || [])].forEach(q => { if (!fsx.existsSync(pathx.join(__dirname, '..', `${c.voiceDir}/${q.id}.mp3`))) E(`brak głosu ${q.id}`); });
    p.statements.filter(x => x.response).forEach(x => { if (!fsx.existsSync(pathx.join(__dirname, '..', `${c.voiceDir}/${x.id}.mp3`))) E(`brak głosu ${x.id}`); });
    (p.deflect || []).forEach((_, i) => { if (!fsx.existsSync(pathx.join(__dirname, '..', `${c.voiceDir}/${p.id}-deflect-${i}.mp3`))) E(`brak głosu ${p.id}-deflect-${i}`); });
    (p.shows || []).forEach(x => { if (!fsx.existsSync(pathx.join(__dirname, '..', `${c.voiceDir}/${x.id}.mp3`))) E(`brak głosu ${x.id}`); });
    (p.showDefault || []).forEach((_, i) => { if (!fsx.existsSync(pathx.join(__dirname, '..', `${c.voiceDir}/${p.id}-show-${i}.mp3`))) E(`brak głosu ${p.id}-show-${i}`); }); });
  if (c.voiceDir) { const VL = JSON.parse(fsx.readFileSync(pathx.join(__dirname, 'voice', 'lines.json'), 'utf8'));
    c.people.forEach(p => { const rec = VL[`${c.id}-${p.id}`]; if (!rec) { E(`brak tekstów nagrań dla ${p.id}`); return; } const byId = Object.fromEntries(rec.lines.map(l => [l.id, l.text]));
      const cur = [...p.questions, ...((c.tableMode && c.tableMode.questions && c.tableMode.questions[p.id]) || [])].map(q => [q.id, q.a]).concat(p.statements.filter(x => x.response).map(x => [x.id, x.response]), (p.deflect || []).map((d, i) => [`deflect-${i}`, d]), (p.shows || []).map(x => [x.id, x.a]), (p.showDefault || []).map((d, i) => [`show-${i}`, d]));
      cur.forEach(([id, t]) => { if (byId[id] !== t) E(`kwestia ${id} różni się od nagrania — nagrać ponownie albo przywrócić tekst`); }); }); }
  [c.voice && c.voice.brief, c.introVideo, c.keyart, ...(c.breakthroughs || []).flatMap(b => [b.img, b.video])].filter(Boolean).forEach(f => { if (!fsx.existsSync(pathx.join(__dirname, '..', f))) E(`brak pliku ${f}`); });

  // 6. Raport
  let total = 0;
  c.report.questions.forEach(q => {
    total += q.points + (q.proof ? q.proof.count * q.proof.each : 0);
    if (q.type === 'single') { if (!q.options.some(o => o[0] === q.correct)) E(`raport ${q.id}: brak poprawnej opcji`); if (new Set(q.options.map(o => o[0])).size !== q.options.length) E(`raport ${q.id}: duplikat opcji`); }
    if (q.type === 'multi') { const ks = q.options.map(o => o[0]); if (new Set(ks).size !== ks.length) E(`raport ${q.id}: duplikat opcji`); if (!Array.isArray(q.correct) || !q.correct.length || q.correct.length >= ks.length) E(`raport ${q.id}: poprawny zbiór musi być niepusty i mniejszy niż liczba opcji`); else q.correct.forEach(k => { if (!ks.includes(k)) E(`raport ${q.id}: poprawna opcja ${k} nie istnieje`); }); }
    if (q.type === 'order') { const a = q.items.map(i => i[0]).sort().join(), b = q.correct.slice().sort().join(); if (a !== b) E(`raport ${q.id}: kolejność nie jest permutacją`); }
    if (q.proof) { q.proof.valid.forEach(x => { needEv(x, `raport ${q.id}`); if (!K.has(x)) E(`raport ${q.id}: dowód ${x} nieosiągalny`); }); if (q.proof.valid.filter(x => K.has(x)).length < q.proof.count) E(`raport ${q.id}: za mało osiągalnych dowodów`); }
  });
  if (total !== 100) E(`raport: suma punktów ${total} ≠ 100`);
  const who = c.report.questions.find(q => q.id === 'r-who');
  if (who) who.options.forEach(o => { if (o[0] !== who.correct && !(c.endings.wrong || {})[o[0]]) E(`brak zakończenia dla błędnego oskarżenia: ${o[0]}`); });
  if (!c.endings.correct || !c.endings.correct.decision) E('brak zakończenia poprawnego z decyzją');

  // 7. Zasoby
  [c.cover, c.keyart, c.ambience, c.art].filter(Boolean).forEach(a => { if (!fs.existsSync(path.join(root, a))) E(`brak pliku ${a}`); });
  c.people.forEach(p => { if (p.img && !fs.existsSync(path.join(root, p.img))) E(`brak portretu ${p.img}`); });
  c.locations.forEach(l => { if (l.img && !fs.existsSync(path.join(root, l.img))) E(`brak grafiki ${l.img}`); });

  console.log(`\n${f}: ${c.title}`);
  console.log(`  dowody ${c.evidence.length} · miejsca ${c.locations.length} (${spots.size} punktów) · osoby ${c.people.length} (${qs.size} pytań, ${st.size} zeznań, ${[...st.values()].filter(s => !s.truth).length} kłamstw) · zagadki ${pz.size} · rundy symulacji ${rounds}`);
  warns.forEach(w => console.log('  UWAGA  ' + w));
  errs.forEach(e => console.log('  BŁĄD   ' + e));
  if (!errs.length) console.log('  OK — brak błędów logiki danych');
  failures += errs.length;
}
process.exit(failures ? 1 : 0);
