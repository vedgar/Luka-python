import pygame as G, dataclasses, random, pathlib

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


@dataclasses.dataclass
class Igrač:
    pos: (int, int)
    slika: G.Surface

    def __init__(self, slika=None):
        while ...:
            pos = random.randrange(visina), random.randrange(širina)
            if pos not in zidovi: break
        self.pos = pos
        self.ime = slika
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


status = G.Surface([650, q * 3])
ekran = G.display.set_mode([q * 3 + status.get_width(), status.get_height()])

Luka = Igrač()
Džordž = Igrač(slika='George')
Ghostface = Igrač(slika='Ghostface')
scary = [Džordž, Ghostface]

sat = G.time.Clock()
statusprav = G.Rect(q * 3, 0, status.get_width(), status.get_height())
G.font.init()
font = G.font.Font(None, 50)

poruka = 'Welcome to the horrible game'

def kraj():
    G.quit()
    raise SystemExit

class Boja:
    bijela = G.Color('white')
    crna = G.Color('black')
    plava = G.Color('blue')
    crvena = G.Color('red')

while ...:
    ekran.fill(Boja.bijela)
    i, j = Luka.pos
    for di in range(3):
        for dj in range(3):
            vidi = i + di - 1, j + dj - 1
            prav = G.Rect(q * dj, q * di, q, q)
            if vidi in zidovi:
                ekran.fill(Boja.crna, prav)
            else:
                for npc in scary:
                    if vidi == npc.pos:
                        ekran.blit(npc.slika, prav)
                        break
                    
    status.fill(Boja.plava)
    tekst = font.render(poruka, True, Boja.crna, Boja.plava)
    status.blit(tekst, (10, 50))
    ekran.blit(status, statusprav)
    G.display.flip()
    for događaj in G.event.get():
        if događaj.type == G.QUIT: kraj()
        elif događaj.type == G.KEYUP:
            if događaj.key == G.K_ESCAPE: kraj()
            elif događaj.key == G.K_LEFT: Luka.pomakni(0, -1)
            elif događaj.key == G.K_RIGHT: Luka.pomakni(0, 1)
            elif događaj.key == G.K_UP: Luka.pomakni(-1, 0)
            elif događaj.key == G.K_DOWN: Luka.pomakni(1, 0)
            for npc in scary: npc.pomakni_slučajno()
            poruka = str({npc.ime: npc.udaljenost() for npc in scary})
        
