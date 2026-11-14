#!/usr/bin/env python3
"""Generuje docs/PROMPTY_*_007.md oraz tools/voice/007-lines.json. Tekst kwestii pobierany 1:1 z cases/007.json.
Głosy od razu w krótkich nagraniach (maks. 5 kwestii i ok. 120 słów) — generator gubi kwestie w długich plikach.
Użycie (z katalogu repo): python3 tools/prompts_007.py"""
import json, re, os
c = json.load(open('cases/007.json', encoding='utf-8'))
CID = '007'
SPOKEN = [
 ('Sobota, 16 stycznia, 8:00.', 'Sobota, szesnastego stycznia, godzina ósma.'), ('1220 m n.p.m.', 'tysiąc dwieście dwadzieścia metrów nad poziomem morza.'),
 ('„Północ 2028”', '„Północ dwa tysiące dwadzieścia osiem”'), ('od 2019 roku', 'od dwa tysiące dziewiętnastego roku'), ('O 22:05', 'O dwudziestej drugiej pięć'),
 ('O 7:10', 'O siódmej dziesięć'), ('GOPR', 'Gopr'), ('w 2025 roku', 'w dwa tysiące dwudziestym piątym roku'), ('Grenlandię 2028', 'Grenlandię dwa tysiące dwadzieścia osiem'),
 ('SMS-a', 'esemesa'), ('z 2025 roku', 'z dwa tysiące dwudziestego piątego roku'), ('od kwietnia 2025', 'od kwietnia dwa tysiące dwudziestego piątego'),
 ('C0112', 'ce zero sto dwanaście'), ('GPS', 'dżipiees'),
]
def clean(t):
    t = re.sub(r'\s*\([^)]*\)\s*', ' ', t).strip()
    for a, b in SPOKEN: t = t.replace(a, b)
    t = re.sub(r'\s{2,}', ' ', t).replace('...', '…')
    return re.sub(r'(^|[.?!] )([a-ząćęłńóśźż])', lambda m: m.group(1) + m.group(2).upper(), t)

VOICE = {
 'narrator': "Mature Polish male narrator in his early 50s. Deep, warm, slightly gravelly baritone, noir documentary style: calm, measured, low and intimate, like a seasoned detective reading a case file at night. If you generated this narrator for an earlier case, reuse exactly the same voice.",
 'adam': "Adam Rogala, Polish man, 47, a famous polar explorer. Confident, smooth, media-trained baritone, a little theatrical, used to interviews; offended when questioned; when he finally admits the fraud — quiet, broken, ashamed, slow.",
 'weronika': "Weronika Kos, Polish woman, 41, marketing manager of a sponsor company. Quick, polite, corporate mezzo, always in control, slightly too smooth when lying; when cornered — quieter, clipped; in her final admissions breathless, shaky, frightened and guilty, but never hysterical, never crying loudly.",
 'igor': "Igor Szadkowski, Polish man, 29, a documentary camera operator. Light, lively tenor, casual modern speech, jokes when nervous; embarrassed and sheepish when caught; genuinely shocked when he recognises his own recording.",
 'natalia': "Natalia Brandt, Polish woman, 36, an expedition doctor. Calm, low, precise voice of a physician, short sentences; defensive and tense about her private life; quiet and resigned when she admits it.",
 'hampel': "Zdzisław Hampel, Polish man, 63, keeper of an old mountain hut. Hearty, gruff, warm bass, unhurried, homely; says „panie władzo”; affectionate when he talks about his old dog.",
 'kuznik': "Mirosław Kuźnik, Polish man, 52, a snow-groomer operator. Blunt, slow, husky baritone, simple plain speech, a man of few words.",
 'krystian': "Krystian Lis, Polish man, 38, an expedition radio operator. Calm, clear, professional radio voice, slightly hoarse from frost, relaxed and routine — a man making an ordinary night radio check in a cold stone hut.",
}
NAME = {'adam': 'Adam Rogala', 'weronika': 'Weronika Kos', 'igor': 'Igor Szadkowski', 'natalia': 'Natalia Brandt', 'hampel': 'Zdzisław Hampel', 'kuznik': 'Mirosław Kuźnik'}
KIND = {'q': 'answer to a question', 'break': 'admits after being confronted with evidence', 'show': 'reaction to evidence shown', 'deflect': 'curt, evasive reply', 'showdef': 'short, indifferent reply',
        'mam': 'a single quiet, casual word said to himself off-camera, as when he stops recording'}
