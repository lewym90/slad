# Wspólne funkcje bazy danych ŚLAD: sumy kontrolne i formaty identyfikatorów.
import datetime

def pesel(birth: datetime.date, serial: int, male: bool) -> str:
    """PESEL z poprawną płcią i cyfrą kontrolną. serial: 0..999."""
    y, m, d = birth.year, birth.month, birth.day
    mm = m + (20 if 2000 <= y < 2100 else 80 if y < 1900 else 0)
    s4 = serial % 1000 * 10
    # cyfra płci: nieparzysta = mężczyzna
    sex = (serial // 1000) % 5 * 2 + (1 if male else 0)
    core = f'{y % 100:02d}{mm:02d}{d:02d}{s4 // 10:03d}{sex}'
    return core + str(pesel_check(core))

def pesel_check(core10: str) -> int:
    w = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    return (10 - sum(int(c) * x for c, x in zip(core10, w)) % 10) % 10

def pesel_ok(p: str) -> bool:
    return len(p) == 11 and p.isdigit() and pesel_check(p[:10]) == int(p[10])

def pesel_birth(p: str) -> datetime.date:
    y, m, d = int(p[0:2]), int(p[2:4]), int(p[4:6])
    if m > 80: y += 1800; m -= 80
    elif m > 20: y += 2000; m -= 20
    else: y += 1900
    return datetime.date(y, m, d)

def pesel_male(p: str) -> bool:
    return int(p[9]) % 2 == 1

def nip(core9: str) -> str:
    w = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    c = sum(int(a) * b for a, b in zip(core9, w)) % 11
    if c == 10: return None
    return core9 + str(c)

def nip_ok(n: str) -> bool:
    return len(n) == 10 and n.isdigit() and nip(n[:9]) == n

KWV = {**{str(i): i for i in range(10)}, 'X': 10, 'A': 11, 'B': 12, 'C': 13, 'D': 14, 'E': 15, 'F': 16, 'G': 17, 'H': 18, 'I': 19, 'J': 20,
       'K': 21, 'L': 22, 'M': 23, 'N': 24, 'O': 25, 'P': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'W': 31, 'Y': 32, 'Z': 33}

def kw(court: str, num: int) -> str:
    body = court + f'{num:08d}'
    w = [1, 3, 7] * 4
    c = sum(KWV[ch] * x for ch, x in zip(body, w)) % 10
    return f'{court}/{num:08d}/{c}'

def kw_ok(s: str) -> bool:
    try:
        court, num, c = s.split('/')
        return len(court) == 4 and len(num) == 8 and kw(court, int(num)) == s
    except Exception:
        return False

def dowod(series: str, num5: int) -> str:
    """Numer dowodu osobistego: 3 litery + cyfra kontrolna + 5 cyfr, zapis 'ABC 123456'."""
    vals = [ord(ch) - 55 for ch in series] + [int(d) for d in f'{num5:05d}']
    w = [7, 3, 1, 7, 3, 1, 7, 3]
    c = sum(v * x for v, x in zip(vals, w)) % 10
    return f'{series} {c}{num5:05d}'

def dowod_ok(s: str) -> bool:
    try:
        series, rest = s.split(' ')
        return len(series) == 3 and len(rest) == 6 and dowod(series, int(rest[1:])) == s
    except Exception:
        return False
