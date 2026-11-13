/* ŚLAD — Service Worker: offline po pierwszym uruchomieniu. */
const VERSION = '2.17.8';
const CACHE = 'slad-' + VERSION;
const CORE = [
  './',
  './index.html',
  './styles.css',
  './app.js',
  './manifest.webmanifest', './assets/vendor/qrcode.js',
  './cases/index.json',
  './data/baza/index.json',
  './data/baza/tlo-osoby.json',
  './data/baza/tlo-pojazdy.json',
  './data/baza/tlo-firmy.json',
  './data/baza/tlo-ksiegi.json',
  './data/baza/sprawa-005.json',
  './data/baza/sprawa-006.json',
  './data/baza/uniwersum.json',
  './cases/001.json',
  './cases/002.json',
  './cases/003.json',
  './cases/004.json',
  './cases/005.json',
  './cases/006.json',
  './assets/audio/case-006.mp3',
  './assets/voice/006-brief.mp3',
  './assets/art/006-keyart.webp',
  './assets/evidence/006-can.webp',
  './assets/evidence/006-clock.webp',
  './assets/evidence/006-coat.webp',
  './assets/evidence/006-leon.webp',
  './assets/evidence/006-photo.webp',
  './assets/evidence/006-posters.webp',
  './assets/evidence/006-scraps.webp',
  './assets/evidence/006-wedge.webp',
  './assets/people/006-damian.webp',
  './assets/people/006-ewa.webp',
  './assets/people/006-grzegorz.webp',
  './assets/people/006-joanna.webp',
  './assets/people/006-lipka.webp',
  './assets/places/006-booth.webp',
  './assets/places/006-flat.webp',
  './assets/places/006-foyer.webp',
  './assets/places/006-office.webp',
  './assets/places/006-yard.webp',
  './assets/audio/case-002.mp3',
  './assets/audio/case-003.mp3',
  './assets/voice/001-brief.mp3',
  './assets/voice/002-brief.mp3',
  './assets/voice/003-brief.mp3',
  './assets/audio/case-005.mp3',
  './assets/voice/005-brief.mp3',
  './assets/art/005-keyart.webp',
  './assets/evidence/005-act.webp',
  './assets/evidence/005-card.webp',
  './assets/evidence/005-desk.webp',
  './assets/evidence/005-keys.webp',
  './assets/evidence/005-m2.webp',
  './assets/evidence/005-note.webp',
  './assets/evidence/005-suitcase.webp',
  './assets/evidence/005-szulc-feb.webp',
  './assets/evidence/005-szulc-id.webp',
  './assets/evidence/005-ticket.webp',
  './assets/evidence/005-wardrobe.webp',
  './assets/people/005-dabrowska.webp',
  './assets/people/005-kosowski.webp',
  './assets/people/005-kraska.webp',
  './assets/people/005-lis.webp',
  './assets/people/005-marta.webp',
  './assets/people/005-morawiec.webp',
  './assets/places/005-archive.webp',
  './assets/places/005-bar.webp',
  './assets/places/005-hall.webp',
  './assets/places/005-parking.webp',
  './assets/places/005-reception.webp',
  './assets/places/005-room.webp',
  './assets/places/005-service.webp',
  './assets/places/005-tech.webp',
  './assets/audio/case-004.mp3',
  './assets/voice/004-brief.mp3',
  './assets/art/004-keyart.webp',
  './assets/evidence/004-dummy.webp',
  './assets/evidence/004-keyswitch.webp',
  './assets/evidence/004-pendrive.webp',
  './assets/evidence/004-phone.webp',
  './assets/evidence/004-safe.webp',
  './assets/evidence/004-sticky.webp',
  './assets/evidence/004-toolcase.webp',
  './assets/evidence/004-watch.webp',
  './assets/evidence/004-wrench.webp',
  './assets/people/004-burda.webp',
  './assets/people/004-hajduk.webp',
  './assets/people/004-kopec.webp',
  './assets/people/004-lasota.webp',
  './assets/people/004-pyka.webp',
  './assets/people/004-szczerba.webp',
  './assets/places/004-chemrud.webp',
  './assets/places/004-city.webp',
  './assets/places/004-czk.webp',
  './assets/places/004-hospital.webp',
  './assets/places/004-newsroom.webp',
  './assets/places/004-parking.webp',
  './assets/places/004-station.webp',
  './assets/places/004-syreon.webp',
  './assets/icons/icon-32.png',
  './assets/icons/icon-180.png',
  './assets/icons/icon-192.png',
  './assets/icons/icon-512.png',
  './assets/icons/maskable-512.png',
  './assets/tex/paper.webp',
  './assets/tex/dark.webp',
  './assets/tex/cork.webp',
  './assets/tex/grain.png',
  './assets/art/001-keyart.webp',
  './assets/art/003-keyart.webp',
  './assets/evidence/003-boots.webp',
  './assets/evidence/003-button.webp',
  './assets/evidence/003-camera.webp',
  './assets/evidence/003-coat.webp',
  './assets/evidence/003-floodlight.webp',
  './assets/evidence/003-frames.webp',
  './assets/evidence/003-journal.webp',
  './assets/evidence/003-net.webp',
  './assets/evidence/003-panel.webp',
  './assets/evidence/003-snow.webp',
  './assets/people/003-halina.webp',
  './assets/people/003-joanna.webp',
  './assets/people/003-kamil.webp',
  './assets/people/003-krystyna.webp',
  './assets/people/003-wilk.webp',
  './assets/people/003-zenon.webp',
  './assets/places/003-attic.webp',
  './assets/places/003-flat.webp',
  './assets/places/003-gatehouse.webp',
  './assets/places/003-grounds.webp',
  './assets/places/003-inn.webp',
  './assets/places/003-stairwell.webp',
  './assets/places/003-villa.webp',
  './assets/plan/paper.webp',
  './assets/plan/marker.webp',
  './assets/plan/body-lying.webp',
  './assets/plan/body-seated.webp',
  './assets/plan/compass.webp',
  './assets/plan/tape1.webp',
  './assets/plan/tape2.webp',
  './assets/plan/clip.webp',
  './assets/evidence/002-cctv.webp',
  './assets/evidence/002-clipping.webp',
  './assets/evidence/002-coat.webp',
  './assets/evidence/002-glasses.webp',
  './assets/evidence/002-lanyard.webp',
  './assets/evidence/002-papers.webp',
  './assets/evidence/002-phone.webp',
  './assets/evidence/002-platform.webp',
  './assets/evidence/002-seal.webp',
  './assets/people/002-damian.webp',
  './assets/people/002-emil.webp',
  './assets/people/002-iga.webp',
  './assets/people/002-roman.webp',
  './assets/people/002-wieslaw.webp',
  './assets/people/002-wrona.webp',
  './assets/places/002-bar.webp',
  './assets/places/002-compartment.webp',
  './assets/places/002-corridor.webp',
  './assets/places/002-loco.webp',
  './assets/places/002-service.webp',
  './assets/places/002-tracks.webp',
  './assets/places/002-wrzos.webp',
  './assets/art/001-manor.webp',
  './assets/art/002-keyart.webp',
  './assets/cases/001-cover.webp',
  './assets/cases/002-cover.webp',
  './assets/cases/003-cover.webp',
  './assets/cases/004-cover.webp',
  './assets/cases/005-cover.webp',
  './assets/cases/006-cover.webp',
  './assets/cases/007-cover.webp',
  './assets/cases/008-cover.webp',
  './assets/cases/009-cover.webp',
  './assets/audio/sfx-paper.mp3',
  './assets/audio/sfx-stamp.mp3',
  './assets/audio/sfx-unlock.mp3',
  './assets/audio/sfx-wrong.mp3',
  './assets/audio/sfx-break.mp3',
  './assets/audio/case-001.mp3',
  './assets/evidence/001-burnt.webp',
  './assets/evidence/001-cups.webp',
  './assets/evidence/001-footprints.webp',
  './assets/evidence/001-gramophone.webp',
  './assets/evidence/001-key.webp',
  './assets/evidence/001-loafers.webp',
  './assets/evidence/001-paperweight.webp',
  './assets/evidence/001-pot.webp',
  './assets/evidence/001-watch.webp',
  './assets/evidence/001-x5-anna2013.webp',
  './assets/people/001-helena.webp',
  './assets/people/001-kinga.webp',
  './assets/people/001-leon.webp',
  './assets/people/001-marta.webp',
  './assets/people/001-wiktor.webp',
  './assets/places/001-guestrooms.webp',
  './assets/places/001-hq.webp',
  './assets/places/001-library.webp',
  './assets/places/001-orangery.webp',
  './assets/places/001-outbuilding.webp',
  './assets/places/001-study.webp',
  './assets/places/001-westwing.webp'
];
const FONTS = [
  './assets/fonts/caveat-latin-600-normal.woff2',
  './assets/fonts/caveat-latin-ext-600-normal.woff2',
  './assets/fonts/cormorant-garamond-latin-500-italic.woff2',
  './assets/fonts/cormorant-garamond-latin-600-normal.woff2',
  './assets/fonts/cormorant-garamond-latin-700-normal.woff2',
  './assets/fonts/cormorant-garamond-latin-ext-500-italic.woff2',
  './assets/fonts/cormorant-garamond-latin-ext-600-normal.woff2',
  './assets/fonts/cormorant-garamond-latin-ext-700-normal.woff2',
  './assets/fonts/ibm-plex-mono-latin-400-normal.woff2',
  './assets/fonts/ibm-plex-mono-latin-500-normal.woff2',
  './assets/fonts/ibm-plex-mono-latin-ext-400-normal.woff2',
  './assets/fonts/ibm-plex-mono-latin-ext-500-normal.woff2',
  './assets/fonts/ibm-plex-sans-latin-400-normal.woff2',
  './assets/fonts/ibm-plex-sans-latin-500-normal.woff2',
  './assets/fonts/ibm-plex-sans-latin-600-normal.woff2',
  './assets/fonts/ibm-plex-sans-latin-ext-400-normal.woff2',
  './assets/fonts/ibm-plex-sans-latin-ext-500-normal.woff2',
  './assets/fonts/ibm-plex-sans-latin-ext-600-normal.woff2',
  './assets/fonts/special-elite-latin-400-normal.woff2',
  './assets/fonts/special-elite-latin-ext-400-normal.woff2'
];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    // Każdy plik osobno: brak jednego zasobu nie blokuje instalacji.
    await Promise.all(CORE.concat(FONTS).map(u => cache.add(new Request(u, { cache: 'reload' })).catch(() => null)));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k.startsWith('slad-') && k !== CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

