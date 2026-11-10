#!/usr/bin/env python3
"""Tnie planszę z grafikami na pojedyncze pliki.
Użycie: python3 tools/cut_sheet.py plansza.png KOLUMNY WIERSZE nazwa1 nazwa2 ... [--ratio 4:5] [--width 900]
Wykrywa ciemne przerwy między kafelkami; jeśli ich nie znajdzie, dzieli planszę równo.
Pliki zapisuje jako WebP pod podanymi ścieżkami (np. assets/people/001-leon.webp)."""
import sys
import numpy as np
from PIL import Image


def bands(profile, n, thr):
    """Zwraca n przedziałów treści, rozdzielonych ciemnymi pasami."""
    L = len(profile)
    dark = profile < thr
    # znajdź ciągi ciemne o długości >= 0.4% wymiaru, nie na samych krawędziach
    cuts = []
    i = 0
    while i < L:
        if dark[i]:
            j = i
            while j < L and dark[j]:
                j += 1
            if j - i >= max(3, L * 0.004) and i > L * 0.03 and j < L * 0.97:
                cuts.append((i, j))
            i = j
        else:
            i += 1
    expected = [L * k / n for k in range(1, n)]
    chosen = []
    for e in expected:
        best = min(cuts, key=lambda c: abs((c[0] + c[1]) / 2 - e), default=None)
        if best and abs((best[0] + best[1]) / 2 - e) < L / n * 0.25:
            chosen.append(best)
        else:
            chosen.append((int(e), int(e)))
    edges = [0] + [x for c in chosen for x in c] + [L]
    return [(edges[2 * k], edges[2 * k + 1]) for k in range(n)]


def trim_dark(im, thr=7):
    a = np.asarray(im.convert('L'), dtype=float)
    rows = np.where(a.mean(axis=1) > thr)[0]
    cols = np.where(a.mean(axis=0) > thr)[0]
    if len(rows) < 10 or len(cols) < 10:
        return im
    return im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))


def fit_ratio(im, ratio):
    if not ratio:
        return im
    rw, rh = map(float, ratio.split(':'))
    w, h = im.size
    target = rw / rh
    if w / h > target:
        nw = int(h * target)
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(w / target)
    y = int((h - nh) * 0.3)  # przy portretach zostaw więcej góry (twarz)
    return im.crop((0, y, w, y + nh))


def main():
    args = sys.argv[1:]
    ratio = width = None
    if '--ratio' in args:
        i = args.index('--ratio'); ratio = args[i + 1]; del args[i:i + 2]
    if '--width' in args:
        i = args.index('--width'); width = int(args[i + 1]); del args[i:i + 2]
    src, cols, rows, names = args[0], int(args[1]), int(args[2]), args[3:]
    assert len(names) == cols * rows, f'Podaj {cols * rows} nazw plików'
    im = Image.open(src).convert('RGB')
    a = np.asarray(im.convert('L'), dtype=float)
    thr = max(14, np.percentile(a, 2) + 10)
    xs = bands(a.mean(axis=0), cols, thr)
    ys = bands(a.mean(axis=1), rows, thr)
    k = 0
    for r in range(rows):
        for c in range(cols):
            tile = im.crop((xs[c][0], ys[r][0], xs[c][1], ys[r][1]))
            tile = trim_dark(tile)
            inset = max(2, int(min(tile.size) * 0.008))
            tile = tile.crop((inset, inset, tile.size[0] - inset, tile.size[1] - inset))
            tile = fit_ratio(tile, ratio)
            if width and tile.size[0] > width:
                tile = tile.resize((width, int(tile.size[1] * width / tile.size[0])), Image.LANCZOS)
            tile.save(names[k], quality=84)
            print(f'{names[k]}: {tile.size[0]}x{tile.size[1]}')
            k += 1


if __name__ == '__main__':
    main()
