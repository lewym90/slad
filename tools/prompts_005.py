#!/usr/bin/env python3
"""Generuje docs/PROMPTY_*_005.md oraz tools/voice/005-lines.json. Tekst kwestii pobierany 1:1 z cases/005.json.
Użycie (z katalogu repo): python3 tools/prompts_005.py"""
import json, re, os
c = json.load(open('cases/005.json', encoding='utf-8'))
CID = '005'

SPOKEN = [
 ('Piątek, 13 marca, 10:40.', 'Piątek, trzynastego marca, godzina dziesiąta czterdzieści.'), ('II piętro', 'drugie piętro'),
 ('Dr Edward Szulc, 63-letni', 'Doktor Edward Szulc, sześćdziesięciotrzyletni'), ('o 9:00', 'o dziewiątej'), ('38 milionów', 'trzydzieści osiem milionów'),
 ('o 23:05', 'o dwudziestej trzeciej zero pięć'), ('O 23:13', 'O dwudziestej trzeciej trzynaście'), ('O 23:50', 'O dwudziestej trzeciej pięćdziesiąt'),
 ('O 9:47', 'O dziewiątej czterdzieści siedem'), ('pokoju 214', 'pokoju dwieście czternaście'),
 ('Doktor Szulc, o 23:05', 'Doktor Szulc, o dwudziestej trzeciej zero pięć'),
 ('214-A', 'dwieście czternaście A'), ('214-B', 'dwieście czternaście B'), ('o 214', 'o dwieście czternaście'),
 ('W 2022 roku', 'W dwa tysiące dwudziestym drugim roku'), ('O 19:32', 'O dziewiętnastej trzydzieści dwa'), ('z 1946 roku', 'z tysiąc dziewięćset czterdziestego szóstego roku'),
 ('O 21:49', 'O dwudziestej pierwszej czterdzieści dziewięć'), ('W październiku 2024 roku', 'W październiku dwa tysiące dwudziestego czwartego roku'),
 ('W 2024 roku', 'W dwa tysiące dwudziestym czwartym roku'), ('z 2018 roku', 'z dwa tysiące osiemnastego roku'),
 ('SMS-em', 'esemesem'), ('SMS-a', 'esemesa'), ('Gryf-Guest', 'Gryf Gest'),
]
def clean(t):
    t = re.sub(r'\s*\([^)]*\)\s*', ' ', t).strip()
    for a, b in SPOKEN: t = t.replace(a, b)
    t = re.sub(r'\s{2,}', ' ', t)
    return re.sub(r'(^|[.?!] )([a-ząćęłńóśźż])', lambda m: m.group(1) + m.group(2).upper(), t)

