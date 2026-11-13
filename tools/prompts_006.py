#!/usr/bin/env python3
"""Generuje docs/PROMPTY_*_006.md oraz tools/voice/006-lines.json. Tekst kwestii pobierany 1:1 z cases/006.json.
Użycie (z katalogu repo): python3 tools/prompts_006.py"""
import json, re, os
c = json.load(open('cases/006.json', encoding='utf-8'))
CID = '006'

SPOKEN = [
 ('Niedziela, 6 grudnia, 9:00.', 'Niedziela, szóstego grudnia, godzina dziewiąta.'), ('35 mm', 'trzydzieści pięć milimetrów'),
 ('w 1958 roku', 'w tysiąc dziewięćset pięćdziesiątym ósmym roku'), ('O 22:41', 'O dwudziestej drugiej czterdzieści jeden'),
]
def clean(t):
    t = re.sub(r'\s*\([^)]*\)\s*', ' ', t).strip()
    for a, b in SPOKEN: t = t.replace(a, b)
    t = re.sub(r'\s{2,}', ' ', t)
    return re.sub(r'(^|[.?!] )([a-ząćęłńóśźż])', lambda m: m.group(1) + m.group(2).upper(), t)

VOICE = {
 'narrator': "Mature Polish male narrator in his early 50s. Deep, warm, slightly gravelly baritone. Noir documentary style: calm, measured, low and intimate, like a seasoned detective reading a case file aloud late at night. Standard Polish pronunciation, no regional accent. If you generated this narrator for an earlier case, reuse exactly the same voice.",
 'ewa': "Polish woman, 52, manager of an old city cinema. Composed, clear, low alto with cultured diction; rational, polite and firm, every sentence under control. When lying she stays calm and slightly too smooth; when cornered her voice gets quieter and harder, and in her last admissions it turns flat and bitter, tired — never hysterical, never crying loudly. Standard Polish.",
 'damian': "Polish man, 31, a cinema projection technician. Soft-spoken light baritone, a bit hoarse from crying the night before, casual modern speech, warm when he talks about his old master; sheepish and embarrassed when he admits a small lie. Standard Polish.",
 'grzegorz': "Polish man, 46, from Warsaw, son of the dead projectionist. Tired, clipped, defensive baritone of a man in debt who has not slept; short sentences, irritated by default; heavy, quiet and guilty when he admits the quarrel with his father. Standard Polish.",
 'joanna': "Polish woman, 58, runs the cinema snack bar for twenty-five years. Warm, chatty, motherly mezzo with a lively rhythm, a little Łódź street-wise colour but standard pronunciation; says „kochanie”; quick and vivid when she describes what she saw, sincere and moved when she talks about the old projectionist. Standard Polish.",
 'lipka': "Polish man, 84, a retired tram driver. Old but sharp, slightly trembling, dignified baritone with old-fashioned politeness and precise, careful speech; proud and certain when he describes what he saw; genuinely flustered, embarrassed and apologetic when he realises his honest mistake. Standard Polish.",
}
NAME = {'narrator': 'Narrator', 'ewa': 'Ewa Sitek', 'damian': 'Damian Wróbel', 'grzegorz': 'Grzegorz Barcz', 'joanna': 'Joanna Rak', 'lipka': 'Stanisław Lipka'}
KIND = {'q': "answer to an investigator's question", 'break': 'reaction after being confronted with hard evidence (the character gives up part of the lie or admits something)',
        'mistake': 'reaction when he suddenly realises he made an honest mistake, not a lie — surprised, embarrassed, apologetic',
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
order = ['ewa', 'damian', 'grzegorz', 'joanna', 'lipka']
blocks = []
for who in order:
    p = next(x for x in c['people'] if x['id'] == who)
    L = [{'id': q['id'], 'kind': 'q', 'text': q['a']} for q in p['questions']]
    L += [{'id': s['id'], 'kind': 'mistake' if s.get('mistake') else 'break', 'text': s['response']} for s in p['statements'] if s.get('response')]
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
PERFORMANCE: Opening narration of the case. Slow, atmospheric, with short pauses between paragraphs. Slight weight on the last sentence of each paragraph. Mood: a grey December Sunday morning in an empty old cinema the day after its farewell screening — quiet, nostalgic, with a cold undertone. The last paragraph is a practical aside from the chief to the team: read it a little lighter and more matter-of-fact. Read it cleanly, no added sound effects.
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
SUN = "Time: Sunday morning in early December, grey overcast daylight after a night of rain — outdoor surfaces still wet and puddles on the ground, but it is NOT raining now."
G = []
G.append(f"""A single photorealistic contact sheet, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): exactly 6 separate portrait panels with a 4:5 vertical aspect, arranged in a strict grid of 3 columns and 2 rows, all panels identical in size, separated by uniform solid pure black gutters about 2% of the image width, black outer margin of the same width. Each panel contains exactly one person, head and shoulders, eye level, facing the camera at a slight three-quarter angle. {STYLE_P} {NOTXTP}
Row 1, panel 1: a 52-year-old Polish woman, the manager of an old city cinema, slim, ash-blonde hair pinned up in a perfectly neat low chignon, fine wrinkles, subtle makeup, a black fine-knit turtleneck, a thin gold wedding ring visible on a hand raised near her collar, composed polite expression with tense, watchful eyes, blurred dim cinema foyer with warm brass lamps behind her.
Row 1, panel 2: a tall 31-year-old Polish man, a cinema projection technician, dark hair tied in a small ponytail, short beard, red tired eyes as if he had cried, a black hooded sweatshirt with a small round embroidered sun emblem on the chest (a simple symbol, no letters), a smartphone in his hand, grieving and nervous expression, blurred projection room with a vintage film projector behind him.
Row 1, panel 3: a 46-year-old Polish man from Warsaw, the son of an old projectionist, short dark hair greying at the temples, unshaven, tired puffy eyes, an expensive dark wool overcoat over a grey sweater, a phone in his hand, closed defensive expression, looking slightly down, blurred cinema auditorium with red seats behind him.
Row 2, panel 1: a 58-year-old Polish woman who runs a cinema snack bar, plump, short curly hennaed auburn hair, a pencil tucked behind her ear, reading glasses on a cord, a dark apron over a patterned blouse, warm motherly face, worried but kind expression, blurred dark-wood bar counter with glasses and a coffee machine behind her.
Row 2, panel 2: an 84-year-old Polish man, a retired tram driver, thin, white hair neatly combed, a grey felt hat in his hand, an old but carefully ironed tweed jacket, white shirt and a dark tie, sharp clear eyes, dignified, slightly proud expression, blurred old tenement room with lace curtains behind him.
Row 2, panel 3: a 73-year-old Polish man, an old cinema projectionist, alive and well, grey hair, thick grey moustache, glasses on a cord around his neck, a grey cotton work coat over a shirt and knitted vest, white cotton gloves tucked in the breast pocket, a gentle proud smile, warm light from a vintage 35mm film projector beside him, blurred projection booth behind him.""")
G.append(f"""A single photorealistic evidence contact sheet, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): exactly 6 separate square panels arranged in a strict grid of 3 columns and 2 rows, all panels identical in size, separated by uniform solid pure black gutters about 2% of the image width, black outer margin of the same width. Each panel is a forensic-style close-up of one subject, hard flashlight-like key light from above at an angle, deep black falloff, muted desaturated colours, subtle film grain, macro detail. No people, no hands, no faces except inside the old photograph in panel 2. {NOTXTP}
Row 1: (1) a round grey steel 35mm film can with its lid, empty, dented at the rim, lying on its side on dark worn linoleum at the foot of a tall grey metal shelf full of film cans; a dark dried smear on the can's rim; part of a white chalk line on the floor beside it; the top shelf above is visibly covered with a thick, untouched layer of grey dust; (2) a framed black-and-white photograph hanging on a dark wall, with a cream passe-partout: inside the photo, in a 1990s projection booth, a 45-year-old man with dark greying hair, a moustache and a grey work coat stands next to a young woman of about 24 with ash-blonde hair pinned up in a bun; both wear white cotton gloves; her gloved hand rests on the changeover lever of a big vintage 35mm film projector; on the passe-partout below the photo a short handwritten caption, illegible scribble; (3) a glass wall display case in a cinema foyer with four framed vintage illustrated film posters from the 1930s–1960s side by side — painted portraits, a ship at sea, a girl on a tram, a river at night — the posters carry no readable lettering, the case has a small lock on its frame.
Row 2: (4) the right sleeve and right pocket of a light beige trench coat hanging on a wooden coat stand, the fabric damp at the shoulder, with smeared rust-brown stains and tiny flakes of red-orange paint along the sleeve from cuff to elbow and on the pocket; (5) a worn light wooden door wedge with a drilled hole and a loop of red cord, lying in a rain puddle on wet dark cobblestones under the bottom step of a rusty red-orange steel fire escape; (6) the inside of a blue plastic recycling container with its lid half open: on top, wet torn pieces of a lined sheet of paper covered with neat handwriting in blue ink, the ink partly blurred by rain and illegible, under them flattened cardboard cup boxes.""")
PLACE = "24mm lens, deep focus, sharp realistic detail across the whole frame, muted desaturated colour grade with cool blue-teal shadows and warm tungsten accents, fine 35mm film grain, no people."
G.append(f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): the projection booth of an old 1950s city cinema, seen from the entrance door, on a grey Sunday morning — the booth has no ordinary windows, only small square projection ports in the front wall looking into a dark auditorium; light comes from a bare ceiling lamp and a small work lamp. Every object must be clearly visible, separate and not hidden behind anything. Composition from left to right: on the LEFT a big vintage 35mm film projector on a heavy pedestal (projector A), switched off, aimed at a projection port, its large rear take-up reel completely FULL of film; in the CENTRE between the two projectors a narrow sloped wooden desk with a thick squared notebook lying OPEN on it; RIGHT of centre an identical second projector (projector B), switched off, its take-up reel also full, a loose end of film hanging down from the reel, and on the floor next to its pedestal an OPEN round grey film can with a white index card lying inside; on the back wall, above an EMPTY film rewinding table, a single framed black-and-white photograph with a cream passe-partout; on the FAR RIGHT wall a grey steel emergency exit door, closed, with a horizontal push bar and a small white paper note taped above the bar; in the right foreground a small wooden side table with a thermos flask, reading glasses on a cord and a white envelope; on the dark linoleum floor in the middle foreground a white chalk outline of a body lying near the rewinding table, and about a metre away from it, at the foot of a tall grey metal shelf full of stacked film cans, a single grey steel film can lying on its side; the top shelf is thick with undisturbed dust. Old cables, a fire extinguisher, a calendar-less bare wall, worn paint, a faint smell-of-dust atmosphere. {PLACE} {NOTXT}""")
G.append(f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): the foyer of an old 1950s city cinema in Łódź the morning after a farewell party: polished marble floor, a dark-wood bar counter with leftover wine glasses and empty bottles, sagging paper garlands, a cash desk with a closed little window, a wide glass entrance door letting in grey daylight from a wet street; on the main wall a glass display case with four framed vintage illustrated film posters (painted artwork, no readable lettering); next to padded double doors leading to the auditorium a small grey metal wall cabinet with light switches and a small brass plate above it (engraving illegible). {SUN} {PLACE} {NOTXT}""")
G.append(f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): the small back-office of an old city cinema: a desk with a grey metal cash box, a stack of printed pages with pen corrections and a desk lamp, a tall wooden filing cabinet with binders and folders, a small open wall key cabinet with labelled keys on hooks (labels illegible), a wooden coat stand with a single light beige trench coat hanging on it, a narrow high window with grey morning light, an old cinema poster frame on the wall turned blank, a door ajar to a narrow corridor. {PLACE} {NOTXT}""")
G.append(f"""A single photorealistic cinematic exterior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): a typical narrow inner courtyard („studnia”) of old 19th-century tenements in Łódź, seen from the courtyard entrance: tall brick and peeling plaster walls, wet dark cobblestones with puddles, one old street lamp (switched off). The main subject is the plain rear wall of an old cinema building: a steel fire escape with two flights and a landing, its railing painted long ago red-orange and now flaking and rusty, climbs from the cobblestones to a grey steel door high on the wall (the door of the projection booth), the door closed. At ground level, a few metres to the left of the stairs, a grey metal back door into the cinema with a small white alarm-sensor box above its frame; right next to that door a blue plastic paper-recycling container with its lid slightly open. Under the lowest flight of the fire escape, in a puddle, a small worn wooden door wedge with a loop of red cord. A strip of plain red-and-white barrier tape (no lettering) is tied across the bottom of the stairs. On the opposite side, the edge of a tenement outbuilding with old windows. All objects clearly visible and not overlapping. {SUN} {PLACE} {NOTXT}""")
G.append(f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): the one-room flat of an 84-year-old retired tram driver in an old Łódź tenement outbuilding, grey Sunday morning light: on the LEFT a dark wooden 1960s sideboard with glass doors, and above it on the wall a round white-faced analogue wall clock with black hands showing ten past ten; in the CENTRE a small table covered with a checked oilcloth, on it an open small cardboard box with an old silver pocket watch on a chain inside, and right next to it an opened pack of batteries with one missing; on the RIGHT an armchair by a tall window with a lace curtain pulled aside; through the window, across a narrow wet courtyard, the rear wall of an old cinema with a rusty red-orange steel fire escape leading to a grey door, small in the distance but clearly visible; a grey felt hat on a hook, a framed old photograph of a tram on the wall, worn parquet floor. {PLACE} {NOTXT}""")
G.append(f"""A single photorealistic cinematic establishing shot, 16:9 at the highest resolution you can generate — ideally 7680×4320 (8K), at minimum 3840×2160 (4K): the facade of an old 1950s single-screen city cinema on a street of old tenements in Łódź on a rainy December night: a curved marquee canopy with warm bulbs, the marquee letter board left blank, tall glass doors glowing amber from the foyer, wet pavement and tram rails reflecting the lights, and high up on the side wall one small lit window of the projection booth. Camera slightly low, nostalgic and ominous, muted desaturated colour grade with deep blue-teal shadows and warm sodium and tungsten accents, subtle 35mm film grain. No people, no vehicles. {NOTXT}""")
G.append(f"""A single photorealistic cinematic wide interior shot, 16:9 at the highest resolution you can generate — ideally 7680×4320 (8K), at minimum 3840×2160 (4K): view from inside a dark projection booth through a small square projection port: a bright beam of light from a vintage 35mm projector cuts through dust over a dark, empty old cinema auditorium with rows of red velvet seats and a balcony rail, and lands on a large screen that glows completely blank white; the projector's rear reel and lamp housing frame the left edge in silhouette. Melancholic, quiet, the end of an era. Muted colour grade, warm projector light against cold teal darkness, subtle 35mm film grain. No people. {NOTXT}""")
names = ['Plansza A — portrety (potnę na 6)', 'Plansza B — dowody (potnę na 6)', 'Kabina projekcyjna', 'Foyer', 'Biuro kierowniczki', 'Podwórze za kinem',
         'Mieszkanie pana Lipki', 'Okładka', 'Grafika tytułowa']