async function rangeResponse(req, res) {
  const range = req.headers.get('range'); if (!range) return res;
  const buf = await res.arrayBuffer(); const n = buf.byteLength; const m = /bytes=(\d*)-(\d*)/.exec(range) || [];
  let start = m[1] ? +m[1] : 0, end = m[2] ? +m[2] : n - 1; if (!m[1] && m[2]) { start = Math.max(0, n - +m[2]); end = n - 1; }
  end = Math.min(end, n - 1); if (start > end) return new Response(null, { status: 416, headers: { 'Content-Range': `bytes */${n}` } });
  return new Response(buf.slice(start, end + 1), { status: 206, headers: { 'Content-Type': res.headers.get('Content-Type') || (/\.mp4/.test(req.url) ? 'video/mp4' : 'audio/mpeg'), 'Content-Range': `bytes ${start}-${end}/${n}`, 'Content-Length': String(end - start + 1), 'Accept-Ranges': 'bytes' } });
}
async function putIfOk(req, res) {
  if (res && res.ok && res.type === 'basic') { const c = await caches.open(CACHE); await c.put(req, res.clone()); }
  return res;
}

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  // Pliki audio z nagłówkiem Range obsługuje przeglądarka bezpośrednio z sieci lub z pełnej odpowiedzi w cache.
  if (req.mode === 'navigate') {
    event.respondWith((async () => {
      try { return await putIfOk(new Request('./index.html'), await fetch(req, { cache: 'no-cache' })); }
      catch (_) { return (await caches.match('./index.html')) || (await caches.match('./')) || Response.error(); }
    })());
    return;
  }
  const isData = url.pathname.endsWith('.json') || url.pathname.endsWith('.js') || url.pathname.endsWith('.css');
  if (isData) {
    // Sieć najpierw (świeże treści spraw), cache jako zapas offline.
    event.respondWith((async () => {
      try { return await putIfOk(req, await fetch(req, { cache: 'no-cache' })); }
      catch (_) { return (await caches.match(req, { ignoreSearch: true })) || Response.error(); }
    })());
    return;
  }
  // Nagrania i filmy: iPhone (Safari) wymaga odpowiedzi 206 na zapytania Range — tniemy pełny plik z cache.
  if (/\.(mp3|mp4)$/i.test(url.pathname)) {
    event.respondWith((async () => {
      let full = await caches.match(url.href, { ignoreSearch: true });
      if (!full) {
        try { const r = await fetch(url.href); if (r.status === 200) { await putIfOk(new Request(url.href), r.clone()); full = r; } else return r; }
        catch (_) { return Response.error(); }
      }
      return rangeResponse(req, full);
    })());
    return;
  }
  // Grafiki, czcionki: cache najpierw, potem sieć (i zapis do cache).
  event.respondWith((async () => {
    const hit = await caches.match(req, { ignoreSearch: true });
    if (hit) return hit;
    try {
      const res = await fetch(req);
      if (res.status === 200) await putIfOk(req, res);
      return res;
    } catch (_) { return Response.error(); }
  })());
});

self.addEventListener('message', e => { if (e.data === 'SKIP_WAITING') self.skipWaiting(); });