VOICE = {
 'narrator': "Mature Polish male narrator in his early 50s. Deep, warm, slightly gravelly baritone. Noir documentary style: calm, measured, low and intimate, like a seasoned detective reading a case file aloud late at night. Standard Polish pronunciation, no regional accent. If you generated this narrator for an earlier case, reuse exactly the same voice.",
 'kraska': "Polish woman, 47, secretary of a city claims commission. Polished, quick, pleasant mezzo-soprano with an office politeness that sounds rehearsed; precise diction. When lying she stays smooth and friendly, slightly too fast; when cornered her voice gets cooler, clipped and controlled, never hysterical. Standard Polish.",
 'kosowski': "Polish man, 52, a Warsaw attorney. Confident, slightly hoarse baritone of a man who talks on the phone all day, a little arrogant, ironic, fluent legal phrasing. Brisk and dismissive by default; defensive and curt when caught. Standard Polish.",
 'dabrowska': "Polish woman, 44, a city legal counsel. Calm, low, dry alto, careful and measured, every word weighed; quiet intensity, a touch of tiredness. Reluctant and embarrassed when admitting something, then concise and firm. Standard Polish.",
 'lis': "Polish young man, 24, a night receptionist after a sleepless shift. Light, slightly nasal tenor, polite service tone, talks a bit too fast when nervous, swallows the ends of sentences; sheepish when he admits something, genuinely shocked in one line. Standard Polish.",
 'morawiec': "Polish man, 61, a court document examiner. Soft, precise, slightly fussy baritone of an old-school scholar, gentle when talking about paper and handwriting, uneasy and evasive when money or timing comes up. Standard Polish.",
 'marta': "Polish woman, 59, a teacher whose husband is missing. Quiet, warm, controlled mezzo with a tremor of fear kept under tight control; very concrete and clear, short sentences, occasionally a breath of emotion, never melodramatic. Standard Polish.",
}
NAME = {'narrator': 'Narrator', 'kraska': 'Iwona Kraska', 'kosowski': 'Adrian Kosowski', 'dabrowska': 'Ewa Dąbrowska', 'lis': 'Bartosz Lis', 'morawiec': 'Lech Morawiec', 'marta': 'Marta Szulc'}
KIND = {'q': "answer to an investigator's question", 'break': 'reaction after being confronted with hard evidence (the character gives up part of the lie or admits something)',
        'show': 'reaction after being shown a piece of evidence (photo, document or printout) — a spontaneous, genuine reaction', 'deflect': 'curt, evasive reaction to a wrong accusation',
        'showdef': 'short, indifferent reaction to being shown something irrelevant'}
COMMON = "Natural, believable acting like in a high-quality Polish radio drama — not a synthetic announcer. Correct Polish pronunciation and stress (on the penultimate syllable). Words in „quotation marks” are the character quoting someone else or something written: mark them with a subtle change of tone, do not imitate another voice."

def head(fname, who, n=None):
    h = f"""Generate a single spoken-voice audio file in Polish.

FILE NAME: {fname}
FORMAT: the highest audio quality available — preferably uncompressed WAV, 48 kHz, 24-bit, mono (if WAV is not possible: the highest-bitrate file available). Dry, close-miked, broadcast-quality studio voice recording, clean and noise-free. No music, no background ambience, no sound effects, no breathing noises between lines beyond what is natural. About 0.3 seconds of silence at the start and at the end.

CHARACTER: {NAME[who]}
VOICE: {VOICE[who]}
"""
    if n:
        h += f"""
STRUCTURE: the recording contains exactly {n} separate spoken lines, in the order given below. Between every two consecutive lines leave EXACTLY 3 seconds of complete silence (pure digital silence, no room tone, no sounds) so the lines can be cut apart. Never speak the line numbers, the stage directions or any of these instructions. Keep the same voice, timbre, pitch and recording level for every line.

ACTING NOTES (do not read aloud) — for each line its type is given; play it accordingly:
"""
    return h

lines_out = {}
md = [f"# ŚLAD — prompty głosowe, sprawa {CID} „{c['title']}”\n",
 "Każda postać to **jeden prompt = jedno nagranie** ze wszystkimi jej kwestiami po kolei, rozdzielonymi ciszą (3 s) — potnę je po ciszy. Narrator ma osobny, krótki prompt.\n",
 "**UWAGA, SPOILERY:** kwestie postaci zdradzają rozwiązanie. Kopiuj przyciskiem kopiowania przy bloku, nie czytaj treści.\n"]