QV = "Quality: the best available — ideally WAV 48 kHz, 24-bit, mono. Dry, clean studio voice. No music, no background, no sound effects."

lines_out, voice_blocks = {}, []
for who in ['adam', 'weronika', 'igor', 'natalia', 'hampel', 'kuznik']:
    p = next(x for x in c['people'] if x['id'] == who)
    L = [{'id': q['id'], 'kind': 'q', 'text': q['a']} for q in p['questions']]
    L += [{'id': s['id'], 'kind': 'break', 'text': s['response']} for s in p['statements'] if s.get('response')]
    L += [{'id': x['id'], 'kind': 'show', 'text': x['a']} for x in p.get('shows', [])]
    L += [{'id': f'deflect-{i}', 'kind': 'deflect', 'text': d} for i, d in enumerate(p.get('deflect', []))]
    L += [{'id': f'show-{i}', 'kind': 'showdef', 'text': d} for i, d in enumerate(p.get('showDefault', []))]
    if who == 'igor': L.append({'id': 'mam', 'kind': 'mam', 'text': 'Mam.'})
    for i, x in enumerate(L, 1): x['n'] = i; x['spoken'] = clean(x['text'])
    for x in L: assert not re.search(r'\d|[A-Z]{2,}', x['spoken']), (who, x['id'], x['spoken'])
    parts, cur, wc = [], [], 0
    for x in L:
        w = len(x['spoken'].split())
        if cur and (len(cur) >= 5 or wc + w > 120): parts.append(cur); cur, wc = [], 0
        cur.append(x); wc += w
    if cur: parts.append(cur)
    lines_out[f'{CID}-{who}'] = {'name': p['name'], 'parts': [{'file': f'{CID}-{who}-{i}.wav', 'n': len(P)} for i, P in enumerate(parts, 1)], 'lines': L}
    for i, P in enumerate(parts, 1):
        deliv = '; '.join(f"line {k} — {KIND[x['kind']]}" for k, x in enumerate(P, 1))
        voice_blocks.append(f"""Polish voice recording — one audio file: {CID}-{who}-{i}.wav
{QV}
Voice: {VOICE[who]} Natural radio-drama acting in standard Polish, correct stress.
{f'Task: read ALL {len(P)} lines below in Polish, word for word, in this order. After every line stop and leave 3 full seconds of total silence. Never skip, shorten, merge or rephrase a line. Do not read these instructions.' if len(P) > 1 else 'Task: read the line below in Polish, word for word, once. Do not read these instructions.'}
Delivery: {deliv}.

""" + '\n\n'.join(x['spoken'] for x in P))
brief = clean(' '.join([c['intro']['lead']] + c['intro']['brief']))
assert not re.search(r'\d', brief), brief
narr = f"""Polish voice recording — one audio file: {CID}-narrator-brief.wav
{QV}
Voice: {VOICE['narrator']} Natural, believable, standard Polish, correct stress.
Delivery: opening narration of a case. Slow and atmospheric, short pauses between paragraphs. Mood: a windy January morning in a snowbound mountain hut after a death on the ridge — quiet, cold, tense. The last paragraph is a short practical note, read lighter.
Task: read the whole text below in Polish, word for word. Do not read these instructions.

{brief}"""
CALL = clean(next(e for e in c['evidence'] if e['id'] == 'e08')['body'][1]['quote'])
krys = f"""Polish voice recording — one audio file: {CID}-krystian-call.wav
{QV}
Voice: {VOICE['krystian']} Natural, believable, standard Polish, correct stress.
Delivery: a routine night radio check-in, spoken towards a handheld microphone, unhurried, calm, a short breath before the first word; a tiny pause after „Baza, tu Mglista.” and before „Bez odbioru.”. Total length about 9–10 seconds.
Task: read the line below in Polish, word for word, once. Do not read these instructions.

{CALL}"""
lines_out[f'{CID}-krystian'] = {'name': 'Krystian Lis', 'parts': [{'file': f'{CID}-krystian-call.wav', 'n': 1}], 'lines': [{'id': 'call', 'kind': 'call', 'text': CALL, 'n': 1, 'spoken': CALL}]}
json.dump(lines_out, open(f'tools/voice/{CID}-lines.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

AQ = "Format: the highest audio quality available — preferably uncompressed WAV, 48 kHz, 24-bit (if WAV is not possible: the highest-bitrate file available)."
sounds = [
 f"""Generate a single ambient soundscape for a detective game, about 3 minutes long, stereo. {AQ}
The place: an old wooden-and-stone mountain hut high in the Karkonosze mountains on a windy January morning, heard from inside the dining room.
— underneath everything: the quiet room tone of a wooden interior and a steady, strong wind outside, rising and falling, whistling softly in the window frames;
— close by: a wood fire crackling in a big stone fireplace, a log settling now and then;
— occasional small sounds: old floorboards and timber creaking, a mug set down on a wooden table far away, a door closing softly somewhere upstairs, a big old dog sighing and shifting on the floor;
— twice over the whole track, very far away, the low engine of a snow groomer passing below the hut and fading out;
— a very low, slow, cold synth pad, barely noticeable.
No melody, no beat, no voices, no speech, no sudden loud sounds. Cold, lonely, tense. Comfortable level for long background listening. The end must blend smoothly into the beginning so the track can loop.""",
 f"""Generate a single ambient soundscape for a detective game, about 3 minutes long, stereo. {AQ}
The place: the same old mountain hut in the Karkonosze mountains, now in a heavy blizzard, heard from inside.
— a powerful snowstorm outside: deep howling wind in long waves, violent gusts that hit the walls and windows, the constant hiss of snow driven against the glass;
— a wooden shutter rattling now and then, the timber of the building groaning under the wind, a chimney moaning;
— inside, quietly: a wood fire crackling in the fireplace and the old building creaking;
— a very low, dark, slow synth drone, barely noticeable.
No melody, no beat, no voices, no speech, no thunder. Oppressive but not chaotic, comfortable for long background listening. The end must blend smoothly into the beginning so the track can loop.""",
 krys,
 f"""Generate a single short sound-effect recording: {CID}-sfx-dog.wav. {AQ} Mono, dry, no music.
A big old shepherd dog barks exactly twice, short and deep — „woof, woof” — close to the microphone, in a wooden hallway right by an open back door. Half a second of silence before the first bark, about half a second between the barks, then two seconds of silence. No other sounds, no growling, no people.""",
 f"""Generate a single sound-effect recording: {CID}-sfx-wind.wav, about 30 seconds long. {AQ} Mono.
Strong mountain wind at night, recorded outdoors right next to the back door of a mountain hut: a steady roar with natural gusts that swell and fade, snow hissing along the wall. No other sounds — no voices, no animals, no engines, no music.""",
 f"""Generate a single sound-effect recording: {CID}-sfx-stove.wav, about 30 seconds long. {AQ} Mono.
A small cast-iron wood stove burning inside a tiny stone mountain hut, recorded close: gentle continuous crackling of burning wood with a few clearly distinct, sharp pops, quiet room tone of a small stone room. No wind, no voices, no other sounds, no music.""",
 narr,
] + voice_blocks

PIC = " Maximum quality: ultra-detailed, tack-sharp, crisp micro-detail and textures that hold up on a very large 4K/8K television screen, no blur, no softness, no smudged or painterly areas, no compression artefacts, no AI artefacts (no extra fingers, no melted objects, no warped lines), clean straight architectural lines. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders anywhere in the image."
LOOK = "24mm lens, deep focus, everything sharp from foreground to background, realistic textures, muted desaturated colour grade with cool blue-grey shadows and warm accents, fine film grain, no people."
DAY = "Time: Saturday morning in mid-January, overcast, strong wind, fresh snow everywhere."
G = [
 f"""A single photorealistic contact sheet, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): exactly 6 separate portrait panels with a 4:5 vertical aspect, in a strict grid of 3 columns and 2 rows, all panels identical in size, separated by uniform solid pure black gutters. Each panel is a waist-up portrait of a different person looking near the camera. Style for every panel: cinematic film still, 85mm lens, shallow depth of field, soft cool daylight from a snowy window with a small warm tungsten accent, muted desaturated colour grade, subtle film grain, realistic skin texture with pores and wrinkles, ordinary Central-European faces, not models, no glamour. All clothing is plain, with no logos or lettering.
Row 1, panel 1: a tall 47-year-old Polish man, a famous polar explorer, weathered wind-burned face, short greying beard, the tip of his nose slightly discoloured by an old frostbite, confident practised expression, a red technical down jacket, blurred wooden mountain-hut dining room behind him.
Row 1, panel 2: a slim 41-year-old Polish woman, a corporate marketing manager, dark-blonde hair in a neat ponytail, careful makeup that does not hide dark circles under her eyes, a white down jacket, a smartphone held in both hands, polite but tense smile, blurred wooden hut corridor behind her.
Row 1, panel 3: a thin 29-year-old Polish man, a documentary camera operator, scruffy light beard, a knitted beanie with a pompom, a camera on a strap around his neck, an uneasy, apologetic grin, blurred snowy wooden terrace behind him.
Row 2, panel 1: a 36-year-old Polish woman, an expedition doctor, dark hair pulled back into a tight bun, no makeup, a dark grey fleece, calm serious face, slightly guarded eyes, blurred plain hut room behind her.
Row 2, panel 2: a stocky 63-year-old Polish man, keeper of a mountain hut, round ruddy face, grey moustache, a knitted wool sweater with a reindeer pattern, an unlit wooden pipe in his hand, the head of a big shaggy grey-and-white sheepdog at the bottom edge of the frame, blurred hut kitchen behind him.
Row 2, panel 3: a broad 52-year-old Polish man, a snow-groomer operator, bushy brush moustache, a woolly cap, grease-stained work overalls, blunt tired expression, blurred metal garage with a red snow groomer behind him.""",
 f"""A single photorealistic evidence contact sheet, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): exactly 6 separate square panels in a strict grid of 3 columns and 2 rows, all identical in size, separated by uniform solid pure black gutters. Each panel is a forensic-style close-up photo, sharp, realistic, muted cold colours, soft directional light, no people's faces.
Row 1: (1) an open cast-iron stove ash pan full of grey wood ash; in the ash a small melted lump of bright orange plastic with a small aluminium carabiner fused into it and a charred fragment of a green circuit board; (2) the sharp corner of an old black cast-iron stove top inside a stone hut, with a small dark dried brownish smear and a few short dark hairs on the edge, wiped carelessly; below it a stained rag stuffed into a metal coal bucket — restrained, not gory; (3) a grainy high-angle night photograph taken from a first-floor wooden terrace: below, in the cone of light from a single lamp above a door in a snowy wall, a person seen from behind walking towards the door with a pair of skis on one shoulder and a small backpack with a bright strip of yellow reflective tape along the shoulder straps; face not visible; snowflakes streaking; digital noise.
Row 2: (4) the steel rungs of a ladder bolted to a grey rock, completely covered with thick feathers of white rime ice, untouched, the base of a thin antenna mast above; (5) a wooden ski rack in a warm drying room: one pair of climbing skins stiff and glistening with ice, frozen lumps of snow on the ski edges and bindings, beside other skins that hang dry and fluffy; (6) at the foot of a snow-covered four-metre rock with a steel ladder and an antenna mast, a human-sized shape completely covered by a gold-and-silver emergency foil blanket, partly drifted with snow, red-and-white barrier tape in the foreground — no body parts visible.""",
 f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): the small office of an old mountain hut keeper: a wooden desk with an old cash register and papers, a wall cabinet with hanging keys, a small window with snow outside; on a shelf a black VHF radio base station with a coiled handset and a small digital recorder beside it; next to it a multi-slot charger holding two handheld radios with short antennas; an open door to a dim corridor. {DAY} {LOOK}""",
 f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): the hot, steamy drying room of an old mountain hut, seen from the doorway. Strict layout: on the LEFT third a wooden ski rack with five pairs of touring skis and one splitboard standing upright, climbing skins hanging over the rail; in the CENTRE background a wooden back door with a small frosted window; on the RIGHT side of the floor, against the wall, four large expedition backpacks and one small ski-touring backpack with a bright yellow reflective strip along its straps; in the far RIGHT corner a black cast-iron wood stove with its ash pan slightly open; boots and gloves on wall pegs; warm tungsten light, steam. {DAY} {LOOK}""",
 f"""A single photorealistic cinematic exterior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): a first-floor wooden terrace of a mountain hut, covered in fresh snow; on a tripod at the railing a camera wearing a thick cap of snow, pointed down at a snowy hiking trail marked with green paint stripes on posts that climbs into dwarf spruce towards the mountains; below the terrace a lamp above a back door. {DAY} {LOOK}""",
 f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): the dining room of an old wooden mountain hut: long dark wooden tables and benches, a big stone fireplace with a fire, old framed expedition photographs on the timber walls, a corner table with an open laptop and two external hard drives, a deck of playing cards and three mugs left on a table, small windows with snow and wind outside. {DAY} {LOOK}""",
 f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): a small plain bedroom in a mountain hut: a single bed, neatly made, the pillow without a dent; under the window a radiator with wool ski socks and ski-boot liners drying on it; a small bedside table with a blister pack of two white tablets and an unopened bottle of water; snowy window light. {DAY} {LOOK}""",
 f"""A single photorealistic cinematic exterior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): a trail junction in the Karkonosze mountains among wind-bent dwarf spruce: a wooden signpost covered in thick rime ice (its boards unreadable), a line of tall wooden marker poles disappearing into mist on the left, and a narrow, steep snowy gully rising above on the right; wind blowing powder snow; grey sky. {DAY} {LOOK}""",
 f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): inside an old one-room stone mountain shelter built in 1936, seen from the door. Strict layout: on the LEFT a black cast-iron wood stove next to wooden bunks, a metal coal bucket beside it; in the CENTRE under a small frost-covered window a wooden table; on the table, clearly separated: in the upper middle a black VHF radio station with its handset on a hook, in the middle an open squared notebook with a pencil, to the LEFT of the notebook a knitted cap and a pair of thick gloves, to the RIGHT of the notebook a small grey electronic temperature logger with a tiny display next to a stack of batteries; on the RIGHT a lower bunk with a powerbank and a dangling charging cable with nothing attached, and at the far RIGHT a large expedition backpack leaning against the bunk; cold grey light, frost on the walls. {DAY} {LOOK}""",
 f"""A single photorealistic cinematic exterior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): a high mountain pass in the Karkonosze: an old low stone shelter on the right, and in the centre a four-metre grey rock with a steel ladder bolted to it and a thin radio antenna mast on top; at the foot of the rock a shape under a gold-and-silver emergency foil blanket and red-and-white barrier tape; far away by the shelter door a mountain rescuer in a red jacket, small, seen from behind; wind blowing snow across the ridge. {DAY} 24mm lens, deep focus, muted desaturated colour grade with cool blue-grey shadows, fine film grain.""",
 f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): a corrugated-metal garage below a mountain hut: two red snow groomers with wide tracks, fuel barrels, tools on the wall, a plywood partition with a small door to an operator's room, the cab door of one groomer open with a sheet of paper lying on the driver's seat; cold daylight from the open gate, snow outside. {DAY} {LOOK}""",
 f"""A single photorealistic cinematic interior, 3:2 landscape at the highest resolution you can generate — ideally 6144×4096, at minimum 3840×2560 (4K): a small room in a mountain hut turned into an investigators' office: a wooden table covered with case files, folders, a hiking map and photographs, a thermos and enamel mugs, a desk lamp, a window with blizzard light. {DAY} {LOOK}""",
 f"""A single photorealistic cinematic establishing shot, 16:9 at the highest resolution you can generate — ideally 7680×4320 (8K), at minimum 3840×2160 (4K): night on a high, wind-swept mountain pass in the Karkonosze: a small old stone shelter with one faintly glowing window, beside it a rock with a thin antenna mast, snow streaming across the ridge in the wind; far below on the dark slope a single tiny headlamp light. Cold blue moonlight through clouds, a small warm accent from the window, deep shadows, cinematic, lonely and ominous. No people visible except the tiny distant light.""",
]
G = [x + PIC for x in G]
GNAMES = ['Plansza A — portrety (potnę na 6)', 'Plansza B — dowody (potnę na 6)', 'Biuro gospodarza', 'Suszarnia', 'Taras', 'Jadalnia', 'Pokój nr 6', 'Rozdroże pod Jaworem',
          'Wnętrze schronu', 'Skała z masztem', 'Garaż ratraków', 'Kwatera śledczych', 'Grafika tytułowa']
