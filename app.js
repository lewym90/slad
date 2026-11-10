/* ŚLAD 2.0 — silnik gry. Wszystkie postacie i zdarzenia są fikcyjne. */
'use strict';
const VERSION = '2.10.2';
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
  key: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v3M21 12v2"/></svg>',
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
const POWERS = {
  koord: { kind: 'trop', name: 'Odprawa u szefa', desc: 'Jeden trop bez utraty punktów.' },
  analityk: { kind: 'search', name: 'Szybkie oględziny', desc: 'Jedno przeszukanie punktu bez zużycia ruchu.' },
  chrono: { kind: 'hint', name: 'Konsultacja', desc: 'Jedna podpowiedź w zagadce bez utraty punktów.' },
  przesl: { kind: 'ask', name: 'Pytanie z doświadczenia', desc: 'Jedno pytanie do świadka bez zużycia ruchu.' },
  weryf: { kind: 'confront', name: 'Sprawdzam', desc: 'Jedna konfrontacja bez ruchu — a jeśli chybi, bez kary.' },
  protokol: { kind: 'par', name: 'Porządek w aktach', desc: 'Norma ruchów tej sprawy rośnie o 3. Działa od razu.' }
};
const DIFFS = {
  rekrut: { name: 'Rekrut', sub: 'Dla zaczynających: łagodniejsza norma i tańsze podpowiedzi.', par: 8, hint: 1, hints: 3, trop: 2, wrong: 1 },
  sledczy: { name: 'Śledczy', sub: 'Pełne zasady, tak jak zaprojektowano sprawę.', par: 0, hint: 2, hints: 3, trop: 3, wrong: 2 },
  weteran: { name: 'Weteran', sub: 'Bez tropów (poza zdolnością Koordynatora), jedna podpowiedź w zagadce, ostrzejsza norma i kary.', par: -4, hint: 3, hints: 1, trop: null, wrong: 3 }
};
const pkt = n => `${n} ${n === 1 ? 'punkt' : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14)) ? 'punkty' : 'punktów'}`;
const podp = n => `${n === 1 ? 'jedna podpowiedź' : n === 2 ? 'dwie podpowiedzi' : n === 3 ? 'trzy podpowiedzi' : n + ' podpowiedzi'}`;
const diffOf = g => DIFFS[(g && g.diff) || 'sledczy'] || DIFFS.sledczy;
const effPar = (c, g) => c.par + diffOf(g).par + (g.parBonus || 0);
const MARK_ORDER = ['001', '002', '003', '004', '005', '006', '007', '008', '009'];
const RANKS = [[92, 'Legenda archiwum'], [78, 'Komisarz'], [60, 'Inspektor'], [40, 'Aspirant'], [0, 'Stażysta']];

/* ---------- pamięć ---------- */
function freshStore() { return { v: 2, settings: { sound: false, text: 'm', motion: 'on' }, games: {}, chronicle: [], marks: {} }; }
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
function newGame(c, names, mode, diff) {
  const seed = Date.now() % 100000;
  const priv = {}; names.forEach((_, i) => { priv[i] = []; });
  if (mode !== 'table') shuffle(c.privateClues, seed).forEach((id, i) => priv[i % names.length].push(id));
  const roles = shuffle(ROLES.map(r => r.id), seed + 7);
  return {
    v: 2, created: Date.now(), mode, phase: mode === 'table' ? 'play' : mode === 'phones' ? 'qr' : 'distribute', distIdx: 0,
    players: names.map((n, i) => ({ name: n, role: roles[i % roles.length] })), priv, shared: [],
    found: c.evidence.filter(e => e.start).map(e => e.id), read: [], spots: [], asked: [], claims: [], broken: [],
    log: {}, failed: 0, actions: 0, puzzles: {}, trops: 0, notes: '', board: { items: [], links: [], zoom: 1 },
    draft: { step: 0, answers: {}, proofs: [], order: null }, report: null,
    diff: diff || 'sledczy', used: {}, armed: null, parBonus: 0, freeTrops: 0, bt: [], matrix: {}, vote: null
  };
}
const G = id => S.games[id];
function usePower(g, kind) { if (g.armed !== kind) return false; const role = g.players.find(p => POWERS[p.role] && POWERS[p.role].kind === kind && !(g.used || {})[p.role]); if (!role) { g.armed = null; return false; } (g.used = g.used || {})[role.role] = true; g.armed = null; toast(POWERS[role.role].name, `Zdolność: ${role.name}`, 'Rola'); return true; }
const known = (g, id) => g.found.includes(id) || g.shared.includes(id);
function has(g, c, tok) {
  if (tok.startsWith('lie:')) return g.broken.includes(tok.slice(4));
  if (tok.startsWith('st:')) return g.claims.includes(tok.slice(3));
  if (c.puzzle[tok]) return !!(g.puzzles[tok] && g.puzzles[tok].solved);
  if (c.spot[tok]) return g.spots.includes(tok);
  if (c.q[tok]) return g.asked.includes(tok);
  return known(g, tok);
}
const visibleEvidence = (g, c) => [...g.found, ...g.shared].filter((id, i, a) => a.indexOf(id) === i && c.ev[id]);
const unread = (g, c) => visibleEvidence(g, c).filter(id => !g.read.includes(id)).length;
function personName(g, p) { return p.revealName && (p.revealOn || []).some(b => g.broken.includes(b)) ? p.revealName : p.name; }
function personRole(g, p) { return p.revealRole && (p.revealOn || []).some(b => g.broken.includes(b)) ? p.revealRole : p.role; }
function gain(g, c, ids, silent) {
  const got = [];
  (ids || []).forEach(id => { if (c.ev[id] && !known(g, id)) { g.found.push(id); got.push(id); } });
  if (got.length && !silent) { got.forEach((id, i) => setTimeout(() => toast(c.ev[id].title, c.ev[id].summary, 'Nowy dowód', id), i * 450)); sfx(); }
  return got;
}

/* ---------- dźwięk (Web Audio: pętla bez przerw, osobne głośności) ---------- */
let currentCaseId = null;
const AU = { ctx: null, bufs: {}, amb: null, ambSrc: null, token: 0 };
const vol = k => Math.max(0, Math.min(1, S.settings[k] == null ? (k === 'music' ? 0.6 : k === 'voice' ? 1 : 0.8) : S.settings[k]));
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
function duck(on) { if (!AU.amb || !AU.ctx) return; try { AU.amb.g.gain.setTargetAtTime(vol('music') * (on ? 0.22 : 0.9), AU.ctx.currentTime, 0.35); } catch (_) {} }
/* głosy świadków: plik = <voiceDir>/<id pytania lub zeznania>.mp3, odmowy: <osoba>-deflect-<n>.mp3 */
const voicesOn = () => S.settings.voices !== false;
function caseMedia(c) { const L = []; if (!c) return L; if (c.voice && c.voice.brief) L.push(c.voice.brief); if (c.introVideo) L.push(c.introVideo, c.introVideo.replace(/\.mp4$/, '.webp'));
  (c.breakthroughs || []).forEach(b => { if (b.video) L.push(b.video, b.video.replace(/\.mp4$/, '.webp')); });
  if (c.voiceDir) c.people.forEach(p => { [...p.questions, ...((c.tableMode && c.tableMode.questions && c.tableMode.questions[p.id]) || [])].forEach(q => L.push(`${c.voiceDir}/${q.id}.mp3`)); p.statements.filter(x => x.response).forEach(x => L.push(`${c.voiceDir}/${x.id}.mp3`)); (p.deflect || []).forEach((_, i) => L.push(`${c.voiceDir}/${p.id}-deflect-${i}.mp3`)); });
  return [...new Set(L)]; }
