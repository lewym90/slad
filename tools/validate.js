#!/usr/bin/env node
/* Walidator logiki spraw ŚLAD. Użycie: node tools/validate.js [cases/001.json ...] */
'use strict';
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const files = process.argv.slice(2).length ? process.argv.slice(2) : JSON.parse(fs.readFileSync(path.join(root, 'cases/index.json'), 'utf8')).cases.filter(c => c.ready).map(c => `cases/${c.id}.json`);
const norm = s => String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ł/g, 'l').replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();
const digits = s => String(s).replace(/\D/g, '');
let failures = 0;

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
  const isTok = t => t.startsWith('lie:') || t.startsWith('st:') ? st.has(t.slice(t.indexOf(':') + 1)) : ev.has(t) || spots.has(t) || qs.has(t) || pz.has(t);
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
  for (const [id, p] of pz) {
    p.requires.forEach(x => { if (!isTok(x)) E(`zagadka ${id}: nieznany wymóg ${x}`); });
    ((p.reward || {}).spots || []).forEach(x => { if (!spots.has(x)) E(`zagadka ${id}: nagroda — brak punktu ${x}`); });
    if (!p.answers.length) E(`zagadka ${id}: brak odpowiedzi`);
    if (!p.hints || p.hints.length !== 3) E(`zagadka ${id}: wymagane 3 stopnie podpowiedzi`);
    // 5. Brak przecieku odpowiedzi
    const text = [p.prompt, p.title].join(' ');
    p.answers.forEach(a => {
      if (p.input === 'text') { if (norm(text).includes(norm(a)) && norm(a).length > 3) E(`zagadka ${id}: odpowiedź „${a}” występuje w treści`); }
      else if (p.input === 'number') { const [lo, hi] = String(a).split('-').map(Number); if (isNaN(lo) || (hi !== undefined && !isNaN(hi) && hi < lo)) E(`zagadka ${id}: zły przedział ${a}`); const nums = (text.match(/\d+/g) || []).map(Number); if (nums.some(n => n >= lo && n <= (isNaN(hi) ? lo : hi))) E(`zagadka ${id}: liczba z przedziału odpowiedzi występuje w treści`); }
      else { if (digits(text).includes(digits(a))) E(`zagadka ${id}: cyfry odpowiedzi ${a} występują w treści`); }
    });
    if (p.input === 'digits4' || p.input === 'time') { const reqText = p.requires.map(r => JSON.stringify((ev.get(r) || {}).body || '')).join(' '); p.answers.forEach(a => { if (reqText.includes(a)) warns.push(`zagadka ${id}: odpowiedź ${a} dosłownie w wymaganym dowodzie — upewnij się, że wymaga przekształcenia`); }); }
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
  c.evidence.forEach(e => { if (!sources.has(e.id)) E(`dowód ${e.id} nie ma źródła — nie da się go zdobyć`); });

  // 2. Symulacja osiągalności (zespół ujawnia wszystkie tajne akta)
  const K = new Set([...c.evidence.filter(e => e.start).map(e => e.id), ...(c.privateClues || [])]);
  const done = new Set(), claims = new Set(), broken = new Set(), solved = new Set();
  const has = t => t.startsWith('lie:') ? broken.has(t.slice(4)) : t.startsWith('st:') ? claims.has(t.slice(3)) : pz.has(t) ? solved.has(t) : spots.has(t) || qs.has(t) ? done.has(t) : K.has(t);
  let changed = true, rounds = 0;
  while (changed && rounds++ < 200) {
    changed = false;
    for (const [id, s] of spots) if (!done.has(id) && (!s.requires || ((!s.requires.puzzle || solved.has(s.requires.puzzle)) && (!s.requires.all || s.requires.all.every(has))))) { done.add(id); (s.gives || []).forEach(x => K.add(x)); changed = true; }
    for (const [id, q] of qs) if (!done.has(id) && (q.requires || []).every(has) && (!q.requiresAny || q.requiresAny.some(has))) { done.add(id); (q.gives || []).forEach(x => K.add(x)); (q.claims || []).forEach(x => claims.add(x)); changed = true; }
    for (const [id, p] of pz) if (!solved.has(id) && p.requires.every(has)) { solved.add(id); if (p.reward && p.reward.search) (p.reward.spots || []).forEach(s => { done.add(s); (spots.get(s).gives || []).forEach(x => K.add(x)); }); changed = true; }
    for (const id of claims) { const s = st.get(id); if (!broken.has(id) && !s.truth && (s.contradicts || []).some(x => x.startsWith('st:') ? claims.has(x.slice(3)) : K.has(x))) { broken.add(id); (s.gives || []).forEach(x => K.add(x)); (s.reveals || []).forEach(x => claims.add(x)); changed = true; } }
  }
  c.evidence.forEach(e => { if (!K.has(e.id)) E(`dowód ${e.id} nieosiągalny w pełnym przejściu`); });
  spots.forEach((_, id) => { if (!done.has(id)) E(`punkt ${id} nieosiągalny`); });
  qs.forEach((_, id) => { if (!done.has(id)) E(`pytanie ${id} nigdy się nie pojawi`); });
  pz.forEach((_, id) => { if (!solved.has(id)) E(`zagadka ${id} nigdy się nie odblokuje`); });
  st.forEach((s, id) => { if (!claims.has(id)) E(`zeznanie ${id} nigdy nie padnie`); else if (!s.truth && !s.unbreakable && !broken.has(id)) E(`kłamstwa ${id} nie da się podważyć`); });

  // 5b. Przełomy, pieczęcie archiwisty, sprzeczności zeznań
  (c.breakthroughs || []).forEach(b => { if (!b.id || !b.title || !b.text) E(`przełom ${b.id}: brak pól`); if (!isTok(b.when)) E(`przełom ${b.id}: nieznany token ${b.when}`); else if (!has(b.when)) E(`przełom ${b.id}: nieosiągalny`); });
  c.evidence.forEach(e => { if (e.mark && !/^[A-ZĄĆĘŁŃÓŚŹŻ]$/.test(e.mark)) E(`dowód ${e.id}: zła pieczęć ${e.mark}`); });
  st.forEach((s, id) => (s.contradicts || []).forEach(x => { if (!isTok(x) && !ev.has(x)) E(`zeznanie ${id}: nieznana sprzeczność ${x}`); if (x.startsWith('st:') && !st.get(x.slice(3)).truth) E(`zeznanie ${id}: ${x} nie jest prawdą`); }));

  // 6. Raport
  let total = 0;
  c.report.questions.forEach(q => {
    total += q.points + (q.proof ? q.proof.count * q.proof.each : 0);
    if (q.type === 'single') { if (!q.options.some(o => o[0] === q.correct)) E(`raport ${q.id}: brak poprawnej opcji`); if (new Set(q.options.map(o => o[0])).size !== q.options.length) E(`raport ${q.id}: duplikat opcji`); }
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
