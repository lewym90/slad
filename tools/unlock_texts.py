"""Komunikaty „przełomu” przy odblokowaniu miejsc (spot.requires.all). Wołane przez buildy przed zapisem JSON."""
SYR = ('Nakaz dla Syreonu', 'Prokurator wydał nakaz przeszukania w Syreon Polska: rejestr kart i kluczy, firmowy bus, wykaz narzędzi i archiwum zamówień.')
RED = ('Nakaz dla redakcji', 'Prokurator wydał nakaz: redakcja „Głosu Rudy” musi wydać notatki reporterki i udostępnić jej skrzynkę pocztową.')
T = {
 '003': {'sp-wardrobe': ('Nakaz przeszukania', 'Prokurator wydał nakaz przeszukania stróżówki. Szafę Zenona Kubika można teraz otworzyć.')},
 '004': {'sp-vice': ('Nakaz przeszukania gabinetu', 'Prokurator uznał, że zeznania wiceprezydenta nie trzymają się dokumentów, i wydał nakaz przeszukania jego gabinetu w Urzędzie Miasta.'),
         'sp-notes': RED, 'sp-mail': RED, 'sp-reg': SYR, 'sp-van': SYR, 'sp-tw': SYR, 'sp-orders': SYR},
 '005': {'sp-wardrobe': ('Powód, by sprawdzić szafę', 'Macie już konkretny powód, żeby dokładnie obejrzeć szafę wnękową w pokoju 214.'),
         'sp-car': ('Zgoda na przeszukanie samochodu', 'Prokurator zgodził się na przeszukanie samochodu Iwony Kraski na parkingu za hotelem.')},
 '006': {'sp-coat': ('Zgoda na zabezpieczenie płaszcza', 'Prokurator zgodził się zabezpieczyć płaszcz kierowniczki kina z wieszaka w jej biurze.')},
 '007': {'sp-laptop': ('Wiecie, czego szukać', 'Wiecie już, czego szukać na laptopie wyprawy w jadalni. Możecie go przejrzeć.'),
         'sp-room': ('Zgoda na przeszukanie pokoju', 'Prokurator zgodził się na przeszukanie pokoju nr 6.'),
         'sp-phone': ('Zgoda na przeszukanie telefonu', 'Prokurator zgodził się na przeszukanie telefonu Weroniki.')},
}
def apply(case):
    m = T.get(case['id'], {})
    for l in case['locations']:
        for s in l.get('spots', []):
            if s['id'] in m: s['unlockTitle'], s['unlockText'] = m[s['id']]
    return case
if __name__ == '__main__':
    import json, os, sys
    for cid in sys.argv[1:]:
        p = os.path.join(os.path.dirname(__file__), '..', 'cases', cid + '.json'); c = json.load(open(p))
        json.dump(apply(c), open(p, 'w'), ensure_ascii=False, indent=1); print(cid)
