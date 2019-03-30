import pygame as G, dataclasses, random, pathlib, contextlib

staza = 'labirint'
labirint = pathlib.Path(staza + '.horor').read_text().splitlines()
header = len(labirint[0]) * '#'
labirint = [header] + labirint + [header]
labirint = ['#' + linija + '#' for linija in labirint]

zidovi = set()
for i, linija in enumerate(labirint):
    for j, ćelija in enumerate(linija):
        if ćelija == '#': zidovi.add((i, j))
visina, širina = i, j
q = 50
s = 5

class Opet(Exception): pass

@dataclasses.dataclass
class Igrač:
    pos: (int, int)
    slika: G.Surface
    ime: str

    def __init__(self, ime=None, slika=None, svakih=None):
        global moj_događaj
        moj_događaj += 1
        self.događaj = moj_događaj
        self.svakih = svakih
        if self.svakih: G.time.set_timer(self.događaj, self.svakih)
        while ...:
            pos = random.randrange(visina), random.randrange(širina)
            if pos not in zidovi: break
        self.pos = pos
        self.ime = ime
        if slika is not None:
            slika = G.image.load(slika + '.png')
            slika = G.transform.scale(slika, (q, q))
            self.slika = slika.convert()

    def pomakni(self, di, dj):
        i, j = self.pos
        i += di
        j += dj
        if (i, j) not in zidovi:
            self.pos = i, j

    def pomakni_slučajno(self):
        self.pomakni(*random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)]))

    def udaljenost(self):
        (i1, j1), (i2, j2) = self.pos, Luka.pos
        return abs(i1 - i2) + abs(j1 - j2)

    def pomakni_pametno(self):
        d = {self.pos: 0}
        promjena = True
        while promjena:
            promjena = False
            for (i, j), n in d.copy().items():
                for di, dj in (0, 1), (0, -1), (-1, 0), (1, 0):
                    i2, j2 = i + di, j + dj
                    if (i2, j2) not in zidovi and (i2, j2) not in d:
                        d[i2, j2] = n + 1
                        promjena = True
        if Luka.pos in d:
            n = d[Luka.pos]
            i, j = Luka.pos
            while n:
                for di, dj in (0, 1), (0, -1), (-1, 0), (1, 0):
                    if d.get((i - di, j - dj)) == n - 1:
                        n -= 1
                        i -= di
                        j -= dj
                        break
            self.pomakni(di, dj)
        else: self.pomakni_slučajno()


status = G.Surface([650, q * s])
ekran = G.display.set_mode([q * s + status.get_width(), status.get_height()])
sat = G.time.Clock()
statusprav = G.Rect(q * s, 0, status.get_width(), status.get_height())
G.font.init()
font = G.font.Font(None, 50)
poruka = 'Welcome to the horrible game'

def kraj(npc=None):
    if npc is None: print('You gave up')
    else: print("You got F'ed by", npc.ime)
    raise Opet(npc.ime)

class Boja:
    bijela = G.Color('white')
    crna = G.Color('black')
    plava = G.Color('blue')
    crvena = G.Color('red')
    svijetlosiva = G.Color('#dddddd')

def splash(poruka):
    ekran.fill(Boja.crvena)
    tekst = font.render(poruka, True, Boja.plava, Boja.crvena)
    ekran.blit(tekst, (10, 50))
    tekst = font.render('Press SPACE', True, Boja.crna, Boja.crvena)
    ekran.blit(tekst, (10, 90))
    G.display.flip()
    while ...:
        for događaj in G.event.get():
            if događaj.type == G.KEYDOWN and događaj.key == G.K_SPACE: return

poruka = ''
while ...:
    try:
        moj_događaj = ubrzanje = G.USEREVENT
        splash(poruka)
        Luka = Igrač()
        scary = [
            Igrač(ime='George', slika='George', svakih=400),
            Igrač(ime='Ghostface', slika='Ghostface', svakih=500)
        ]
        while ...:
            ekran.fill(Boja.bijela)
            i, j = Luka.pos
            for di in range(s):
                for dj in range(s):
                    vidi = i + di - s//2, j + dj - s//2
                    prav = G.Rect(q * dj, q * di, q, q)
                    if vidi in zidovi:
                        ekran.fill(Boja.crna, prav)
                    else:
                        for npc in scary:
                            if vidi == npc.pos:
                                ekran.blit(npc.slika, prav)
                                if vidi == Luka.pos:
                                    kraj(npc)
                                break
                    if vidi == Luka.pos:
                        ekran.fill(Boja.svijetlosiva, prav)
                            
            status.fill(Boja.plava)
            tekst = font.render(poruka, True, Boja.crna, Boja.plava)
            status.blit(tekst, (10, 50))
            ekran.blit(status, statusprav)
            G.display.flip()
            poruka = str({npc.ime: npc.udaljenost() for npc in scary})
            for događaj in G.event.get():
                if događaj.type == G.QUIT: kraj()
                elif događaj.type == G.KEYUP:
                    if događaj.key == G.K_ESCAPE: kraj()
                    elif događaj.key == G.K_LEFT: Luka.pomakni(0, -1)
                    elif događaj.key == G.K_RIGHT: Luka.pomakni(0, 1)
                    elif događaj.key == G.K_UP: Luka.pomakni(-1, 0)
                    elif događaj.key == G.K_DOWN: Luka.pomakni(1, 0)
                else:
                    for npc in scary:
                        if događaj.type == npc.događaj: npc.pomakni_pametno()
    except Opet as ex:
        poruka = "You got F'ed by " + ex.args[0]
