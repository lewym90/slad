#!/usr/bin/env python3
"""Generuje prompty do nagrania kwestii postaci (docs/PROMPTY_GLOSY_NNN.md). Tekst kwestii pobierany 1:1 z cases/NNN.json."""
import json, re, sys
cid = sys.argv[1] if len(sys.argv) > 1 else '001'
c = json.load(open(f'cases/{cid}.json', encoding='utf-8'))

VOICE = {
 'narrator': "Mature Polish male narrator in his early 50s. Deep, warm, slightly gravelly baritone. Noir documentary style: calm, measured, low and intimate, like a seasoned detective reading a case file aloud late at night. Standard Polish pronunciation, no regional accent.",
 'helena': "Polish woman, 58, a housekeeper who has lived and worked in a small-town manor for 26 years. Warm, slightly husky alto with plain, unpretentious speech and a soft small-town warmth. Baseline state: shaken and exhausted after a sleepless night when she found her employer dead; she tends to speak a little too fast, swallows the ends of sentences and trails off.",
 'anna': "Polish woman, 32. Low, calm, controlled mezzo voice; measured and deliberate, slightly cold and guarded, every sentence sounds rehearsed. Clear diction, neutral standard Polish without regional accent. Underneath the control there is old grief she does not want to show.",
 'wiktor': "Polish man, 55, a notary. Deep, smooth, cultured baritone with precise lawyer's diction. Unhurried, polite and composed, with a faint note of condescension, as if he were explaining things to people slower than himself. Never raises his voice.",
 'marta': "Polish woman, 60, elegant and educated. Mature, refined mezzo voice with careful diction, worn down by thirteen years of grief. Restrained anger and bitterness under the sadness; her voice occasionally trembles but she does not cry openly.",
}
NAME = {'narrator': 'Narrator', 'helena': 'Helena Wolska', 'anna': 'Kinga Wolska (introduces herself as Anna Różycka)', 'wiktor': 'Wiktor Różycki', 'marta': 'Marta Różycka'}