const prefetched = new Set();
const cachedMedia = new Set(); // ścieżki nagrań i filmów zapisanych w pamięci offline
const mediaKey = u => { try { return new URL(u, location.href).pathname; } catch (_) { return u; } };
const mediaOK = u => !!u && (navigator.onLine !== false || cachedMedia.has(mediaKey(u)));
if ('caches' in window) caches.open('slad-' + VERSION).then(c => c.keys()).then(K => K.forEach(r => { const pth = new URL(r.url).pathname; if (/\.(mp3|mp4)$/.test(pth)) cachedMedia.add(pth); })).catch(() => {});
async function prefetchMedia(c) { // zapis nagrań i filmów sprawy do pamięci offline, w tle i po kolei
  if (!c || prefetched.has(c.id) || !('caches' in window) || (navigator.connection && navigator.connection.saveData)) return; prefetched.add(c.id);
  try { const cache = await caches.open('slad-' + VERSION); for (const u of caseMedia(c)) { if (await cache.match(u)) { cachedMedia.add(mediaKey(u)); continue; } try { const r = await fetch(u); if (r.ok && r.status === 200) { await cache.put(u, r); cachedMedia.add(mediaKey(u)); } } catch (_) {} await new Promise(r => setTimeout(r, 40)); } } catch (_) {}
}
function voiceFor(c, pid, m) {
  if (!c || !c.voiceDir || !m || m.t === 'q') return null; if (m.v) return m.v;
  const p = c.person[pid]; if (!p) return null;
  if (m.t === 'a') { const q = p.questions.find(x => x.a === m.text) || ((c.tableMode && c.tableMode.questions && c.tableMode.questions[pid]) || []).find(x => x.a === m.text); return q ? `${c.voiceDir}/${q.id}.mp3` : null; }
  if (m.t === 'break') { const st = p.statements.find(x => x.response === m.text); return st ? `${c.voiceDir}/${st.id}.mp3` : null; }
  if (m.t === 'deflect') { const i = (p.deflect || []).indexOf(m.text); return i >= 0 ? `${c.voiceDir}/${pid}-deflect-${i}.mp3` : null; }
  return null;
}
const VO = typeof Audio !== 'undefined' ? new Audio() : null; let voTok = 0; // jeden odtwarzacz: iPhone odblokowuje go przy pierwszym dotknięciu
function speak(src, btn) {
  stopVoice(); if (!VO || !src || !mediaOK(src)) { if (btn && src) toast('Nagranie niedostępne bez internetu', 'Odsłuchacie je po połączeniu z siecią.', 'Głos'); return; }
  const tok = ++voTok; VO.src = src; VO.volume = vol('voice'); window.__voice = VO; duck(true);
  document.querySelectorAll('.vplay.on').forEach(b => b.classList.remove('on')); if (btn) btn.classList.add('on');
  const done = () => { if (tok !== voTok) return; window.__voice = null; duck(false); if (btn) btn.classList.remove('on'); };
  VO.onended = VO.onerror = done; VO.onpause = () => { if (!VO.ended) done(); }; VO.play().catch(done);
}
function stopVoice() { voTok++; const v = window.__voice; if (v) { try { v.pause(); } catch (_) {} window.__voice = null; } document.querySelectorAll('.vplay.on').forEach(b => b.classList.remove('on')); duck(false); }
async function sfx(name = 'paper') {
  if (!S.settings.sound) return;
  try { const ctx = audioCtx(); const b = await loadBuf(`assets/audio/sfx-${name}.mp3`); if (!ctx || !b) return;
    const n = ctx.createBufferSource(); n.buffer = b; const g = ctx.createGain(); g.gain.value = vol('fx'); n.connect(g).connect(ctx.destination); n.start(); } catch (_) {}
}
['pointerdown', 'keydown'].forEach(ev => document.addEventListener(ev, () => { if (S.settings.sound && (!AU.amb || (AU.ctx && AU.ctx.state !== 'running'))) syncAudio(); }, { passive: true }));
/* blokada powiększania strony gestem (iOS ignoruje user-scalable=no) — poza podglądem zdjęcia */
const zoomOK = e => !!(e.target && e.target.closest && e.target.closest('.zoom'));
['gesturestart', 'gesturechange', 'gestureend'].forEach(ev => document.addEventListener(ev, e => { if (!zoomOK(e)) e.preventDefault(); }, { passive: false }));
document.addEventListener('touchmove', e => { if ((e.touches.length > 1 || (e.scale && e.scale !== 1)) && !zoomOK(e)) e.preventDefault(); }, { passive: false });
document.addEventListener('wheel', e => { if (e.ctrlKey && !zoomOK(e)) e.preventDefault(); }, { passive: false });
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
window.addEventListener('hashchange', () => { stopVoice(); ovStack = []; renderOv(); render(); });

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
    else if (r.name === 'kronika') { currentCaseId = null; await renderChronicle(); }
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
     <div class="actions"><button class="btn" data-a="open-case" data-id="${c1.id}">${G(c1.id) ? 'Wróć do śledztwa' : 'Otwórz sprawę 001'}</button><button class="btn ghost" data-a="how">Jak grać</button><button class="btn ghost" data-a="chronicle">Kronika wydziału</button></div></div>
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
let setupCount = 2; let setupNames = []; let setupMode = null; let setupDiff = 'sledczy';
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
   <div class="intro-hero">${c.introVideo && S.settings.motion !== 'off' && mediaOK(c.introVideo) ? `<video src="${esc(c.introVideo)}" poster="${esc(c.introVideo.replace(/\.mp4$/, '.webp'))}" autoplay muted loop playsinline preload="auto" aria-label="${esc(c.title)}"></video>` : `<img src="${esc(c.keyart || c.art || c.cover)}" alt="${esc(c.title)} — plansza tytułowa">`}<button class="icon-btn back" data-a="home" aria-label="Archiwum">${I.back}</button></div>
   <div class="intro-wrap">
    <article class="paper brief"><span class="stamp">Ściśle tajne</span>
     <div class="eyebrow" style="color:var(--red)">Akta sprawy ${esc(c.id)} · ${esc(c.genre)}</div>
     <h1>${esc(c.title)}</h1><p class="lead tw">${esc(c.intro.lead)}</p>
     ${c.voice && c.voice.brief ? `<button class="btn small ghost voice-btn" data-a="voice" data-src="${esc(c.voice.brief)}">${I.sound} <span class="vl">Odsłuchaj briefing szefa wydziału</span></button>` : ''}
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
      <div class="eyebrow" style="margin-top:18px">Poziom trudności</div>
      <div class="diffs">${Object.entries(DIFFS).map(([k, d]) => `<button class="diff ${setupDiff === k ? 'on' : ''}" aria-pressed="${setupDiff === k}" data-a="diff" data-k="${k}"><b>${esc(d.name)}</b><small>${esc(d.sub)}</small></button>`).join('')}</div>
      <details class="rules"><summary>Zasady tej sprawy</summary><ul>${rules.map(r => `<li>${esc(r)}</li>`).join('')}</ul></details>
      <button class="btn block" data-a="begin" data-id="${c.id}">${setupMode === 'table' ? 'Rozpocznij śledztwo' : 'Rozdaj tajne akta'}</button></div>` : ''}`}
   </div></div>`;
  const tw = app().querySelector('.tw');
  if (tw && S.settings.motion !== 'off' && !inProgress && !tw.dataset.done) { const full = tw.textContent; tw.dataset.done = 1; tw.textContent = ''; tw.classList.add('typing'); let k = 0; const step = () => { if (!document.body.contains(tw)) return; k += 2; tw.textContent = full.slice(0, k); if (k < full.length) setTimeout(step, 22); else tw.classList.remove('typing'); }; setTimeout(step, 300); }
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
   ${(() => { const qw = c.report.questions.find(q => q.id === 'r-who'), qm = c.report.questions.find(q => q.id === 'r-motive'); return qw ? `<section class="vote-phone"><div class="eyebrow">Głosowanie zespołu</div><h3>Mój typ</h3><p class="muted">Wybierz po cichu. Pokażesz ekran, gdy wspólny ekran da sygnał.</p>
     <label class="field"><span>Sprawca</span><select class="input" id="v-who">${['<option value="">— wybierz —</option>', ...qw.options.map(o => `<option>${esc(o[1])}</option>`)].join('')}</select></label>
     ${qm ? `<label class="field"><span>Motyw</span><select class="input" id="v-mot">${['<option value="">— wybierz —</option>', ...qm.options.map(o => `<option>${esc(o[1])}</option>`)].join('')}</select></label>` : ''}
     <button class="btn block" data-a="vote-card">Gotowe — schowaj</button><div id="v-card" class="vote-card" hidden></div></section>` : ''; })()}
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
  if (!prefetched.has(c.id)) setTimeout(() => prefetchMedia(c), 4000);
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
    if (b.log) return `<div class="log">${b.log.map(l => `<span class="ln"><span class="lw">${esc(l)}</span><span class="lc">${esc(l.trim().replace(/\s{2,}/g, ' · '))}</span></span>`).join('')}</div>`;
    if (b.quote) return `<blockquote class="quote">${esc(b.quote)}${b.by ? `<cite>— ${esc(b.by)}</cite>` : ''}</blockquote>`;
    if (b.note) return `<div class="note">${esc(b.note)}</div>`;
    return '';
  }).join('');
}
function docHTML(c, e, compact) {
  const kind = e.private ? 'Tajne akta' : e.testimony ? 'Protokół' : 'Dowód';
  return `<article class="paper doc"><div class="dh"><div><small>Akta ${esc(c.id)} · ${kind} ${esc(e.id.toUpperCase())}</small><h3>${esc(e.title)}</h3></div><span class="stamp">${esc(e.type)}</span></div>
   ${imgsOf(e).length ? `<div class="photos">${imgsOf(e).map((src, i) => `<figure class="photo${e.wide ? ' wide' : ''}" style="--rot:${i % 2 ? '1.6deg' : '-1.2deg'}"><button class="zoomable" data-a="pzoom" data-src="${esc(src)}" aria-label="Powiększ zdjęcie"><img src="${esc(src)}" alt="${esc(e.title)}" loading="lazy"><span class="zoom-ic">⤢</span></button></figure>`).join('')}</div>` : ''}
   ${compact ? '' : `<p style="font-style:italic;color:var(--paperMuted);margin-top:0">${esc(e.summary)}</p>`}${blocksHTML(e.body)}${e.mark && !compact ? `<button class="amark ${(S.marks || {})[c.id] ? 'got' : ''}" data-a="amark" data-c="${esc(c.id)}" data-l="${esc(e.mark)}" title="Ta pieczęć nie należy do sprawy."><span class="amark-ic">${I.key || '⚿'}</span><span>ARCH.</span><b>${esc(e.mark)}</b></button>` : ''}</article>`;
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


/* --- PLAN MIEJSCA ZDARZENIA (szkic SVG z danych sprawy) --- */
const planView = {};
function spotLoc(c, sid) { const l = c.locations.find(l => l.spots.some(s => s.id === sid)); return l ? l.id : null; }
function spotNo(c, sid) { const l = c.locations.find(l => l.spots.some(s => s.id === sid)); return l ? l.spots.findIndex(s => s.id === sid) + 1 : 0; }
function planSvg(c, g, v) {
  const n = x => Math.round(x * 10) / 10;
  const out = [];
  const lbl = (x, y, t, cls, extra = '') => `<text class="${cls}" x="${n(x)}" y="${n(y)}" ${extra}>${esc(t)}</text>`;
  v.items.forEach(it => {
    if (it.req && it.t !== 'body' && !has(g, c, it.req)) return;
    if (it.unless && has(g, c, it.unless)) return;
    if (it.t === 'room') {
      const live = it.loc && c.loc[it.loc];
      const lx = it.lx != null ? it.lx : it.x + it.w / 2, ly = it.ly != null ? it.ly : it.y + it.h / 2 + 5;
      out.push(`<g class="pr ${it.cls || ''} ${live ? 'go' : ''}" ${live ? `data-a="loc" data-id="${it.loc}" role="button" tabindex="0" aria-label="${esc(c.loc[it.loc].name)}"` : ''}>
        <rect x="${it.x}" y="${it.y}" width="${it.w}" height="${it.h}"/>${it.label ? lbl(lx, ly, it.label, 'pl') : ''}${it.sub ? lbl(lx, ly + 17, it.sub, 'ps') : ''}</g>`);
    } else if (it.t === 'furn') {
      const cx = it.x + it.w / 2, cy = it.y + it.h / 2;
      out.push(`<g class="pf" ${it.rot ? `transform="rotate(${it.rot} ${cx} ${cy})"` : ''}><rect x="${it.x}" y="${it.y}" width="${it.w}" height="${it.h}" rx="2"/></g>${it.label ? lbl(it.lx != null ? it.lx : cx, it.ly != null ? it.ly : it.y + it.h + 13, it.label, 'pfl') : ''}`);
    } else if (it.t === 'circ') out.push(`<circle class="pc ${it.cls || ''}" cx="${it.x}" cy="${it.y}" r="${it.r}"/>`);
    else if (it.t === 'door') { const [a, b, x, y] = it.p; out.push(`<line class="pd" x1="${a}" y1="${b}" x2="${x}" y2="${y}"/>`); }
    else if (it.t === 'win') { const [a, b, x, y] = it.p; out.push(`<line class="pwg" x1="${a}" y1="${b}" x2="${x}" y2="${y}"/><line class="pw" x1="${a}" y1="${b}" x2="${x}" y2="${y}"/>`); }
    else if (it.t === 'line') { const [a, b, x, y] = it.p; out.push(`<line class="pln ${it.cls || ''}" x1="${a}" y1="${b}" x2="${x}" y2="${y}"/>`); }
    else if (it.t === 'text') out.push(lbl(it.x, it.y, it.label, 'pn ' + (it.cls || ''), `text-anchor="${it.anchor || 'middle'}" ${it.rot ? `transform="rotate(${it.rot} ${it.x} ${it.y})"` : ''}`));
    else if (it.t === 'body' && has(g, c, it.req)) out.push(it.pose === 'seated'
      ? `<g class="pbody" transform="translate(${it.x} ${it.y}) rotate(${it.rot || 0}) scale(${it.s || 1})"><image href="assets/plan/body-seated.webp" x="-35" y="-26" width="70" height="52"/></g>`
      : `<g class="pbody" transform="translate(${it.x} ${it.y}) rotate(${it.rot || 0}) scale(${it.s || 1})"><image href="assets/plan/body-lying.webp" transform="rotate(90)" x="0" y="-16" width="64" height="32"/></g>`);
  });
  Object.entries(v.spots || {}).forEach(([sid, [x, y]]) => {
    if (!g.spots.includes(sid)) return;
    const lid = spotLoc(c, sid); if (!lid) return;
    out.push(`<g class="mk" data-a="loc" data-id="${lid}" role="button" aria-label="${esc(c.spot[sid] ? c.spot[sid].name : '')}" transform="translate(${x} ${y})"><image href="assets/plan/marker.webp" x="-13" y="-15" width="26" height="28"/><text y="7">${spotNo(c, sid)}</text></g>`);
  });
  return `<svg class="plan" viewBox="0 0 ${v.w} ${v.h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Szkic: ${esc(v.name)}" style="--pw:${v.w}">
    <defs><pattern id="ph" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="10" stroke="rgba(43,34,25,.35)" stroke-width="2"/></pattern>
    <pattern id="pfo" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="3.2" fill="rgba(58,90,52,.38)"/><circle cx="13" cy="12" r="2.6" fill="rgba(58,90,52,.3)"/></pattern></defs>
    ${out.join('')}${v.north ? `<image class="pnorth" href="assets/plan/compass.webp" x="${v.w - 80}" y="6" width="72" height="70"/><text class="pn small" x="${v.w - 44}" y="90" text-anchor="middle">N ↑</text>` : ''}</svg>`;
}
function planBlock(c, g) {
  const views = c.plan.views.filter(v => !v.req || has(g, c, v.req)); let i = planView[c.id] || 0; if (!views[i]) i = 0;
  const marks = views.reduce((a, v) => a + Object.keys(v.spots || {}).filter(s => g.spots.includes(s)).length, 0);
  return `<section class="plan-card">
    <div class="plan-top"><div><div class="eyebrow">Szkic miejsca zdarzenia</div><small class="muted">Stuknijcie pomieszczenie, by do niego przejść. Żółte znaczniki — przeszukane punkty (${marks}).</small></div>
    ${views.length > 1 ? `<div class="plan-tabs">${views.map((v, k) => `<button class="chip ${k === i ? 'on' : ''}" data-a="plan-view" data-i="${k}">${esc(v.name)}</button>`).join('')}</div>` : ''}</div>
    <div class="plan-sheet"><img class="pdeco tape-a" src="assets/plan/tape1.webp" alt=""><img class="pdeco tape-b" src="assets/plan/tape2.webp" alt=""><img class="pdeco clip" src="assets/plan/clip.webp" alt=""><div class="plan-hint">← przesuńcie szkic w bok →</div><div class="plan-scroll">${planSvg(c, g, views[i])}</div></div></section>`;
}

/* --- MIEJSCA --- */
const ART_POS = ['30% 45%', '75% 35%', '50% 80%', '15% 70%', '90% 55%', '55% 20%'];
function locArt(c, l, i) { const img = l.img || (i % 2 ? c.cover : (c.art || c.cover)); return `background-image:url('${esc(img)}');background-position:${l.img ? 'center' : ART_POS[i % ART_POS.length]};${l.img ? '' : 'filter:saturate(.6) brightness(.75)'}`; }
function viewPlaces(c, g) {
  return `<div class="page-head"><div><div class="eyebrow">Plan miejsc</div><h2>Miejsca</h2><p>Każde przeszukanie punktu to jeden ruch. Niektóre punkty otworzycie dopiero, gdy będziecie wiedzieć, czego szukać.</p></div></div>
  ${c.plan ? planBlock(c, g) : ''}
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
  if (s.requires && s.requires.all && !s.requires.all.every(t => has(g, c, t))) return 'locked';
  return 'open';
}
function ovLocation(c, g, id) {
  const l = c.loc[id]; const i = c.locations.indexOf(l);
  return { title: l.name, kicker: l.kind, full: true, body: `<div class="scene" style="${locArt(c, l, i)}">${l.img ? `<button class="scene-zoom" data-a="pzoom" data-src="${esc(l.img)}" aria-label="Powiększ zdjęcie miejsca">⤢</button>` : ''}<div class="in"><div class="eyebrow">${esc(l.kind)}</div><h2>${esc(l.name)}</h2></div></div>
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
  if (!usePower(g, 'search')) g.actions++; g.spots.push(sid); gain(g, c, s.gives); save();
}

/* --- OSOBY --- */
function portrait(p, g, cls = '') { return `<div class="polaroid ${cls}" style="--rot:${rot(p.id)}"><div class="ph" ${p.img ? `style="background-image:url('${esc(p.img)}')"` : ''}>${p.img ? '' : `<span>${esc(initials(personName(g, p)))}</span>`}</div><div class="cap">${esc(personName(g, p))}</div></div>`; }
const initials = n => n.replace(/[„”"]/g, '').split(/\s+/).map(w => w[0]).join('').slice(0, 2).toUpperCase();
function availableQs(c, g, p) { return p.questions.filter(q => (!q.requires || q.requires.every(r => has(g, c, r))) && (!q.requiresAny || q.requiresAny.some(r => has(g, c, r)))); }
function openStatements(g, p) { return p.statements.filter(s => g.claims.includes(s.id)); }
function viewPeople(c, g) {
  return `<div class="page-head"><div><div class="eyebrow">Przesłuchania</div><h2>Osoby</h2><p>Każde pytanie to jeden ruch. Zeznania, które padną, trafiają do protokołu — możecie je podważyć dowodem. Nietrafiona konfrontacja kosztuje ${pkt(diffOf(g).wrong)}.</p></div></div>
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
  const tr = log.map(m => { if (m.t === 'q') return `<div class="tq">${esc(m.text)}</div>`; const vs = voiceFor(c, p.id, m); return `<div class="ta ${m.t === 'break' ? 'break' : m.t === 'deflect' ? 'deflect' : ''}"><span class="who">${esc(personName(g, p))}${m.t === 'break' ? ' · po konfrontacji' : ''}${vs ? `<button class="vplay" data-a="vplay" data-src="${esc(vs)}" aria-label="Odsłuchaj wypowiedź">${I.sound}</button>` : ''}</span>${esc(m.text)}</div>`; }).join('');
  return { title: personName(g, p), kicker: 'Przesłuchanie', full: true, body: head + `${c.voiceDir ? `<div class="vbar"><button class="btn small ghost" data-a="voices-toggle">${voicesOn() ? I.sound + ' Głosy świadków: włączone' : I.mute + ' Głosy świadków: wyłączone'}</button></div>` : ''}<div class="transcript" id="transcript">${tr || '<p class="muted">Rozmowa jeszcze się nie zaczęła.</p>'}</div>
   <div class="eyebrow" style="margin:18px 0 8px">Zadaj pytanie · 1 ruch</div>
   <div class="qlist">${qs.map(q => `<button class="q ${g.asked.includes(q.id) ? 'asked' : ''}" data-a="ask" data-id="${q.id}" ${g.asked.includes(q.id) ? 'disabled' : ''}>${esc(q.q)}</button>`).join('')}</div>
   ${qs.length < p.questions.length ? `<p class="muted" style="font-size:.85rem;margin-top:10px">Kolejne pytania pojawią się, gdy zdobędziecie odpowiednie materiały.</p>` : ''}` };
}
function doAsk(c, g, qid) {
  const q = c.q[qid]; if (g.asked.includes(qid)) return;
  if (!usePower(g, 'ask')) g.actions++; g.asked.push(qid);
  (g.log[q.person] = g.log[q.person] || []).push({ t: 'q', text: q.q }, { t: 'a', text: q.a, v: c.voiceDir ? `${c.voiceDir}/${q.id}.mp3` : undefined });
  (q.claims || []).forEach(s => { if (!g.claims.includes(s)) g.claims.push(s); });
  gain(g, c, q.gives); save();
}
function ovConfront(c, g, sid) {
  const s = c.stmt[sid]; const p = c.person[s.person];
  const ids = visibleEvidence(g, c);
  const others = g.claims.map(id => c.stmt[id]).filter(x => x && x.person !== s.person);
  return { title: 'Konfrontacja', kicker: personName(g, p), body: `<div class="stmt"><q>${esc(s.text)}</q></div>
   <p class="muted" style="margin:14px 0 4px">Co przeczy temu zeznaniu? Możecie okazać dowód albo zestawić je z zeznaniem innej osoby. Konfrontacja kosztuje 1 ruch; nietrafiona dodatkowo ${diffOf(g).wrong} pkt.${g.armed === 'confront' ? ' <b>Aktywna zdolność „Sprawdzam”: bez ruchu i bez kary.</b>' : ''}</p>
   <div class="eyebrow" style="margin-top:12px">Dowody</div>
   <div class="pick">${ids.map(id => `<button data-a="confront-with" data-s="${sid}" data-id="${id}"><small>${esc(c.ev[id].type)} · ${esc(id.toUpperCase())}</small>${esc(c.ev[id].title)}</button>`).join('')}</div>
   ${others.length ? `<div class="eyebrow" style="margin-top:16px">Zeznania innych osób</div><div class="pick">${others.map(x => `<button data-a="confront-with" data-s="${sid}" data-id="st:${x.id}"><small>${esc(personName(g, c.person[x.person]))}</small>„${esc(x.text)}”</button>`).join('')}</div>` : ''}` };
}
function doConfront(c, g, sid, evid) {
  const s = c.stmt[sid]; const p = c.person[s.person];
  const L = (g.log[p.id] = g.log[p.id] || []);
  const free = usePower(g, 'confront'); if (!free) g.actions++;
  L.push({ t: 'q', text: evid.startsWith('st:') ? `Konfrontacja: „${s.text}” — zestawiamy z zeznaniem: ${personName(g, c.person[c.stmt[evid.slice(3)].person])} — „${c.stmt[evid.slice(3)].text}”.` : `Konfrontacja: „${s.text}” — okazujemy: ${c.ev[evid].title}.` });
  if (!s.truth && (s.contradicts || []).includes(evid)) {
    g.broken.push(sid); L.push({ t: 'break', text: s.response, v: c.voiceDir ? `${c.voiceDir}/${sid}.mp3` : undefined });
    (s.reveals || []).forEach(r => { if (!g.claims.includes(r)) g.claims.push(r); });
    gain(g, c, s.gives); save();
    toast('Zeznanie podważone', personName(g, p), 'Konfrontacja'); sfx('break');
    return true;
  }
  if (!free) g.failed++; const d = p.deflect || ['To niczego nie dowodzi.'];
  const di = (g.failed + L.length) % d.length; L.push({ t: 'deflect', text: d[di], v: c.voiceDir && p.deflect ? `${c.voiceDir}/${p.id}-deflect-${di}.mp3` : undefined }); save();
  toast('Nietrafiona konfrontacja', free ? 'Zdolność „Sprawdzam” — bez kary' : `−${diffOf(g).wrong} pkt w raporcie`, 'Błąd'); sfx('wrong');
  return false;
}

/* --- ANALIZA --- */
let anaTab = 'zagadki';
function puzzleVisible(c, g, pz) { return pz.requires.every(r => has(g, c, r)); }
function viewAnalysis(c, g) {
  const tabs = [['zagadki', 'Zagadki'], ['czas', 'Oś czasu'], ['podejrzani', 'Podejrzani'], ...(c.mode === 'table' ? [] : [['tajne', 'Tajne akta']]), ['zespol', 'Zespół'], ['notatki', 'Notatki']];
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
  if (anaTab === 'podejrzani') inner = matrixHTML(c, g);
  if (anaTab === 'zespol') inner = teamHTML(c, g);
  if (anaTab === 'notatki') inner = `<div class="field"><label for="notes">Wspólne notatki zespołu</label><textarea class="input" id="notes" data-notes placeholder="Hipotezy, podejrzenia, pytania do sprawdzenia…">${esc(g.notes)}</textarea></div>`;
  return `<div class="page-head"><div><div class="eyebrow">Warsztat dedukcji</div><h2>Analiza</h2><p>Zagadki, oś czasu, podejrzani${c.mode === 'table' ? '' : ', tajne akta'}, zespół i notatki. Gdy jesteście pewni — złóżcie akt oskarżenia.</p></div></div>
   <div class="tabs">${tabs.map(([k, l]) => `<button aria-pressed="${anaTab === k}" data-a="ana" data-t="${k}">${l}</button>`).join('')}</div>${inner}
   ${g.report ? `<button class="big-cta" data-a="tab" data-tab="wynik"><span class="seal">Ś</span><span><b>Raport złożony</b><span class="muted">Wynik: ${g.report.total} pkt — zobacz rozwiązanie</span></span></button>` :
   `<button class="big-cta" data-a="to-report"><span class="seal">Ś</span><span><b>Akt oskarżenia</b><span class="muted">Złóżcie raport końcowy. Po podpisaniu nie da się go zmienić.</span></span></button>`}`;
}
const MX_COLS = [['motyw', 'Motyw'], ['okazja', 'Okazja'], ['alibi', 'Alibi'], ['uwagi', 'Uwagi']];
function matrixHTML(c, g) {
  const m = g.matrix || {};
  return `<p class="muted">Wasza wspólna tabela podejrzanych. Gra niczego tu nie podpowiada — wpisujcie własne ustalenia. Licznik podważonych zeznań bierze się z protokołów.</p>
   <div class="mx">${c.people.map(p => { const br = p.statements.filter(s => g.broken.includes(s.id)).length; return `<div class="mx-row"><div class="mx-who">${portrait(p, g, 'mini')}<div><b>${esc(personName(g, p))}</b><small>${esc(personRole(g, p))}</small>${br ? `<span class="chip red">${br} podważone</span>` : ''}</div></div>
     <div class="mx-cells">${MX_COLS.map(([k, l]) => `<label class="mx-cell"><span>${l}</span><textarea data-mx="${p.id}|${k}" rows="2" placeholder="—">${esc((m[p.id] || {})[k] || '')}</textarea></label>`).join('')}</div></div>`; }).join('')}</div>`;
}
function teamHTML(c, g) {
  const D = diffOf(g);
  const pw = g.players.map(pl => { const P = POWERS[pl.role]; const used = (g.used || {})[pl.role]; const armed = g.armed === P.kind && !used;
    return `<div class="panel power ${used ? 'used' : ''}"><div class="eyebrow">${esc(ROLES.find(r => r.id === pl.role).name)}</div><h3>${esc(pl.name)}</h3><p><b>${esc(P.name)}</b> — ${esc(P.desc)}</p>
     ${used ? '<span class="chip">Wykorzystana</span>' : armed ? `<span class="chip red">Aktywna — zadziała przy następnej akcji</span> <button class="btn small ghost" data-a="power-off">Anuluj</button>` : `<button class="btn small" data-a="power" data-role="${pl.role}" ${g.report ? 'disabled' : ''}>Użyj zdolności</button>`}</div>`; }).join('');
  const vote = g.mode === 'phones' ? `<div class="panel"><div class="eyebrow">Przed aktem oskarżenia</div><h3>Głosowanie zespołu</h3><p>Każdy w swoim telefonie (w teczce) typuje sprawcę i motyw — po cichu. Na sygnał wszyscy pokazujecie ekrany. Jeśli się nie zgadzacie, najpierw dyskusja, potem raport.</p><button class="btn" data-a="vote" ${g.report ? 'disabled' : ''}>Rozpocznij głosowanie</button>${g.vote ? `<p class="muted" style="margin-top:10px">Ostatnie głosowanie: ${g.vote === 'zgodni' ? 'zespół zgodny' : 'zespół podzielony'}.</p>` : ''}</div>` : '';
  return `<p class="muted">Poziom trudności: <b>${esc(D.name)}</b> · norma ruchów: <b>${effPar(c, g)}</b>. Każda rola ma jedną zdolność na całą sprawę. Uzgodnijcie, kto i kiedy jej użyje.</p>
   ${vote}<div class="cards2" style="margin-top:16px">${pw}</div>`;
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
   <div class="row-actions"><button class="btn" data-a="solve" data-id="${id}">Sprawdź</button>${(st.hints || 0) < Math.min(pz.hints.length, diffOf(g).hints) ? `<button class="btn ghost" data-a="phint" data-id="${id}">Podpowiedź (${g.armed === 'hint' ? 'zdolność: bez kary' : '−' + diffOf(g).hint + ' pkt'})</button>` : ''}</div>
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
  return `<div class="page-head"><div><div class="eyebrow">Tablica śledcza</div><h2>Tablica</h2><p>Przypinajcie dowody i osoby z akt i przesłuchań. Przeciągajcie karty, łączcie je czerwoną nitką. Dotknij nitki, by ją usunąć. Tablicę przybliżacie dwoma palcami, przyciskami + i − albo Ctrl + kółkiem myszy.</p></div></div>
   <div class="board-tools"><button class="btn small ${linkMode ? 'red' : 'ghost'}" data-a="link-mode">${I.link} ${linkMode ? 'Wybierz dwie karty' : 'Połącz'}</button>
    <button class="btn small ghost" data-a="note-add">${I.plus} Notatka</button>
    <button class="btn small ghost" data-a="board-del" ${boardSel ? '' : 'disabled'}>${I.trash} Usuń kartę</button>
    <span style="flex:1"></span><button class="icon-btn" data-a="zoom" data-d="-1" aria-label="Pomniejsz">${I.minus}</button><button class="icon-btn" data-a="zoom" data-d="1" aria-label="Powiększ">${I.plus}</button></div>
   <div class="board-wrap" id="bwrap"><div style="position:relative;width:${1700 * (g.board.zoom || 1)}px;height:${1150 * (g.board.zoom || 1)}px"><div class="board" id="board" style="transform:scale(${g.board.zoom || 1})"></div></div></div>
   ${g.board.items.length ? '' : '<p class="muted" style="margin-top:10px">Tablica jest pusta. Otwórzcie dowód lub osobę i użyjcie przycisku „Na tablicę”.</p>'}`;
}
let boardPinch = false;
function boardZoomTo(g, nz, fx, fy) { // fx, fy — punkt w oknie tablicy, który ma zostać pod palcami
  const w = $('#bwrap'), b = $('#board'); if (!w || !b) return; const z0 = g.board.zoom || 1; nz = Math.max(0.4, Math.min(1.6, nz)); if (Math.abs(nz - z0) < 0.001) return;
  const bx = (w.scrollLeft + fx) / z0, by = (w.scrollTop + fy) / z0; g.board.zoom = nz;
  b.style.transform = `scale(${nz})`; b.parentElement.style.width = 1700 * nz + 'px'; b.parentElement.style.height = 1150 * nz + 'px'; b.parentElement.style.setProperty('--z', nz);
  w.scrollLeft = bx * nz - fx; w.scrollTop = by * nz - fy;
}
function mountBoardGestures(g) {
  const w = $('#bwrap'); if (!w || w.dataset.g) return; w.dataset.g = '1';
  let d0 = 0, z0 = 1; const pts = e => [...e.touches].slice(0, 2); const rel = (t, r) => ({ x: (t[0].clientX + t[1].clientX) / 2 - r.left, y: (t[0].clientY + t[1].clientY) / 2 - r.top });
  w.addEventListener('touchstart', e => { if (e.touches.length === 2) { const t = pts(e); d0 = Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY); z0 = g.board.zoom || 1; boardPinch = true; } }, { passive: true });
  w.addEventListener('touchmove', e => { if (e.touches.length !== 2 || !d0) return; e.preventDefault(); const t = pts(e); const d = Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY); const c = rel(t, w.getBoundingClientRect()); boardZoomTo(g, z0 * d / d0, c.x, c.y); }, { passive: false });
  const end = e => { if (boardPinch && e.touches.length < 2) { boardPinch = false; d0 = 0; save(); } };
  w.addEventListener('touchend', end); w.addEventListener('touchcancel', end);
  w.addEventListener('wheel', e => { if (!e.ctrlKey) return; e.preventDefault(); const r = w.getBoundingClientRect(); boardZoomTo(g, (g.board.zoom || 1) * Math.exp(-e.deltaY / 300), e.clientX - r.left, e.clientY - r.top); clearTimeout(w._t); w._t = setTimeout(save, 300); }, { passive: false });
}
function mountBoard(c, g) {
  const b = $('#board'); if (!b) return; mountBoardGestures(g);
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
    if (pid !== e.pointerId) return; if (boardPinch) { moved = true; return; } const z = g.board.zoom || 1;
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
  const D = diffOf(g); const par = effPar(c, g);
  const hintPen = Object.values(g.puzzles).reduce((s, p) => s + Math.max(0, (p.hints || 0) - (p.free || 0)) * D.hint, 0);
  const pen = [['Podpowiedzi w zagadkach', hintPen], ['Tropy', g.trops * (D.trop || 0)], ['Nietrafione konfrontacje', g.failed * D.wrong], [`Ruchy ponad normę (${g.actions}/${par})`, Math.min(15, Math.ceil(Math.max(0, g.actions - par) / 2))]];
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
  return `<div class="rep-step"><div class="score"><div class="eyebrow">Wynik zespołu</div><div class="n">${R.total}</div><div class="eyebrow">na 100 punktów</div><div class="rank stamp drop">${esc(R.rank)}</div></div>
   <div class="breakdown">${R.lines.map(l => `<div><span>${esc(l[0])}</span><b class="${l[3] ? 'ok' : 'no'}">${l[1]}/${l[2]}</b></div>`).join('')}${R.pen.filter(p => p[1]).map(p => `<div><span>${esc(p[0])}</span><b class="no">−${p[1]}</b></div>`).join('')}</div>
   ${ending}
   <details class="panel" style="margin-top:18px"><summary class="eyebrow" style="cursor:pointer;padding:6px 0">Pełne rozwiązanie — jak można było to wydedukować</summary>
    <p style="font-family:var(--f-display);font-size:1.4rem;color:var(--txt)">${esc(c.solution.summary)}</p>${c.solution.steps.map(s => `<div class="sol-step"><b>${esc(s.h)}</b><p>${esc(s.p)}</p></div>`).join('')}</details>
   <div class="row-actions"><button class="btn" data-a="home">Archiwum spraw</button><button class="btn ghost" data-a="print-report">Akt oskarżenia do druku / PDF</button><button class="btn ghost" data-a="chronicle">Kronika wydziału</button><button class="btn ghost" data-a="restart" data-id="${c.id}">Zagraj ponownie</button></div></div>`;
}

