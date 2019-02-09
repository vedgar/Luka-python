import pygame as G, random
from dataclasses import dataclass

širina, visina = 7, 7
q = 100

labirint = '''\
    .|.|-.x
    .|-.|||
    ..|..x|
    --....|
    -..|.x|
    |.-x|.|
    xx--x-x
'''

class Boja:
    zidovi = G.Color('black')
    mojtenk = G.Color('blue')
    npctenk = G.Color('red')

@dataclass
class Kvadratić:
    gore: bool
    dolje: bool
    lijevo: bool
    desno: bool

    def nacrtaj(self, x, y):
        if self.lijevo:
            G.draw.line(ekran, Boja.zidovi, (x, y), (x, y+q-1))
        if self.desno:
            G.draw.line(ekran, Boja.zidovi, (x+q-1, y), (x+q-1, y+q-1))
        if self.gore:
            G.draw.line(ekran, Boja.zidovi, (x, y), (x+q-1, y))
        if self.dolje:
            G.draw.line(ekran, Boja.zidovi, (x, y+q-1), (x+q-1, y+q-1))

slika_tenk = G.image.load('tenk.png')
slika_tenk = G.transform.scale(slika_tenk, (q, q))
slika_tenk.set_colorkey(G.Color('white'))

@dataclass
class Tenk:
    i: int
    j: int
    boja: Boja

    def nacrtaj(self):
        ekran.fill(self.boja, G.Rect(self.j * q, self.i * q, q, q))
        ekran.blit(slika_tenk, (self.j * q, self.i * q))

    def pomakni(self, di, dj):
        gdjesam = karta[self.i, self.j]
        if (di, dj) == (-1, 0):
            zid = gdjesam.gore
        elif (di, dj) == (1, 0):
            zid = gdjesam.dolje
        elif (di, dj) == (0, 1):
            zid = gdjesam.desno
        elif (di, dj) == (0, -1):
            zid = gdjesam.lijevo
        if zid:
            return
        i, j = self.i + di, self.j + dj
        for tenk in mojtenk, npc:
            if (tenk.i, tenk.j) == (i, j):
                return
        self.i, self.j = i, j

mojtenk = Tenk(0, 0, Boja.mojtenk)
npc = Tenk(6, 6, Boja.npctenk)

karta = {}
for i, linija in enumerate(labirint.splitlines()):
    for j, znak in enumerate(linija.strip()):
        desno_zid = znak in '|x'
        dolje_zid = znak in '-x'
        gore_zid = not i or karta[i-1, j].dolje
        lijevo_zid = not j or karta[i, j-1].desno
        karta[i, j] = Kvadratić(gore_zid, dolje_zid, lijevo_zid, desno_zid)

ekran = G.display.set_mode([širina * q, visina * q])
sat = G.time.Clock()
G.time.set_timer(G.USEREVENT, 1000)

def kraj():
    G.quit()
    raise SystemExit

while True:
    ekran.fill(G.Color('white'))
    mojtenk.nacrtaj()
    npc.nacrtaj()
    for i, j in karta:
        karta[i, j].nacrtaj(j * q, i * q)
    gdjesam = karta[mojtenk.i, mojtenk.j]
    G.display.flip()
    sat.tick(100)
    # print(sat.get_fps())
    for događaj in G.event.get():
        if događaj.type == G.QUIT:
            kraj()
        elif događaj.type == G.KEYDOWN:
            if događaj.key == G.K_ESCAPE: kraj()
            elif događaj.key == G.K_LEFT: mojtenk.pomakni(0, -1)
            elif događaj.key == G.K_RIGHT: mojtenk.pomakni(0, 1)
            elif događaj.key == G.K_UP: mojtenk.pomakni(-1, 0)
            elif događaj.key == G.K_DOWN: mojtenk.pomakni(1, 0)
        elif događaj.type == G.USEREVENT:
            # di, dj = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            # npc.pomakni(di, dj)
            d = {}
            d[npc.i, npc.j] = 0
            while (mojtenk.i, mojtenk.j) not in d:
                for i, j in d.copy():
                    n = d[i, j] + 1
                    if not karta[i, j].lijevo: d.setdefault((i, j-1), n)
                    if not karta[i, j].desno: d.setdefault((i, j+1), n)
                    if not karta[i, j].gore: d.setdefault((i-1, j), n)
                    if not karta[i, j].dolje: d.setdefault((i+1, j), n)
##            if False:
##              for i in range(7):
##                for j in range(7):
##                    print(d[i, j] % 10 if (i, j) in d else '*', end='')
##                print()
            i, j = mojtenk.i, mojtenk.j
            n = d[i, j]
            while n:
                #print(n, end=' ')
                for dj, di, smjer in (-1, 0, 'desno'), (1, 0, 'lijevo'), (0, -1, 'dolje'), (0, 1, 'gore'):
                    # smjerovi su obrnuti jer želimo vidjeti u kom smjeru se NPC treba kretati a ne obrnuto
                    # print('probam', smjer, 'sa', i, j, 'zid', getattr(karta[i, j], smjer), 'broj', d.get((i - di, j - dj)))
                    if d.get((i - di, j - dj)) == n - 1 and not getattr(karta[i, j], smjer):
                        # print('idem', smjer, 'sa', i, j)
                        n -= 1
                        i -= di
                        j -= dj
                        break
            print()
            npc.pomakni(di, dj)