QUAL = ' Maximum quality: ultra-detailed, tack-sharp, crisp micro-detail and textures that hold up on a very large 4K/8K television screen, no blur, no softness, no smudged or painterly areas, no compression artefacts, no upscaling artefacts, no AI artefacts (no extra fingers, no melted objects, no warped lines), clean straight architectural lines.'
G = [x + QUAL for x in G]
g = [f"# ŚLAD — prompty graficzne, sprawa {CID} „{c['title']}”\n", "Każdy blok to osobny obraz — wklejaj bez zmian. Plansze potnę i podepnę do gry. Obrazy nie zawierają tekstu.\n"]
for i, b in enumerate(G, 1):
    g.append(f"## {i}\n```\n{b}\n```\n")
open(f'docs/PROMPTY_GRAFIK_{CID}.md', 'w', encoding='utf-8').write('\n'.join(g))
json.dump(names, open(f'tools/voice/{CID}-graphics-order.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

VID = "Format: 16:9 at the highest resolution and quality available — ideally 3840×2160 (4K), at minimum 1920×1080 — highest bitrate, 24 fps, about 8 seconds, no sound, no text, no letters, no numbers, no logos, no faces visible. Photorealistic cinematic style, muted desaturated colour grade, cool blue-teal tones with warm tungsten accents, subtle 35mm film grain."
VQ = ' Maximum quality: crisp, stable, artefact-free footage with no flicker except where described, no warping, no morphing objects, no compression blocks; smooth natural motion; every detail sharp enough for a very large 4K television.'
vids = [
 ('006-intro.mp4', f"A seamless looping shot: a very slow, smooth drift through a dark, empty old cinema auditorium towards a large blank screen; a soft beam of projector light passes overhead from a small window at the back, dust motes floating slowly in it, the screen glowing faintly white with a gentle film flicker. The very first and the very last frame must look nearly identical so the clip loops without a visible cut. {VID}"),
 ('006-bt-change.mp4', f"Close-up in a dim projection booth: the lamp housing of a vintage 35mm film projector lights up from inside with a warm glow, then its big feed reel starts to turn by itself and the film begins to run through the gate with a fast, steady flicker of light; the camera slowly racks focus from the turning reel to the projection port, where the beam shoots out into darkness. No hands, no people. {VID}"),
 ('006-bt-clock.mp4', f"An extreme close-up of a round white-faced analogue wall clock in an old man's room in grey morning light: the second hand sweeps slowly, the camera pushes in very slowly until the black hour hand fills the frame, then gently pulls focus to a lace curtain and a rainy courtyard window behind it. {VID}"),
 ('006-bt-student.mp4', f"A slow push-in on a framed black-and-white photograph hanging on the dark wall of a projection booth: in the photo a middle-aged projectionist and a young blonde woman in white gloves at a vintage film projector, both seen small and slightly from the side so their faces stay soft and not detailed; flickering projector light from off-screen washes over the glass of the frame. {VID}"),
 ('006-bt-letter.mp4', f"Top-down close-up on a dark wooden table under a desk lamp: nine wet, torn pieces of a lined handwritten letter slowly slide together by themselves and join into one whole sheet, the torn edges matching; the blue ink is blurred and completely illegible; drops of water glisten on the paper. No hands. {VID}"),
]
v = [f"# ŚLAD — prompty filmowe i dźwiękowe, sprawa {CID} „{c['title']}”\n", "Każdy film to osobny prompt. Filmy bez dźwięku — dźwięk dodaje gra. Kolejność plików: wstęp, potem cztery przełomy.\n", "## WIDEO\n"]
for i, (f, p) in enumerate(vids, 1):
    v.append(f"### {i}\n```\n{p}{VQ}\n```\n")
v.append("## DŹWIĘK\n")
v.append("""### 1
```
Generate a single ambient soundscape for a detective game, about 3 minutes long, stereo, at the highest audio quality available — preferably uncompressed WAV, 48 kHz, 24-bit (if WAV is not possible: the highest-bitrate file available). The place: a large, empty old 1950s cinema on a grey December Sunday morning, the day after its very last screening. Build it as a slowly evolving scene, not a flat noise bed:
— underneath everything, the quiet, deep room tone of a big empty auditorium with soft natural reverb and a very low, barely audible hum of old electrical installations;
— outside, muffled through thick walls, light rain dripping from gutters into a courtyard and, every minute or so, a distant tram passing on the street with a soft rumble and the faint squeal of rails;
— inside, occasional small sounds far away in the building: an old wooden seat creaking as it settles, a radiator ticking and knocking, a door closing softly somewhere in a corridor, footsteps on a marble floor fading away;
— about three times over the whole track, very faint and as if remembered, the rhythmic mechanical clatter of a vintage 35mm film projector running for a few seconds and dying away again, as distant as a memory;
— a very low, slow, warm and melancholic synth pad, barely noticeable, rising and falling gently.
No melody, no beat, no voices, no speech, no music hooks, no sudden loud sounds. Calm, nostalgic, slightly eerie. Mix level comfortable for long background listening. The end must blend smoothly back into the beginning so the track can loop.
```
""")
open(f'docs/PROMPTY_FILMY_DZWIEK_{CID}.md', 'w', encoding='utf-8').write('\n'.join(v))
print('OK', {k: len(x['lines']) for k, x in lines_out.items()}, 'grafiki', len(G), 'filmy', len(vids))
