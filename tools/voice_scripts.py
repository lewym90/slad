"""Generuje teksty dla lektora (kwestie świadków) i mapę kwestii do późniejszego cięcia nagrań.
Wynik: tools/voice/<case>-<person>.json  [{id, kind, text, spoken}]"""
import json, re, os, sys
SPOKEN = [  # zamiana zapisu na wymowę (tylko w wersji mówionej)
 ('na 112', 'na sto dwanaście'), ('przed 23:40', 'przed dwudziestą trzecią czterdzieści'),
 ('w marcu 2019 roku', 'w marcu dwa tysiące dziewiętnastego roku'), ('Lipiec 2013', 'Lipiec dwa tysiące trzynaście'),
 ('planowo, 21:40', 'planowo, dwudziesta pierwsza czterdzieści'), ('od 22:58 do 23:15', 'od dwudziestej drugiej pięćdziesiąt osiem do dwudziestej trzeciej piętnaście'),
 ('była 23:06', 'była dwudziesta trzecia zero sześć'), ('koło 23:03', 'koło dwudziestej trzeciej zero trzy'),
 ('w 2016 roku', 'w dwa tysiące szesnastym roku'), ('Około 22:20', 'Około dwudziestej drugiej dwadzieścia'),
 ('2016–2018', 'dwa tysiące szesnaście — dwa tysiące osiemnaście'), ('W marcu 2018 roku', 'W marcu dwa tysiące osiemnastego roku'),
 ('przyjazd 1:40', 'przyjazd pierwsza czterdzieści'), ('na II piętrze, w sali 7', 'na drugim piętrze, w sali siedem'), ('II piętr', 'drugie piętr'),
]
def spoken(t):
    t = re.sub(r'\s*\([^)]*\)\s*', ' ', t).strip()          # didaskalia w nawiasach nie są czytane
    for a, b in SPOKEN: t = t.replace(a, b)
    return re.sub(r'\s{2,}', ' ', t)
out = {}
for cid in ['001', '002', '003']:
    c = json.load(open(f'cases/{cid}.json', encoding='utf-8'))
    extra = (c.get('tableMode') or {}).get('questions', {})
    for p in c['people']:
        L = [{'id': q['id'], 'kind': 'q', 'text': q['a']} for q in p['questions'] + extra.get(p['id'], [])]
        L += [{'id': s['id'], 'kind': 'break', 'text': s['response']} for s in p['statements'] if s.get('response')]
        L += [{'id': f'deflect-{i}', 'kind': 'deflect', 'text': d} for i, d in enumerate(p.get('deflect', []))]
        for x in L: x['spoken'] = spoken(x['text'])
        out[f'{cid}-{p["id"]}'] = {'name': p['name'], 'lines': L}
os.makedirs('tools/voice', exist_ok=True)
json.dump(out, open('tools/voice/lines.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
bad = [(k, x['id'], x['spoken']) for k, v in out.items() for x in v['lines'] if re.search(r'\d|[IVX]{2,}', x['spoken'])]
for b in bad: print('LICZBA:', b)
print(sum(len(v['lines']) for v in out.values()), 'kwestii')
