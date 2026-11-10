/* ŚLAD 2.0 — silnik gry. Wszystkie postacie i zdarzenia są fikcyjne. */
'use strict';
const VERSION = '2.3.0';
const BUILD = '10.11.2026';
let swReg = null;
const STORE_KEY = 'slad.v2';

/* ---------- narzędzia ---------- */
const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const norm = s => String(s ?? '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ł/g, 'l').replace(/[^a-z0-9:/ ]+/g, ' ').replace(/\s+/g, ' ').trim();
const digits = s => String(s ?? '').replace(/\D/g, '');
const hash = s => { let h = 0; for (const c of String(s)) h = (h * 31 + c.charCodeAt(0)) | 0; return Math.abs(h); };
const rot = id => (((hash(id) % 9) - 4) * 0.55).toFixed(2) + 'deg';
const MONTHS = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia'];
const DAYS = ['Niedziela', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota'];

const I = {
  files: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M3 10h18"/></svg>',
  map: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
  people: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5"/><circle cx="17" cy="9" r="2.6"/><path d="M16 14.6c2.6-.3 4.8 1.2 5.5 4.4"/></svg>',
  brain: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l5 5"/><path d="M8.5 11h5M11 8.5v5"/></svg>',
  board: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="4" width="18" height="16" rx="1"/><circle cx="8" cy="9" r="1.2" fill="currentColor"/><circle cx="16" cy="8" r="1.2" fill="currentColor"/><circle cx="12" cy="15.5" r="1.2" fill="currentColor"/><path d="M8 9l8-1-4 7.5z"/></svg>',
  back: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M15 5l-7 7 7 7"/></svg>',
  close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  bulb: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/></svg>',
  menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
  sound: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/></svg>',
  mute: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M17 9l5 6M22 9l-5 6"/></svg>',
  pin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 3h6l-1 6 3 3H7l3-3z"/><path d="M12 12v9"/></svg>',
  link: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>',
  trash: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/></svg>',
  plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 5v14M5 12h14"/></svg>',
  minus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 12h14"/></svg>',
  lock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="5" y="10" width="14" height="10" rx="1"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
  table: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="4" width="18" height="12" rx="1"/><path d="M8 20h8M12 16v4"/></svg>',
  phones: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="4" width="13" height="9" rx="1"/><path d="M6 17h5"/><rect x="16" y="8" width="6" height="12" rx="1.2"/><path d="M18.5 17.5h1"/></svg>',
  gear: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/></svg>'
};

const ROLES = [
  { id: 'koord', name: 'Koordynator', tip: 'Pilnujesz głównych pytań sprawy i decydujesz, kiedy zespół jest gotów złożyć raport.' },
  { id: 'analityk', name: 'Analityk dowodów', tip: 'Czytasz dokumenty jako pierwszy i szukasz w nich liczb, dat i drobnych niezgodności.' },
  { id: 'chrono', name: 'Chronolog', tip: 'Prowadzisz oś czasu. Każda godzina musi się zgadzać — sprawdzaj, w jakim czasie ją zapisano.' },
  { id: 'przesl', name: 'Prowadzący przesłuchania', tip: 'Zadajesz pytania i wyłapujesz zdania, które można podważyć dowodem.' },
  { id: 'weryf', name: 'Weryfikator hipotez', tip: 'Twoja rola to mówić „sprawdzam”. Każdą teorię zespołu próbuj obalić, zanim trafi do raportu.' },
  { id: 'protokol', name: 'Protokolant', tip: 'Prowadzisz notatki i tablicę. Kto ma motyw, kto okazję, kto kłamał?' }
];
const RANKS = [[92, 'Legenda archiwum'], [78, 'Komisarz'], [60, 'Inspektor'], [40, 'Aspirant'], [0, 'Stażysta']];

/* ---------- pamięć ---------- */
function freshStore() { return { v: 2, settings: { sound: false, text: 'm', motion: 'on' }, games: {} }; }
function loadStore() {
  try { const s = JSON.parse(localStorage.getItem(STORE_KEY)); if (s && s.v === 2 && s.games && s.settings) return s; } catch (_) {}
  return freshStore();
}
let S = loadStore();
let saveFailed = false;
function save() {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(S)); saveFailed = false; }
  catch (_) { if (!saveFailed) toast('Zapis nie powiódł się', 'Pamięć przeglądarki jest pełna albo zablokowana. Wyeksportuj zapis w ustawieniach.', 'Błąd'); saveFailed = true; }
}
if (navigator.storage && navigator.storage.persist) navigator.storage.persist().catch(() => {});
function applySettings() {
  document.documentElement.dataset.text = S.settings.text;
  document.documentElement.dataset.motion = S.settings.motion;
  document.documentElement.dataset.tv = S.settings.tv ? 'on' : 'off';
}

/* ---------- dane spraw ---------- */
let CATALOG = null;
const CASES = {};
async function fetchJSON(url) { const r = await fetch(url, { cache: 'no-cache' }); if (!r.ok) throw new Error(url + ' ' + r.status); return r.json(); }
async function getCatalog() { if (!CATALOG) CATALOG = (await fetchJSON('cases/index.json')).cases; return CATALOG; }
function indexCase(c) {
  c.ev = Object.fromEntries(c.evidence.map(e => [e.id, e]));
  c.person = Object.fromEntries(c.people.map(p => [p.id, p]));
  c.loc = Object.fromEntries(c.locations.map(l => [l.id, l]));
  c.spot = {}; c.locations.forEach(l => l.spots.forEach((s, i) => { c.spot[s.id] = { ...s, loc: l.id, n: i + 1 }; }));
  c.stmt = {}; c.q = {};
  c.people.forEach(p => { p.statements.forEach(s => { c.stmt[s.id] = { ...s, person: p.id }; }); p.questions.forEach(q => { c.q[q.id] = { ...q, person: p.id }; }); });
  c.puzzle = Object.fromEntries(c.puzzles.map(p => [p.id, p]));
  return c;
}
async function getCase(id) {
  if (CASES[id]) return CASES[id];
  CASES[id] = indexCase(await fetchJSON(`cases/${id}.json`)); return CASES[id];
}
/* Wariant sprawy dla trybu: „Wspólny stół” przenosi tajne akta do świata gry. */
function variant(base, mode) {
  if (!base || mode !== 'table') return base;
  if (base._table) return base._table;
  const t = base.tableMode || {};
  const c = { ...base };
  c.evidence = base.evidence.map(e => e.private ? { ...e, private: false, coop: true } : e);
  c.locations = [...base.locations, ...(t.locations || [])];
  c.people = base.people.map(p => (t.questions || {})[p.id] ? { ...p, questions: [...p.questions, ...t.questions[p.id]] } : p);
  c.privateClues = []; c.par = base.par + (t.parBonus || 0); c.mode = 'table';
  base._table = indexCase(c); return base._table;
}
const caseFor = (id) => { const g = G(id); return variant(CASES[id], g && g.mode); };
const MODES = {
  table: { name: 'Wspólny stół', sub: 'Jeden ekran: laptop, telewizor albo tablet', points: ['Wszyscy widzicie wszystko i gracie jak jeden zespół detektywów przy jednym stole.', 'Nie ma tajnych akt. Informacje, które w drugim trybie trafiają do kieszeni graczy, trzeba zdobyć w śledztwie — m.in. w miejscu „Centrala wydziału”.', 'Najlepszy we dwoje: jedna osoba czyta dokumenty na głos, druga prowadzi tablicę i oś czasu.'] },
  phones: { name: 'Telewizor + telefony', sub: 'Wspólny ekran i prywatne teczki w telefonach', points: ['Gra toczy się na wspólnym ekranie. Na starcie każdy skanuje aparatem telefonu swój kod QR i widzi tylko swoje tajne akta.', 'Sami decydujecie, kiedy podzielić się wiedzą: możecie ją opowiedzieć albo ujawnić dokument na wspólnym ekranie, wpisując jego kod z telefonu.', 'Najlepszy dla 3–6 osób. Telefon potrzebuje internetu tylko przy pierwszym otwarciu kodu. Ktoś bez telefonu może zajrzeć do teczki na wspólnym ekranie.'] }
};
const codeFor = (g, id) => {
  let h = 2166136261; for (const ch of g.created + ':' + id + ':slad') { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619); }
  h ^= h >>> 13; h = Math.imul(h, 0x5bd1e995); h ^= h >>> 15;
  const A = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; let o = ''; for (let i = 0; i < 4; i++) o += A[(h >>> (i * 5)) & 31]; return o;
};

