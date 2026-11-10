/* ŚLAD — Service Worker: offline po pierwszym uruchomieniu. */
const VERSION = '2.0.1';
const CACHE = 'slad-' + VERSION;
const CORE = [
  './', './index.html', './styles.css', './app.js', './manifest.webmanifest',
  './cases/index.json', './cases/001.json',
  './assets/icons/icon-32.png', './assets/icons/icon-180.png', './assets/icons/icon-192.png', './assets/icons/icon-512.png', './assets/icons/maskable-512.png',
  './assets/tex/paper.webp', './assets/tex/dark.webp', './assets/tex/cork.webp', './assets/tex/grain.png',
  './assets/art/001-keyart.webp', './assets/art/001-manor.webp',
  './assets/cases/001-cover.webp', './assets/cases/002-cover.webp', './assets/cases/003-cover.webp', './assets/cases/004-cover.webp', './assets/cases/005-cover.webp',
  './assets/cases/006-cover.webp', './assets/cases/007-cover.webp', './assets/cases/008-cover.webp', './assets/cases/009-cover.webp',
  './assets/audio/reveal.mp3', './assets/audio/case-001.mp3',
  './assets/evidence/001-burnt.webp',
  './assets/evidence/001-cups.webp',
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
  // Grafiki, czcionki, dźwięk: cache najpierw, potem sieć (i zapis do cache).
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