order = ['kraska', 'kosowski', 'dabrowska', 'lis', 'morawiec', 'marta']
blocks = []
for who in order:
    p = next(x for x in c['people'] if x['id'] == who)
    L = [{'id': q['id'], 'kind': 'q', 'text': q['a']} for q in p['questions']]
    L += [{'id': s['id'], 'kind': 'break', 'text': s['response']} for s in p['statements'] if s.get('response')]
    L += [{'id': x['id'], 'kind': 'show', 'text': x['a']} for x in p.get('shows', [])]
    L += [{'id': f'deflect-{i}', 'kind': 'deflect', 'text': d} for i, d in enumerate(p.get('deflect', []))]
    L += [{'id': f'show-{i}', 'kind': 'showdef', 'text': d} for i, d in enumerate(p.get('showDefault', []))]
    for i, x in enumerate(L, 1): x['n'] = i; x['spoken'] = clean(x['text'])
    for x in L: assert not re.search(r'\d|[A-Z]{2,}', x['spoken']), (who, x['id'], x['spoken'])
    fname = f'{CID}-{who}-all.wav'
    lines_out[f'{CID}-{who}'] = {'name': p['name'], 'file': fname, 'lines': L}
    notes = '\n'.join(f"Line {x['n']}: {KIND[x['kind']]}." for x in L)
    spoken = '\n\n'.join(x['spoken'] for x in L)
    blocks.append(head(fname, who, len(L)) + notes + f"""

{COMMON}

TEXT TO SPEAK — {len(L)} lines, separated here by blank lines. Read each one exactly as written, in Polish, word for word, then leave 3 seconds of silence before the next one. Do not add, omit, translate or read any of these instructions aloud:
<<<
{spoken}
>>>""")
brief = clean(' '.join([c['intro']['lead']] + c['intro']['brief']))
assert not re.search(r'\d', brief), brief
nar = head(f'{CID}-narrator-brief.wav', 'narrator') + f"""
PERFORMANCE: Opening narration of the case. Slow, atmospheric, with short pauses between paragraphs. Slight weight on the last sentence of each paragraph. Mood: a rainy night in an old hotel, a locked windowless room, quiet urgency — but read it cleanly, no added sound effects.
{COMMON}

TEXT TO SPEAK — read it exactly as written, in Polish, word for word. Do not add, omit, translate or read any of these instructions aloud:
<<<
{brief}
>>>"""
for i, b in enumerate([nar] + blocks, 1):
    md.append(f"## {i}\n```\n{b}\n```\n")
