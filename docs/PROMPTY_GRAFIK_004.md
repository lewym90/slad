# ŚLAD — prompty graficzne, sprawa 004 „Martwy kanał”

Każda plansza i każdy obraz to osobny prompt — wklejaj bez zmian. Kafle w planszach są w stałej kolejności (opisanej przy każdej planszy); potnę je narzędziem `tools/cut_sheet.py` i podepnę do gry.

Obrazy nie zawierają tekstu — wszystkie napisy w grze są dodawane w interfejsie.

## Plansza A — portrety (format 3:2, np. 1536×1024)
Kolejność kafli: wiersz 1: Lasota, Kopeć, Burda; wiersz 2: Szczerba, Hajduk, Pyka.

```
A single photorealistic contact sheet: exactly 6 separate square portrait panels arranged in a strict grid of 3 columns and 2 rows, all panels identical in size, separated by uniform solid pure black gutters about 2% of the image width, black outer margin of the same width. Each panel contains exactly one person, head and shoulders, eye level, facing the camera at a slight three-quarter angle. Style for every panel: cinematic film still, 85mm lens, shallow depth of field, low-key lighting with a cold blue-teal key light and a small warm sodium-orange accent, muted desaturated colour grade, subtle 35mm film grain, realistic skin texture with pores and wrinkles, ordinary Central-European faces, not models, no glamour makeup, dark blurred modern Polish industrial or office interior in the background. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders inside the panels.
Row 1, panel 1: a 56-year-old Polish municipal crisis-management official, grey thinning hair, tired intelligent eyes behind thin rimless glasses, slightly rumpled dark blue blazer over an open-collar shirt, a lanyard with a blank plastic badge, expression of dry worry and quiet stubbornness, softly lit office with a window of night rain behind him.
Row 1, panel 2: a 49-year-old Polish service engineer, lean face, short dark hair with grey at the temples, stubble, calm closed expression, eyes that slide slightly to the side, navy company work jacket with reflective stripes, dark workshop with blurred equipment racks and a green status LED glowing behind him.
Row 1, panel 3: a 38-year-old Polish woman, a night-shift control-room operator, dark blonde hair in a messy ponytail, pale tired face, dark circles under her eyes, a headset resting around her neck, grey cardigan, blurred wall of glowing monitors behind her in a dim control room.
Row 2, panel 1: a 51-year-old Polish deputy mayor, well-groomed grey-brown hair, a confident practised half-smile, tailored charcoal suit, light blue shirt, small enamel city pin on the lapel, tidy modern city-hall corridor with a blurred glass door behind him.
Row 2, panel 2: a 33-year-old Polish woman, a local newspaper reporter, short dark bob with damp strands, sharp alert dark eyes, a trace of irony in her mouth, olive field jacket, a press lanyard with a blank card around her neck, a blurred rainy street at night with car lights behind her.
Row 2, panel 3: a 60-year-old Polish chairman of a chemical plant, heavy-set, grey crew cut, deep nasolabial folds, bloodshot eyes, an impatient hard stare, dark wool overcoat over a white shirt without a tie, blurred industrial pipes and a red warning lamp glowing behind him.
```

## Miejsca — osobne obrazy (format 3:2, 1536×1024 każdy)
Każde miejsce to osobny prompt (osobny obraz), bo na dużym ekranie plansza zbiorcza byłaby rozmyta.

### Miejsce: plik docelowy `assets/places/004-station.webp`
```
The interior of a small brick radio transmitter station at night: a tall grey equipment cabinet in the centre-left with its door open, behind a transparent safety panel a bank of copper busbars and insulators, on the cabinet front a two-position key switch with NO key in it (an empty key slot, a thin trace of white talc powder around it), rows of small status LEDs, a thick bundle of cables running to a cable duct, a very narrow dark gap between the back of the cabinet and the wall, on the right a heavy steel door with a card reader beside it, next to the door a small grey wall safe with a lead seal on its handle, bare red-brick walls, a single cold fluorescent tube overhead, clean dry scuffed concrete floor with NO footprints and no objects on it, nobody present. Photorealistic cinematic wide still, 3:2 landscape, 1536×1024, shot on a full-frame camera with a 24mm lens, deep focus, moody low-key lighting, muted desaturated colour grade with cold blue-teal tones and small warm sodium-orange accents, fine 35mm film grain, rich realistic textures and sharp detail across the whole frame, no people visible. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders anywhere in the image.
```

### Miejsce: plik docelowy `assets/places/004-czk.webp`
```
A crisis-management dispatch room at night: ONE long console desk with three large monitors showing abstract city map shapes, a desk phone, a headset on the desk, a desk lamp, a paper cup, a yellow sticky note and a notebook on the desk, an office chair slightly pushed back, a wire bin under the desk with crumpled paper, behind the desk a wall of monitors and equipment racks showing only calm green and amber status lights and NO red lights, a tall window with a drizzle on the glass, fog and the lights of a town far away, a small camera in the ceiling above the console. Photorealistic cinematic wide still, 3:2 landscape, 1536×1024, shot on a full-frame camera with a 24mm lens, deep focus, moody low-key lighting, muted desaturated colour grade with cold blue-teal tones and small warm sodium-orange accents, fine 35mm film grain, rich realistic textures and sharp detail across the whole frame, no people visible. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders anywhere in the image.
```

