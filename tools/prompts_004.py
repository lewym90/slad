#!/usr/bin/env python3
"""Generuje docs/PROMPTY_*_004.md oraz tools/voice/004-lines.json. Tekst kwestii pobierany 1:1 z cases/004.json.
Użycie (z katalogu repo): python3 tools/prompts_004.py"""
import json, re, os
c = json.load(open('cases/004.json', encoding='utf-8'))
CID = '004'

# ---------- zapis mówiony (liczby, skróty) ----------
SPOKEN = [
 ('Piątek, 27 listopada, 10:00.', 'Piątek, dwudziestego siódmego listopada, godzina dziesiąta.'),
 ('O 6:10', 'O szóstej dziesięć'), ('o 1:47', 'o pierwszej czterdzieści siedem'), ('O 9:00', 'O dziewiątej'),
 ('23 osoby', 'dwadzieścia trzy osoby'), ('W 2024', 'W dwa tysiące dwudziestym czwartym'),
 ('o 0:41', 'o zero czterdzieści jeden'), ('o 0:12', 'o zero dwanaście'), ('od 1:03', 'od pierwszej zero trzy'),
 ('o 23:30', 'o dwudziestej trzeciej trzydzieści'), ('o 3:12', 'o trzeciej dwanaście'), ('od 1:52', 'od pierwszej pięćdziesiąt dwa'),
 ('25 watów', 'dwadzieścia pięć watów'), ('MW-2611', 'em wu dwadzieścia sześć jedenaście'),
 ('do PRACA', 'do pracy'), ('NIK', 'Nik'), ('SERWIS', 'serwis'), ('PRACA', 'praca'), ('K3', 'ka trzy'), ('PIN', 'pin'),
]
def clean(t):
    t = re.sub(r'\s*\([^)]*\)\s*', ' ', t).strip()
    for a, b in SPOKEN: t = t.replace(a, b)
    t = re.sub(r'\s{2,}', ' ', t)
    return re.sub(r'(^|[.?!] )([a-ząćęłńóśźż])', lambda m: m.group(1) + m.group(2).upper(), t)

# ---------- głosy ----------
VOICE = {
 'narrator': "Mature Polish male narrator in his early 50s. Deep, warm, slightly gravelly baritone. Noir documentary style: calm, measured, low and intimate, like a seasoned detective reading a case file aloud late at night. Standard Polish pronunciation, no regional accent.",
 'kopec': "Polish man, 49, a service engineer. Even, quiet, matter-of-fact baritone with a technical, precise way of speaking, slightly nasal, no emotion in the voice by default. Under pressure he speeds up a little and his sentences get shorter; when he lies he sounds helpful and relaxed, a notch too smooth. Standard Polish, no regional accent.",
 'burda': "Polish woman, 38, a night-shift control-room operator. Clear, tired, mid-range mezzo with a professional, procedural tone, a little hoarse after a night of talking on the phone. Defensive when questioned, quieter and shakier when she admits something. Standard Polish.",
 'szczerba': "Polish man, 51, a deputy mayor. Smooth, confident, well-modulated tenor-baritone with a public speaker's polish, friendly and a little patronising. Fast, fluent, rehearsed when lying; when cornered he gets clipped and irritated, then falls back on administrative phrases. Standard Polish.",
 'hajduk': "Polish woman, 33, a local newspaper reporter. Quick, clear, slightly husky alto with a lively, alert delivery, sharp and a little sarcastic. Guarded and curt while hiding something; fast and urgent when she finally talks. Standard Polish.",
 'pyka': "Polish man, 60, the chairman of a chemical plant. Heavy, gruff baritone with a tired rasp, impatient and authoritative, used to being obeyed. Dismissive when asked uncomfortable questions; defensive and bitter when confronted. Standard Polish.",
}
NAME = {'narrator': 'Narrator', 'kopec': 'Dariusz Kopeć', 'burda': 'Agnieszka Burda', 'szczerba': 'Piotr Szczerba', 'hajduk': 'Lena Hajduk', 'pyka': 'Witold Pyka'}
KIND = {'q': 'answer to an investigator\'s question', 'break': 'reaction after being confronted with hard evidence (the character gives up part of the lie)', 'deflect': 'curt, evasive reaction to a wrong accusation'}
COMMON = "Natural, believable acting like in a high-quality Polish radio drama — not a synthetic announcer. Correct Polish pronunciation and stress (on the penultimate syllable). Words in „quotation marks” are the character quoting someone else: mark them with a subtle change of tone, do not imitate another voice."