os.makedirs('docs', exist_ok=True)
open(f'docs/PROMPTY_GLOSY_{CID}.md', 'w', encoding='utf-8').write('\n'.join(md))
json.dump(lines_out, open(f'tools/voice/{CID}-lines.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- GRAFIKA ----------
NOTXT = "Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders anywhere in the image."
NOTXTP = "Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders inside the panels."
STYLE_P = "Style for every panel: cinematic film still, 85mm lens, shallow depth of field, low-key lighting with a cool blue-teal key light and a small warm tungsten accent, muted desaturated colour grade, subtle 35mm film grain, realistic skin texture with pores and wrinkles, ordinary Central-European faces, not models, no glamour makeup."
PL = "Photorealistic cinematic wide still, 3:2 landscape at the highest resolution you can generate (ideally 6144×4096, at minimum 3840×2560), full-frame camera, 24mm lens, deep focus, sharp realistic detail across the whole frame, muted desaturated colour grade with cool blue-teal shadows and warm tungsten accents, fine 35mm film grain, no people visible. " + NOTXT
TIME = "Time: Friday late morning in March, overcast, after a night of rain — outdoor surfaces still wet, but it is NOT raining now."
g = [f"# ŚLAD — prompty graficzne, sprawa {CID} „{c['title']}”\n",
 "Każdy blok to osobny obraz — wklejaj bez zmian. Plansze potnę i podepnę do gry. Obrazy nie zawierają tekstu.\n"]
G = []
G.append(f"""A single photorealistic contact sheet, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): exactly 6 separate portrait panels with a 4:5 vertical aspect, arranged in a strict grid of 3 columns and 2 rows, all panels identical in size, separated by uniform solid pure black gutters about 2% of the image width, black outer margin of the same width. Each panel contains exactly one person, head and shoulders, eye level, facing the camera at a slight three-quarter angle. {STYLE_P} {NOTXTP}
Row 1, panel 1: a 47-year-old Polish woman, a city commission secretary, shoulder-length dark brown hair perfectly styled, subtle makeup, small pearl earrings, a thin gold wedding ring visible on a hand resting near her collar, navy tailored skirt-suit jacket over a white blouse, polite controlled half-smile that does not reach her watchful eyes, blurred elegant hotel conference room with warm lamps behind her.
Row 1, panel 2: a 52-year-old Polish attorney from Warsaw, short dark hair greying at the sides, two-day stubble, tired but sharp eyes, expensive dark grey suit, white shirt with the top button undone, loosened tie, a smartphone held near his chest, a faint ironic smirk, blurred hotel bar with brass lamps behind him.
Row 1, panel 3: a 44-year-old Polish woman, a city legal counsel, slim, straight light-brown hair tied back, no-nonsense face, minimal makeup, thin-framed glasses, a red wool coat over a dark grey blazer, serious, measured, slightly tired expression, blurred hotel lobby with leather armchairs behind her.
Row 2, panel 1: a 24-year-old Polish man, a night hotel receptionist after a sleepless shift, short messy light-brown hair, pale face with dark circles under the eyes, slight stubble, a dark hotel uniform jacket thrown over a grey hooded sweatshirt, anxious polite expression, blurred dark-wood reception counter with a small desk lamp behind him.
Row 2, panel 2: a 61-year-old Polish forensic document examiner, short, balding with neat grey hair at the sides, round wire glasses, tweed jacket with a small magnifying loupe in the breast pocket, a mild scholarly but uneasy expression, blurred hotel room with a desk lamp behind him.
Row 2, panel 3: a 59-year-old Polish woman, a teacher whose husband is missing, short ash-blonde hair, kind tired face with fine wrinkles, eyes red from worry but composed, a beige cardigan over a simple blouse, holding a smartphone tightly in both hands near her chest, blurred hotel corridor with warm wall lamps behind her.""")
G.append(f"""A single photorealistic sheet, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): exactly 2 panels side by side, each with a 4:5 vertical aspect, identical in size, separated by a uniform solid pure black gutter about 2% of the image width, black outer margin of the same width. Both panels show THE SAME Polish man — the same face, the same nose, eyes, ears, eyebrows and the same thin-rimmed rectangular glasses — photographed eight years apart. {NOTXTP}
Panel 1 (left): an official identity-document style head-and-shoulders photograph of him at about 55 years old: plain light-grey background, flat even frontal lighting, neutral expression, looking straight at the camera, grey hair cut short, a short neatly trimmed greying full beard and moustache, dark jacket, white shirt. Slightly flat, slightly faded colours like a scan of an ID photo.
Panel 2 (right): a warm candid snapshot of the same man at 62–63 years old at a home birthday dinner: COMPLETELY CLEAN-SHAVEN (no beard, no moustache, smooth chin), silver-grey hair cut short, the same glasses, a navy knitted sweater, smiling warmly, sitting at a table with a white tablecloth, a small cake and teacups, warm tungsten home light, shallow depth of field, a blurred living room behind him.""")
G.append(f"""A single photorealistic evidence contact sheet, 1:1 square at the highest resolution you can generate — ideally 4096×4096 or more: exactly 9 separate square panels arranged in a strict grid of 3 columns and 3 rows, all panels identical in size, separated by uniform solid pure black gutters about 2% of the image width, black outer margin of the same width. Each panel is a forensic-style close-up of one subject, lit by a hard flashlight-like key light from above at an angle, deep black falloff, muted desaturated colours, subtle film grain, macro detail. No people, no hands, no faces. {NOTXTP}
Row 1: (1) a grey fabric wheeled suitcase lying open on a hotel luggage rack: two folded shirts, a folded sweater, a plain grey document folder and a CLOSED, zipped dark toiletry bag on top — nothing else; (2) the inside of a hotel built-in wardrobe: the back wall panel has been removed and leans aside, revealing a steel service door with a small keyhole and a simple thumb-turn knob on this side, fine white plaster dust on the wardrobe floor, empty hangers pushed to one side of the rail; (3) a dusty narrow service corridor with pipes along the wall: a grey steel door whose handle and escutcheon are noticeably clean and dust-free, and on the dusty floor in front of it a clean swept semicircle where the door has recently swung open.
Row 2: (4) a crumpled paper train ticket wedged between the metal seat rails under the passenger seat of a dark car, a rubber floor mat with dried muddy shoe marks, the ticket's print illegible; (5) a hotel room desk: a plain white envelope with a blank white key card half sticking out of it, a blank hotel notepad and a pen in a leather holder; (6) an old photocopy of a typed 1940s official document with round stamp shapes and a signature scrawl, all writing illegible, in the top corner a faint grey ghostly outline of an oval watermark, the copy slightly smudged.
Row 3: (7) a yellow sticky note stuck to the edge of a computer monitor, covered with hasty handwritten scribble and three exclamation marks, the handwriting illegible; (8) an open metal key cabinet on a basement wall with rows of keys hanging on hooks, small blank round tags, no empty hooks; (9) a concrete staircase landing with a cast-iron radiator, and on the floor under the radiator a plain white plastic hotel key card lying face down (its blank back side up).""")
G.append(f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): a narrow hotel room WITHOUT ANY WINDOW, lit only by warm bedside lamps and a ceiling light: a neatly made double bed with an untouched bedspread and two plumped pillows, a small desk with a lamp, a closed built-in wardrobe filling one side wall, a grey wheeled suitcase standing CLOSED on a luggage rack, a small square ventilation grille high on the wall near the ceiling with four screws, an open bathroom door showing folded dry white towels, the entrance door standing wide open to the corridor with its inner security latch visibly cut through (a cleanly cut metal latch hanging), faint damp shoe smudges on the carpet near the door, clean and quiet. 24mm lens, deep focus, muted colour grade with warm tungsten and cool teal shadows, fine film grain, no people. {NOTXT}""")
G.append(f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): the reception and lobby of an old, elegant mid-size city hotel in Szczecin: a long dark-wood reception counter with a computer screen turned away from the camera, a small document scanner and a brass desk bell on the counter, a key-card encoder, behind it a wall with pigeonholes, a lobby with leather armchairs and a low table, brass wall lamps, a wide entrance glass door on one side showing a grey overcast street with wet cobblestones, an arched passage on the other side leading to a dim bar. {TIME} 24mm lens, deep focus, muted colour grade, fine film grain, no people. {NOTXT}""")
G.append(f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): a hotel conference room called amber room, with warm amber-toned wood panelling: a long table for twelve with leather chairs, glass carafes of water, closed document folders with coloured tabs at each seat, one chair at the head of the table, a projector on the table, a binder lying open in the middle, papers left as if a meeting was suddenly interrupted, two cold cups of coffee, tall windows with heavy curtains showing a grey overcast sky. {TIME} 24mm lens, deep focus, muted colour grade, fine film grain, no people. {NOTXT}""")
G.append(f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): the basement office of a hotel's technical manager: metal shelving full of old binders and rolled architectural drawings, a large old floor plan drawing spread on a desk under a green-shaded lamp (lines of rooms and corridors, no readable text), an open metal key cabinet with rows of keys on hooks, a door-controller panel with small LEDs on the wall, pipes and cable trays under a low ceiling, a single small high basement window with grey daylight. 24mm lens, deep focus, muted colour grade, fine film grain, no people. {NOTXT}""")
G.append(f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): a narrow, dusty service corridor inside an old hotel, running along an outer wall: bare painted walls, pipes and cable trays under the ceiling, a few grey steel inspection doors set into the wall at intervals, a thin layer of dust on the concrete floor, at the far end a grey staff staircase with a metal handrail going down, lit by a few cold fluorescent tubes, one tube flickering dimmer. 24mm lens, deep focus, muted colour grade, fine film grain, no people. {NOTXT}""")
G.append(f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): a small classic hotel bar with dark wood and brass: a bar counter with brass lamps and shelves of bottles, a cash register, four small round tables with chairs, one corner table with an empty whisky glass and a bowl of peanuts left on it, a doorway on one side giving a partial view of the lobby, warm dim light, chairs not yet stacked. 24mm lens, deep focus, muted colour grade with warm tungsten tones, fine film grain, no people. {NOTXT}""")
G.append(f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): the office of a senior archivist in a state archive in Koszalin, as seen in daylight: tall shelves packed with grey archival boxes and bundles of old files, a wooden desk with a desk lamp with a green glass shade, a computer monitor with several small yellow sticky notes on its edges (illegible handwriting), a wooden card-catalogue cabinet with many small drawers, one drawer pulled out, a magnifying glass and a light box on the desk, an empty office chair, grey daylight from a window. 24mm lens, deep focus, muted colour grade, fine film grain, no people. {NOTXT}""")
G.append(f"""A single photorealistic cinematic exterior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): a small car park behind an old city hotel in Szczecin: an automatic barrier with a camera on a short pole at the entrance, about a dozen parking bays on wet asphalt with puddles, exactly seven parked cars, no more: a navy blue Toyota Corolla-like sedan, a white Kia Sportage-like compact SUV, a grey Opel Insignia-like car, a green Dacia Duster-like small SUV, a dark graphite Audi A4-like sedan, a red Fiat Tipo-like compact car and a white Volkswagen Touran-like minivan — NO silver cars, no visible badges or number plates, along the back wall of the hotel a narrow alley leading about thirty metres to a plain grey staff door with a lamp above it and a small dark camera next to it, a tiny smokers' shelter with a bench near that door, old plastered rear walls with drainpipes. {TIME} 24mm lens, deep focus, muted colour grade, fine film grain, no people. {NOTXT}""")
G.append(f"""A single photorealistic cinematic establishing shot, 16:9 at the highest resolution you can generate — ideally 7680×4320 (8K), at minimum 3840×2160 (4K): an old, elegant six-storey city hotel on a cobbled old-town street in Szczecin at night in steady rain, warm light in a few windows, a lit entrance canopy, wet cobblestones reflecting the lamps, most windows on one upper floor dark, the camera slightly low, ominous and quiet, muted desaturated colour grade with deep blue-teal shadows and warm sodium accents, subtle 35mm film grain. The hotel facade is centred. No people, no vehicles. {NOTXT}""")
G.append(f"""A single photorealistic cinematic wide interior shot, 16:9 at the highest resolution you can generate — ideally 7680×4320 (8K), at minimum 3840×2160 (4K): a long windowless hotel corridor in the early morning, the warm wall sconces still on, patterned carpet, one door in the middle standing ajar with cold light spilling out and its cut security latch visible, the carpet in front of it empty and clean, the far end of the corridor fading into darkness, shallow depth of field, warm tungsten and cold teal light, subtle 35mm film grain, quiet and tense. No people. {NOTXT}""")
names = ['Plansza A — portrety (potnę na 6)', 'Plansza B — dr Szulc: zdjęcie z dowodu i zdjęcie z lutego (potnę na 2)', 'Plansza C — dowody (potnę na 9)',
         'Pokój 214', 'Recepcja i hol', 'Sala „Bursztynowa”', 'Dział techniczny', 'Korytarz gospodarczy', 'Bar „Kotwica”', 'Archiwum w Koszalinie', 'Parking za hotelem', 'Okładka', 'Grafika tytułowa']