### Miejsce: plik docelowy `assets/places/004-chemrud.webp`
```
A chemical plant at early grey morning, cold fog and a light drizzle, wet asphalt: tall pipe racks and steel stairways, a chlorine production hall, one section of the yard cordoned off with red-and-white barrier tape, a closed valve station inside the cordon, yellow safety railings, a chain-link fence with a hazard sign shape (no readable text) in the foreground, thin pale mist hanging low over the ground, NO visible gas cloud, no smoke plume and no flashing beacon lights, quiet and deserted, the outline of a cooling tower in the haze. Photorealistic cinematic wide still, 3:2 landscape, 1536×1024, shot on a full-frame camera with a 24mm lens, deep focus, moody low-key lighting, muted desaturated colour grade with cold blue-teal tones and small warm sodium-orange accents, fine 35mm film grain, rich realistic textures and sharp detail across the whole frame, no people visible. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders anywhere in the image.
```

### Miejsce: plik docelowy `assets/places/004-hospital.webp`
```
A hospital emergency-department corridor at night: a long perspective down a glossy floor, empty gurneys parked along the left wall, an IV stand, a single white doctor's coat on a hook, a dim triage desk on the right with a computer monitor turned away from the camera, cold green-white fluorescent lights, a closed double door at the far end with a small green exit light, the floor reflecting the lights, quiet and empty. Photorealistic cinematic wide still, 3:2 landscape, 1536×1024, shot on a full-frame camera with a 24mm lens, deep focus, moody low-key lighting, muted desaturated colour grade with cold blue-teal tones and small warm sodium-orange accents, fine 35mm film grain, rich realistic textures and sharp detail across the whole frame, no people visible. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders anywhere in the image.
```

### Miejsce: plik docelowy `assets/places/004-city.webp`
```
A municipal office corridor at early grey morning: a blue carpet with a patterned border leading down the corridor, a row of closed wooden office doors with blank nameplates, the last door on the right is closed and sealed with a plain white paper police seal strip across the door frame and a short piece of red-white tape, no light coming from under it, a window with blinds at the end letting in cold dawn light, a potted plant by the wall, a state-eagle plaque on the wall without readable text, empty and silent. Photorealistic cinematic wide still, 3:2 landscape, 1536×1024, shot on a full-frame camera with a 24mm lens, deep focus, moody low-key lighting, muted desaturated colour grade with cold blue-teal tones and small warm sodium-orange accents, fine 35mm film grain, rich realistic textures and sharp detail across the whole frame, no people visible. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders anywhere in the image.
```

### Miejsce: plik docelowy `assets/places/004-parking.webp`
```
A forest gravel car park at early grey morning in thick fog with a light drizzle, wet gravel with a few puddles: exactly ONE dark grey Skoda Octavia liftback parked alone at the far edge near the trees, right beside it an EMPTY parking bay where in the damp gravel two sets of boot prints (one large, one small) are visible, in the foreground a trail camera strapped to a pine trunk, a wooden bollard with two paper takeaway coffee cups from a petrol station and a plain empty white envelope lying on top of it, tall dark pines fading into fog, no street lamps, no other vehicles. Photorealistic cinematic wide still, 3:2 landscape, 1536×1024, shot on a full-frame camera with a 24mm lens, deep focus, moody low-key lighting, muted desaturated colour grade with cold blue-teal tones and small warm sodium-orange accents, fine 35mm film grain, rich realistic textures and sharp detail across the whole frame, no people visible. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders anywhere in the image.
```

### Miejsce: plik docelowy `assets/places/004-newsroom.webp`
```
A small local-newspaper office open space above a print shop at night: two cluttered desks under a large rainy window, stacks of old newspapers, an old typewriter shape on a shelf, a cork board covered with pinned printed photographs and papers (no readable text), a desk lamp switched on casting a warm pool of light on one desk with a computer monitor, binders on shelves, an office chair, rain running down the glass with orange streetlights outside. Photorealistic cinematic wide still, 3:2 landscape, 1536×1024, shot on a full-frame camera with a 24mm lens, deep focus, moody low-key lighting, muted desaturated colour grade with cold blue-teal tones and small warm sodium-orange accents, fine 35mm film grain, rich realistic textures and sharp detail across the whole frame, no people visible. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders anywhere in the image.
```