# ---------- GŁOSY ----------
lines_out = {}
md = [f"# ŚLAD — prompty głosowe, sprawa {CID} „{c['title']}”\n",
 "Każda postać to **jeden prompt = jedno nagranie** ze wszystkimi jej kwestiami po kolei, rozdzielonymi dłuższą ciszą (ok. 3 s) — potnę je po ciszy. Narrator ma osobny, krótki prompt.\n",
 "**UWAGA, SPOILERY:** kwestie postaci zdradzają rozwiązanie. Kopiuj przyciskiem kopiowania przy bloku, nie czytaj treści. Generuj każdą postać w osobnej rozmowie lub trzymaj ją w tej samej, żeby głos był spójny.\n",
 "Gotowe pliki (jeden MP3 na postać + narrator) wrzuć do czatu. Nazwy plików są w promptach.\n"]

def block(fname, who, direction, texts, many):
    head = f"""Generate a single spoken-voice audio file in Polish.

FILE NAME: {fname}
FORMAT: MP3, 44.1 kHz, mono. Dry, close-miked studio voice recording. No music, no background ambience, no sound effects, no breathing noises between lines beyond what is natural. About 0.3 seconds of silence at the start and at the end.

CHARACTER: {NAME[who]}
VOICE: {VOICE[who]}
"""
    if many:
        head += f"""
STRUCTURE: the recording contains exactly {len(texts)} separate spoken lines, in the order given below. Between every two consecutive lines leave EXACTLY 3 seconds of complete silence (pure digital silence, no room tone, no sounds) so the lines can be cut apart. Never speak the line numbers, the stage directions or any of these instructions. Keep the same voice, timbre, pitch and recording level for every line.

ACTING NOTES (do not read aloud) — for each line its type is given; play it accordingly:
"""
    return head

for who in ['kopec', 'burda', 'szczerba', 'hajduk', 'pyka']:
    p = next(x for x in c['people'] if x['id'] == who)
    L = [{'id': q['id'], 'kind': 'q', 'text': q['a']} for q in p['questions']]
    L += [{'id': s['id'], 'kind': 'break', 'text': s['response']} for s in p['statements'] if s.get('response')]
    L += [{'id': f'deflect-{i}', 'kind': 'deflect', 'text': d} for i, d in enumerate(p.get('deflect', []))]
    for i, x in enumerate(L, 1): x['n'] = i; x['spoken'] = clean(x['text'])
    for x in L:
        assert not re.search(r'\d|[A-Z]{2,}', x['spoken']), (who, x['id'], x['spoken'])
    lines_out[f'{CID}-{who}'] = {'name': p['name'], 'file': f'{CID}-{who}-all.mp3', 'lines': L}
    fname = f'{CID}-{who}-all.mp3'
    notes = '\n'.join(f"Line {x['n']}: {KIND[x['kind']]}." for x in L)
    spoken = '\n\n'.join(x['spoken'] for x in L)
    prm = block(fname, who, '', L, True) + notes + f"""

{COMMON}

TEXT TO SPEAK — {len(L)} lines, separated here by blank lines. Read each one exactly as written, in Polish, word for word, then leave 3 seconds of silence before the next one. Do not add, omit, translate or read any of these instructions aloud:
<<<
{spoken}
>>>"""
    md.append(f"## {p['name']} — {p['role']} ({len(L)} kwestii)\n```\n{prm}\n```\n")