# Kierowanie aktorskie dla każdej kwestii
DIR = {
 'brief': "Opening narration of the case. Slow, atmospheric, with short pauses between paragraphs. Slight weight on the last sentence of each paragraph. Rain-night mood, but read it cleanly — no added sound effects.",
 'h-q1': "Recounting the evening to investigators. Nervous, a bit breathless. Hesitates noticeably before 'z… z tą panią', as if unsure how to call the woman. Quotes the doctor's shouted words in a lowered, uneasy voice — she does not shout.",
 'h-q2': "Trying hard to be precise and helpful. Slight tremor. The final word 'Sama.' is added after a short pause, a little too firmly — as if she wanted to close the subject.",
 'h-q3': "Simple, factual, a little tired. Neutral tone.",
 'h-q4': "Reliving the moment she found the body. Voice tightens and gets quieter; small catch in the breath at 'oczy otwarte'. Speeds up at the end, reliving the panic.",
 'h-q5': "Evasive and uncomfortable. Short pause before 'Nie mnie to oceniać.' Ends with humble resignation.",
 'h-q6': "Painful memory about her daughter. Softer, slower. The repeated 'Ani razu' at the end is said quieter, with suppressed tears and a long breath before it.",
 'a-q1': "Calm, firm, almost cold. Each sentence lands like a verdict. Slight emphasis on 'prawdę'.",
 'a-q2': "Controlled but with irritation underneath when she quotes him ('nie będę stawiać mu warunków'). The last sentence is delivered smoothly and a little too fast — it is a rehearsed lie.",
 'a-q3': "Defensive, with dry sarcasm in the last sentence.",
 'a-q4': "Casual on the surface, too casual. A faint, warm smile in the voice on 'najlepsze racuchy', then quickly neutral again.",
 'a-q5': "Fragmented, quiet. Short pauses between the first sentences. At the ellipsis she stops abruptly, takes a breath, and the final sentence is cold and closed.",
 'w-q1': "Polished and relaxed, a touch bored, as if the question were a formality.",
 'w-q2': "Dismissive. A small contemptuous pause before 'tą osobą'. Slightly superior tone.",
 'w-q3': "Starts with cold contempt for the woman, builds a smooth insinuation. Delivers the sentence about the blow to the back of the head casually, as an aside — he does not notice he said too much. The last sentence is calm and reassuring.",
 'w-q4': "Confident, professional, reassuring. Slightly too smooth, like a prepared statement.",
 'w-q5': "Mild irritation behind politeness. The second part ('I uprzedzając pytanie…') is a bit faster and very firm.",
 'm-q1': "Torn between hope and doubt. Gentle and vulnerable at first, then a defensive edge on the question 'Czy to zbrodnia…'. The last sentence is flat and quick.",
 'm-q2': "Tired, matter-of-fact, a trace of bitterness on 'jak co noc od trzynastu lat'.",
 'm-q3': "Cold, unapologetic, quiet anger. Firm emphasis on 'Nie żałuję.'",
 'm-q4': "Grief and old resentment. Voice cracks slightly on 'mnie nie pozwolono nawet zobaczyć ciała'. Ends calmer and determined.",
 'm-q5': "Indignant and certain. 'Nigdy. Nikomu.' short and sharp. The rest is clear and factual, slightly shaky.",
 'm-q6': "Warm memory, a tiny smile in the voice about the teacher and the school row. The final question is suddenly wary.",
 'm-q7': "Tender and protective, talking about a photo she always carries. Quiet, careful, the last sentence almost a whisper.",
 'h-l1': "Caught in a lie. Starts with a defeated sigh. Speaks fast, nervously, over-explaining. Insists too hard on 'Byłam sama, przysięgam.'",
 'h-l2': "Begin with two seconds of silence (the character struggles). Then breaks down: emotional confession, voice trembling, growing intensity. 'To Kinga.' almost whispered; 'Ta kobieta to moja Kinga.' with tears in the voice. The last sentence is a desperate, protective plea.",
 'a-l1': "Caught. A short resigned exhale before 'Dobrze. Wyszłam.' Then a tense, quiet, fast account, like reliving it. Slower and lower when describing the body. The last sentence is bitter and tired.",
 'a-l2': "The mask falls. Starts quiet and steady with her real name, then the story grows heavier: controlled pain, pauses before the key moments ('widziałam z ogrodu…', 'Wtedy zobaczyłam ogień.'). Anger rises at Leon's threat. The final two sentences are defiant and honest, with a bitter edge.",
 'w-l1': "Smoothly backpedals, pretending it is a trivial detail. Light, reasonable tone, a hint of tension. 'nic ważnego' dismissive. Last sentence with false candour.",
 'w-l2': "Begin with three seconds of silence (he is composing himself). Then very cold, clipped, controlled. 'To była figura retoryczna.' said slowly and precisely. The last two sentences: icy, final, closing the conversation.",
 'w-l3': "Quick, firm, rehearsed justification. Slight contempt for Marta in 'Po prostu nie pamięta'. The final sentence is curt.",
 'w-l4': "Flustered for the first time — short hesitation after 'Wyszedłem…'. Then irritated defensiveness rising to cold indignation in the last sentence.",
 'm-l1': "Admits it with emotion: softer, remembering the call, a tremor at 'Pierwszy raz od lat płakał'. Last sentence slower, uneasy, as if she only now realises something.",
}
DEFLECT = {'helena': "Nervous, defensive, a little hurt.", 'anna': "Cool, sarcastic, unimpressed.", 'wiktor': "Polite, condescending, perfectly calm.", 'marta': "Tired, bitter, defensive."}

def clean(t):
    t = t.replace('(urywa)', '…').replace('(długa cisza) ', '').replace('(Wiktor długo milczy, potem poprawia mankiet) ', '')
    return re.sub(r'\s+', ' ', t).strip()

