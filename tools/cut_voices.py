#!/usr/bin/env python3
"""Tnie nagrania postaci po ciszy na pojedyncze kwestie i zapisuje MP3 do assets/voice/NNN/.
Użycie: python3 tools/cut_voices.py NNN katalog_z_wav [--dry]
Pliki wejściowe: *NNN-<postać>-all.wav (z dowolnym przedrostkiem) i *NNN-narrator-brief.wav.
Liczba kwestii musi się zgadzać z tools/voice/NNN-lines.json — inaczej skrypt przerywa i wypisuje znalezione odcinki."""
import json, os, re, subprocess, sys, glob

def segments(path, noise='-45dB', d=2.0):
    out = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', f'silencedetect=noise={noise}:d={d}', '-f', 'null', '-'], capture_output=True, text=True).stderr
    dur = float(re.search(r'Duration: (\d+):(\d+):([\d.]+)', out).groups()[2]) + 60 * float(re.search(r'Duration: (\d+):(\d+)', out).group(2)) + 3600 * float(re.search(r'Duration: (\d+)', out).group(1))
    starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
    sil = list(zip(starts, ends + [dur] * (len(starts) - len(ends))))
    segs, t = [], 0.0
    for a, b in sil:
        if a - t > 0.25: segs.append((t, a))
        t = b
    if dur - t > 0.25: segs.append((t, dur))
    return segs, dur

def export(src, a, b, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    a = max(0, a - 0.12); b = b + 0.18
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', src, '-af', 'loudnorm=I=-17:TP=-1.5:LRA=11,aresample=44100',
                    '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '112k', dst], check=True)

def main():
    cid, src = sys.argv[1], sys.argv[2]; dry = '--dry' in sys.argv
    lines = json.load(open(f'tools/voice/{cid}-lines.json', encoding='utf-8'))
    ok = True
    for key, v in lines.items():
        pid = key.split('-', 1)[1]
        parts = v.get('parts') or [{'file': f'{cid}-{pid}-all.wav', 'n': len(v['lines'])}]
        k = 0
        for part in parts:
            f = glob.glob(os.path.join(src, '*' + part['file']))
            chunk = v['lines'][k:k + part['n']]; k += part['n']
            if not f: print('BRAK pliku', part['file']); ok = False; continue
            segs, dur = segments(f[0])
            print(f"{part['file']}: {len(segs)} odcinków / oczekiwano {part['n']} ({dur:.1f} s)")
            if len(segs) != part['n']:
                ok = False
                for i, (a, b) in enumerate(segs): print(f'   {i + 1:2d} {a:7.2f}–{b:7.2f} ({b - a:5.2f} s)')
                continue
            for (a, b), ln in zip(segs, chunk):
                words = len(ln['spoken'].split()); rate = words / (b - a)
                if rate < 1.3 or rate > 3.9: print(f'   {ln["id"]}: {b - a:.1f} s, {words} słów  <-- tempo {rate:.2f} słów/s, sprawdzić'); ok = False
                lid = ln['id']; name = f'{pid}-{lid}' if re.fullmatch(r'(deflect|show)-\d+', lid) else lid
                if not dry: export(f[0], a, b, f'assets/voice/{cid}/{name}.mp3')
    nb = glob.glob(os.path.join(src, f'*{cid}-narrator-brief.wav'))
    if nb and not dry:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', nb[0], '-af', 'loudnorm=I=-17:TP=-1.5:LRA=11,aresample=44100', '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '112k', f'assets/voice/{cid}-brief.mp3'], check=True)
        print('narrator OK')
    sys.exit(0 if ok else 1)

main()