/* ---------- nakładki: render ---------- */
async function renderOv() {
  const root = $('#overlay-root'); const o = topOv();
  if (!o) { root.innerHTML = ''; document.body.style.overflow = ''; return; }
  const r = route(); const c = r.id && caseFor(r.id); const g = r.id && G(r.id);
  let v;
  if (o.type === 'settings') v = ovSettings();
  else if (o.type === 'menu') v = ovMenu(c, g);
  else if (o.type === 'guide') v = ovGuide(o);
  else if (o.type === 'zoom') { root.innerHTML = `<div class="zoom" id="zoom"><img src="${esc(o.src)}" alt="" id="zoomimg" draggable="false"><div class="zoom-bar"><span><span class="zh-touch">Rozsuń dwa palce, by przybliżyć · przeciągnij, by przesunąć · dwa stuknięcia: przybliż lub wróć</span><span class="zh-mouse">Kółko myszy przybliża · przeciągnij, by przesunąć · dwuklik: przybliż lub wróć</span></span><button class="icon-btn" data-a="close" aria-label="Zamknij">${I.close}</button></div></div>`; document.body.style.overflow = 'hidden'; mountZoom(); return; }
  else if (o.type === 'vote') v = ovVote(c, g, o);
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
  else if (o.type === 'trop') v = o.text ? { title: 'Trop', kicker: 'Podpowiedź zespołu', body: `<div class="hint-box" style="font-size:1.05rem">${esc(o.text)}</div>` } : { title: 'Trop', kicker: 'Podpowiedź', body: diffOf(g).trop == null && g.armed !== 'trop' ? `<p>Na poziomie <b>Weteran</b> szef wydziału nie daje tropów. Radzicie sobie sami.</p>` : `<p>Utknęliście? Szef wydziału podsunie kierunek. ${g.armed === 'trop' ? '<b>Aktywna zdolność „Odprawa u szefa”: ten trop jest bez kary.</b>' : `Każdy trop kosztuje <b>${diffOf(g).trop} pkt</b> w raporcie końcowym.`} Wykorzystane tropy: ${g.trops + (g.freeTrops || 0)}.</p><div class="row-actions"><button class="btn" data-a="trop-go">Pokaż trop${g.armed === 'trop' ? '' : ` (−${diffOf(g).trop} pkt)`}</button><button class="btn ghost" data-a="close">Jeszcze nie</button></div>` };
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
   <div class="settings-row"><div><b>Głosy świadków</b><small>Odpowiedzi w przesłuchaniach czyta lektor — każda postać ma własny głos. Działa niezależnie od dźwięku klimatu. Każdą kwestię możecie odsłuchać ponownie.</small></div><button class="switch" aria-pressed="${s.voices !== false}" data-a="voices-toggle" aria-label="Głosy świadków"></button></div>
   <div class="settings-row ${s.voices !== false ? '' : 'off'}"><div style="flex:1"><b>Głośność głosów</b><input type="range" min="0" max="100" step="5" value="${Math.round(vol('voice') * 100)}" data-vol="voice" aria-label="Głośność głosów" class="range"></div></div>
   <div class="settings-row"><div><b>Wielkość tekstu</b><small>Dla czytania przy stole</small></div><div class="seg">${[['m', 'A'], ['l', 'A+'], ['xl', 'A++']].map(([k, l]) => `<button aria-pressed="${s.text === k}" data-a="text" data-v="${k}">${l}</button>`).join('')}</div></div>
   <div class="settings-row"><div><b>Instruktaż przed sprawą</b><small>Krótki przewodnik po zasadach i ekranach gry, pokazywany po wybraniu trybu. W trakcie gry zawsze dostępny w menu.</small></div><button class="switch" aria-pressed="${s.guide !== false}" data-a="guide-toggle" aria-label="Instruktaż przed sprawą"></button></div>
   <div class="settings-row"><div><b>Animacje</b><small>Wyłącz, jeśli przeszkadzają</small></div><button class="switch" aria-pressed="${s.motion === 'on'}" data-a="motion" aria-label="Animacje"></button></div>
   <div class="settings-row"><div><b>Kopia zapasowa</b><small>Postęp jest zapisywany na tym urządzeniu. Eksportuj, by przenieść go gdzie indziej.</small></div></div>
   <div class="row-actions"><button class="btn small ghost" data-a="export">Eksportuj zapis</button><label class="btn small ghost" style="cursor:pointer">Importuj zapis<input type="file" accept="application/json,.json" data-import hidden></label></div>
   <hr class="sep"><button class="btn small ghost" data-a="wipe">Usuń wszystkie zapisy</button>` };
}
function ovMenu(c, g) {
  return { title: 'Menu sprawy', kicker: c ? 'Akta ' + c.id : '', body: `<div class="qlist">
   <button class="q" data-a="show-brief">Briefing i zadania sprawy</button>
   <button class="q" data-a="show-guide">Jak grać — instruktaż</button>
   <button class="q" data-a="sound">${S.settings.sound ? 'Wyłącz dźwięk' : 'Włącz dźwięk'}</button>
   <button class="q" data-a="settings">Ustawienia · wersja ${VERSION}</button>
   <button class="q" data-a="restart" data-id="${c ? c.id : ''}">Zacznij sprawę od nowa</button>
   <button class="q" data-a="home">Wróć do archiwum</button></div>` };
}

/* ---------- powiększanie zdjęć ---------- */
function mountZoom() {
  const box = $('#zoom'), img = $('#zoomimg'); if (!box || !img) return;
  let s = 1, x = 0, y = 0; const pts = new Map(); let start = null;
  const apply = () => { img.style.transform = `translate(${x}px,${y}px) scale(${s})`; };
  const clamp = () => { s = Math.min(6, Math.max(1, s)); if (s === 1) { x = 0; y = 0; } };
  box.addEventListener('wheel', e => { e.preventDefault(); const k = e.deltaY < 0 ? 1.15 : 1 / 1.15; s *= k; x *= k; y *= k; clamp(); apply(); }, { passive: false });
  box.addEventListener('dblclick', e => { if (e.target.closest('.zoom-bar')) return; s = s > 1 ? 1 : 2.5; x = 0; y = 0; apply(); });
  box.addEventListener('pointerdown', e => { if (e.target.closest('.zoom-bar')) return; box.setPointerCapture(e.pointerId); pts.set(e.pointerId, { x: e.clientX, y: e.clientY }); start = { s, x, y, pts: new Map(pts) }; });
  box.addEventListener('pointermove', e => { if (!pts.has(e.pointerId)) return; pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    const a0 = [...start.pts.values()], a1 = [...pts.values()];
    if (a1.length >= 2 && a0.length >= 2) { const d0 = Math.hypot(a0[0].x - a0[1].x, a0[0].y - a0[1].y), d1 = Math.hypot(a1[0].x - a1[1].x, a1[0].y - a1[1].y); s = start.s * d1 / (d0 || 1); clamp(); }
    else if (a1.length === 1 && a0.length >= 1 && s > 1) { x = start.x + (a1[0].x - a0[0].x); y = start.y + (a1[0].y - a0[0].y); }
    apply(); });
  const end = e => { pts.delete(e.pointerId); start = { s, x, y, pts: new Map(pts) }; };
  box.addEventListener('pointerup', end); box.addEventListener('pointercancel', end);
}
/* ---------- głosowanie zespołu (tryb z telefonami) ---------- */
function ovVote(c, g, o) {
  const st = o.st || 0;
  if (st === 0) return { title: 'Głosowanie zespołu', kicker: 'Przed aktem oskarżenia', body: `<p>Każdy otwiera swoją teczkę w telefonie i na samym dole wybiera w sekcji <b>„Mój typ”</b> sprawcę i motyw. Po cichu, bez podglądania.</p><p>Gdy wszyscy są gotowi, naciśnijcie start — po odliczaniu wszyscy jednocześnie pokazujecie telefony.</p><button class="btn" data-a="vote-go">Wszyscy gotowi — start</button>` };
  if (st === 1) return { title: 'Głosowanie zespołu', kicker: 'Uwaga…', body: `<div class="vote-count" id="votecount">3</div>` };
  return { title: 'Pokażcie telefony!', kicker: 'Głosowanie zespołu', body: `<div class="vote-show">Ekrany do góry!</div><p>Czy wszyscy wskazali tę samą osobę i ten sam motyw?</p><div class="row-actions"><button class="btn" data-a="vote-res" data-v="zgodni">Tak — jesteśmy zgodni</button><button class="btn ghost" data-a="vote-res" data-v="podzieleni">Nie — musimy porozmawiać</button></div>` };
}
/* ---------- kronika wydziału ---------- */
function badgesFor(c, g, R) {
  const b = [];
  if (!g.trops && !g.freeTrops) b.push('Bez tropów');
  if (!g.failed) b.push('Zero pomyłek');
  if (!Object.values(g.puzzles).some(p => p.hints)) b.push('Bez podpowiedzi');
  if (g.actions <= effPar(c, g)) b.push('Oszczędni');
  if (g.diff === 'weteran') b.push('Weterani');
  if (R.total >= 92) b.push('Legenda');
  return b;
}
function addChronicle(c, g) {
  const R = g.report; S.chronicle = S.chronicle || [];
  S.chronicle.push({ id: c.id, title: c.title, total: R.total, rank: R.rank, actions: g.actions, par: effPar(c, g), diff: g.diff || 'sledczy', mode: g.mode, team: g.players.map(p => p.name), at: R.at, badges: badgesFor(c, g, R) });
}
async function renderChronicle() {
  const cat = await getCatalog(); const L = (S.chronicle || []).slice().sort((x, y) => y.at - x.at); const M = S.marks || {};
  const slots = MARK_ORDER.map(id => `<span class="mslot ${M[id] ? 'on' : ''}">${M[id] ? esc(M[id]) : ''}</span>`).join('');
  app().innerHTML = `<div class="chron"><header class="chron-head"><button class="icon-btn" data-a="home" aria-label="Archiwum">${I.back}</button><div><div class="eyebrow">Wydział spraw niewyjaśnionych</div><h1>Kronika wydziału</h1></div></header>
   <section class="panel"><div class="eyebrow">Ślady Archiwisty</div><h3>Pieczęcie, które nie należały do żadnej sprawy</h3><p class="muted">W aktach niektórych spraw ktoś zostawił obcą pieczęć z kluczem. Zabezpieczajcie je — każda kryje jedną literę. Kiedy zbierzecie wszystkie, otworzą się akta, których nie ma w archiwum.</p><div class="mslots">${slots}</div><p class="muted" style="font-size:.85rem">${Object.keys(M).length} z ${MARK_ORDER.length}</p></section>
   ${L.length ? `<div class="chron-list">${L.map(e => `<article class="paper chron-item"><div class="eyebrow">Akta ${esc(e.id)} · ${new Date(e.at).toLocaleDateString('pl-PL')} · ${esc((DIFFS[e.diff] || DIFFS.sledczy).name)} · ${e.mode === 'phones' ? 'Telewizor + telefony' : 'Wspólny stół'}</div><h3>${esc(e.title)}</h3><div class="chron-score"><b>${e.total}</b><span>pkt</span><span class="stamp">${esc(e.rank)}</span></div><p>Zespół: ${e.team.map(esc).join(', ')} · ruchy: ${e.actions}/${e.par}</p>${e.badges.length ? `<div class="badges">${e.badges.map(x => `<span class="badge-m">${esc(x)}</span>`).join('')}</div>` : ''}</article>`).join('')}</div>` : '<div class="empty">Kronika jest jeszcze pusta. Zamknijcie pierwszą sprawę.</div>'}
   <section class="panel"><div class="eyebrow">Odznaki</div><p class="muted">Bez tropów · Zero pomyłek (bez nietrafionych konfrontacji) · Bez podpowiedzi · Oszczędni (w normie ruchów) · Weterani (poziom Weteran) · Legenda (92+ pkt)</p></section></div>`;
}
/* ---------- akt oskarżenia do druku ---------- */
function printReport(c, g) {
  const R = g.report; const Q = c.report.questions;
  const ans = q => q.type === 'order' ? (R.order || []).map(k => (q.items.find(x => x[0] === k) || [, k])[1]).join(' → ') : ((q.options.find(o => o[0] === R.answers[q.id]) || [, '—'])[1]);
  const role = id => (ROLES.find(r => r.id === id) || { name: '' }).name;
  const el = document.createElement('div'); el.id = 'printable';
  el.innerHTML = `<div class="pr-doc"><div class="pr-top"><div>WYDZIAŁ SPRAW NIEWYJAŚNIONYCH<br><small>Archiwum ŚLAD · dokument fikcyjny</small></div><div>Sygn. akt: ${esc(c.id)}/${new Date(R.at).getFullYear()}<br>${new Date(R.at).toLocaleDateString('pl-PL')}</div></div>
   <h1>AKT OSKARŻENIA</h1><h2>w sprawie: ${esc(c.title)}</h2>
   <table class="pr-t">${Q.map(q => `<tr><th>${esc(q.type === 'order' ? 'Przebieg wydarzeń' : q.q)}</th><td>${esc(ans(q))}</td></tr>`).join('')}<tr><th>Dowody wskazane przeciwko sprawcy</th><td>${(R.proofs || []).map(id => esc(c.ev[id] ? c.ev[id].title : id)).join('; ') || '—'}</td></tr></table>
   <p class="pr-score">Ocena zespołu: <b>${R.total}/100</b> · ranga: <b>${esc(R.rank)}</b> · ruchy: ${g.actions}/${effPar(c, g)} · poziom: ${esc(diffOf(g).name)}</p>
   <div class="pr-sign">${g.players.map(p => `<div><span></span>${esc(p.name)}<small>${esc(role(p.role))}</small></div>`).join('')}</div>
   <p class="pr-foot">Wszystkie osoby, miejsca i zdarzenia są fikcyjne. Dokument wygenerowany przez grę ŚLAD.</p></div>`;
  document.body.appendChild(el); document.body.classList.add('printing');
  const done = () => { document.body.classList.remove('printing'); el.remove(); window.removeEventListener('afterprint', done); };
  window.addEventListener('afterprint', done); setTimeout(() => window.print(), 50); setTimeout(() => { if (document.body.classList.contains('printing')) done(); }, 60000);
}

/* ---------- instruktaż przed sprawą ---------- */
function guideCards(mode, diff) {
  const phones = mode === 'phones'; const D = DIFFS[diff || 'sledczy'] || DIFFS.sledczy;
  return [
   { k: 'Witajcie w wydziale', t: 'O co chodzi w tej grze', b: `<p>Jesteście zespołem śledczych. Dostajecie akta sprawy i macie ją rozwiązać: <b>kto, jak, kiedy i dlaczego</b>.</p><p>Na końcu składacie <b>akt oskarżenia</b> i każdy wniosek podpieracie dowodami. Nie ma limitu czasu ani losowości — wszystko, czego potrzebujecie, jest w aktach, miejscach i zeznaniach.</p><p class="g-tip">To planszówka do rozmowy. Ekran to tylko teczka z aktami — najważniejsze dzieje się między wami: czytajcie na głos, spierajcie się, notujcie, sprawdzajcie się nawzajem.</p>` },
   { k: 'Ekran gry', t: 'Pięć zakładek i górny pasek', b: `<ul class="g-list"><li><b>${I.files} Akta</b> — wszystkie zdobyte dokumenty. Nowe mają czerwony licznik. Każdy dokument można przypiąć na tablicę.</li><li><b>${I.map} Miejsca</b> — szkic miejsca zdarzenia i karty miejsc do przeszukania.</li><li><b>${I.people} Osoby</b> — przesłuchania świadków i podejrzanych.</li><li><b>${I.brain} Analiza</b> — zagadki, oś czasu, tabela podejrzanych${phones ? ', tajne akta' : ''}, zespół i zdolności ról, notatki i akt oskarżenia.</li><li><b>${I.board} Tablica</b> — korkowa tablica z czerwoną nitką.</li></ul><p>Na górze: <b>licznik ruchów</b>, <b>żarówka</b> (trop, gdy utkniecie), dźwięk i <b>menu</b> — tam jest briefing sprawy, ten instruktaż i ustawienia.</p>` },
   { k: 'Ruchy i punkty', t: 'Co kosztuje, a co jest za darmo', b: `<p><b>Jeden ruch</b> to: przeszukanie punktu w miejscu, jedno pytanie zadane świadkowi albo jedna konfrontacja.</p><p><b>Za darmo:</b> czytanie akt, szkic, zagadki, oś czasu, notatki i tablica.</p><p>Wybrany poziom: <b>${esc(D.name)}</b>.</p><table class="g-table"><tr><td>Ruchy ponad normę sprawy</td><td>−1 pkt za każde 2 ruchy (najwyżej −15)</td></tr><tr><td>Podpowiedź w zagadce</td><td>−${D.hint} pkt (najwyżej ${D.hints} na zagadkę)</td></tr><tr><td>Trop (żarówka)</td><td>${D.trop == null ? 'niedostępny (wyjątek: zdolność Koordynatora)' : '−' + D.trop + ' pkt'}</td></tr><tr><td>Nietrafiona konfrontacja</td><td>−${D.wrong} pkt</td></tr></table><p>Rangi: Stażysta, Aspirant (40), Inspektor (60), Komisarz (78), <b>Legenda archiwum (92+)</b>. Zanim wydacie ruch — porozmawiajcie, czy warto.</p>` },
   { k: 'Miejsca', t: 'Przeszukiwanie i szkic miejsca zdarzenia', b: `<p>Każde miejsce ma kilka <b>punktów</b>. Przeszukanie punktu to jeden ruch i zwykle daje nowe dowody.</p><p>Niektóre punkty są <b>zablokowane</b> ${I.lock}. Otwiera je rozwiązana zagadka albo postęp w śledztwie — na przykład nakaz prokuratora po podważeniu czyjegoś zeznania. Opis blokady podpowiada, czego brakuje.</p><p>Nad kartami jest <b>szkic</b>: stuknijcie pomieszczenie, by do niego przejść. Na przeszukanych punktach pojawiają się żółte tabliczki z numerami, a obrys ciała — dopiero po oględzinach. Szkic pokazuje tylko to, co widzielibyście na miejscu.</p><p>Każde zdjęcie — w aktach i w miejscach — możecie <b>powiększyć</b> dotknięciem. Przybliżajcie palcami albo kółkiem myszy: szczegóły mają znaczenie.</p>` },
   { k: 'Przesłuchania', t: 'Pytania, protokół, konfrontacje', b: `<p>Wybierzcie osobę i zadawajcie pytania. <b>Nowe pytania pojawiają się</b>, gdy zdobędziecie dowody, które dają do nich podstawę.</p><p>Ważne zdania świadków trafiają do <b>protokołu</b>. Jeśli macie dowód, który przeczy zeznaniu — zróbcie <b>konfrontację</b>: wskażcie zdanie i dowód. Możecie też <b>zestawić dwa zeznania</b> — gdy jeden świadek mówi coś, co wyklucza wersję drugiego. Trafiona konfrontacja zmusza świadka do zmiany wersji i często daje nowe informacje. Nietrafiona kosztuje ${pkt(D.wrong)}.</p><p class="g-tip">Słuchajcie uważnie. Świadkowie odpowiadają dokładnie na to, o co pytacie. Jeśli ktoś powie za dużo albo wie coś, czego nie mógł wiedzieć — to nie przypadek. Na taką wpadkę nie ma przycisku: musicie ją wyłapać sami.</p><p><b>Każdy świadek ma swój głos</b> — odpowiedzi czyta lektor, a przycisk z głośnikiem przy wypowiedzi odtwarza ją ponownie. Głosy wyłączycie w oknie przesłuchania albo w ustawieniach.</p>` },
   { k: 'Analiza', t: 'Zagadki, oś czasu, tablica', b: `<p><b>Zagadki</b> pojawiają się, gdy macie potrzebne materiały. Odpowiedzi nie ma w żadnym dokumencie wprost — trzeba połączyć kilka faktów. Na tym poziomie każda ma ${D.hints === 1 ? `jedną podpowiedź (−${D.hint} pkt)` : `${podp(D.hints)} (po −${D.hint} pkt)`}.</p><p><b>Oś czasu</b> zbiera godziny z dokumentów i zeznań. Wpisy oznaczone „ustalone” pochodzą z rozwiązanych zagadek. Pamiętajcie: zeznanie to wersja świadka, nie fakt.</p><p><b>Podejrzani</b> to wspólna tabela: motyw, okazja, alibi — wypełniacie ją sami. <b>Notatki</b> są wspólne, a na <b>tablicy</b> przypinacie dowody i osoby i łączycie je nitką.</p><p>Gdy odkryjecie coś kluczowego, ekran zatrzyma się na chwilę — to <b>przełom</b> w śledztwie.</p>` },
   { k: 'Zespół', t: 'Role i ich zdolności', b: `<p>Każdy gracz dostaje <b>rolę</b>. Rola podpowiada, czym się zająć, i daje <b>jedną zdolność na całą sprawę</b> (Analiza → Zespół):</p><table class="g-table">${ROLES.map(r => `<tr><td>${esc(r.name)}</td><td>${esc(POWERS[r.id].name)}: ${esc(POWERS[r.id].desc)}</td></tr>`).join('')}</table><p>Zdolność uruchamiacie przyciskiem — zadziała przy następnej pasującej akcji. Uzgodnijcie, kiedy jej użyć: to wasze asy w rękawie.</p>` },
   phones
   ? { k: 'Tryb: telewizor + telefony', t: 'Tajne akta w waszych telefonach', b: `<p>Każdy gracz skanuje <b>swój kod QR</b> i dostaje w telefonie teczkę z dokumentami, których <b>nie widzi reszta</b>. Niektóre z nich są niezbędne do rozwiązania zagadek.</p><p>Wy decydujecie, kiedy i czy się nimi dzielić. Możecie czytać na głos albo <b>ujawnić dokument</b> na wspólnym ekranie: Analiza → Tajne akta → wpiszcie 4-znakowy kod widoczny przy dokumencie w telefonie.</p><p>Gracz bez telefonu wybiera na ekranie kodów „Nie mam telefonu — pokaż tutaj”: teczka otworzy się na wspólnym ekranie pod pieczęcią — reszta niech wtedy odwróci wzrok.</p><p>Przed aktem oskarżenia zróbcie <b>głosowanie</b>: każdy w teczce w telefonie typuje sprawcę i motyw, a na sygnał wszyscy pokazujecie ekrany.</p><p class="g-tip">Najczęstszy błąd: ktoś siedzi na kluczowym dokumencie i o nim nie mówi. Co jakiś czas zróbcie rundę „co kto ma”.</p>` }
   : { k: 'Tryb: wspólny stół', t: 'Jeden ekran, wszystko razem', b: `<p>Wszyscy widzicie to samo. Nie ma tajnych akt — informacje, które w trybie z telefonami mają poszczególni gracze, zdobywacie sami.</p><p>Służy do tego <b>Centrala wydziału</b> — dodatkowe miejsce na liście. Jej punkty to zapytania: archiwa, laboratoria, urzędy, eksperci. <b>Każde zapytanie to ruch</b>, dlatego norma ruchów w tym trybie jest odpowiednio wyższa.</p><p class="g-tip">Zanim zapytacie centralę, ustalcie, czego właściwie szukacie. Dobre pytanie to połowa odpowiedzi.</p>` },
   { k: 'Gdy utkniecie', t: 'Trop i podpowiedzi', b: `<p><b>Żarówka</b> na górnym pasku daje <b>trop</b> od szefa wydziału — kierunek, w którym warto pójść teraz (${D.trop == null ? 'na poziomie Weteran tylko dzięki zdolności Koordynatora' : '−' + D.trop + ' pkt'}).</p><p>Przy zagadkach ${D.hints === 1 ? 'jest <b>jedna podpowiedź</b>' : `są <b>${podp(D.hints)}</b>, coraz bardziej konkretne`} (${D.hints === 1 ? '' : 'po '}−${D.hint} pkt).${D.hints >= 3 ? ' Trzecia praktycznie podaje rozwiązanie.' : ''}</p><p>Briefing i zadania sprawy znajdziecie zawsze w menu. Postęp zapisuje się sam — możecie przerwać i wrócić innego dnia.</p>` },
   { k: 'Finał', t: 'Akt oskarżenia', b: `<p>Gdy jesteście gotowi: <b>Analiza → Akt oskarżenia</b>. Odpowiadacie na pytania o sprawcę, sposób, czas, motyw i tło sprawy, układacie kolejność zdarzeń i wskazujecie <b>trzy dowody</b> przeciwko sprawcy.</p><p><b>Po podpisaniu raportu nie da się go zmienić.</b> Dostaniecie wynik 0–100, rangę, pełne rozwiązanie krok po kroku i epilog — a na końcu jedną decyzję, którą musicie podjąć jako zespół.</p><p>Wynik trafia do <b>Kroniki wydziału</b> razem z odznakami, a akt oskarżenia możecie wydrukować albo zapisać jako PDF.</p><p class="g-tip">Składajcie raport, gdy każdy wniosek umiecie podeprzeć dowodem — nie wtedy, gdy „pewnie tak było”.</p><p class="muted" style="font-size:.9em">I jeszcze jedno: w niektórych aktach ktoś zostawił obcą pieczęć z kluczem. Nie dotyczy sprawy. Zabezpieczajcie ją — Kronika podpowie, po co.</p>` },
  ];
}
function ovGuide(o) {
  const cards = guideCards(o.mode, o.diff); const i = Math.max(0, Math.min(cards.length - 1, o.i || 0)); const cd = cards[i]; const last = i === cards.length - 1;
  return { title: 'Jak grać', kicker: `Instruktaż · ${o.mode === 'phones' ? 'Telewizor + telefony' : 'Wspólny stół'}`, body: `
   <div class="g-dots">${cards.map((_, k) => `<button class="${k === i ? 'on' : ''}" data-a="guide-go" data-i="${k}" aria-label="Karta ${k + 1}"></button>`).join('')}</div>
   <article class="paper g-card"><div class="eyebrow">${String(i + 1).padStart(2, '0')} / ${String(cards.length).padStart(2, '0')} · ${esc(cd.k)}</div><h2>${esc(cd.t)}</h2>${cd.b}</article>
   <div class="g-nav">${i > 0 ? `<button class="btn ghost" data-a="guide-go" data-i="${i - 1}">Wstecz</button>` : '<span></span>'}${last ? `<button class="btn" data-a="guide-end">Zaczynamy</button>` : `<button class="btn" data-a="guide-go" data-i="${i + 1}">Dalej</button>`}</div>
   ${o.after ? `<div class="g-skip"><button class="linkish" data-a="guide-end">Pomiń instruktaż</button><button class="linkish" data-a="guide-off">Nie pokazuj go przed kolejnymi sprawami</button></div>` : ''}` };
}

function startMsg(c, g) {
  const roles = g.players.map(p => `<li><b>${esc(p.name)}</b> — ${esc(ROLES.find(r => r.id === p.role).name)}: <span class="muted">${esc(ROLES.find(r => r.id === p.role).tip)}</span></li>`).join('');
  openOv({ type: 'msg', title: 'Śledztwo rozpoczęte', kicker: 'Akta ' + c.id, body: `<p>Macie przed sobą akta startowe — zacznijcie od nich. Potem przeszukujcie miejsca i przesłuchujcie świadków.</p>${c.mode === 'table' ? '<p class="muted">Gracie przy wspólnym stole: wszystko widzicie razem. Pamiętajcie o Centrali wydziału — niektóre informacje są tylko tam.</p>' : '<p class="muted">Pamiętajcie: każdy z was wie coś, czego nie wie reszta.</p>'}<h4 class="eyebrow" style="margin-top:18px">Podział ról</h4><ul class="roles">${roles}</ul>` });
}
/* ---------- akcje ---------- */
const ctx = () => { const r = route(); return { c: caseFor(r.id), g: G(r.id), r }; };
let btTimer = null, btShow = null;
function renderBt() {
  let root = $('#bt-root'); if (!root) { root = document.createElement('div'); root.id = 'bt-root'; document.body.appendChild(root); }
  const r = route(); const c = btShow && r.id && CASES[r.id] && caseFor(r.id); const b = c && (c.breakthroughs || []).find(x => x.id === btShow);
  if (!b) { const ov = root.querySelector('video'); if (ov) { ov.pause(); duck(false); } root.innerHTML = ''; btShow = null; if (!ovStack.length) document.body.style.overflow = ''; return; }
  const vOK = b.video && mediaOK(b.video) && S.settings.motion !== 'off'; const pst = vOK ? b.video.replace(/\.mp4$/, '.webp') : (b.img || c.art || c.cover);
  const media = vOK ? `<div class="bt-media"><div class="bt-bg" style="background-image:url('${esc(pst)}')"></div><video class="bt-fg bt-vid" src="${esc(b.video)}" poster="${esc(pst)}" autoplay muted playsinline preload="auto"></video></div>` : `<div class="bt-media"><div class="bt-bg" style="background-image:url('${esc(b.img || c.art || c.cover)}')"></div><img class="bt-fg kb" src="${esc(b.img || c.art || c.cover)}" alt=""></div>`;
  root.innerHTML = `<div class="bt" data-a="bt-close" role="dialog" aria-modal="true" aria-label="Przełom: ${esc(b.title)}"><div class="bt-in">${media}<div class="bt-shade"></div><div class="bt-text"><span class="bt-stamp">Przełom</span><h2>${esc(b.title)}</h2><p>${esc(b.text)}</p><button class="btn" data-a="bt-close">Dalej</button></div></div></div>`;
  document.body.style.overflow = 'hidden'; const vid = root.querySelector('video');
  if (vid) { vid.volume = vol('fx'); vid.onended = () => { vid.currentTime = Math.max(0, vid.duration - 0.05); vid.pause(); }; const go = () => vid.play().catch(() => {}); if (S.settings.sound) { vid.muted = false; duck(true); vid.play().catch(() => { vid.muted = true; go(); }); } else go(); }
  const bt = root.querySelector('.btn'); if (bt) setTimeout(() => bt.focus({ preventScroll: true }), 900);
}
function checkLater(id) { const r = route(); const g = r.id && G(r.id); if (g) { g.bt = (g.bt || []).filter(x => x !== id); save(); } }
function checkBreakthroughs() {
  const r = route(); if (r.name !== 'gra' || !r.id) return; const g = G(r.id); const c = r.id && CASES[r.id] && caseFor(r.id); if (!c || !g || g.report || !c.breakthroughs) return;
  if (!g.bt) { g.bt = c.breakthroughs.filter(b => has(g, c, b.when)).map(b => b.id); save(); return; } // gra sprzed 2.9: bez zaległych przełomów
  const nb = c.breakthroughs.find(b => !g.bt.includes(b.id) && has(g, c, b.when));
  if (!nb) return; g.bt.push(nb.id); save();
  clearTimeout(btTimer); btTimer = setTimeout(() => { if (btShow) return checkLater(nb.id); btShow = nb.id; renderBt(); sfx('break'); }, 650);
}
const rerender = () => { render(); renderOv(); checkBreakthroughs(); };
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
    S.games[c.id] = newGame(c, names, setupMode, setupDiff); save(); distRevealed = false; go(`gra/${c.id}/akta`);
    const mode = setupMode;
    if (S.settings.guide !== false) setTimeout(() => openOv({ type: 'guide', mode, diff: setupDiff, i: 0, after: true }), 250);
    else if (mode === 'table') setTimeout(() => startMsg(variant(c, 'table'), S.games[c.id]), 250);
  },
  restart: el => { const id = el.dataset.id; if (!confirm('Zacząć sprawę od nowa? Obecny postęp zostanie usunięty.')) return; delete S.games[id]; save(); ovStack = []; renderOv(); go('sprawa/' + id); },
  'dist-open': () => { distRevealed = true; sfx('stamp'); render(); },
  'dist-next': () => { const { g, c } = ctx(); distRevealed = false; g.distIdx++; if (g.distIdx >= g.players.length) { g.phase = 'play'; save(); render(); setTimeout(() => startMsg(c, g), 200); } else { save(); render(); } },
  tab: el => go(`gra/${route().id}/${el.dataset.tab}`),
  filter: el => { filesFilter = el.dataset.f; render(); },
  ana: el => { anaTab = el.dataset.t; render(); },
  ev: el => openOv({ type: 'ev', id: el.dataset.id }),
  loc: el => openOv({ type: 'loc', id: el.dataset.id }),
  'plan-view': el => { planView[route().id] = +el.dataset.i; render(); },
  person: el => openOv({ type: 'person', id: el.dataset.id, mode: 'talk' }),
  pmode: el => { const o = topOv(); o.mode = el.dataset.m; renderOv(); },
  search: el => { const { c, g } = ctx(); doSearch(c, g, el.dataset.id); rerender(); },
  ask: el => { const { c, g } = ctx(); if (g.asked.includes(el.dataset.id)) return; doAsk(c, g, el.dataset.id); topOv().scrollEnd = true; rerender(); if (voicesOn() && c.voiceDir) { const q = c.q[el.dataset.id]; const L = g.log[q.person]; speak(L[L.length - 1].v); } },
  confront: el => openOv({ type: 'confront', id: el.dataset.id }),
  'confront-with': el => { const { c, g } = ctx(); doConfront(c, g, el.dataset.s, el.dataset.id); if (voicesOn() && c.voiceDir) { const L = g.log[c.stmt[el.dataset.s].person]; speak(L[L.length - 1].v); } ovStack.pop(); history.back(); const o = topOv(); if (o && o.type === 'person') { o.mode = 'talk'; o.scrollEnd = true; } setTimeout(rerender, 30); },
  puzzle: el => openOv({ type: 'puzzle', id: el.dataset.id }),
  'puzzle-from-spot': el => { const { c, g } = ctx(); const pz = c.puzzle[el.dataset.id]; if (puzzleVisible(c, g, pz)) openOv({ type: 'puzzle', id: pz.id }); else openOv({ type: 'msg', title: pz.title, kicker: 'Za mało danych', body: '<p>Na razie nie macie materiałów, które pozwoliłyby się do tego zabrać. Szukajcie dalej.</p>' }); },
  dial: el => { const id = el.dataset.id, i = +el.dataset.i; const { c } = ctx(); const max = c.puzzle[id].input === 'time' && i === 0 ? 3 : c.puzzle[id].input === 'time' && i === 2 ? 6 : 10; dialVals[id][i] = (dialVals[id][i] + +el.dataset.d + max) % max; renderOv(); },
  solve: el => { const { c, g } = ctx(); const msg = doSolve(c, g, el.dataset.id); const o = topOv(); o.msg = msg; rerender(); },
  phint: el => { const { g } = ctx(); const st = (g.puzzles[el.dataset.id] = g.puzzles[el.dataset.id] || { hints: 0, attempts: 0 }); st.hints = (st.hints || 0) + 1; if (usePower(g, 'hint')) st.free = (st.free || 0) + 1; save(); renderOv(); },
  priv: el => openOv({ type: 'priv', i: +el.dataset.i, opened: false }),
  'priv-open': () => { topOv().opened = true; sfx('stamp'); renderOv(); },
  share: el => { const { c, g } = ctx(); if (!g.shared.includes(el.dataset.id)) { g.shared.push(el.dataset.id); save(); toast(c.ev[el.dataset.id].title, 'Ujawniono zespołowi', 'Tajne akta'); } rerender(); },
  pin: el => { const { g } = ctx(); pinToBoard(g, el.dataset.key); },
  'link-mode': () => { linkMode = !linkMode; if (!linkMode) boardSel = null; render(); if (linkMode) toast('Łączenie', 'Dotknij pierwszej, potem drugiej karty', 'Tablica'); },
  'note-add': () => { const t = prompt('Treść notatki na tablicy:'); if (t && t.trim()) { const { g } = ctx(); pinToBoard(g, 'n:' + Date.now(), t.trim().slice(0, 140)); render(); } },
  'board-del': () => { const { g } = ctx(); if (!boardSel) return; g.board.items = g.board.items.filter(x => x.key !== boardSel); g.board.links = g.board.links.filter(l => l.a !== boardSel && l.b !== boardSel); boardSel = null; save(); render(); },
  zoom: el => { const { g } = ctx(); const w = $('#bwrap'); boardZoomTo(g, Math.round(((g.board.zoom || 1) + 0.2 * +el.dataset.d) * 10) / 10, w ? w.clientWidth / 2 : 0, w ? w.clientHeight / 2 : 0); save(); },
  trop: () => openOv({ type: 'trop' }),
  'trop-go': () => { const { c, g } = ctx(); const rule = c.hintTrail.find(h => (!h.when || h.when.every(t => has(g, c, t))) && !(h.unless && h.unless.every(t => has(g, c, t)))); if (usePower(g, 'trop')) g.freeTrops = (g.freeTrops || 0) + 1; else g.trops++; save(); topOv().text = rule ? rule.text : 'Macie wszystko, czego potrzeba.'; rerender(); },
  rstep: el => { const { g, c } = ctx(); g.draft.step = Math.max(0, Math.min(c.report.questions.length, g.draft.step + +el.dataset.d)); save(); render(); $('#main') && ($('#main').scrollTop = 0); },
  ropt: el => { const { g } = ctx(); g.draft.answers[el.dataset.q] = el.dataset.k; save(); render(); },
  rproof: el => { const { g } = ctx(); const p = g.draft.proofs; const id = el.dataset.id; const i = p.indexOf(id); if (i >= 0) p.splice(i, 1); else if (p.length < +el.dataset.max) p.push(id); else toast('Limit dowodów', 'Odznacz jeden, by wybrać inny', 'Raport'); save(); render(); },
  rord: el => { const { g } = ctx(); const o = g.draft.order; const i = +el.dataset.i, j = i + +el.dataset.d; if (j < 0 || j >= o.length) return; [o[i], o[j]] = [o[j], o[i]]; save(); render(); },
  submit: () => { const { c, g } = ctx(); if (!confirm('Złożyć raport? Nie będzie można go zmienić.')) return; g.report = score(c, g); g.phase = 'done'; addChronicle(c, g); save(); sfx('stamp'); go(`gra/${c.id}/wynik`); },
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
  'guide-toggle': () => { S.settings.guide = S.settings.guide === false; save(); renderOv(); },
  chronicle: () => { ovStack = []; renderOv(); go('kronika'); },
  diff: el => { setupDiff = el.dataset.k; render(); },
  vplay: el => { if (el.classList.contains('on')) { stopVoice(); el.classList.remove('on'); return; } speak(el.dataset.src, el); },
  'voices-toggle': () => { S.settings.voices = !voicesOn(); save(); if (!voicesOn()) stopVoice(); renderOv(); },
  power: el => { const { g } = ctx(); const P = POWERS[el.dataset.role]; if (!P || (g.used || {})[el.dataset.role]) return; if (P.kind === 'par') { g.used[el.dataset.role] = true; g.parBonus = (g.parBonus || 0) + 3; toast(P.name, 'Norma ruchów +3', 'Rola'); } else { g.armed = P.kind; toast(P.name, 'Zadziała przy następnej pasującej akcji', 'Rola'); } save(); render(); },
  'power-off': () => { const { g } = ctx(); g.armed = null; save(); render(); },
  'to-report': () => { const { c, g } = ctx(); if (g.mode === 'phones' && !g.vote) openOv({ type: 'msg', title: 'Najpierw głosowanie?', kicker: 'Przed aktem oskarżenia', body: `<p>Zanim podpiszecie raport, sprawdźcie, czy cały zespół myśli to samo. Głosowanie zajmie minutę.</p><div class="row-actions"><button class="btn" data-a="vote">Głosujemy</button><button class="btn ghost" data-a="report-go">Pomiń — prosto do raportu</button></div>` }); else go(`gra/${c.id}/raport`); },
  'report-go': () => { const { c } = ctx(); ovStack = []; renderOv(); go(`gra/${c.id}/raport`); },
  vote: () => { if (ovStack.length) { ovStack = [{ type: 'vote', st: 0 }]; renderOv(); } else openOv({ type: 'vote', st: 0 }); },
  'vote-go': () => { const o = topOv(); o.st = 1; renderOv(); let n = 3; const tick = () => { const el = $('#votecount'); if (!el) return; if (n > 1) { n--; el.textContent = n; sfx('paper'); setTimeout(tick, 900); } else { o.st = 2; renderOv(); sfx('stamp'); } }; setTimeout(tick, 900); },
  'vote-res': el => { const { c, g } = ctx(); g.vote = el.dataset.v; save(); ovStack.pop(); history.back(); setTimeout(() => { if (g.vote === 'zgodni') go(`gra/${c.id}/raport`); else { anaTab = 'podejrzani'; render(); toast('Dyskusja', 'Wróćcie do tabeli podejrzanych', 'Zespół'); } }, 60); },
  'vote-card': () => { const w = $('#v-who'), m = $('#v-mot'), card = $('#v-card'); if (!w || !w.value) { alert('Wybierz sprawcę.'); return; } card.hidden = false; card.innerHTML = `<div class="eyebrow">Mój typ</div><b>${esc(w.value)}</b>${m && m.value ? `<small>${esc(m.value)}</small>` : ''}<p class="muted">Schowaj telefon ekranem w dół do sygnału.</p>`; card.scrollIntoView({ behavior: 'smooth' }); },
  'bt-close': (el, e) => { if (e && e.target.closest('.bt-text') && !e.target.closest('[data-a="bt-close"].btn')) return; btShow = null; renderBt(); renderOv(); setTimeout(checkBreakthroughs, 60); },
  pzoom: el => openOv({ type: 'zoom', src: el.dataset.src }),
  amark: el => { S.marks = S.marks || {}; if (!S.marks[el.dataset.c]) { S.marks[el.dataset.c] = el.dataset.l; save(); toast('Zabezpieczono obcą pieczęć', `Ślady Archiwisty: ${Object.keys(S.marks).length} z ${MARK_ORDER.length}`, 'Archiwum'); sfx('stamp'); } else toast('Ta pieczęć jest już w kronice', '', 'Archiwum'); renderOv(); },
  'print-report': () => { const { c, g } = ctx(); if (g && g.report) printReport(c, g); },
  voice: el => { if (window.__voice && !window.__voice.paused && el.classList.contains('on')) { stopVoice(); return; } const L = el.querySelector('.vl'), T0 = L && (L.dataset.t || (L.dataset.t = L.textContent)); speak(el.dataset.src); const v = window.__voice; if (!v) return; el.classList.add('on'); if (L) L.textContent = 'Zatrzymaj briefing'; const off = () => { el.classList.remove('on'); if (L) L.textContent = T0; }; const t0 = voTok; const chk = setInterval(() => { if (voTok !== t0 || !window.__voice || window.__voice.paused) { clearInterval(chk); off(); } }, 300); },
  'show-guide': () => { const { g } = ctx(); ovStack.pop(); history.back(); setTimeout(() => openOv({ type: 'guide', mode: g.mode === 'table' ? 'table' : 'phones', diff: g.diff, i: 0 }), 60); },
  'guide-go': el => { const o = topOv(); if (o && o.type === 'guide') { o.i = +el.dataset.i; renderOv(); const b = $('.ov-body'); if (b) b.scrollTop = 0; } },
  'guide-off': () => { S.settings.guide = false; save(); handlers['guide-end'](); },
  'guide-end': () => { const o = topOv(); ovStack.pop(); history.back(); setTimeout(renderOv, 0); if (o && o.after) { const { c, g } = ctx(); if (c && g && g.mode === 'table' && g.phase === 'play') setTimeout(() => startMsg(c, g), 120); } },
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
  if (e.target.dataset.mx) { const { g } = ctx(); const [pid, col] = e.target.dataset.mx.split('|'); g.matrix = g.matrix || {}; (g.matrix[pid] = g.matrix[pid] || {})[col] = e.target.value; clearTimeout(handlers._mt); handlers._mt = setTimeout(save, 400); }
  if (e.target.dataset.notes !== undefined) { const { g } = ctx(); g.notes = e.target.value; clearTimeout(handlers._nt); handlers._nt = setTimeout(save, 400); }
});
document.addEventListener('change', async e => {
  if (e.target.dataset.import === undefined) return;
  const f = e.target.files[0]; if (!f) return;
  try { const j = JSON.parse(await f.text()); const d = j && j.app === 'slad' ? j.data : null; if (!d || d.v !== 2 || !d.games || !d.settings) throw new Error('To nie jest plik zapisu ŚLAD 2.'); if (!confirm('Zastąpić obecny postęp danymi z pliku?')) return; S = d; save(); ovStack = []; renderOv(); toast('Zapis wczytany', '', 'Kopia'); go(''); }
  catch (err) { toast('Nie wczytano pliku', err.message, 'Błąd'); }
});
document.addEventListener('keydown', e => { if (e.key === 'Escape' && btShow) { handlers['bt-close'](); return; } if (e.key === 'Escape' && ovStack.length) closeOv(); const o = topOv(); if (o && o.type === 'guide' && (e.key === 'ArrowRight' || e.key === 'ArrowLeft')) { const n = (o.i || 0) + (e.key === 'ArrowRight' ? 1 : -1); if (n >= 0 && n < guideCards(o.mode, o.diff).length) handlers['guide-go']({ dataset: { i: n } }); } });

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