def prompt(fname, who, text, direction):
    return f"""Generate a single spoken-voice audio file in Polish.

FILE NAME: {fname}
FORMAT: MP3, 44.1 kHz, mono. Dry, close-miked studio voice recording. No music, no background ambience, no sound effects. About 0.3 seconds of silence at the start and at the end.

CHARACTER: {NAME[who]}
VOICE: {VOICE[who]}
If you have already generated this character's voice earlier in this conversation, reuse exactly the same voice, timbre and pitch.

PERFORMANCE: {direction}
Natural, believable acting like in a high-quality Polish radio drama — not a synthetic announcer. Correct Polish pronunciation and stress (on the penultimate syllable). Words in „quotation marks” are the character quoting someone else: mark them with a subtle change of tone, do not imitate another voice.

TEXT TO SPEAK — read it exactly as written, in Polish, word for word. Do not add, omit, translate or read any of these instructions aloud:
<<<
{text}
>>>"""

out = []
def add(title, fname, who, text, d):
    out.append((title, fname, prompt(fname, who, text, d)))

add('Narrator — wprowadzenie do sprawy', f'{cid}-narrator-brief.mp3', 'narrator', ' '.join([c['intro']['lead']] + c['intro']['brief']), DIR['brief'])
P = {p['id']: p for p in c['people']}
extra = (c.get('tableMode') or {}).get('questions', {})
for pid in ['helena', 'anna', 'wiktor', 'marta']:
    for q in P[pid]['questions'] + extra.get(pid, []):
        add(f"{NAME[pid].split(' (')[0]} — odpowiedź na: „{q['q']}”" + (' (tylko tryb Wspólny stół)' if q in extra.get(pid, []) else ''), f"{cid}-{pid}-{q['id']}.mp3", pid, clean(q['a']), DIR[q['id']])
deflects = []
for pid in ['helena', 'anna', 'wiktor', 'marta']:
    for i, t in enumerate(P[pid]['deflect'], 1):
        deflects.append((f"{NAME[pid].split(' (')[0]} — reakcja na nietrafioną konfrontację {i}", f"{cid}-{pid}-deflect-{i}.mp3", prompt(f"{cid}-{pid}-deflect-{i}.mp3", pid, t, DEFLECT[pid] + " A short reaction to being confronted with irrelevant evidence.")))
spoil = []
for pid in ['helena', 'anna', 'wiktor', 'marta']:
    for s in P[pid]['statements']:
        if s.get('response'):
            spoil.append((f"{NAME[pid].split(' (')[0]} — po udanej konfrontacji ({s['id']})", f"{cid}-{pid}-{s['id']}.mp3", prompt(f"{cid}-{pid}-{s['id']}.mp3", pid, clean(s['response']), DIR[s['id']])))

md = [f"# ŚLAD — prompty głosowe, sprawa {cid}\n", "Generuj wszystkie kwestie jednej postaci w jednej rozmowie — wtedy głos będzie spójny.\n",
      "## Część 1 — narrator i odpowiedzi na pytania (bez spoilerów)\n"]
md += [f"### {t}\n```\n{p}\n```\n" for t, f, p in out]
md += ["## Część 2 — reakcje na nietrafione konfrontacje (bez spoilerów)\n"] + [f"### {t}\n```\n{p}\n```\n" for t, f, p in deflects]
md += ["## Część 3 — UWAGA, SPOILERY: zeznania po udanej konfrontacji\nKopiuj przyciskiem, nie czytaj treści — te kwestie zdradzają rozwiązanie.\n"] + [f"### {t}\n```\n{p}\n```\n" for t, f, p in spoil]
open(f'docs/PROMPTY_GLOSY_{cid}.md', 'w', encoding='utf-8').write('\n'.join(md))
print(len(out), len(deflects), len(spoil))