QUAL = ' Maximum quality: ultra-detailed, tack-sharp, crisp micro-detail and textures that hold up on a very large 4K/8K television screen, no blur, no softness, no smudged or painterly areas, no compression artefacts, no upscaling artefacts, no AI artefacts (no extra fingers, no melted objects, no warped lines), clean straight architectural lines.'
G = [x + QUAL for x in G]
for i, b in enumerate(G, 1):
    g.append(f"## {i}\n```\n{b}\n```\n")
open(f'docs/PROMPTY_GRAFIK_{CID}.md', 'w', encoding='utf-8').write('\n'.join(g))
json.dump(names, open(f'tools/voice/{CID}-graphics-order.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

VID = "Format: 16:9 at the highest resolution and quality available — ideally 3840×2160 (4K), at minimum 1920×1080 — highest bitrate, 24 fps, about 8 seconds, no sound, no text, no letters, no numbers, no logos, no faces visible. Photorealistic cinematic style, muted desaturated colour grade, cool blue-teal tones with warm tungsten accents, subtle 35mm film grain."
VQ = ' Maximum quality: crisp, stable, artefact-free footage with no flicker, no warping, no morphing objects, no compression blocks; smooth natural motion; every detail sharp enough for a very large 4K television.'
vids = [
 ('005-intro.mp4', f"A seamless looping shot: a very slow, smooth push along a long, empty hotel corridor at night, patterned carpet, warm steady wall sconces, all doors closed, at the far end a dark window streaked with rain. The very first and the very last frame must look nearly identical so the clip loops without a visible cut. {VID}"),
 ('005-bt-beard.mp4', f"Extreme close-up on a hotel reception counter at night: the green light bar of a flatbed document scanner slides slowly under its glass lid, a warm desk lamp beside it, then the camera drifts up to a small framed mirror behind the counter that reflects only a blurred grey shape of a hat and coat — no face; the light bar returns. {VID}"),
 ('005-bt-door.mp4', f"A slow push-in inside a hotel built-in wardrobe lit by a flashlight beam: a back wall panel is lifted away and leaned aside by itself (no hands visible), revealing a grey steel door with a keyhole; fine plaster dust drifts in the beam and settles on the wardrobe floor; empty hangers sway gently on the rail. {VID}"),
 ('005-bt-pass.mp4', f"Inside a dark parked car at night in heavy rain: raindrops streak down the windscreen lit by orange street lamps, the camera slowly tilts down from the empty passenger seat to the floor, where a crumpled paper train ticket lies wedged between the seat rails next to a muddy floor mat; wipers are still. {VID}"),
 ('005-bt-ring.mp4', f"Close-up in a dark hotel room at night: a woman's hand with a thin gold wedding ring rests on the trackpad of an open laptop, the screen glow lights the hand; on the screen a blurred, completely illegible document, one blurred line vanishes as the hand moves slightly; the camera racks focus from the screen to the glinting wedding ring. Only the hand is visible, no face. {VID}"),
]
v = [f"# ŚLAD — prompty filmowe i dźwiękowe, sprawa {CID} „{c['title']}”\n", "Każdy film to osobny prompt. Filmy bez dźwięku — dźwięk dodaje gra. Kolejność plików: wstęp, potem cztery przełomy.\n", "## WIDEO\n"]
for i, (f, p) in enumerate(vids, 1):
    v.append(f"### {i}\n```\n{p}{VQ}\n```\n")
v.append("## DŹWIĘK\n")
v.append("""### 1
```
Generate a single seamless-loop ambient audio track, about 3 minutes long, stereo, at the highest audio quality available — preferably uncompressed WAV, 48 kHz, 24-bit (if WAV is not possible: the highest-bitrate file available). The night atmosphere of an old city hotel during steady rain: soft rain on windows and an old roof, a very faint distant hum of a ventilation system, now and then a muffled far-away elevator mechanism and the creak of old floorboards in a corridor, a very low, slow, barely changing dark synth drone underneath. No melody, no beat, no voices, no music hooks, no sudden loud sounds. The first and last seconds must match so the track loops without an audible seam. Quiet, steady background suitable to sit under spoken dialogue.
```
""")
open(f'docs/PROMPTY_FILMY_DZWIEK_{CID}.md', 'w', encoding='utf-8').write('\n'.join(v))
print('OK', {k: len(x['lines']) for k, x in lines_out.items()}, 'grafiki', len(G), 'filmy', len(vids))