### Miejsce: plik docelowy `assets/places/004-syreon.webp`
```
A service company's garage and workshop in the early morning: a large white high-roof Fiat Ducato-style panel van with a roof rack carrying an aluminium ladder parked in the centre, damp mud splashes on its lower body from a wet gravel road, parked with its rear doors closed, behind it shelves with cable drums, plastic crates and spare parts, a wall board with tools, an open red tool trolley in front, harsh fluorescent light with cold daylight coming through a half-open roller door, concrete floor with wet tyre marks near the door, no readable text or logos on the van. Photorealistic cinematic wide still, 3:2 landscape, 1536×1024, shot on a full-frame camera with a 24mm lens, deep focus, moody low-key lighting, muted desaturated colour grade with cold blue-teal tones and small warm sodium-orange accents, fine 35mm film grain, rich realistic textures and sharp detail across the whole frame, no people visible. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders anywhere in the image.
```

## Plansza C — dowody i rekwizyty (format 1:1, np. 1024×1024)
Kolejność kafli: wiersz 1: klucz dynamometryczny, zegarek, przełącznik kluczykowy; wiersz 2: atrapa anteny, żółta karteczka, skrzynka narzędziowa; wiersz 3: sejf, telefon, pendrive.

```
A single photorealistic evidence contact sheet: exactly 9 separate square panels arranged in a strict grid of 3 columns and 3 rows, all panels identical in size, separated by uniform solid pure black gutters about 2% of the image width, black outer margin of the same width. Each panel is a forensic-style close-up still life of one object, lit by a single hard flashlight-like key light from above at an angle, deep black falloff, muted desaturated colours, subtle film grain, macro detail. No people, no hands, no gore. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders inside the panels.
Row 1: (1) a heavy steel adjustable torque wrench, about 50 cm long, scuffed and worn, a dull rust-brown dried stain in the groove of the head, lying on a bare concrete floor; (2) a black smartwatch with a cracked screen and a torn strap lying on a grey concrete floor, the screen dark; (3) a close-up of an industrial key switch with two positions on a grey metal panel, the key missing, a thin trace of white talc powder around the switch.
Row 2: (4) a cylindrical metal RF dummy load terminator with a coaxial connector, connected to a thick coaxial cable inside a cabinet, cool teal light; (5) two torn halves of a yellow sticky note lying on a white plastic waste-bin liner, handwritten pencil scribble on the pieces, illegible; (6) an open grey service-van toolbox, one empty shaped cut-out in black foam where a large wrench belongs, next to a crumpled pair of blue latex gloves.
Row 3: (7) a small grey wall safe with a four-digit mechanical dial lock, standing half hidden behind a wooden cabinet; (8) a smartphone without a lock screen lying face up on a dark pocket lining, the screen showing only blurred soft notification shapes; (9) a small black USB flash drive on a plain notebook page, a ring of coffee stain beside it.
```

## Poprawka rekwizytu — sejf (format 3:2, 1536×1024)
Plik docelowy: `assets/evidence/004-safe.webp` (zastępuje kafel 7 z planszy C).

```
A forensic-style close-up still life, 3:2 landscape, 1536×1024: a small grey wall safe standing half hidden behind a wooden cabinet in an office, its door closed, on the door a mechanical combination lock with exactly FOUR numbered dials in a row (four separate rotating wheels), lit by a single hard flashlight-like key light from above at an angle, deep black falloff, muted desaturated colours, subtle film grain, macro detail. No people, no hands. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders.
```

## Obraz D — okładka sprawy (format 16:9, np. 1536×864)
Plik docelowy: `assets/cases/004-cover.webp` (kadruję do 900×520, więc główny motyw trzymaj na środku).

```
A single photorealistic cinematic wide establishing shot, 16:9: a tall lattice radio mast on a fog-covered hill at night, a small brick transmitter station at its foot with one lit window, a row of silent loudspeaker sirens on the mast frame and a faint red aviation warning light blinking at the top, in the valley far below a sleepy industrial town with orange street lights and a faint pale green haze drifting from a chemical plant on the horizon, thick cold mist, muted desaturated colour grade with deep blue-teal shadows and small warm sodium accents, subtle 35mm film grain, atmospheric, ominous, quiet. The main subject — the mast and the station — is centred. No people, no vehicles. Absolutely no text, letters, numbers, captions, logos, watermarks, frames or borders.
```

## Obraz E — grafika tytułowa sprawy (format 16:9, np. 1536×864)
Plik docelowy: `assets/art/004-keyart.webp`.

```
A single photorealistic cinematic wide interior shot, 16:9: a crisis-management control room at night seen from behind the console, an empty operator chair, three big monitors glowing cold blue with abstract map shapes and a row of small red dots, a wall-sized map of a town with a ring of numbered-less speaker symbols that all remain unlit, a tall window showing in the distance a lattice radio mast on a foggy hill with a blinking red light, a paper cup of cold coffee and a yellow sticky note on the desk, cold teal light with a few warm orange accents, shallow depth of field, subtle 35mm film grain, quiet and tense. No people. Absolutely no readable text, letters, numbers, captions, logos, watermarks, frames or borders.
```