/* ---------- stan rozgrywki ---------- */
function shuffle(arr, seed) { const a = arr.slice(); let s = seed || 1; for (let i = a.length - 1; i > 0; i--) { s = (s * 9301 + 49297) % 233280; const j = Math.floor(s / 233280 * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
function newGame(c, names, mode) {
  const seed = Date.now() % 100000;
  const priv = {}; names.forEach((_, i) => { priv[i] = []; });
  if (mode !== 'table') shuffle(c.privateClues, seed).forEach((id, i) => priv[i % names.length].push(id));
  const roles = shuffle(ROLES.map(r => r.id), seed + 7);
  return {
    v: 2, created: Date.now(), mode, phase: mode === 'table' ? 'play' : mode === 'phones' ? 'qr' : 'distribute', distIdx: 0,
    players: names.map((n, i) => ({ name: n, role: roles[i % roles.length] })), priv, shared: [],
    found: c.evidence.filter(e => e.start).map(e => e.id), read: [], spots: [], asked: [], claims: [], broken: [],
    log: {}, failed: 0, actions: 0, puzzles: {}, trops: 0, notes: '', board: { items: [], links: [], zoom: 1 },
    draft: { step: 0, answers: {}, proofs: [], order: null }, report: null
  };
}
const G = id => S.games[id];
const known = (g, id) => g.found.includes(id) || g.shared.includes(id);
function has(g, c, tok) {
  if (tok.startsWith('lie:')) return g.broken.includes(tok.slice(4));
  if (c.puzzle[tok]) return !!(g.puzzles[tok] && g.puzzles[tok].solved);
  if (c.spot[tok]) return g.spots.includes(tok);
  if (c.q[tok]) return g.asked.includes(tok);
  return known(g, tok);
}
const visibleEvidence = (g, c) => [...g.found, ...g.shared].filter((id, i, a) => a.indexOf(id) === i && c.ev[id]);
const unread = (g, c) => visibleEvidence(g, c).filter(id => !g.read.includes(id)).length;
function personName(g, p) { return p.revealName && (p.revealOn || []).some(b => g.broken.includes(b)) ? p.revealName : p.name; }
function personRole(g, p) { return p.revealName && personName(g, p) === p.revealName ? (p.revealRole || p.role) : p.role; }
function gain(g, c, ids, silent) {
  const got = [];
  (ids || []).forEach(id => { if (c.ev[id] && !known(g, id)) { g.found.push(id); got.push(id); } });
  if (got.length && !silent) { got.forEach((id, i) => setTimeout(() => toast(c.ev[id].title, c.ev[id].summary, 'Nowy dowód', id), i * 450)); sfx(); }
  return got;
}

/* ---------- dźwięk (Web Audio: pętla bez przerw, osobne głośności) ---------- */
let currentCaseId = null;
const AU = { ctx: null, bufs: {}, amb: null, ambSrc: null, token: 0 };
const vol = k => Math.max(0, Math.min(1, S.settings[k] == null ? (k === 'music' ? 0.6 : 0.8) : S.settings[k]));
function audioCtx() {
  if (!AU.ctx) { const C = window.AudioContext || window.webkitAudioContext; if (!C) return null; AU.ctx = new C(); try { if (navigator.audioSession) navigator.audioSession.type = 'playback'; } catch (_) {} }
  if (AU.ctx.state === 'suspended') AU.ctx.resume().catch(() => {});
  return AU.ctx;
}
async function loadBuf(url) {
  if (AU.bufs[url]) return AU.bufs[url];
  const ctx = audioCtx(); if (!ctx) return null;
  const data = await (await fetch(url)).arrayBuffer();
  AU.bufs[url] = await new Promise((res, rej) => ctx.decodeAudioData(data, res, rej));
  return AU.bufs[url];
}
function loopBounds(b) { // pomija ciszę dodaną przez koder MP3, żeby pętla była bez przerw
  const d = b.getChannelData(0); let s = 0, e = d.length - 1;
  while (s < d.length && Math.abs(d[s]) < 1e-4) s++; while (e > s && Math.abs(d[e]) < 1e-4) e--;
  return [s / b.sampleRate, (e + 1) / b.sampleRate];
}
function stopAmb(fade = 0.8) {
  const a = AU.amb; AU.amb = null; AU.ambSrc = null; if (!a || !AU.ctx) return;
  const t = AU.ctx.currentTime; try { a.g.gain.cancelScheduledValues(t); a.g.gain.setValueAtTime(a.g.gain.value, t); a.g.gain.linearRampToValueAtTime(0, t + fade); a.n.stop(t + fade + 0.05); } catch (_) {}
}
async function syncAudio() {
  const c = currentCaseId && CASES[currentCaseId]; const src = c && c.ambience;
  const want = S.settings.sound && src && !document.hidden;
  const my = ++AU.token;
  if (!want) { stopAmb(); return; }
  const ctx = audioCtx(); if (!ctx) return;
  if (AU.amb && AU.ambSrc === src) { AU.amb.g.gain.setTargetAtTime(vol('music') * 0.9, ctx.currentTime, 0.2); return; }
  stopAmb(0.6);
  let buf; try { buf = await loadBuf(src); } catch (_) { return; }
  if (my !== AU.token || !buf) return; // w międzyczasie zmieniono ustawienia lub sprawę
  const n = ctx.createBufferSource(); n.buffer = buf; n.loop = true;
  const [ls, le] = loopBounds(buf); n.loopStart = ls; n.loopEnd = le;
  const g = ctx.createGain(); g.gain.value = 0; n.connect(g).connect(ctx.destination);
  n.start(0, ls); g.gain.linearRampToValueAtTime(vol('music') * 0.9, ctx.currentTime + 2.5);
  AU.amb = { n, g }; AU.ambSrc = src;
}
async function sfx(name = 'paper') {
  if (!S.settings.sound) return;
  try { const ctx = audioCtx(); const b = await loadBuf(`assets/audio/sfx-${name}.mp3`); if (!ctx || !b) return;
    const n = ctx.createBufferSource(); n.buffer = b; const g = ctx.createGain(); g.gain.value = vol('fx'); n.connect(g).connect(ctx.destination); n.start(); } catch (_) {}
}
['pointerdown', 'keydown'].forEach(ev => document.addEventListener(ev, () => { if (S.settings.sound && (!AU.amb || (AU.ctx && AU.ctx.state !== 'running'))) syncAudio(); }, { passive: true }));
document.addEventListener('visibilitychange', () => { if (!AU.ctx) return; if (document.hidden) AU.ctx.suspend().catch(() => {}); else { AU.ctx.resume().catch(() => {}); syncAudio(); } });

/* ---------- toasty ---------- */
function toast(title, sub, label = 'Akta', evId) {
  const t = document.createElement('div'); t.className = 'toast';
  t.innerHTML = `<span class="stamp">${esc(label)}</span><div><b>${esc(title)}</b>${sub ? `<small>${esc(sub)}</small>` : ''}</div>`;
  if (evId) { t.style.cursor = 'pointer'; t.onclick = () => openOv({ type: 'ev', id: evId }); }
  const box = $('#toasts'); box.appendChild(t); while (box.children.length > 3) box.firstElementChild.remove();
  setTimeout(() => { t.classList.add('out'); setTimeout(() => t.remove(), 320); }, 3400);
}

/* ---------- routing ---------- */
function route() {
  const h = location.hash.replace(/^#\/?/, '').split('/').filter(Boolean);
  return { name: h[0] || 'home', id: h[1], sub: h[2] };
}
function go(path) { if (location.hash !== '#/' + path) location.hash = '#/' + path; else render(); }
window.addEventListener('hashchange', () => { ovStack = []; renderOv(); render(); });

/* ---------- nakładki (stos, z obsługą przycisku Wstecz) ---------- */
let ovStack = [];
function openOv(o) { ovStack.push(o); history.pushState({ ov: ovStack.length }, '', location.href); renderOv(); }
function closeOv() { if (!ovStack.length) return; if (history.state && history.state.ov) history.back(); else { ovStack.pop(); renderOv(); } }
window.addEventListener('popstate', () => { const depth = (history.state && history.state.ov) || 0; if (ovStack.length > depth) { ovStack = ovStack.slice(0, depth); renderOv(); } });
const topOv = () => ovStack[ovStack.length - 1];

/* ---------- render główny ---------- */
const app = () => $('#app');
async function render() {
  const r = route(); applySettings();
  try {
    if (r.name === 'teczka' && r.id) { currentCaseId = null; await renderFolder(r.id); }
    else if (r.name === 'sprawa' && r.id) { currentCaseId = r.id; await renderIntro(r.id); }
    else if (r.name === 'gra' && r.id) { currentCaseId = r.id; await renderGame(r.id, r.sub || 'akta'); }
    else { currentCaseId = null; await renderHome(); }
  } catch (err) {
    console.error(err);
    app().innerHTML = `<div class="section"><div class="empty"><h2>Nie udało się otworzyć akt</h2><p>${esc(err.message)}</p><p>Sprawdź połączenie przy pierwszym uruchomieniu — potem gra działa offline.</p><button class="btn" data-a="home">Wróć do archiwum</button></div></div>`;
  }
  document.body.classList.toggle('locked', r.name === 'gra');
  syncAudio();
}

/* ---------- ekran główny ---------- */
async function renderHome() {
  const cat = await getCatalog();
  const c1 = cat[0];
  const cards = cat.map(k => {
    const g = G(k.id);
    const status = !k.ready ? '' : g && g.report ? `<span class="chip status">Zamknięta · ${g.report.total} pkt</span>` : g ? '<span class="chip red status">W toku</span>' : '';
    return `<button class="case-card ${k.ready ? '' : 'soon'}" data-a="${k.ready ? 'open-case' : 'soon'}" data-id="${k.id}">
      <div class="cv" style="background-image:url('${esc(k.cover)}')"><span class="num">AKTA · ${esc(k.id)}</span>${k.ready ? '' : '<span class="seal">Ś</span>'}</div>
      ${status}
      <div class="body"><h3>${esc(k.title)}</h3><div class="tl">${esc(k.tagline)}</div>
      <div class="meta"><span class="chip">${esc(k.duration)}</span><span class="chip">${esc(k.players)} graczy</span><span class="chip">${k.ready ? esc(k.difficulty) : 'W przygotowaniu'}</span></div></div></button>`;
  }).join('');
  app().innerHTML = `<div class="home">
   <header class="hero"><div class="hero-bg" style="background-image:url('assets/art/001-manor.webp')"></div>
    <div class="hero-top"><span class="mini">Wydział spraw niewyjaśnionych</span><button class="icon-btn" data-a="settings" aria-label="Ustawienia">${I.gear}</button></div>
    <div class="hero-inner"><div class="logo">ŚLAD</div><div class="tag">Interaktywna gra detektywistyczna · 2–6 graczy</div>
     <p class="lead">Każda sprawa ma swoją prawdę. Wy macie jedną noc, żeby ją odkryć.</p>
     <div class="actions"><button class="btn" data-a="open-case" data-id="${c1.id}">${G(c1.id) ? 'Wróć do śledztwa' : 'Otwórz sprawę 001'}</button><button class="btn ghost" data-a="how">Jak grać</button></div></div>
   </header>
   <section class="section"><div class="section-head"><div><div class="eyebrow">Archiwum</div><h2>Akta spraw</h2></div></div><div class="cases">${cards}</div></section>
   <section class="section" id="how"><div class="section-head"><div><div class="eyebrow">Przy jednym stole</div><h2>Jak się gra</h2></div></div>
    <div class="how">
     <div class="step"><span class="eyebrow">01</span><b>Wybierzcie tryb</b><p><b style="display:inline;font-family:inherit;font-size:inherit">Wspólny stół</b> — wszystko na jednym ekranie, idealny we dwoje przy telewizorze. <b style="display:inline;font-family:inherit;font-size:inherit">Telewizor + telefony</b> — każdy ma w telefonie tajne akta, które widzi tylko on.</p></div>
     <div class="step"><span class="eyebrow">02</span><b>Śledztwo</b><p>Przeszukujcie miejsca, przesłuchujcie świadków, łamcie kłamstwa dowodami. Każdy ruch się liczy.</p></div>
     <div class="step"><span class="eyebrow">03</span><b>Dedukcja</b><p>Zagadki nie mają odpowiedzi w pytaniu. Trzeba połączyć dwa, trzy dokumenty — i nie dać się złapać w pułapki.</p></div>
     <div class="step"><span class="eyebrow">04</span><b>Akt oskarżenia</b><p>Wskażcie sprawcę, narzędzie, godzinę i motyw — i podeprzyjcie je dowodami. Raport oceni każdy wniosek.</p></div>
    </div></section>
   <footer class="foot"><span>ŚLAD · wersja ${VERSION}</span><span>Wszystkie postacie i zdarzenia są fikcyjne</span></footer></div>`;
}

/* ---------- wprowadzenie do sprawy ---------- */
let setupCount = 2; let setupNames = []; let setupMode = null;
async function renderIntro(id) {
  const c = await getCase(id); const g = G(id);
  if (!setupNames.length) setupNames = ['', '', '', '', '', ''];
  const names = Array.from({ length: setupCount }, (_, i) => `<div class="field"><label for="pn${i}">Gracz ${i + 1}</label><input class="input" id="pn${i}" data-name="${i}" maxlength="18" placeholder="Imię gracza ${i + 1}" value="${esc(setupNames[i])}"></div>`).join('');
  const rules = [...c.intro.rules, ...(setupMode && c.intro.modeRules ? [c.intro.modeRules[setupMode]] : [])];
  const tiles = Object.entries(MODES).map(([k, m]) => `<button class="mode ${setupMode === k ? 'on' : ''}" aria-pressed="${setupMode === k}" data-a="mode" data-m="${k}">
     <span class="mode-ic">${k === 'table' ? I.table : I.phones}</span><b>${esc(m.name)}</b><small>${esc(m.sub)}</small>
     <ul>${m.points.map(p => `<li>${esc(p)}</li>`).join('')}</ul><span class="mode-pick">${setupMode === k ? 'Wybrano' : 'Wybierz ten tryb'}</span></button>`).join('');
  const inProgress = g && !['distribute', 'qr'].includes(g.phase);
  app().innerHTML = `<div class="intro">
   <div class="intro-hero"><img src="${esc(c.keyart || c.cover)}" alt="${esc(c.title)} — plansza tytułowa"><button class="icon-btn back" data-a="home" aria-label="Archiwum">${I.back}</button></div>
   <div class="intro-wrap">
    <article class="paper brief"><span class="stamp">Ściśle tajne</span>
     <div class="eyebrow" style="color:var(--red)">Akta sprawy ${esc(c.id)} · ${esc(c.genre)}</div>
     <h1>${esc(c.title)}</h1><p class="lead">${esc(c.intro.lead)}</p>
     ${c.intro.brief.map(p => `<p>${esc(p)}</p>`).join('')}
     <h4>Zadanie zespołu</h4><ol>${c.intro.task.map(t => `<li>${esc(t)}</li>`).join('')}</ol>
     <h4>Parametry</h4><p>${esc(c.duration)} · ${esc(c.players)} graczy · trudność: ${esc(c.difficulty)}</p>
    </article>
    ${inProgress ? `<div class="setup"><div class="eyebrow">Śledztwo w toku · ${esc((MODES[g.mode] || { name: 'przekazywanie urządzenia' }).name)}</div><h3>${g.report ? 'Sprawa zamknięta' : 'Wróćcie do akt'}</h3>
      <p class="muted">Zespół: ${g.players.map(p => esc(p.name)).join(', ')} · ruchy: ${g.actions}${g.report ? ` · wynik: ${g.report.total} pkt` : ''}</p>
      <div class="row-actions"><button class="btn" data-a="continue" data-id="${c.id}">${g.report ? 'Zobacz raport' : 'Kontynuuj śledztwo'}</button><button class="btn ghost" data-a="restart" data-id="${c.id}">Zacznij od nowa</button></div></div>` :
    `<div class="setup"><div class="eyebrow">Krok 1 z 2</div><h3>Jak gracie?</h3>
      <div class="modes">${tiles}</div>
      <button class="tv-chip" data-a="tv" aria-pressed="${!!S.settings.tv}"><span class="switch" aria-hidden="true" aria-pressed="${!!S.settings.tv}"></span><span><b>Tryb telewizora</b> — większy tekst, czytelny z kanapy. ${S.settings.tv ? 'Włączony.' : 'Włącz, jeśli gracie na telewizorze.'} Zmienisz go też w ustawieniach (⚙).</span></button>
    </div>
    ${setupMode ? `<div class="setup"><div class="eyebrow">Krok 2 z 2</div><h3>Kto siada do stołu?</h3>
      <p class="muted">${setupMode === 'table' ? 'Imiona przydadzą się do podziału ról w zespole. Każdy dostanie funkcję, która podpowiada, czym się zająć.' : 'Za chwilę na ekranie pojawi się kod QR dla każdego gracza. Każdy skanuje swój — i nie pokazuje telefonu reszcie.'}</p>
      <div class="count" role="group" aria-label="Liczba graczy">${[2, 3, 4, 5, 6].map(n => `<button aria-pressed="${n === setupCount}" data-a="count" data-n="${n}">${n}</button>`).join('')}</div>
      <div class="names">${names}</div>
      <details class="rules"><summary>Zasady tej sprawy</summary><ul>${rules.map(r => `<li>${esc(r)}</li>`).join('')}</ul></details>
      <button class="btn block" data-a="begin" data-id="${c.id}">${setupMode === 'table' ? 'Rozpocznij śledztwo' : 'Rozdaj tajne akta'}</button></div>` : ''}`}
   </div></div>`;
}

/* --- rozdanie kodów QR (Telewizor + telefony) --- */
const b64u = s => btoa(unescape(encodeURIComponent(s))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const unb64u = s => decodeURIComponent(escape(atob(s.replace(/-/g, '+').replace(/_/g, '/'))));
function folderURL(c, g, i) {
  const pl = g.players[i];
  const payload = b64u(JSON.stringify({ c: c.id, n: pl.name, r: pl.role, e: g.priv[i] || [], s: g.created }));
  return location.href.split('#')[0] + '#/teczka/' + payload;
}
function qrSVG(text) {
  if (typeof qrcode !== 'function') return '<p class="muted">Generator kodów QR niedostępny.</p>';
  const q = qrcode(0, 'M'); q.addData(text); q.make();
  return q.createSvgTag({ cellSize: 6, margin: 3, scalable: true });
}
function renderQR(c, g) {
  app().innerHTML = `<div class="qr-screen"><div class="eyebrow">Telewizor + telefony · rozdanie tajnych akt</div>
   <h2>Zeskanujcie swoje teczki</h2>
   <p class="muted">Każdy otwiera aparat w telefonie, celuje w kod ze swoim imieniem i dotyka linku. Nie pokazujcie sobie telefonów. Kod działa też później — znajdziecie go w <b>Analiza → Tajne akta</b>.</p>
   <div class="qr-grid">${g.players.map((pl, i) => `<div class="qr-card"><div class="qr">${qrSVG(folderURL(c, g, i))}</div><b>${esc(pl.name)}</b><small>${esc(ROLES.find(r => r.id === pl.role).name)}</small>
     <button class="btn small ghost" data-a="priv" data-i="${i}">Nie mam telefonu — pokaż tutaj</button></div>`).join('')}</div>
   <button class="btn" data-a="qr-done">Wszyscy mają swoje akta — zaczynamy</button></div>`;
}

/* --- teczka gracza na jego telefonie --- */
async function renderFolder(payload) {
  let d; try { d = JSON.parse(unb64u(payload)); } catch (_) { app().innerHTML = '<div class="section"><div class="empty"><h2>Nieprawidłowy kod</h2><p>Zeskanujcie kod jeszcze raz z głównego ekranu.</p></div></div>'; return; }
  const c = await getCase(d.c); const role = ROLES.find(r => r.id === d.r) || ROLES[0];
  const g = { created: d.s };
  app().innerHTML = `<div class="folder"><div class="folder-top"><div class="logo">ŚLAD</div><span class="stamp" style="color:#e8695e;border-color:#e8695e">Tylko dla: ${esc(d.n)}</span></div>
   <p class="muted">Sprawa ${esc(c.id)} · ${esc(c.title)}. Nie pokazuj tego ekranu innym graczom. Gra toczy się na wspólnym ekranie — tutaj masz tylko swoje tajne akta.</p>
   <div class="role-card"><span class="eyebrow">Twoja funkcja w zespole</span><br><b>${esc(role.name)}</b><p class="muted" style="margin:.4em 0 0">${esc(role.tip)}</p></div>
   <p style="margin-top:18px">Chcesz pokazać dokument wszystkim? Na wspólnym ekranie wybierz <b>Analiza → Tajne akta → Ujawnij dokument</b> i wpisz jego kod.</p>
   ${(d.e || []).filter(id => c.ev[id]).map(id => `<div class="code-tag">Kod do ujawnienia: <b>${esc(codeFor(g, id))}</b></div>${docHTML(c, c.ev[id], true)}`).join('')}
   <p class="muted" style="text-align:center;margin:30px 0 10px">Możesz zablokować telefon — ta strona zostanie w przeglądarce.</p></div>`;
}

/* ---------- gra ---------- */
async function renderGame(id, tab) {
  const g = G(id); const c = variant(await getCase(id), g && g.mode);
  if (!g) return go('sprawa/' + id);
  if (g.phase === 'distribute') return renderDistribute(c, g);
  if (g.phase === 'qr') return renderQR(c, g);
  if (tab === 'raport' && !g.report) return renderShell(c, g, 'analiza', renderReport(c, g));
  if (tab === 'wynik' || (tab === 'raport' && g.report)) { if (!g.report) return go(`gra/${id}/analiza`); return renderShell(c, g, 'analiza', renderResult(c, g)); }
  const views = { akta: viewFiles, miejsca: viewPlaces, osoby: viewPeople, analiza: viewAnalysis, tablica: viewBoard };
  const view = views[tab] || viewFiles;
  renderShell(c, g, views[tab] ? tab : 'akta', view(c, g));
  if (tab === 'tablica') mountBoard(c, g);
}
function renderShell(c, g, tab, inner) {
  const n = unread(g, c);
  const tabs = [['akta', 'Akta', I.files], ['miejsca', 'Miejsca', I.map], ['osoby', 'Osoby', I.people], ['analiza', 'Analiza', I.brain], ['tablica', 'Tablica', I.board]];
  const keepScroll = app().querySelector('.main') && app().dataset.tab === tab ? app().querySelector('.main').scrollTop : 0;
  app().dataset.tab = tab;
  app().innerHTML = `<div class="shell">
   <header class="topbar"><button class="icon-btn" data-a="home" aria-label="Archiwum">${I.back}</button>
    <div class="t"><small>Akta ${esc(c.id)}${g.report ? ' · zamknięta' : ''}</small><b>${esc(c.title)}</b></div>
    <div class="moves" title="Ruchy śledcze">Ruchy<b>${g.actions}</b></div>
    ${g.report ? '' : `<button class="icon-btn" data-a="trop" aria-label="Trop — podpowiedź">${I.bulb}</button>`}
    <button class="icon-btn hide-sm" data-a="sound" aria-label="Dźwięk">${S.settings.sound ? I.sound : I.mute}</button>
    <button class="icon-btn" data-a="case-menu" aria-label="Menu sprawy">${I.menu}</button></header>
   <nav class="nav" aria-label="Sekcje śledztwa"><div class="brand-rail"><div class="logo">ŚLAD</div><small>Akta ${esc(c.id)}</small></div>
    ${tabs.map(([k, l, ic]) => `<button data-a="tab" data-tab="${k}" ${k === tab ? 'aria-current="page"' : ''}>${ic}<span>${l}</span>${k === 'akta' && n ? `<span class="badge">${n}</span>` : ''}</button>`).join('')}</nav>
   <main class="main" id="main"><div class="main-inner">${inner}</div></main></div>`;
  if (keepScroll) app().querySelector('.main').scrollTop = keepScroll;
}

/* --- dystrybucja tajnych akt --- */
let distRevealed = false;
function renderDistribute(c, g) {
  const p = g.players[g.distIdx]; const role = ROLES.find(r => r.id === p.role);
  if (!distRevealed) {
    app().innerHTML = `<div class="pass"><div class="eyebrow">Tajne akta · ${g.distIdx + 1} z ${g.players.length}</div>
     <p>Przekażcie urządzenie graczowi:</p><div class="who">${esc(p.name)}</div><p>Pozostali niech nie patrzą. Złam pieczęć, gdy trzymasz urządzenie tylko ty.</p>
     <button class="seal" data-a="dist-open" aria-label="Złam pieczęć">Ś</button><span class="eyebrow">Dotknij pieczęci</span></div>`;
    return;
  }
  app().innerHTML = `<div class="pass" style="justify-content:flex-start"><div class="eyebrow">Tylko dla: ${esc(p.name)}</div>
   <div class="role-card"><span class="eyebrow">Twoja funkcja w zespole</span><br><b>${esc(role.name)}</b><p class="muted" style="margin:.4em 0 0">${esc(role.tip)}</p></div>
   <p style="margin-top:18px">Twoje tajne akta. Zapamiętaj je. Później możesz je przeczytać ponownie i ujawnić zespołowi w zakładce <b>Analiza → Tajne akta</b>.</p>
   <div class="private-list">${g.priv[g.distIdx].map(id => docHTML(c, c.ev[id], true)).join('')}</div>
   <button class="btn" data-a="dist-next">${g.distIdx + 1 < g.players.length ? 'Zamknij teczkę i przekaż dalej' : 'Zamknij teczkę i zacznij śledztwo'}</button></div>`;
  $('.pass').scrollTop = 0;
}

/* --- dokument --- */
function blocksHTML(body) {
  return (body || []).map(b => {
    if (typeof b === 'string') return `<p>${esc(b)}</p>`;
    if (b.h) return `<h5>${esc(b.h)}</h5>`;
    if (b.kv) return `<dl class="kv">${b.kv.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>`;
    if (b.log) return `<div class="log">${b.log.map(esc).join('\n')}</div>`;
    if (b.quote) return `<blockquote class="quote">${esc(b.quote)}${b.by ? `<cite>— ${esc(b.by)}</cite>` : ''}</blockquote>`;
    if (b.note) return `<div class="note">${esc(b.note)}</div>`;
    return '';
  }).join('');
}
function docHTML(c, e, compact) {
  const kind = e.private ? 'Tajne akta' : e.testimony ? 'Protokół' : 'Dowód';
  return `<article class="paper doc"><div class="dh"><div><small>Akta ${esc(c.id)} · ${kind} ${esc(e.id.toUpperCase())}</small><h3>${esc(e.title)}</h3></div><span class="stamp">${esc(e.type)}</span></div>
   ${imgsOf(e).length ? `<div class="photos">${imgsOf(e).map((src, i) => `<figure class="photo" style="--rot:${i % 2 ? '1.6deg' : '-1.2deg'}"><img src="${esc(src)}" alt="${esc(e.title)}" loading="lazy"></figure>`).join('')}</div>` : ''}
   ${compact ? '' : `<p style="font-style:italic;color:var(--paperMuted);margin-top:0">${esc(e.summary)}</p>`}${blocksHTML(e.body)}</article>`;
}

/* --- AKTA --- */
let filesFilter = 'all';
const imgsOf = e => !e.img ? [] : Array.isArray(e.img) ? e.img : [e.img];
function evCard(c, g, id) {
  const e = c.ev[id]; const isNew = !g.read.includes(id); const im = imgsOf(e)[0];
  return `<button class="ev ${e.testimony ? 'testimony' : ''} ${e.private ? 'private' : ''}" style="--rot:${rot(id)}" data-a="ev" data-id="${id}">
   ${isNew ? '<span class="new">NOWE</span>' : ''}${im ? `<span class="thumb" style="background-image:url('${esc(im)}')"></span>` : ''}<span class="type">${esc(e.type)}</span><h4>${esc(e.title)}</h4><p>${esc(e.summary)}</p><span class="id">${esc(id.toUpperCase())}</span></button>`;
}
function viewFiles(c, g) {
  let ids = visibleEvidence(g, c).slice().reverse();
  const counts = { all: ids.length, docs: ids.filter(i => !c.ev[i].testimony && !c.ev[i].private).length, test: ids.filter(i => c.ev[i].testimony).length, priv: ids.filter(i => c.ev[i].private).length };
  if (filesFilter === 'docs') ids = ids.filter(i => !c.ev[i].testimony && !c.ev[i].private);
  if (filesFilter === 'test') ids = ids.filter(i => c.ev[i].testimony);
  if (filesFilter === 'priv') ids = ids.filter(i => c.ev[i].private);
  const total = c.evidence.length;
  return `<div class="page-head"><div><div class="eyebrow">Materiał dowodowy</div><h2>Akta sprawy</h2><p>Zebrane dokumenty, fotografie i protokoły${c.mode === 'table' ? '' : ' oraz ujawnione tajne akta'}. Zebrano ${visibleEvidence(g, c).length} z ${total} pozycji.</p></div></div>
   <div class="tabs" role="group">${[['all', 'Wszystkie'], ['docs', 'Dowody'], ['test', 'Protokoły'], ...(c.mode === 'table' ? [] : [['priv', 'Ujawnione tajne']])].map(([k, l]) => `<button aria-pressed="${filesFilter === k}" data-a="filter" data-f="${k}">${l} · ${counts[k]}</button>`).join('')}</div>
   ${ids.length ? `<div class="ev-grid">${ids.map(id => evCard(c, g, id)).join('')}</div>` : '<div class="empty">Brak materiałów w tej kategorii.</div>'}`;
}

/* --- MIEJSCA --- */
const ART_POS = ['30% 45%', '75% 35%', '50% 80%', '15% 70%', '90% 55%', '55% 20%'];
function locArt(c, l, i) { const img = l.img || (i % 2 ? c.cover : (c.art || c.cover)); return `background-image:url('${esc(img)}');background-position:${l.img ? 'center' : ART_POS[i % ART_POS.length]};${l.img ? '' : 'filter:saturate(.6) brightness(.75)'}`; }
function viewPlaces(c, g) {
  return `<div class="page-head"><div><div class="eyebrow">Plan miejsc</div><h2>Miejsca</h2><p>Każde przeszukanie punktu to jeden ruch. Niektóre punkty otworzycie dopiero, gdy będziecie wiedzieć, czego szukać.</p></div></div>
  <div class="loc-grid">${c.locations.map((l, i) => {
    const done = l.spots.filter(s => g.spots.includes(s.id)).length;
    return `<button class="loc" data-a="loc" data-id="${l.id}"><div class="art" style="${locArt(c, l, i)}"></div><div class="in"><div class="k">${String(i + 1).padStart(2, '0')} · ${esc(l.kind)}</div><h3>${esc(l.name)}</h3>
     <div class="muted" style="font-size:.88rem">${esc(l.desc)}</div><div class="prog">${l.spots.map(s => `<i class="${g.spots.includes(s.id) ? 'on' : ''}"></i>`).join('')}</div>
     <small class="eyebrow" style="display:block;margin-top:6px">${done}/${l.spots.length} punktów</small></div></button>`;
  }).join('')}</div>`;
}
function spotState(c, g, s) {
  if (g.spots.includes(s.id)) return 'done';
  if (s.requires && s.requires.puzzle && !has(g, c, s.requires.puzzle)) return 'locked';
  return 'open';
}
function ovLocation(c, g, id) {
  const l = c.loc[id]; const i = c.locations.indexOf(l);
  return { title: l.name, kicker: l.kind, full: true, body: `<div class="scene" style="${locArt(c, l, i)}"><div class="in"><div class="eyebrow">${esc(l.kind)}</div><h2>${esc(l.name)}</h2></div></div>
   <p style="margin:14px 2px 0;color:#d6cebf">${esc(l.desc)}</p>
   <div class="spots">${l.spots.map((s, k) => {
     const st = spotState(c, g, s);
     const found = st === 'done' ? (s.gives || []).filter(e => known(g, e)) : [];
     return `<div class="spot ${st}"><span class="tent">${k + 1}</span><div style="flex:1"><b>${esc(s.name)}</b>
       <p>${esc(st === 'locked' ? s.lockedText : s.text)}</p>
       ${st === 'done' ? `<div class="found-list">${found.map(e => `<button class="chip" data-a="ev" data-id="${e}">${esc(c.ev[e].title)}</button>`).join('')}</div>` : ''}
       ${st === 'open' ? `<div class="act"><button class="btn small" data-a="search" data-id="${s.id}">Przeszukaj · 1 ruch</button></div>` : ''}
       ${st === 'locked' && s.requires.puzzle ? `<div class="act"><button class="btn small ghost" data-a="puzzle-from-spot" data-id="${s.requires.puzzle}">${I.lock} ${esc(c.puzzle[s.requires.puzzle].title)}</button></div>` : ''}
     </div></div>`;
   }).join('')}</div>` };
}
function doSearch(c, g, sid) {
  const s = c.spot[sid]; if (g.spots.includes(sid) || spotState(c, g, s) === 'locked') return;
  g.actions++; g.spots.push(sid); gain(g, c, s.gives); save();
}

/* --- OSOBY --- */
function portrait(p, g, cls = '') { return `<div class="polaroid ${cls}" style="--rot:${rot(p.id)}"><div class="ph" ${p.img ? `style="background-image:url('${esc(p.img)}')"` : ''}>${p.img ? '' : `<span>${esc(initials(personName(g, p)))}</span>`}</div><div class="cap">${esc(personName(g, p))}</div></div>`; }
const initials = n => n.replace(/[„”"]/g, '').split(/\s+/).map(w => w[0]).join('').slice(0, 2).toUpperCase();
function availableQs(c, g, p) { return p.questions.filter(q => (!q.requires || q.requires.every(r => has(g, c, r))) && (!q.requiresAny || q.requiresAny.some(r => has(g, c, r)))); }
function openStatements(g, p) { return p.statements.filter(s => g.claims.includes(s.id)); }
function viewPeople(c, g) {
  return `<div class="page-head"><div><div class="eyebrow">Przesłuchania</div><h2>Osoby</h2><p>Każde pytanie to jeden ruch. Zeznania, które padną, trafiają do protokołu — możecie je podważyć dowodem. Nietrafiona konfrontacja kosztuje 2 punkty.</p></div></div>
  <div class="ppl-grid">${c.people.map(p => {
    const qs = availableQs(c, g, p); const left = qs.filter(q => !g.asked.includes(q.id)).length;
    const br = p.statements.filter(s => g.broken.includes(s.id)).length;
    return `<button class="person" data-a="person" data-id="${p.id}">${portrait(p, g)}<div class="info"><b>${esc(personName(g, p))}</b><small>${esc(personRole(g, p))}</small>
     <div class="tally">${left ? `<span class="chip">${left} nowe pytania</span>` : ''}${br ? `<span class="chip red">${br} podważone</span>` : ''}</div></div></button>`;
  }).join('')}</div>`;
}
function ovPerson(c, g, id, mode) {
  const p = c.person[id]; const log = g.log[id] || [];
  const qs = availableQs(c, g, p); const stm = openStatements(g, p);
  const head = `<div class="room-head">${portrait(p, g)}<div><div class="eyebrow">${esc(personRole(g, p))}${p.age ? ' · ' + p.age + ' l.' : ''}</div><h3>${esc(personName(g, p))}</h3><p>${esc(p.desc)}</p></div></div>
   <div class="tabs"><button aria-pressed="${mode !== 'stmt'}" data-a="pmode" data-id="${id}" data-m="talk">Rozmowa</button><button aria-pressed="${mode === 'stmt'}" data-a="pmode" data-id="${id}" data-m="stmt">Protokół zeznań · ${stm.length}</button><button data-a="pin" data-key="p:${id}">${I.pin} Na tablicę</button></div>`;
  if (mode === 'stmt') {
    return { title: personName(g, p), kicker: 'Protokół zeznań', full: true, body: head + (stm.length ? `<p class="muted" style="font-size:.9rem">Wybierzcie zeznanie i wskażcie dowód, który mu przeczy. Prawdziwe zeznania też tu są — nie każde zdanie to kłamstwo.</p>
     <div class="stmts">${stm.map(s => { const b = g.broken.includes(s.id); return `<div class="stmt ${b ? 'broken' : ''}"><q>${esc(s.text)}</q><div class="row"><span class="eyebrow">${b ? 'Podważone' : 'Zeznanie'}</span>${b ? '' : `<button class="btn small red" data-a="confront" data-id="${s.id}">Konfrontuj</button>`}</div></div>`; }).join('')}</div>` : '<div class="empty">Ta osoba nie złożyła jeszcze żadnych twierdzeń. Zacznijcie od pytań.</div>') };
  }
  const tr = log.map(m => m.t === 'q' ? `<div class="tq">${esc(m.text)}</div>` : `<div class="ta ${m.t === 'break' ? 'break' : m.t === 'deflect' ? 'deflect' : ''}"><span class="who">${esc(personName(g, p))}${m.t === 'break' ? ' · po konfrontacji' : ''}</span>${esc(m.text)}</div>`).join('');
  return { title: personName(g, p), kicker: 'Przesłuchanie', full: true, body: head + `<div class="transcript" id="transcript">${tr || '<p class="muted">Rozmowa jeszcze się nie zaczęła.</p>'}</div>
   <div class="eyebrow" style="margin:18px 0 8px">Zadaj pytanie · 1 ruch</div>
   <div class="qlist">${qs.map(q => `<button class="q ${g.asked.includes(q.id) ? 'asked' : ''}" data-a="ask" data-id="${q.id}" ${g.asked.includes(q.id) ? 'disabled' : ''}>${esc(q.q)}</button>`).join('')}</div>
   ${qs.length < p.questions.length ? `<p class="muted" style="font-size:.85rem;margin-top:10px">Kolejne pytania pojawią się, gdy zdobędziecie odpowiednie materiały.</p>` : ''}` };
}
function doAsk(c, g, qid) {
  const q = c.q[qid]; if (g.asked.includes(qid)) return;
  g.actions++; g.asked.push(qid);
  (g.log[q.person] = g.log[q.person] || []).push({ t: 'q', text: q.q }, { t: 'a', text: q.a });
  (q.claims || []).forEach(s => { if (!g.claims.includes(s)) g.claims.push(s); });
  gain(g, c, q.gives); save();
}
function ovConfront(c, g, sid) {
  const s = c.stmt[sid]; const p = c.person[s.person];
  const ids = visibleEvidence(g, c);
  return { title: 'Konfrontacja', kicker: personName(g, p), body: `<div class="stmt"><q>${esc(s.text)}</q></div>
   <p class="muted" style="margin:14px 0 4px">Który materiał przeczy temu zeznaniu? Konfrontacja kosztuje 1 ruch; nietrafiona dodatkowo 2 punkty.</p>
   <div class="pick">${ids.map(id => `<button data-a="confront-with" data-s="${sid}" data-id="${id}"><small>${esc(c.ev[id].type)} · ${esc(id.toUpperCase())}</small>${esc(c.ev[id].title)}</button>`).join('')}</div>` };
}
function doConfront(c, g, sid, evid) {
  const s = c.stmt[sid]; const p = c.person[s.person];
  const L = (g.log[p.id] = g.log[p.id] || []);
  g.actions++;
  L.push({ t: 'q', text: `Konfrontacja: „${s.text}” — okazujemy: ${c.ev[evid].title}.` });
  if (!s.truth && (s.contradicts || []).includes(evid)) {
    g.broken.push(sid); L.push({ t: 'break', text: s.response });
    (s.reveals || []).forEach(r => { if (!g.claims.includes(r)) g.claims.push(r); });
    gain(g, c, s.gives); save();
    toast('Zeznanie podważone', personName(g, p), 'Przełom'); sfx('break');
    return true;
  }
  g.failed++; const d = p.deflect || ['To niczego nie dowodzi.'];
  L.push({ t: 'deflect', text: d[g.failed % d.length] }); save();
  toast('Nietrafiona konfrontacja', '−2 punkty w raporcie', 'Błąd'); sfx('wrong');
  return false;
}

/* --- ANALIZA --- */
let anaTab = 'zagadki';
function puzzleVisible(c, g, pz) { return pz.requires.every(r => has(g, c, r)); }
function viewAnalysis(c, g) {
  const tabs = [['zagadki', 'Zagadki'], ['czas', 'Oś czasu'], ...(c.mode === 'table' ? [] : [['tajne', 'Tajne akta']]), ['notatki', 'Notatki']];
  if (c.mode === 'table' && anaTab === 'tajne') anaTab = 'zagadki';
  let inner = '';
  if (anaTab === 'zagadki') {
    const vis = c.puzzles.filter(pz => puzzleVisible(c, g, pz));
    inner = vis.length ? `<div class="cards2">${vis.map(pz => { const st = g.puzzles[pz.id] || {}; return `<div class="panel ${st.solved ? 'solved' : ''}"><div class="eyebrow">${esc(pz.kind)}</div><h3>${esc(pz.title)}</h3><p>${esc(pz.prompt)}</p>
      ${st.solved ? `<div class="result-ok"><b>Rozwiązane.</b> ${esc(pz.solution)}</div>` : `<button class="btn small" data-a="puzzle" data-id="${pz.id}">Rozwiąż</button>`}</div>`; }).join('')}</div>
      ${vis.length < c.puzzles.length ? `<p class="muted" style="margin-top:14px">Pozostałe zagadki (${c.puzzles.length - vis.length}) pojawią się, gdy zdobędziecie potrzebne materiały.</p>` : ''}` : '<div class="empty">Na razie brak zagadek. Zbierajcie materiały — pojawią się same.</div>';
  }
  if (anaTab === 'czas') inner = timelineHTML(c, g);
  if (anaTab === 'tajne' && g.mode === 'phones') inner = `<p class="muted">Każdy ma swoją teczkę w telefonie. Żeby ujawnić dokument na wspólnym ekranie, wpiszcie jego kod — widnieje przy dokumencie w telefonie.</p>
    <button class="btn" data-a="reveal">Ujawnij dokument z teczki</button>
    <div class="cards2" style="margin-top:16px">${g.players.map((pl, i) => { const all = g.priv[i] || []; const sh = all.filter(id => g.shared.includes(id)).length; return `<div class="panel"><div class="eyebrow">${esc(ROLES.find(r => r.id === pl.role).name)}</div><h3>${esc(pl.name)}</h3><p>Teczka: ${all.length} dokumenty · ujawnione: ${sh}</p><div class="row-actions"><button class="btn small ghost" data-a="qr" data-i="${i}">Pokaż kod QR</button><button class="btn small ghost" data-a="priv" data-i="${i}">${I.lock} Pokaż na tym ekranie</button></div></div>`; }).join('')}</div>`;
  else if (anaTab === 'tajne') inner = `<p class="muted">Każdy gracz ma swoje tajne akta. Przekażcie urządzenie właścicielowi — tylko on może je przeczytać i zdecydować o ujawnieniu.</p>
    <div class="cards2">${g.players.map((pl, i) => { const all = g.priv[i] || []; const sh = all.filter(id => g.shared.includes(id)).length; return `<div class="panel"><div class="eyebrow">${esc(ROLES.find(r => r.id === pl.role).name)}</div><h3>${esc(pl.name)}</h3><p>Teczka: ${all.length} dokumenty · ujawnione: ${sh}</p><button class="btn small ghost" data-a="priv" data-i="${i}">${I.lock} Otwórz teczkę</button></div>`; }).join('')}</div>`;
  if (anaTab === 'notatki') inner = `<div class="field"><label for="notes">Wspólne notatki zespołu</label><textarea class="input" id="notes" data-notes placeholder="Hipotezy, podejrzenia, pytania do sprawdzenia…">${esc(g.notes)}</textarea></div>`;
  return `<div class="page-head"><div><div class="eyebrow">Warsztat dedukcji</div><h2>Analiza</h2><p>Zagadki, oś czasu, tajne akta i notatki. Gdy jesteście pewni — złóżcie akt oskarżenia.</p></div></div>
   <div class="tabs">${tabs.map(([k, l]) => `<button aria-pressed="${anaTab === k}" data-a="ana" data-t="${k}">${l}</button>`).join('')}</div>${inner}
   ${g.report ? `<button class="big-cta" data-a="tab" data-tab="wynik"><span class="seal">Ś</span><span><b>Raport złożony</b><span class="muted">Wynik: ${g.report.total} pkt — zobacz rozwiązanie</span></span></button>` :
   `<button class="big-cta" data-a="tab" data-tab="raport"><span class="seal">Ś</span><span><b>Akt oskarżenia</b><span class="muted">Złóżcie raport końcowy. Po podpisaniu nie da się go zmienić.</span></span></button>`}`;
}
function timeFacts(c, g) {
  const f = [];
  visibleEvidence(g, c).forEach(id => (c.ev[id].time || []).forEach(t => f.push({ k: t[0], text: t[1], src: t[2] })));
  g.asked.forEach(qid => (c.q[qid].time || []).forEach(t => f.push({ k: t[0], text: t[1], src: t[2] })));
  g.broken.forEach(sid => (c.stmt[sid].time || []).forEach(t => f.push({ k: t[0], text: t[1], src: t[2] })));
  c.puzzles.forEach(pz => { if (g.puzzles[pz.id] && g.puzzles[pz.id].solved) (pz.reward.time || []).forEach(t => f.push({ k: t[0], text: t[1], src: t[2], key: true })); });
  const seen = new Set(); return f.filter(x => { const k = x.k + x.text; if (seen.has(k)) return false; seen.add(k); return true; }).sort((a, b) => a.k.localeCompare(b.k));
}
function timelineHTML(c, g) {
  const f = timeFacts(c, g); if (!f.length) return '<div class="empty">Oś czasu wypełni się godzinami z zebranych materiałów i zeznań.</div>';
  let day = ''; let out = '<p class="muted">Godziny z dokumentów i zeznań, w kolejności. Zeznania to wersje świadków — nie fakty. Surowe dane techniczne trafią tu dopiero wtedy, gdy je przeanalizujecie.</p><div class="tl">';
  f.forEach(x => {
    const [d, t] = x.k.split(' '); const [y, m, dd] = d.split('-').map(Number);
    if (d !== day) { day = d; const dt = new Date(y, m - 1, dd); out += `<div class="tl-day">${DAYS[dt.getDay()]}, ${dd} ${MONTHS[m - 1]} ${y}</div>`; }
    out += `<div class="tl-item ${x.key ? 'key' : ''}"><time>${t && t !== '00:00' ? t : '—'}</time><p>${esc(x.text)}</p><small>Źródło: ${esc(x.src)}</small></div>`;
  });
  return out + '</div>';
}

/* zagadka */
let dialVals = {};
function ovPuzzle(c, g, id, msg) {
  const pz = c.puzzle[id]; const st = g.puzzles[id] || { hints: 0, attempts: 0 };
  if (!dialVals[id]) dialVals[id] = [0, 0, 0, 0];
  let input = '';
  if (pz.input === 'digits4' || pz.input === 'time') {
    input = `<div class="dials">${dialVals[id].map((v, i) => `${pz.input === 'time' && i === 2 ? '<span class="dial-sep">:</span>' : ''}<div class="dial"><button data-a="dial" data-id="${id}" data-i="${i}" data-d="1" aria-label="W górę">▲</button><div class="num">${v}</div><button data-a="dial" data-id="${id}" data-i="${i}" data-d="-1" aria-label="W dół">▼</button></div>`).join('')}</div>`;
  } else if (pz.input === 'number') input = `<div class="field" style="margin:16px 0;max-width:260px"><label for="pzin">Liczba</label><input class="input" id="pzin" inputmode="decimal" autocomplete="off" placeholder="np. 123" style="font-family:var(--f-mono);font-size:1.6rem"></div>`;
  else input = `<div class="field" style="margin:16px 0"><label for="pzin">Odpowiedź</label><input class="input" id="pzin" autocomplete="off" placeholder="Wpiszcie odpowiedź"></div>`;
  const hints = pz.hints.slice(0, st.hints || 0).map((h, i) => `<div class="hint-box"><span class="eyebrow">Podpowiedź ${i + 1}</span><br>${esc(h)}</div>`).join('');
  return { title: pz.title, kicker: pz.kind, body: st.solved ? `<div class="result-ok"><b>Rozwiązane.</b> ${esc(pz.solution)}</div>` :
   `<p style="font-family:var(--f-display);font-size:1.3rem;margin-top:0">${esc(pz.prompt)}</p>
   <p class="muted" style="font-size:.88rem">Potrzebne materiały: ${pz.requires.map(r => c.ev[r] ? `<button class="chip" data-a="ev" data-id="${r}">${esc(c.ev[r].title)}</button>` : '').join(' ')} ${c.mode === 'table' ? '— i może coś, czego dowiecie się w centrali.' : '— i może coś, co ma ktoś z was w tajnych aktach.'}</p>
   ${input}${msg ? `<div class="result-bad">${esc(msg)}</div>` : ''}${hints}
   <div class="row-actions"><button class="btn" data-a="solve" data-id="${id}">Sprawdź</button>${(st.hints || 0) < pz.hints.length ? `<button class="btn ghost" data-a="phint" data-id="${id}">Podpowiedź (−2 pkt)</button>` : ''}</div>
   <p class="muted" style="font-size:.8rem;margin-top:12px">Próby: ${st.attempts || 0}. Błędne próby nie kosztują punktów.</p>` };
}
function doSolve(c, g, id) {
  const pz = c.puzzle[id]; const st = (g.puzzles[id] = g.puzzles[id] || { hints: 0, attempts: 0 });
  let val;
  if (pz.input === 'digits4' || pz.input === 'time') val = dialVals[id].join('');
  else val = ($('#pzin') || {}).value || '';
  const num = parseFloat(String(val).replace(',', '.').replace(/[^0-9.\-]/g, ''));
  const ok = pz.input === 'text' ? pz.answers.some(a => norm(a) === norm(val))
    : pz.input === 'number' ? !isNaN(num) && pz.answers.some(a => { const [lo, hi] = String(a).split('-').map(Number); return num >= lo && num <= (isNaN(hi) ? lo : hi); })
    : pz.answers.some(a => digits(a) === digits(val));
  st.attempts++;
  if (!ok) { save(); sfx('wrong'); return pz.input === 'digits4' ? 'Zamek ani drgnie.' : pz.input === 'number' ? 'Ta liczba nie zgadza się z materiałem. Policzcie jeszcze raz.' : pz.input === 'time' ? 'Ta godzina nie zgadza się z danymi. Sprawdźcie jeszcze raz.' : 'To nie pasuje do materiału. Spróbujcie inaczej.'; }
  st.solved = true;
  if (pz.reward && pz.reward.search) (pz.reward.spots || []).forEach(s => { if (!g.spots.includes(s)) { g.spots.push(s); gain(g, c, c.spot[s].gives); } });
  save(); toast(pz.title, 'Zagadka rozwiązana', 'Rozwiązane'); sfx('unlock');
  return null;
}

/* tajne akta po dystrybucji */
function ovPrivate(c, g, i, opened) {
  const pl = g.players[i];
  if (!opened) return { title: 'Tajne akta', kicker: pl.name, body: `<div style="text-align:center;padding:20px 0"><p>Przekażcie urządzenie graczowi</p><div class="who" style="font-family:var(--f-display);font-size:2.6rem">${esc(pl.name)}</div><p class="muted">Tylko ${esc(pl.name)} powinien teraz patrzeć.</p><button class="seal" style="width:96px;height:96px;margin:18px auto;border:0;font-size:2.4rem" data-a="priv-open" data-i="${i}">Ś</button></div>` };
  return { title: 'Tajne akta', kicker: pl.name, full: true, body: (g.priv[i] || []).map(id => `${docHTML(c, c.ev[id], true)}<div class="row-actions" style="margin:10px 0 26px">${g.shared.includes(id) ? '<span class="chip">Ujawnione zespołowi</span>' : `<button class="btn small" data-a="share" data-id="${id}" data-i="${i}">Ujawnij zespołowi</button>`}</div>`).join('') };
}

/* --- TABLICA --- */
function boardLabel(c, g, key) {
  const [t, id] = key.split(':');
  if (t === 'ev') return { kind: 'ev', title: c.ev[id] ? c.ev[id].title : '?', sub: c.ev[id] ? c.ev[id].type : '' };
  if (t === 'p') { const p = c.person[id]; return { kind: 'person', title: p ? personName(g, p) : '?', p }; }
  return { kind: 'note', title: (g.board.items.find(x => x.key === key) || {}).text || '' };
}
let boardSel = null, linkMode = false;
function viewBoard(c, g) {
  return `<div class="page-head"><div><div class="eyebrow">Tablica śledcza</div><h2>Tablica</h2><p>Przypinajcie dowody i osoby z akt i przesłuchań. Przeciągajcie karty, łączcie je czerwoną nitką. Dotknij nitki, by ją usunąć.</p></div></div>
   <div class="board-tools"><button class="btn small ${linkMode ? 'red' : 'ghost'}" data-a="link-mode">${I.link} ${linkMode ? 'Wybierz dwie karty' : 'Połącz'}</button>
    <button class="btn small ghost" data-a="note-add">${I.plus} Notatka</button>
    <button class="btn small ghost" data-a="board-del" ${boardSel ? '' : 'disabled'}>${I.trash} Usuń kartę</button>
    <span style="flex:1"></span><button class="icon-btn" data-a="zoom" data-d="-1" aria-label="Pomniejsz">${I.minus}</button><button class="icon-btn" data-a="zoom" data-d="1" aria-label="Powiększ">${I.plus}</button></div>
   <div class="board-wrap" id="bwrap"><div style="position:relative;width:${1700 * (g.board.zoom || 1)}px;height:${1150 * (g.board.zoom || 1)}px"><div class="board" id="board" style="transform:scale(${g.board.zoom || 1})"></div></div></div>
   ${g.board.items.length ? '' : '<p class="muted" style="margin-top:10px">Tablica jest pusta. Otwórzcie dowód lub osobę i użyjcie przycisku „Na tablicę”.</p>'}`;
}
function mountBoard(c, g) {
  const b = $('#board'); if (!b) return;
  const z = g.board.zoom || 1;
  b.parentElement.style.setProperty('--z', z);
  const items = g.board.items.map(it => {
    const L = boardLabel(c, g, it.key);
    const inner = L.kind === 'person' ? `<div class="bcard person" style="--rot:${rot(it.key)}"><div class="ph" ${L.p.img ? `style="background-image:url('${esc(L.p.img)}')"` : ''}>${L.p.img ? '' : `<span>${esc(initials(L.title))}</span>`}</div>${esc(L.title)}</div>`
      : L.kind === 'note' ? `<div class="bcard note" style="--rot:${rot(it.key)}">${esc(L.title)}</div>`
      : `<div class="bcard" style="--rot:${rot(it.key)}"><small>${esc(L.sub)}</small>${esc(L.title)}</div>`;
    return `<div class="bitem ${boardSel === it.key ? 'sel' : ''}" data-key="${esc(it.key)}" style="left:${it.x}px;top:${it.y}px"><span class="pin"></span>${inner}</div>`;
  }).join('');
  b.innerHTML = `<svg id="strings"></svg>${items}`;
  drawStrings(g);
  b.querySelectorAll('.bitem').forEach(el => attachDrag(el, c, g));
}
function center(g, key) { const el = document.querySelector(`.bitem[data-key="${CSS.escape(key)}"]`); const it = g.board.items.find(x => x.key === key); if (!it) return null; return { x: it.x + 85, y: it.y + (el ? Math.min(el.offsetHeight / 2, 60) : 50) }; }
function drawStrings(g) {
  const svg = $('#strings'); if (!svg) return;
  svg.innerHTML = g.board.links.map((l, i) => { const a = center(g, l.a), b = center(g, l.b); if (!a || !b) return ''; const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2 + Math.min(80, Math.hypot(a.x - b.x, a.y - b.y) * 0.12); return `<path d="M${a.x},${a.y - 40} Q${mx},${my} ${b.x},${b.y - 40}" data-link="${i}"/>`; }).join('');
  svg.querySelectorAll('path').forEach(p => p.addEventListener('click', e => { e.stopPropagation(); if (confirm('Usunąć to połączenie?')) { g.board.links.splice(+p.dataset.link, 1); save(); drawStrings(g); } }));
}
function attachDrag(el, c, g) {
  let sx, sy, ox, oy, moved = false, pid = null;
  const it = () => g.board.items.find(x => x.key === el.dataset.key);
  el.addEventListener('pointerdown', e => { pid = e.pointerId; el.setPointerCapture(pid); const i = it(); sx = e.clientX; sy = e.clientY; ox = i.x; oy = i.y; moved = false; el.classList.add('drag'); });
  el.addEventListener('pointermove', e => {
    if (pid !== e.pointerId) return; const z = g.board.zoom || 1;
    const dx = (e.clientX - sx) / z, dy = (e.clientY - sy) / z; if (Math.abs(dx) + Math.abs(dy) > 4) moved = true;
    if (!moved) return; const i = it(); i.x = Math.max(0, Math.min(1530, ox + dx)); i.y = Math.max(10, Math.min(1000, oy + dy));
    el.style.left = i.x + 'px'; el.style.top = i.y + 'px'; drawStrings(g);
  });
  const end = e => {
    if (pid !== e.pointerId) return; pid = null; el.classList.remove('drag');
    if (moved) { save(); return; }
    const key = el.dataset.key;
    if (linkMode && boardSel && boardSel !== key) {
      if (!g.board.links.some(l => (l.a === boardSel && l.b === key) || (l.b === boardSel && l.a === key))) g.board.links.push({ a: boardSel, b: key });
      boardSel = null; linkMode = false; save(); render(); return;
    }
    boardSel = boardSel === key ? null : key; render();
  };
  el.addEventListener('pointerup', end); el.addEventListener('pointercancel', end);
}
function pinToBoard(g, key, text) {
  if (key.startsWith('n:')) { g.board.items.push({ key, text, x: 80 + Math.random() * 600, y: 60 + Math.random() * 400 }); }
  else if (!g.board.items.some(x => x.key === key)) { const n = g.board.items.length; g.board.items.push({ key, x: 40 + (n % 7) * 220, y: 40 + Math.floor(n / 7) * 230 }); }
  else { toast('Już na tablicy', '', 'Tablica'); return; }
  save(); toast('Przypięto do tablicy', '', 'Tablica');
}

/* --- RAPORT --- */
function renderReport(c, g) {
  const Q = c.report.questions; const d = g.draft; const step = Math.min(d.step, Q.length);
  const prog = `<div class="rep-progress">${Q.map((_, i) => `<i class="${i <= step ? 'on' : ''}"></i>`).join('')}<i class="${step >= Q.length ? 'on' : ''}"></i></div>`;
  if (step >= Q.length) {
    const missing = Q.filter(q => q.type === 'order' ? !d.order : !d.answers[q.id]).length;
    return `<div class="rep-step">${prog}<div class="eyebrow">Ostatni krok</div><h2 style="font-size:2.2rem;margin:.2em 0 .4em">Podpis i złożenie raportu</h2>
     <div class="panel">${Q.map(q => `<p style="margin:.6em 0"><span class="eyebrow">${esc(q.q)}</span><br>${q.type === 'order' ? (d.order ? d.order.map(k => esc(q.items.find(x => x[0] === k)[1])).join(' → ') : '<i>brak</i>') : esc((q.options.find(o => o[0] === d.answers[q.id]) || [, '— brak odpowiedzi —'])[1])}</p>`).join('')}
     <p><span class="eyebrow">Wskazane dowody</span><br>${d.proofs.length ? d.proofs.map(id => esc(c.ev[id].title)).join(' · ') : '<i>brak</i>'}</p></div>
     ${missing ? `<div class="result-bad">Brakuje odpowiedzi na ${missing} pytań. Możecie złożyć raport, ale stracicie te punkty.</div>` : ''}
     <div class="row-actions"><button class="btn ghost" data-a="rstep" data-d="-1">Wstecz</button><button class="btn red" data-a="submit">Podpisz i złóż raport</button></div>
     <p class="muted" style="font-size:.85rem;margin-top:10px">Po złożeniu raportu poznacie rozwiązanie. Nie da się go już zmienić.</p></div>`;
  }
  const q = Q[step]; let body = '';
  if (q.type === 'single') {
    body = q.options.map(([k, l]) => `<button class="opt" aria-pressed="${d.answers[q.id] === k}" data-a="ropt" data-q="${q.id}" data-k="${k}">${esc(l)}</button>`).join('');
    if (q.proof) body += `<div class="eyebrow" style="margin-top:22px">${esc(q.proof.label)} (${d.proofs.length}/${q.proof.count})</div>
      <div class="pick">${visibleEvidence(g, c).map(id => `<button aria-pressed="${d.proofs.includes(id)}" data-a="rproof" data-id="${id}" data-max="${q.proof.count}"><small>${esc(c.ev[id].type)}</small>${esc(c.ev[id].title)}</button>`).join('')}</div>`;
  } else {
    if (!d.order) { d.order = shuffle(q.items.map(x => x[0]), g.created % 997 + 3); save(); }
    body = `<p class="muted">Przestawiajcie strzałkami. Pierwsze wydarzenie na górze.</p><ol class="order">${d.order.map((k, i) => `<li><span>${esc(q.items.find(x => x[0] === k)[1])}</span><button data-a="rord" data-i="${i}" data-d="-1" aria-label="W górę" ${i ? '' : 'disabled'}>▲</button><button data-a="rord" data-i="${i}" data-d="1" aria-label="W dół" ${i < d.order.length - 1 ? '' : 'disabled'}>▼</button></li>`).join('')}</ol>`;
  }
  return `<div class="rep-step">${prog}<div class="eyebrow">Akt oskarżenia · pytanie ${step + 1} z ${Q.length} · ${q.points + (q.proof ? q.proof.count * q.proof.each : 0)} pkt</div>
   <h2 style="font-size:clamp(1.8rem,6vw,2.4rem);margin:.25em 0 .7em">${esc(q.q)}</h2>${body}
   <div class="row-actions"><button class="btn ghost" data-a="rstep" data-d="-1" ${step ? '' : 'disabled'}>Wstecz</button><button class="btn" data-a="rstep" data-d="1">Dalej</button></div></div>`;
}
function score(c, g) {
  const d = g.draft; const lines = []; let pts = 0;
  c.report.questions.forEach(q => {
    if (q.type === 'single') {
      const ok = d.answers[q.id] === q.correct; pts += ok ? q.points : 0; lines.push([q.q, ok ? q.points : 0, q.points, ok]);
      if (q.proof) { const v = d.proofs.filter(id => q.proof.valid.includes(id)).length; const p = Math.min(v, q.proof.count) * q.proof.each; pts += p; lines.push(['Dowody wskazujące sprawcę', p, q.proof.count * q.proof.each, v >= q.proof.count]); }
    } else {
      const ok = (d.order || []).filter((k, i) => q.correct[i] === k).length; const p = Math.round(q.points * ok / q.correct.length); pts += p; lines.push([q.q, p, q.points, ok === q.correct.length]);
    }
  });
  const hintPen = Object.values(g.puzzles).reduce((s, p) => s + (p.hints || 0) * 2, 0);
  const pen = [['Podpowiedzi w zagadkach', hintPen], ['Tropy', g.trops * 3], ['Nietrafione konfrontacje', g.failed * 2], [`Ruchy ponad normę (${g.actions}/${c.par})`, Math.min(15, Math.ceil(Math.max(0, g.actions - c.par) / 2))]];
  const total = Math.max(0, pts - pen.reduce((s, p) => s + p[1], 0));
  return { pts, lines, pen, total, rank: RANKS.find(r => total >= r[0])[1], answers: { ...d.answers }, proofs: d.proofs.slice(), order: (d.order || []).slice(), at: Date.now() };
}
function renderResult(c, g) {
  const R = g.report; const E = c.endings; const who = R.answers['r-who'];
  const correctWho = who === c.report.questions.find(q => q.id === 'r-who').correct;
  const allCore = correctWho && R.lines.filter(l => l[2] >= 10).every(l => l[3]);
  let ending;
  if (correctWho) {
    const dec = E.correct.decision; const ch = R.decision && dec.options.find(o => o.id === R.decision);
    ending = `<article class="paper ending"><span class="stamp" style="position:absolute;right:16px;top:16px">Epilog</span><h3>${esc(E.correct.title)}</h3><p>${esc(E.correct.text)}</p>${allCore ? '' : `<p><i>${esc(E.partial)}</i></p>`}
     ${ch ? `<h5 style="font-family:var(--f-ui);font-size:.66rem;letter-spacing:.22em;color:var(--red);text-transform:uppercase">Wasza decyzja: ${esc(ch.label)}</h5><p>${esc(ch.text)}</p>` : ''}</article>
     ${ch ? '' : `<div class="panel"><div class="eyebrow">Decyzja zespołu</div><h3>${esc(dec.q)}</h3>${dec.options.map(o => `<button class="opt" data-a="decide" data-id="${o.id}">${esc(o.label)}</button>`).join('')}</div>`}`;
  } else {
    const w = E.wrong[who] || { title: 'Sprawa przegrana', text: 'Nie wskazaliście sprawcy. Sprawa trafia do archiwum spraw niewyjaśnionych.' };
    ending = `<article class="paper ending"><span class="stamp" style="position:absolute;right:16px;top:16px">Epilog</span><h3>${esc(w.title)}</h3><p>${esc(w.text)}</p></article>`;
  }
  return `<div class="rep-step"><div class="score"><div class="eyebrow">Wynik zespołu</div><div class="n">${R.total}</div><div class="eyebrow">na 100 punktów</div><div class="rank stamp">${esc(R.rank)}</div></div>
   <div class="breakdown">${R.lines.map(l => `<div><span>${esc(l[0])}</span><b class="${l[3] ? 'ok' : 'no'}">${l[1]}/${l[2]}</b></div>`).join('')}${R.pen.filter(p => p[1]).map(p => `<div><span>${esc(p[0])}</span><b class="no">−${p[1]}</b></div>`).join('')}</div>
   ${ending}
   <details class="panel" style="margin-top:18px"><summary class="eyebrow" style="cursor:pointer;padding:6px 0">Pełne rozwiązanie — jak można było to wydedukować</summary>
    <p style="font-family:var(--f-display);font-size:1.4rem;color:var(--txt)">${esc(c.solution.summary)}</p>${c.solution.steps.map(s => `<div class="sol-step"><b>${esc(s.h)}</b><p>${esc(s.p)}</p></div>`).join('')}</details>
   <div class="row-actions"><button class="btn" data-a="home">Archiwum spraw</button><button class="btn ghost" data-a="restart" data-id="${c.id}">Zagraj ponownie</button></div></div>`;
}

/* ---------- nakładki: render ---------- */
async function renderOv() {
  const root = $('#overlay-root'); const o = topOv();
  if (!o) { root.innerHTML = ''; document.body.style.overflow = ''; return; }
  const r = route(); const c = r.id && caseFor(r.id); const g = r.id && G(r.id);
  let v;
  if (o.type === 'settings') v = ovSettings();
  else if (o.type === 'menu') v = ovMenu(c, g);
  else if (o.type === 'msg') v = { title: o.title, kicker: o.kicker || '', body: o.body };
  else if (!c || !g) { ovStack = []; root.innerHTML = ''; return; }
  else if (o.type === 'ev') { v = { title: c.ev[o.id].title, kicker: 'Akta ' + c.id, body: docHTML(c, c.ev[o.id]) + `<div class="doc-actions"><button class="btn small ghost" data-a="pin" data-key="ev:${o.id}">${I.pin} Na tablicę</button></div>` }; if (!g.read.includes(o.id)) { g.read.push(o.id); save(); setTimeout(render, 0); } }
  else if (o.type === 'loc') v = ovLocation(c, g, o.id);
  else if (o.type === 'person') v = ovPerson(c, g, o.id, o.mode);
  else if (o.type === 'confront') v = ovConfront(c, g, o.id);
  else if (o.type === 'puzzle') v = ovPuzzle(c, g, o.id, o.msg);
  else if (o.type === 'priv') v = ovPrivate(c, g, o.i, o.opened);
  else if (o.type === 'qr') v = { title: 'Kod teczki', kicker: g.players[o.i].name, body: `<div class="qr-card big"><div class="qr">${qrSVG(folderURL(c, g, o.i))}</div><b>${esc(g.players[o.i].name)}</b><small>Zeskanuj aparatem telefonu</small></div>` };
  else if (o.type === 'reveal') v = { title: 'Ujawnij dokument', kicker: 'Tajne akta', body: `<p>Wpisz kod widoczny przy dokumencie w telefonie. Dokument trafi do wspólnych akt.</p><div class="field" style="margin:14px 0"><label for="revcode">Kod dokumentu</label><input class="input" id="revcode" maxlength="6" autocomplete="off" autocapitalize="characters" style="font-family:var(--f-mono);font-size:1.6rem;letter-spacing:.3em;text-transform:uppercase"></div>${o.msg ? `<div class="result-bad">${esc(o.msg)}</div>` : ''}<button class="btn" data-a="reveal-go">Ujawnij</button>` };
  else if (o.type === 'trop') v = o.text ? { title: 'Trop', kicker: 'Podpowiedź zespołu', body: `<div class="hint-box" style="font-size:1.05rem">${esc(o.text)}</div>` } : { title: 'Trop', kicker: 'Podpowiedź', body: `<p>Utknęliście? Szef wydziału podsunie kierunek. Każdy trop kosztuje <b>3 punkty</b> w raporcie końcowym. Wykorzystane tropy: ${g.trops}.</p><div class="row-actions"><button class="btn" data-a="trop-go">Pokaż trop (−3 pkt)</button><button class="btn ghost" data-a="close">Jeszcze nie</button></div>` };
  root.innerHTML = `<div class="ov" data-a="ov-bg"><div class="ov-panel ${v.full ? 'full' : ''}" role="dialog" aria-modal="true" aria-label="${esc(v.title)}">
   <div class="ov-head">${ovStack.length > 1 ? `<button class="icon-btn" data-a="close" aria-label="Wstecz">${I.back}</button>` : ''}<div class="t"><small>${esc(v.kicker)}</small><b>${esc(v.title)}</b></div><button class="icon-btn" data-a="close-all" aria-label="Zamknij">${I.close}</button></div>
   <div class="ov-body">${v.body}</div></div></div>`;
  document.body.style.overflow = 'hidden';
  const tr = $('#transcript'); if (tr && o.scrollEnd) { tr.lastElementChild && tr.lastElementChild.scrollIntoView({ block: 'center' }); o.scrollEnd = false; }
  const inp = $('#pzin'); if (inp) inp.addEventListener('keydown', e => { if (e.key === 'Enter') handlers.solve({ dataset: { id: o.id } }); });
  const rc = $('#revcode'); if (rc) { rc.focus(); rc.addEventListener('keydown', e => { if (e.key === 'Enter') handlers['reveal-go'](); }); }
}
function ovSettings() {
  const s = S.settings;
  return { title: 'Ustawienia', kicker: 'ŚLAD ' + VERSION, body: `
   <div class="settings-row"><div><b>Wersja gry: ${VERSION}</b><small>Wydanie z ${BUILD}. Gra aktualizuje się sama przy każdym otwarciu z internetem.</small></div><button class="btn small ghost" data-a="check-update">Sprawdź</button></div>
   <div class="settings-row"><div><b>Tryb telewizora</b><small>Większy tekst, karty i przyciski — czytelne z kanapy. Włącz, gdy gra jest wyświetlana na telewizorze.</small></div><button class="switch" aria-pressed="${!!s.tv}" data-a="tv" aria-label="Tryb telewizora"></button></div>
   <div class="settings-row"><div><b>Dźwięk</b><small>Klimat sprawy (deszcz, burza, zegar) i efekty: dokumenty, pieczęcie, zamki, przełomy w przesłuchaniach.</small></div><button class="switch" aria-pressed="${s.sound}" data-a="sound" aria-label="Dźwięk"></button></div>
   <div class="settings-row ${s.sound ? '' : 'off'}"><div style="flex:1"><b>Głośność klimatu</b><input type="range" min="0" max="100" step="5" value="${Math.round(vol('music') * 100)}" data-vol="music" aria-label="Głośność klimatu" class="range"></div></div>
   <div class="settings-row ${s.sound ? '' : 'off'}"><div style="flex:1"><b>Głośność efektów</b><input type="range" min="0" max="100" step="5" value="${Math.round(vol('fx') * 100)}" data-vol="fx" aria-label="Głośność efektów" class="range"></div><button class="btn small ghost" data-a="test-fx">Test</button></div>
   <div class="settings-row"><div><b>Wielkość tekstu</b><small>Dla czytania przy stole</small></div><div class="seg">${[['m', 'A'], ['l', 'A+'], ['xl', 'A++']].map(([k, l]) => `<button aria-pressed="${s.text === k}" data-a="text" data-v="${k}">${l}</button>`).join('')}</div></div>
   <div class="settings-row"><div><b>Animacje</b><small>Wyłącz, jeśli przeszkadzają</small></div><button class="switch" aria-pressed="${s.motion === 'on'}" data-a="motion" aria-label="Animacje"></button></div>
   <div class="settings-row"><div><b>Kopia zapasowa</b><small>Postęp jest zapisywany na tym urządzeniu. Eksportuj, by przenieść go gdzie indziej.</small></div></div>
   <div class="row-actions"><button class="btn small ghost" data-a="export">Eksportuj zapis</button><label class="btn small ghost" style="cursor:pointer">Importuj zapis<input type="file" accept="application/json,.json" data-import hidden></label></div>
   <hr class="sep"><button class="btn small ghost" data-a="wipe">Usuń wszystkie zapisy</button>` };
}
function ovMenu(c, g) {
  return { title: 'Menu sprawy', kicker: c ? 'Akta ' + c.id : '', body: `<div class="qlist">
   <button class="q" data-a="show-brief">Briefing i zadania sprawy</button>
   <button class="q" data-a="sound">${S.settings.sound ? 'Wyłącz dźwięk' : 'Włącz dźwięk'}</button>
   <button class="q" data-a="settings">Ustawienia · wersja ${VERSION}</button>
   <button class="q" data-a="restart" data-id="${c ? c.id : ''}">Zacznij sprawę od nowa</button>
   <button class="q" data-a="home">Wróć do archiwum</button></div>` };
}

function startMsg(c, g) {
  const roles = g.players.map(p => `<li><b>${esc(p.name)}</b> — ${esc(ROLES.find(r => r.id === p.role).name)}: <span class="muted">${esc(ROLES.find(r => r.id === p.role).tip)}</span></li>`).join('');
  openOv({ type: 'msg', title: 'Śledztwo rozpoczęte', kicker: 'Akta ' + c.id, body: `<p>Macie przed sobą akta startowe — zacznijcie od nich. Potem przeszukujcie miejsca i przesłuchujcie świadków.</p>${c.mode === 'table' ? '<p class="muted">Gracie przy wspólnym stole: wszystko widzicie razem. Pamiętajcie o Centrali wydziału — niektóre informacje są tylko tam.</p>' : '<p class="muted">Pamiętajcie: każdy z was wie coś, czego nie wie reszta.</p>'}<h4 class="eyebrow" style="margin-top:18px">Podział ról</h4><ul class="roles">${roles}</ul>` });
}
/* ---------- akcje ---------- */
const ctx = () => { const r = route(); return { c: caseFor(r.id), g: G(r.id), r }; };
const rerender = () => { render(); renderOv(); };
const handlers = {
  home: () => { ovStack = []; renderOv(); go(''); },
  how: () => $('#how').scrollIntoView({ behavior: 'smooth' }),
  soon: () => openOv({ type: 'msg', title: 'W przygotowaniu', kicker: 'Archiwum', body: '<p>Te akta są w opracowaniu. Każda sprawa przechodzi pełny audyt logiki, zanim trafi do archiwum — pojawi się w jednej z najbliższych aktualizacji.</p>' }),
  'open-case': el => go('sprawa/' + el.dataset.id),
  continue: el => go(`gra/${el.dataset.id}/${G(el.dataset.id).report ? 'wynik' : 'akta'}`),
  count: el => { setupCount = +el.dataset.n; render(); },
  mode: el => { setupMode = el.dataset.m; render(); setTimeout(() => { const st = document.querySelectorAll('.setup')[1]; st && st.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 60); },
  'qr-done': () => { const { g, c } = ctx(); g.phase = 'play'; save(); render(); startMsg(c, g); },
  qr: el => openOv({ type: 'qr', i: +el.dataset.i }),
  reveal: () => openOv({ type: 'reveal' }),
  'reveal-go': () => { const { c, g } = ctx(); const v = (($('#revcode') || {}).value || '').trim().toUpperCase().replace(/[^A-Z0-9]/g, '');
    let hit = null; Object.values(g.priv).flat().forEach(id => { if (codeFor(g, id) === v) hit = id; });
    const o = topOv();
    if (!hit) { o.msg = 'Nie ma dokumentu z takim kodem. Sprawdź kod w telefonie.'; renderOv(); return; }
    if (!g.shared.includes(hit)) { g.shared.push(hit); save(); toast(c.ev[hit].title, 'Ujawniono zespołowi', 'Tajne akta'); }
    ovStack.pop(); history.back(); setTimeout(() => { rerender(); openOv({ type: 'ev', id: hit }); }, 60); },
  begin: async el => {
    const c = await getCase(el.dataset.id);
    const names = Array.from({ length: setupCount }, (_, i) => (setupNames[i] || '').trim() || `Gracz ${i + 1}`);
    if (!setupMode) return;
    S.games[c.id] = newGame(c, names, setupMode); save(); distRevealed = false; go(`gra/${c.id}/akta`);
    if (setupMode === 'table') setTimeout(() => startMsg(variant(c, 'table'), S.games[c.id]), 250);
  },
  restart: el => { const id = el.dataset.id; if (!confirm('Zacząć sprawę od nowa? Obecny postęp zostanie usunięty.')) return; delete S.games[id]; save(); ovStack = []; renderOv(); go('sprawa/' + id); },
  'dist-open': () => { distRevealed = true; sfx('stamp'); render(); },
  'dist-next': () => { const { g, c } = ctx(); distRevealed = false; g.distIdx++; if (g.distIdx >= g.players.length) { g.phase = 'play'; save(); render(); setTimeout(() => startMsg(c, g), 200); } else { save(); render(); } },
  tab: el => go(`gra/${route().id}/${el.dataset.tab}`),
  filter: el => { filesFilter = el.dataset.f; render(); },
  ana: el => { anaTab = el.dataset.t; render(); },
  ev: el => openOv({ type: 'ev', id: el.dataset.id }),
  loc: el => openOv({ type: 'loc', id: el.dataset.id }),
  person: el => openOv({ type: 'person', id: el.dataset.id, mode: 'talk' }),
  pmode: el => { const o = topOv(); o.mode = el.dataset.m; renderOv(); },
  search: el => { const { c, g } = ctx(); doSearch(c, g, el.dataset.id); rerender(); },
  ask: el => { const { c, g } = ctx(); doAsk(c, g, el.dataset.id); topOv().scrollEnd = true; rerender(); },
  confront: el => openOv({ type: 'confront', id: el.dataset.id }),
  'confront-with': el => { const { c, g } = ctx(); doConfront(c, g, el.dataset.s, el.dataset.id); ovStack.pop(); history.back(); const o = topOv(); if (o && o.type === 'person') { o.mode = 'talk'; o.scrollEnd = true; } setTimeout(rerender, 30); },
  puzzle: el => openOv({ type: 'puzzle', id: el.dataset.id }),
  'puzzle-from-spot': el => { const { c, g } = ctx(); const pz = c.puzzle[el.dataset.id]; if (puzzleVisible(c, g, pz)) openOv({ type: 'puzzle', id: pz.id }); else openOv({ type: 'msg', title: pz.title, kicker: 'Za mało danych', body: '<p>Na razie nie macie materiałów, które pozwoliłyby się do tego zabrać. Szukajcie dalej.</p>' }); },
  dial: el => { const id = el.dataset.id, i = +el.dataset.i; const { c } = ctx(); const max = c.puzzle[id].input === 'time' && i === 0 ? 3 : c.puzzle[id].input === 'time' && i === 2 ? 6 : 10; dialVals[id][i] = (dialVals[id][i] + +el.dataset.d + max) % max; renderOv(); },
  solve: el => { const { c, g } = ctx(); const msg = doSolve(c, g, el.dataset.id); const o = topOv(); o.msg = msg; rerender(); },
  phint: el => { const { g } = ctx(); const st = (g.puzzles[el.dataset.id] = g.puzzles[el.dataset.id] || { hints: 0, attempts: 0 }); st.hints = (st.hints || 0) + 1; save(); renderOv(); },
  priv: el => openOv({ type: 'priv', i: +el.dataset.i, opened: false }),
  'priv-open': () => { topOv().opened = true; sfx('stamp'); renderOv(); },
  share: el => { const { c, g } = ctx(); if (!g.shared.includes(el.dataset.id)) { g.shared.push(el.dataset.id); save(); toast(c.ev[el.dataset.id].title, 'Ujawniono zespołowi', 'Tajne akta'); } rerender(); },
  pin: el => { const { g } = ctx(); pinToBoard(g, el.dataset.key); },
  'link-mode': () => { linkMode = !linkMode; if (!linkMode) boardSel = null; render(); if (linkMode) toast('Łączenie', 'Dotknij pierwszej, potem drugiej karty', 'Tablica'); },
  'note-add': () => { const t = prompt('Treść notatki na tablicy:'); if (t && t.trim()) { const { g } = ctx(); pinToBoard(g, 'n:' + Date.now(), t.trim().slice(0, 140)); render(); } },
  'board-del': () => { const { g } = ctx(); if (!boardSel) return; g.board.items = g.board.items.filter(x => x.key !== boardSel); g.board.links = g.board.links.filter(l => l.a !== boardSel && l.b !== boardSel); boardSel = null; save(); render(); },
  zoom: el => { const { g } = ctx(); g.board.zoom = Math.max(0.4, Math.min(1.4, Math.round(((g.board.zoom || 1) + 0.2 * +el.dataset.d) * 10) / 10)); save(); render(); },
  trop: () => openOv({ type: 'trop' }),
  'trop-go': () => { const { c, g } = ctx(); const rule = c.hintTrail.find(h => (!h.when || h.when.every(t => has(g, c, t))) && !(h.unless && h.unless.every(t => has(g, c, t)))); g.trops++; save(); topOv().text = rule ? rule.text : 'Macie wszystko, czego potrzeba.'; rerender(); },
  rstep: el => { const { g, c } = ctx(); g.draft.step = Math.max(0, Math.min(c.report.questions.length, g.draft.step + +el.dataset.d)); save(); render(); $('#main') && ($('#main').scrollTop = 0); },
  ropt: el => { const { g } = ctx(); g.draft.answers[el.dataset.q] = el.dataset.k; save(); render(); },
  rproof: el => { const { g } = ctx(); const p = g.draft.proofs; const id = el.dataset.id; const i = p.indexOf(id); if (i >= 0) p.splice(i, 1); else if (p.length < +el.dataset.max) p.push(id); else toast('Limit dowodów', 'Odznacz jeden, by wybrać inny', 'Raport'); save(); render(); },
  rord: el => { const { g } = ctx(); const o = g.draft.order; const i = +el.dataset.i, j = i + +el.dataset.d; if (j < 0 || j >= o.length) return; [o[i], o[j]] = [o[j], o[i]]; save(); render(); },
  submit: () => { const { c, g } = ctx(); if (!confirm('Złożyć raport? Nie będzie można go zmienić.')) return; g.report = score(c, g); g.phase = 'done'; save(); sfx('stamp'); go(`gra/${c.id}/wynik`); },
  decide: el => { const { g } = ctx(); g.report.decision = el.dataset.id; save(); render(); },
  sound: () => { S.settings.sound = !S.settings.sound; save(); if (S.settings.sound) audioCtx(); syncAudio(); if (S.settings.sound) setTimeout(() => sfx('paper'), 150); rerender(); },
  text: el => { S.settings.text = el.dataset.v; save(); applySettings(); renderOv(); },
  'test-fx': () => sfx('stamp'),
  tv: () => { S.settings.tv = !S.settings.tv; save(); applySettings(); rerender(); },
  motion: () => { S.settings.motion = S.settings.motion === 'on' ? 'off' : 'on'; save(); applySettings(); renderOv(); },
  settings: () => openOv({ type: 'settings' }),
  'check-update': async () => {
    if (!swReg || !navigator.onLine) { toast('Brak połączenia', 'Sprawdzę, gdy wróci internet', 'Aktualizacja'); return; }
    toast('Sprawdzam aktualizację…', 'Wersja ' + VERSION, 'Aktualizacja');
    try { await swReg.update(); } catch (_) {}
    setTimeout(() => { if (swReg.installing || swReg.waiting) toast('Pobieram nową wersję', 'Gra za chwilę przeładuje się sama', 'Aktualizacja'); else toast('Masz najnowszą wersję', 'Wersja ' + VERSION, 'Aktualizacja'); }, 1200);
  },
  'case-menu': () => openOv({ type: 'menu' }),
  'show-brief': () => { const { c } = ctx(); openOv({ type: 'msg', title: c.title, kicker: 'Briefing', body: `<article class="paper brief"><p class="lead">${esc(c.intro.lead)}</p>${c.intro.brief.map(p => `<p>${esc(p)}</p>`).join('')}<h4>Zadanie zespołu</h4><ol>${c.intro.task.map(t => `<li>${esc(t)}</li>`).join('')}</ol><h4>Zasady</h4><ul>${c.intro.rules.map(t => `<li>${esc(t)}</li>`).join('')}</ul></article>` }); },
  export: async () => { const name = `slad-zapis-${new Date().toISOString().slice(0, 10)}.json`; const blob = new Blob([JSON.stringify({ app: 'slad', version: VERSION, exported: new Date().toISOString(), data: S }, null, 1)], { type: 'application/json' });
    try { const file = new File([blob], name, { type: 'application/json' }); if (navigator.canShare && navigator.canShare({ files: [file] })) { await navigator.share({ files: [file], title: 'Zapis ŚLAD' }); return; } } catch (err) { if (err && err.name === 'AbortError') return; }
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `slad-zapis-${new Date().toISOString().slice(0, 10)}.json`; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500); },
  wipe: () => { if (!confirm('Usunąć wszystkie zapisy na tym urządzeniu?')) return; S = freshStore(); save(); ovStack = []; renderOv(); go(''); },
  close: () => closeOv(),
  'close-all': () => { const n = ovStack.length; if (history.state && history.state.ov) history.go(-n); else { ovStack = []; renderOv(); } },
  'ov-bg': (el, e) => { if (e.target === el) handlers['close-all'](); }
};
document.addEventListener('click', e => {
  const el = e.target.closest('[data-a]'); if (!el || el.disabled) return;
  const h = handlers[el.dataset.a]; if (!h) return;
  if (el.dataset.a === 'ov-bg' && e.target !== el) return;
  e.preventDefault(); h(el, e);
});
document.addEventListener('input', e => {
  if (e.target.dataset.vol) { S.settings[e.target.dataset.vol] = +e.target.value / 100; clearTimeout(handlers._vt); handlers._vt = setTimeout(save, 300); if (e.target.dataset.vol === 'music' && AU.amb && AU.ctx) AU.amb.g.gain.setTargetAtTime(vol('music') * 0.9, AU.ctx.currentTime, 0.1); return; }
  if (e.target.dataset.name !== undefined) setupNames[+e.target.dataset.name] = e.target.value;
  if (e.target.dataset.notes !== undefined) { const { g } = ctx(); g.notes = e.target.value; clearTimeout(handlers._nt); handlers._nt = setTimeout(save, 400); }
});
document.addEventListener('change', async e => {
  if (e.target.dataset.import === undefined) return;
  const f = e.target.files[0]; if (!f) return;
  try { const j = JSON.parse(await f.text()); const d = j && j.app === 'slad' ? j.data : null; if (!d || d.v !== 2 || !d.games || !d.settings) throw new Error('To nie jest plik zapisu ŚLAD 2.'); if (!confirm('Zastąpić obecny postęp danymi z pliku?')) return; S = d; save(); ovStack = []; renderOv(); toast('Zapis wczytany', '', 'Kopia'); go(''); }
  catch (err) { toast('Nie wczytano pliku', err.message, 'Błąd'); }
});
document.addEventListener('keydown', e => { if (e.key === 'Escape' && ovStack.length) closeOv(); });

/* ---------- PWA: automatyczna aktualizacja ---------- */
if ('serviceWorker' in navigator && location.protocol !== 'file:') {
  const hadController = !!navigator.serviceWorker.controller;
  let reloading = false;
  // Nowa wersja przejęła kontrolę → przeładuj raz (postęp jest zapisany, wracamy w to samo miejsce).
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (!hadController || reloading) return; reloading = true;
    try { sessionStorage.setItem('slad.updated', '1'); } catch (_) {}
    location.reload();
  });
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js', { updateViaCache: 'none' }).then(reg => {
      swReg = reg;
      const check = () => { if (navigator.onLine !== false) reg.update().catch(() => {}); };
      check();
      document.addEventListener('visibilitychange', () => { if (!document.hidden) check(); });
      window.addEventListener('focus', check);
      window.addEventListener('online', check);
      setInterval(check, 15 * 60 * 1000);
    }).catch(() => {});
  });
  try { if (sessionStorage.getItem('slad.updated')) { sessionStorage.removeItem('slad.updated'); setTimeout(() => toast('Gra zaktualizowana', 'Wersja ' + VERSION, 'Aktualizacja'), 600); } } catch (_) {}
}
applySettings();
render();
