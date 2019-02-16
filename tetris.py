import pygame as G, random, enum, os, time, collections, contextlib

lijevi_odmak, gornji_odmak = 200, 35
širina, visina = 10, 15
margina = 10
q = 40
cheat = False
bodovi = 0

class Oblik(enum.Enum):
    S = [' ##',
         '## ']
    Z =         ['## ',
                 ' ##']
    O = ['##',
         '##']
    T =         [' # ',
                 '###']
    J = ['#  ',
         '###']
    L =         ['  #',
                 '###']
    I = ['####']

##    Ivan = ['  #  ',
##            ' ### ',
##            '#####',
##            ' ### ',
##            '  #  ']

    def popuni(self, di=0, dj=0):
        opolje = set()
        for i, linija in enumerate(self.value, start=self.i+di):
            for j, znak in enumerate(linija, start=self.j+dj):
                if znak == '#': opolje.add(Blok(i, j, self.boja))
        return opolje

    def kolizija(self, di=0, dj=0):
        opolje = self.popuni(di, dj)
        if opolje.isdisjoint(polje):
            self.i += di
            self.j += dj
        else: return self.popuni()

    def nacrtaj(self):
        for blok in self.popuni(): blok.nacrtaj()


def novi_oblik(oblici = list(Oblik)):
    o = random.choice(oblici)
    o.i, o.j = 0, širina // 2 - 1
    print(*o.value, sep='\n')
    print('-' * 10)
    o.boja = random.choice(Boja.za_oblike)
    if o.kolizija(): raise Kraj
    dodaj_bodove(1)
    return o


def dodaj_bodove(b):
    global bodovi
    bodovi += b


def konsolidiraj():
    polje.update(o.popuni())
    iznad = set()
    linije = 0
    while ...:
        for i in range(visina):
            linija = {blok for blok in polje if blok.i == i and blok.unutra()}
            if len(linija) < širina: iznad |= linija
            else:
                dodaj_bodove(100)
                polje.difference_update(iznad | linija)
                polje.update(blok.dolje() for blok in iznad)
                break
        else: break


class Blok(collections.namedtuple('BlokBaza', 'i j boja')):
    def nacrtaj(self): G.draw.rect(ekran, self.boja,
        G.Rect(self.j*q + margina, self.i*q + margina, q, q))
    def pozicija(self): return self.i, self.j
    def dolje(self): return self._replace(i=self.i + 1)
    def unutra(self): return self.i < visina and 1 <= self.j <= širina
    def __hash__(self): return hash(self.pozicija())
    def __eq__(self, other): return self.pozicija() == other.pozicija()
        

class Boja:
    crvena = G.Color('#ff0000')
    crna = G.Color('black')
    plava = G.Color('blue')
    siva = G.Color('gray')
    žuta = G.Color('yellow')
    narančasta = G.Color('orange')
    zelena = G.Color('green')
    za_oblike = [crvena, plava, žuta, narančasta, zelena]


class Kraj(Exception): pass


os.environ['SDL_VIDEO_WINDOW_POS'] = f'{lijevi_odmak},{gornji_odmak}'
dimenzije = margina + (širina+2)*q + 200, margina*2 + (visina+1)*q
ekran = G.display.set_mode(dimenzije)
G.key.set_repeat(1, 100)
G.mixer.init()
G.mixer.music.load('tetrisc.mid')
G.mixer.music.play(-1)
polje = {Blok(i, 0, Boja.siva) for i in range(1 + visina)} \
    | {Blok(visina, i, Boja.siva) for i in range(1, 1 + širina)} \
    | {Blok(i, 1 + širina, Boja.siva) for i in range(1 + visina)}
o = novi_oblik()
gravitacija = G.USEREVENT
G.time.set_timer(gravitacija, 500)

with contextlib.suppress(Kraj):
    while ...:
        ekran.fill(Boja.crna)
        for blok in polje: blok.nacrtaj()
        o.nacrtaj()
        if bodovi > 10_000 and not cheat:
            print('Cheat code activated! Press CAPS LOCK...')
            cheat = True
        G.display.flip()
        for događaj in G.event.get():
            if događaj.type == G.QUIT: raise Kraj
            elif događaj.type == gravitacija:
                if o.kolizija(1):
                    konsolidiraj()
                    o = novi_oblik()
            elif događaj.type == G.KEYDOWN:
                if događaj.key == G.K_ESCAPE: raise Kraj
                elif događaj.key == G.K_LEFT: o.kolizija(0, -1)
                elif događaj.key == G.K_RIGHT: o.kolizija(0, 1)
                elif događaj.key == G.K_DOWN: o.kolizija(1)
                elif događaj.key == G.K_SPACE:
                    while not o.kolizija(1): dodaj_bodove(5)
                    konsolidiraj()
                    o = novi_oblik()
                elif događaj.key == G.K_CAPSLOCK and cheat: o.i = 0
G.quit()
print('This is the end, my friend...\nBodovi:', bodovi)
