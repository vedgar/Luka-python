def filestarter():
    igrači = {Čovjek('Veky'), PametniKomp('Komp')}
    return vars()

import pygame as G, types, random, itertools, enum, string, pathlib, os
import contextlib, operator, collections

assert G.init() == (6, 0)
pad, width, quad = 5, 1, 150
side = pad*2 + quad + width
field = pad * 6 + width * 2 + quad * 3
brojke = string.digits[1:]
pobjede = set(map(frozenset, '123 456 789 147 258 369 159 357'.split()))
header = 50
head_rect = G.Rect(0, 0, field, header)
ekran = G.display.set_mode([field, field + header])
printer = G.font.Font(G.font.match_font('lucidabright'), 96)

def učitaj_zvuk(filename):
    filepath = pathlib.Path(__file__).parent / filename
    return G.mixer.Sound(file=filepath.open('rb'))

# zvuk_pobjeda = učitaj_zvuk('Metroid_Door-Brandino.wav')
# zvuk_neriješeno = učitaj_zvuk('ok.wav')

class Igrač(types.SimpleNamespace):
    def __init__(self, ime=None):
        self.ime = ime or type(self).__name__
        self.bodovi = 0
        self.stavljeno = set()
    __hash__ = object.__hash__
    __eq__ = object.__eq__

class Čovjek(Igrač):
    @staticmethod
    def potez(slobodno):
        G.display.flip()
        for događaj in itertools.chain.from_iterable(iter(G.event.get, None)):
            if događaj.type == G.KEYDOWN:
                if događaj.key == G.K_ESCAPE:
                    G.quit()
                    for igrač in sorted(igrači, reverse=True,
                                        key=operator.attrgetter('bodovi')):
                        print(igrač.ime.rjust(10), igrač.bodovi, '\t',
                              igrač.simbol*igrač.bodovi)
                    raise SystemExit
                znak = događaj.unicode
                if znak.isdigit():
                    broj = int(znak)
                    if broj in slobodno:
                        return broj

class Komp(Igrač):
    @staticmethod
    def potez(slobodno):
        return random.choice(list(slobodno))

class PametniKomp(Komp):
    def potez(self, slobodno):
        spriječi = None
        for linija in pobjede:
            rezultat = ja, protivnik, prazno = self.statistika(linija)
            if len(prazno) == 1 and 2 in map(len, rezultat):
                return int(prazno.pop())
        return super().potez(slobodno)
            
    def statistika(self, linija):
        ja, protivnik, prazno = (set() for _ in range(3))
        for polje in linija:
            if polje in self.stavljeno: meta = ja
            elif polje in self.protivnik.stavljeno: meta = protivnik
            else: meta = prazno
            meta.add(polje)
        return ja, protivnik, prazno


class Boja:
    crna = G.Color('black')
    bijela = G.Color('white')
    zelena = G.Color('green')
    pozadina = G.Color('#4cd9cb')
    brojke = G.Color('#6c9133')
    siva = G.Color('gray')
    crvena = G.Color('red')

def stavi(i, j, znak, boja):
    rect = G.Rect(side*j + pad, side*(2 - i) + pad + header, quad, quad)
    otisak = printer.render(str(znak), True, boja)
    ekran.fill(Boja.pozadina, rect)
    ekran.blit(otisak, otisak.get_rect(center=rect.center))
    G.display.flip()

def print_head(boja=Boja.crna, naredu=None):
    ekran.fill(Boja.siva, head_rect)
    if naredu:
        ekran.fill(Boja.pozadina, nrp[naredu.simbol])
    lijevi, desni = igrači
    s = lijevi.ime + lijevi.simbol.join('()') + str(lijevi.bodovi) + ':' \
        + str(desni.bodovi) + desni.simbol.join('()') + desni.ime
    head_printer = G.font.Font(G.font.match_font('couriernew'), 40)
    otisak = head_printer.render(s, True, boja)
    ekran.blit(otisak, otisak.get_rect(center=head_rect.center))
    G.display.flip()

simboja = dict(O=Boja.zelena, X=Boja.crvena)
nrp = dict(O=G.Rect(field*.9, 0, field*.1, header),
           X=G.Rect(0, 0, field*.1, header))
for prav in nrp.values():
    prav.inflate_ip(-header/2, -header/2)
vars().update(filestarter())
assert len(igrači) == 2
igrači = list(igrači)
random.shuffle(igrači)

class Opet(Exception):
    pass

def početak():
    ekran.fill(Boja.pozadina)
    ekran.fill(Boja.siva, head_rect)
    for x1, y1, x2, y2 in [(0, side + header, field, side + header),
                           (0, side*2 + header, field, side*2 + header),
                           (side, header, side, field + header),
                           (2*side, header, 2*side, field + header)]:
        G.draw.aaline(ekran, Boja.crna, (x1, y1), (x2, y2))
    for i in range(3):
        for j in range(3):
            stavi(i, j,  3*i + j + 1, Boja.brojke)
    for igrač, simbol in zip(igrači, 'XO'):
        igrač.simbol = simbol
        igrač.stavljeno.clear()
    i1, i2 = igrači
    i1.protivnik = i2
    i2.protivnik = i1
    G.event.clear()

def igra():
    početak()
    slobodno = set(range(1, 10))
    for naredu in itertools.cycle(igrači):
        print_head(Boja.crna, naredu)
        broj = naredu.potez(slobodno)
        i, j = divmod(broj - 1, 3)
        stavi(i, j, naredu.simbol, Boja.crna)
        slobodno.remove(broj)
        naredu.stavljeno.add(str(broj))
        for kombinacija in pobjede:
            if kombinacija <= naredu.stavljeno:
                for pozicija in kombinacija:
                    i, j = divmod(int(pozicija) - 1, 3)
                    simb = naredu.simbol
                    stavi(i, j, simb, simboja[simb])
                kraj(naredu)
        if not slobodno:
            kraj(None)

def kraj(pobjednik):
    if pobjednik:
        pobjednik.bodovi += 1
        print_head(simboja[pobjednik.simbol])
        # zvuk_pobjeda.play()
    else:
        # zvuk_neriješeno.play()
    igrači.reverse()
    G.event.clear()    
    G.time.wait(1000)
    raise Opet

while True:
    with contextlib.suppress(Opet):
        igra()