VID = "Format: 16:9 at the highest resolution and quality available — ideally 3840×2160 (4K), at minimum 1920×1080 — highest bitrate, 24 fps, about 8 seconds, no sound, no text, no letters, no numbers, no logos, no faces visible. Photorealistic cinematic style, muted desaturated colour grade, cold blue-grey tones with a small warm accent, fine film grain. Maximum quality: crisp, stable, artefact-free footage, no warping, no morphing objects, smooth natural motion, sharp enough for a very large 4K television."
V = [
 f"A seamless looping shot: a very slow, smooth push towards a small old stone shelter on a dark, wind-swept mountain pass at night; one small window glows faintly warm; beside the shelter a thin antenna mast on a rock; powder snow streams steadily across the frame in the wind. The last frame must match the first so the clip loops. {VID}",
 f"Close-up in a dark mountain-hut office at night: a black VHF radio base station on a shelf; its small display glows green, a red transmit light flickers on and off for a few seconds, the coiled handset lies still beside it; shadows of snowflakes from the window drift across the wall. No people. {VID}",
 f"Night in the mountains: seen from far away, a single headlamp moves steadily up a snowy slope between dwarf spruces, leaving a faint double ski track behind; wind blows snow across the beam; the figure is only a dark silhouette, too far to see any face. {VID}",
 f"Night, blizzard: the heavy wooden door of an old stone mountain shelter swings slowly open from inside, warm light spills out onto the snow and snow swirls in through the doorway; nobody is visible in the doorway. {VID}",
 f"Blue hour before dawn on a high mountain pass after a storm: total silence and stillness, a snow-covered rock with a steel ladder and a thin antenna mast, fine snow drifting slowly along the ground; a very slow push-in. No people, no blankets, no tape. {VID}",
]
VNAMES = ['007-intro.mp4', '007-bt-voice.mp4', '007-bt-skis.mp4', '007-bt-window.mp4', '007-bt-cold.mp4']
os.makedirs('docs', exist_ok=True)
open(f'docs/PROMPTY_{CID}.md', 'w', encoding='utf-8').write('\n'.join(
  [f"# ŚLAD — prompty mediów, sprawa {CID} „{c['title']}”\n", '**UWAGA, SPOILERY.** Kopiuj przyciskiem kopiowania, nie czytaj treści.\n', '## GRAFIKI\n']
  + [f"### {i}\n```\n{b}\n```\n" for i, b in enumerate(G, 1)] + ['## VIDEO\n'] + [f"### {i}\n```\n{b}\n```\n" for i, b in enumerate(V, 1)]
  + ['## DŹWIĘK\n'] + [f"### {i}\n```\n{b}\n```\n" for i, b in enumerate(sounds, 1)]))
json.dump({'graphics': GNAMES, 'videos': VNAMES, 'sounds': ['ambient', 'ambient-storm', 'krystian-call', 'sfx-dog', 'sfx-wind', 'sfx-stove', 'narrator-brief'] + [f"{k}-{p['file']}" for k, v in lines_out.items() if k != f'{CID}-krystian' for p in v['parts']]},
          open(f'tools/voice/{CID}-media-order.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('grafiki', len(G), 'filmy', len(V), 'dźwięki', len(sounds), {k: len(v['parts']) for k, v in lines_out.items()})
