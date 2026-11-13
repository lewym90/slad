#!/usr/bin/env python3
"""Sprawdza i podmienia grafiki przeskalowane w Upscaylu.
Użycie: python3 tools/import_upscaled.py paczka.zip [--apply] [--q 82]
Dopasowuje pliki po nazwie (usuwa dopiski _upscayl...), sprawdza skalę, różnicę kompozycji, robi arkusz podglądu /tmp/up-sheet.jpg."""
import sys, os, re, glob, zipfile, tempfile, shutil
from PIL import Image, ImageChops, ImageStat

A = os.path.join(os.path.dirname(__file__), '..', 'assets')
DIRS = ['art', 'cases', 'people', 'places', 'evidence', 'video']

def main():
    zp = sys.argv[1]; apply = '--apply' in sys.argv
    q = int(sys.argv[sys.argv.index('--q') + 1]) if '--q' in sys.argv else 82
    tmp = tempfile.mkdtemp(); zipfile.ZipFile(zp).extractall(tmp)
    idx = {}
    for d in DIRS:
        for f in glob.glob(f'{A}/{d}/*.webp'): idx.setdefault(os.path.basename(f), []).append(d)
    files = [f for f in glob.glob(tmp + '/**/*', recursive=True) if os.path.isfile(f) and f.lower().endswith(('.webp', '.png', '.jpg', '.jpeg'))]
    rows, problems, used_dirs = [], [], set()
    for f in sorted(files):
        name = re.sub(r'_upscayl.*$', '', os.path.splitext(os.path.basename(f))[0]) + '.webp'
        ds = idx.get(name)
        if not ds: problems.append(f'nieznany plik: {os.path.basename(f)}'); continue
        if len(ds) > 1: problems.append(f'nazwa w kilku folderach: {name} {ds}')
        d = ds[0]; used_dirs.add(d)
        o = Image.open(f'{A}/{d}/{name}'); u = Image.open(f)
        sc = u.size[0] / o.size[0]
        if abs(u.size[1] / o.size[1] - sc) > 0.02: problems.append(f'zmienione proporcje: {name}')
        diff = ImageStat.Stat(ImageChops.difference(o.convert('L'), u.convert('L').resize(o.size, Image.LANCZOS))).mean[0]
        if diff > 8: problems.append(f'duża różnica kompozycji ({diff:.1f}): {name}')
        rows.append((d, name, o.size, u.size, sc, diff, f))
    for d in sorted(used_dirs):
        have = {r[1] for r in rows if r[0] == d}
        miss = sorted(n for n, ds in idx.items() if d in ds and n not in have)
        print(f'{d}: {len(have)} plików w paczce, brakuje {len(miss)}', miss if miss else '')
    scales = sorted({round(r[4], 2) for r in rows}); print('skale:', scales, '| największa różnica:', max((round(r[5], 2), r[1]) for r in rows) if rows else '-')
    for p in problems: print('PROBLEM:', p)
    W, H = 260, 200; n = len(rows); cols = 8
    sheet = Image.new('RGB', (W * cols, H * ((n + cols - 1) // cols)))
    for i, r in enumerate(rows):
        t = Image.open(r[6]).convert('RGB'); t.thumbnail((W, H)); sheet.paste(t, ((i % cols) * W, (i // cols) * H))
    sheet.save('/tmp/up-sheet.jpg', quality=80)
    if apply and not problems:
        t0 = t1 = 0
        for d, name, _, _, _, _, f in rows:
            dst = f'{A}/{d}/{name}'; t0 += os.path.getsize(dst)
            Image.open(f).convert('RGB').save(dst, quality=q, method=6); t1 += os.path.getsize(dst)
        print(f'PODMIENIONO {len(rows)} plików: {t0 / 2**20:.1f} MB -> {t1 / 2**20:.1f} MB')
    elif apply: print('NIE podmieniono — najpierw rozwiąż problemy.')
    shutil.rmtree(tmp)

main()