brief = clean(' '.join([c['intro']['lead']] + c['intro']['brief']))
assert not re.search(r'\d', brief), brief
nar = f"""Generate a single spoken-voice audio file in Polish.

FILE NAME: {CID}-narrator-brief.mp3
FORMAT: MP3, 44.1 kHz, mono. Dry, close-miked studio voice recording. No music, no background ambience, no sound effects. About 0.3 seconds of silence at the start and at the end.

CHARACTER: Narrator
VOICE: {VOICE['narrator']}
If you have already generated this character's voice earlier in this conversation, reuse exactly the same voice, timbre and pitch.

PERFORMANCE: Opening narration of the case. Slow, atmospheric, with short pauses between paragraphs. Slight weight on the last sentence of each paragraph. Cold, technical night mood — fog, silence, a dead control room — but read it cleanly, no added sound effects.
{COMMON}

TEXT TO SPEAK — read it exactly as written, in Polish, word for word. Do not add, omit, translate or read any of these instructions aloud:
<<<
{brief}
>>>"""
md.insert(4, f"## Narrator — wprowadzenie do sprawy\n```\n{nar}\n```\n")
os.makedirs('docs', exist_ok=True); os.makedirs('tools/voice', exist_ok=True)
open(f'docs/PROMPTY_GLOSY_{CID}.md', 'w', encoding='utf-8').write('\n'.join(md))
json.dump(lines_out, open(f'tools/voice/{CID}-lines.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- GRAFIKA ----------
NOTXT = "Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders inside the panels."
STYLE_P = "Style for every panel: cinematic film still, 85mm lens, shallow depth of field, low-key lighting with a cold blue-teal key light and a small warm sodium-orange accent, muted desaturated colour grade, subtle 35mm film grain, realistic skin texture with pores and wrinkles, ordinary Central-European faces, not models, no glamour makeup, dark blurred modern Polish industrial or office interior in the background."
g = [f"# ŚLAD — prompty graficzne, sprawa {CID} „{c['title']}”\n",
 "Każda plansza i każdy obraz to osobny prompt — wklejaj bez zmian. Kafle w planszach są w stałej kolejności (opisanej przy każdej planszy); potnę je narzędziem `tools/cut_sheet.py` i podepnę do gry.\n",
 "Obrazy nie zawierają tekstu — wszystkie napisy w grze są dodawane w interfejsie.\n",
 "## Plansza A — portrety (format 3:2, np. 1536×1024)\nKolejność kafli: wiersz 1: Lasota, Kopeć, Burda; wiersz 2: Szczerba, Hajduk, Pyka.\n",
 f"""```
A single photorealistic contact sheet: exactly 6 separate square portrait panels arranged in a strict grid of 3 columns and 2 rows, all panels identical in size, separated by uniform solid pure black gutters about 2% of the image width, black outer margin of the same width. Each panel contains exactly one person, head and shoulders, eye level, facing the camera at a slight three-quarter angle. {STYLE_P} {NOTXT}
Row 1, panel 1: a 56-year-old Polish municipal crisis-management official, grey thinning hair, tired intelligent eyes behind thin rimless glasses, slightly rumpled dark blue blazer over an open-collar shirt, a lanyard with a blank plastic badge, expression of dry worry and quiet stubbornness, softly lit office with a window of night rain behind him.
Row 1, panel 2: a 49-year-old Polish service engineer, lean face, short dark hair with grey at the temples, stubble, calm closed expression, eyes that slide slightly to the side, navy company work jacket with reflective stripes, dark workshop with blurred equipment racks and a green status LED glowing behind him.
Row 1, panel 3: a 38-year-old Polish woman, a night-shift control-room operator, dark blonde hair in a messy ponytail, pale tired face, dark circles under her eyes, a headset resting around her neck, grey cardigan, blurred wall of glowing monitors behind her in a dim control room.
Row 2, panel 1: a 51-year-old Polish deputy mayor, well-groomed grey-brown hair, a confident practised half-smile, tailored charcoal suit, light blue shirt, small enamel city pin on the lapel, tidy modern city-hall corridor with a blurred glass door behind him.
Row 2, panel 2: a 33-year-old Polish woman, a local newspaper reporter, short dark bob with damp strands, sharp alert dark eyes, a trace of irony in her mouth, olive field jacket, a press lanyard with a blank card around her neck, a blurred rainy street at night with car lights behind her.
Row 2, panel 3: a 60-year-old Polish chairman of a chemical plant, heavy-set, grey crew cut, deep nasolabial folds, bloodshot eyes, an impatient hard stare, dark wool overcoat over a white shirt without a tie, blurred industrial pipes and a red warning lamp glowing behind him.
```
""",
 "## Plansza B — miejsca (format 3:2, np. 1536×1024)\nKolejność kafli: wiersz 1: stacja nadawcza, Centrum Zarządzania Kryzysowego; wiersz 2: zakład Chemrud, szpital; wiersz 3: Urząd Miasta, parking leśny; wiersz 4: redakcja, garaż Syreon.\n",
 f"""```
A single photorealistic sheet of exactly 8 separate wide cinematic panels arranged in a strict grid of 2 columns and 4 rows, all panels identical in size and in a wide landscape shape, separated by uniform solid pure black gutters about 2% of the image width, black outer margin of the same width. Every panel is a moody cinematic still of a place at night or in early grey morning, muted desaturated colour grade with cold blue-teal tones and small warm accents, subtle film grain, no people visible. {NOTXT}
Row 1, left: the inside of a small brick radio transmitter station at night, a tall grey equipment cabinet with its door open, an exposed bank of copper busbars behind a transparent safety panel, a key switch on the cabinet front, a heavy steel door with a card reader beside it, cold fluorescent light, a thin layer of dust on the concrete floor.
Row 1, right: a crisis-management dispatch room at night, a long console with three large monitors and a headset on the desk, a wall of dark screens with a few red status lights, an office chair pushed back, a bin under the desk, fog-grey light from a window.
Row 2, left: the night view of a chemical plant: tall pipe racks and a chlorine production hall with a cloud of pale greenish vapour drifting between lit floodlights, a closed control-room window with warning lights, wet asphalt, the outline of a cooling tower in the haze.
Row 2, right: a hospital emergency-department corridor at night, empty gurneys lined up along the wall, a single doctor's coat on a hook, cold green-white lighting, a dim triage desk with a computer monitor turned away from camera.
Row 3, left: a municipal office corridor with a blue carpet and a row of closed office doors, a half-open door at the end showing a desk with a lamp and a stack of binders, a small grey safe visible behind a cabinet, early grey morning light through a window.
Row 3, right: a forest gravel car park at night in thick fog, two cars parked at the far edge, a trail camera strapped to a pine trunk in the foreground with a tiny red LED, a wooden bollard, cold mist between the trees.
Row 4, left: a small local-newspaper office open space over a print shop, two desks under a rainy window, stacks of old newspapers, a cork board with printed photographs pinned to it, a desk lamp switched on, night.
Row 4, right: a service company garage in the early morning, a white panel van with a roof rack carrying an aluminium ladder, shelves of cable drums and plastic crates behind it, an open toolbox on the floor, harsh fluorescent light.
```
""",
 "## Plansza C — dowody i rekwizyty (format 1:1, np. 1024×1024)\nKolejność kafli: wiersz 1: klucz dynamometryczny, zegarek, przełącznik kluczykowy; wiersz 2: atrapa anteny, żółta karteczka, skrzynka narzędziowa; wiersz 3: sejf, telefon, pendrive.\n",
 f"""```
A single photorealistic evidence contact sheet: exactly 9 separate square panels arranged in a strict grid of 3 columns and 3 rows, all panels identical in size, separated by uniform solid pure black gutters about 2% of the image width, black outer margin of the same width. Each panel is a forensic-style close-up still life of one object, lit by a single hard flashlight-like key light from above at an angle, deep black falloff, muted desaturated colours, subtle film grain, macro detail. No people, no hands, no gore. {NOTXT}
Row 1: (1) a heavy steel adjustable torque wrench, about 50 cm long, scuffed and worn, a dull rust-brown dried stain in the groove of the head, lying on a bare concrete floor; (2) a black smartwatch with a cracked screen and a torn strap lying on a grey concrete floor, the screen dark; (3) a close-up of an industrial key switch with two positions on a grey metal panel, the key missing, a thin trace of white talc powder around the switch.
Row 2: (4) a cylindrical metal RF dummy load terminator with a coaxial connector, connected to a thick coaxial cable inside a cabinet, cool teal light; (5) two torn halves of a yellow sticky note lying on a white plastic waste-bin liner, handwritten pencil scribble on the pieces, illegible; (6) an open grey service-van toolbox, one empty shaped cut-out in black foam where a large wrench belongs, next to a crumpled pair of blue latex gloves.
Row 3: (7) a small grey wall safe with a four-digit mechanical dial lock, standing half hidden behind a wooden cabinet; (8) a smartphone without a lock screen lying face up on a dark pocket lining, the screen showing only blurred soft notification shapes; (9) a small black USB flash drive on a plain notebook page, a ring of coffee stain beside it.
```
""",
 "## Obraz D — okładka sprawy (format 16:9, np. 1536×864)\nPlik docelowy: `assets/cases/004-cover.webp` (kadruję do 900×520, więc główny motyw trzymaj na środku).\n",
 """```
A single photorealistic cinematic wide establishing shot, 16:9: a tall lattice radio mast on a fog-covered hill at night, a small brick transmitter station at its foot with one lit window, a row of silent loudspeaker sirens on the mast frame and a faint red aviation warning light blinking at the top, in the valley far below a sleepy industrial town with orange street lights and a faint pale green haze drifting from a chemical plant on the horizon, thick cold mist, muted desaturated colour grade with deep blue-teal shadows and small warm sodium accents, subtle 35mm film grain, atmospheric, ominous, quiet. The main subject — the mast and the station — is centred. No people, no vehicles. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders.
```
""",
 "## Obraz E — grafika tytułowa sprawy (format 16:9, np. 1536×864)\nPlik docelowy: `assets/art/004-keyart.webp`.\n",
 """```
A single photorealistic cinematic wide interior shot, 16:9: a crisis-management control room at night seen from behind the console, an empty operator chair, three big monitors glowing cold blue with abstract map shapes and a row of small red dots, a wall-sized map of a town with a ring of numbered-less speaker symbols that all remain unlit, a tall window showing in the distance a lattice radio mast on a foggy hill with a blinking red light, a paper cup of cold coffee and a yellow sticky note on the desk, cold teal light with a few warm orange accents, shallow depth of field, subtle 35mm film grain, quiet and tense. No people. Absolutely no readable text, letters, numbers, captions, logos, watermarks, frames or borders.
```
"""]
open(f'docs/PROMPTY_GRAFIK_{CID}.md', 'w', encoding='utf-8').write('\n'.join(g).replace('NOKXT', ''))

# ---------- FILMY I DŹWIĘK ----------
VID = "Format: 16:9, 1280×720, 24 fps, about 8 seconds, no sound, no text, no letters, no numbers, no logos, no people's faces visible. Photorealistic cinematic style, muted desaturated colour grade, cold blue-teal tones with small warm accents, subtle 35mm film grain."
vids = [
 ('004-intro.mp4', 'Wideo wprowadzające (zapętlane w tle ekranu sprawy — początek i koniec muszą płynnie się łączyć)',
  f"A seamless looping shot: a slow, very smooth push-in toward a tall lattice radio mast on a fog-covered hill at night, a row of silent loudspeaker sirens on the mast frame, a faint red aviation warning light blinking slowly at the top, drifting banks of mist, far below a sleepy town with orange street lights and a pale greenish haze over a chemical plant in the distance. The very first and the very last frame must look nearly identical so the clip loops without a visible cut. {VID}"),
 ('004-bt-service.mp4', 'Przełom: „Głucha stacja” (zagadka p-service)',
  f"Extreme close-up inside a dark transmitter cabinet: a gloved hand in blue latex turns a small key switch on a grey metal panel from one position to the other, a row of status LEDs on the panel changes from steady green to amber one by one, the lights of a cabinet interior fall to a low cold glow, the camera slowly pushes in on the amber LEDs, behind the panel a cooling fan spins down. Only the gloved hand is visible, no face. {VID}"),
 ('004-bt-k3.mp4', 'Przełom: „Martwy kanał” (telemetria K3)',
  f"A slow tracking shot along the bottom of an open equipment cabinet in cold teal light: a thick coaxial cable runs from a connector and ends in a small cylindrical metal dummy load, the camera glides past it, follows a second thick cable that is capped with a plastic cap and coiled loosely behind the cabinet in the dust, ending in darkness; dust motes float in the light, a thin line of dust lies over the coiled cable as if it had not been touched for a long time. No people. {VID}"),
 ('004-bt-time.mp4', 'Przełom: „Siedem minut” (zegarek i billing)',
  f"A locked-off close-up on a grey concrete floor: a black smartwatch with a cracked screen lies beside the base of a metal cabinet; a second, clean analog wall clock without numerals is reflected in the lens edge at the top of the frame; the camera slowly racks focus from the cracked watch to the wall clock and back, and the hands of the wall clock visibly sweep forward by a short interval while the watch stays frozen, creating the feeling that the two disagree by a few minutes; cold fluorescent light. No people. {VID}"),
 ('004-bt-blow.mp4', 'Przełom: „Jedno uderzenie” (klucz dynamometryczny)',
  f"A low-angle slow dolly shot in the dark narrow gap behind a grey equipment cabinet: the beam of a handheld flashlight sweeps slowly across a cable duct and stops on a heavy steel torque wrench lying half hidden in the dust, a dull rust-brown stain in the groove of its head catching the light, the beam holds, the surrounding dust motes drift in the light, then the camera pushes in slowly on the stain. No people, no hands, no gore. {VID}"),
]
v = [f"# ŚLAD — prompty filmowe i dźwiękowe, sprawa {CID} „{c['title']}”\n",
 "Każdy film to osobny prompt. Z każdego filmu zrobię plakat `.webp` (pierwsza klatka) o tej samej nazwie. Filmy bez dźwięku — dźwięk dodaje gra.\n",
 "UWAGA: opisy przełomów w grze zdradzają rozwiązanie zagadek; same prompty są ogólne, ale lepiej ich nie czytać przed grą.\n"]
for f, t, p in vids:
    v.append(f"## {t}\nPlik docelowy: `assets/video/{f}`\n```\n{p}\n```\n")
v.append("""## Dźwięk tła sprawy (zapętlany w czasie gry)
Plik docelowy: `assets/audio/case-004.mp3`
```
Generate a single seamless-loop ambient audio track, about 3 minutes long, stereo, MP3. A cold, tense industrial night atmosphere around a remote radio transmitter station: a very low steady electrical hum of transformers, a faint distant wind over a hill, very sparse, soft relay clicks and a subtle slow synthesised drone underneath that barely changes, an occasional distant metallic creak. No melody, no beat, no voices, no sudden loud sounds, no music hooks. The first and the last seconds must match so the track loops without an audible seam. Volume: quiet, steady background, suitable to sit under spoken dialogue.
```
""")
open(f'docs/PROMPTY_FILMY_DZWIEK_{CID}.md', 'w', encoding='utf-8').write('\n'.join(v))
print('OK', {k: len(x['lines']) for k, x in lines_out.items()})
