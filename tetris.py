import pygame as G, random, enum, os, time, collections, contextlib

os.environ['SDL_VIDEO_WINDOW_POS'] = '200,35'

širina, visina = 10, 15
q = 30
cheat_code_activated = False
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

    def popuni(self, i0, j0):
        opolje = set()
        for i, linija in enumerate(self.value, start=i0):
            for j, znak in enumerate(linija, start=j0):
                if znak == '#':
                    opolje.add(Blok(i, j, self.boja))
        return opolje

oblici = list(Oblik)

class Blok(collections.namedtuple('BlokBaza', 'i j boja')):
    def nacrtaj(self):
        G.draw.rect(ekran, self.boja, G.Rect(self.j*q + 10, self.i*q + 10, q, q))

    def __hash__(self):
        return hash((self.i, self.j))

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j
        
class Boja:
    crvena = G.Color('#ff0000')
    crna = G.Color('black')
    plava = G.Color('blue')
    siva = G.Color('gray')
    žuta = G.Color('yellow')
    narančasta = G.Color('orange')

    @classmethod
    def slučajna(cls):
        boje = [boja for boja in vars(Boja).values()
                if isinstance(boja, G.Color)
                and boja not in [Boja.crna, Boja.siva]]
        return random.choice(boje)

ekran = G.display.set_mode([10 + (širina+2)*q + 200, 10 + (visina+1)*q + 10])
playground = G.Rect(10, 10, (širina+2)*q, (visina+1)*q)
G.key.set_repeat(1, 100)
G.mixer.init()
G.mixer.music.load('tetrisb.mid')
G.mixer.music.play(-1)
# G.font.init()
# font = G.font.SysFont('Arial', 24, bold=True)
polje = {Blok(i, 0, Boja.siva) for i in range(16)}
polje |= {Blok(15, i, Boja.siva) for i in range(1, 11)}
polje |= {Blok(i, 11, Boja.siva) for i in range(16)}

def kraj():
    G.key.set_repeat()
    G.mixer.music.stop()
    G.quit()
    print('This is the end, my friend...')
    print('Bodovi:', bodovi)
    raise SystemExit

def novi_oblik():
    o = random.choice(oblici)
    o.i, o.j = 0, 3
    print(*o.value, sep='\n')
    print()
    o.boja = Boja.slučajna()
    opolje = o.popuni(o.i, o.j)
    if opolje.isdisjoint(polje):
        return o
    raise Kraj
    
class Kraj(Exception):
    pass

o = None
score = 0
G.time.set_timer(G.USEREVENT, 500)

with contextlib.suppress(Kraj):
    while ...:
        if o is None:
            o = novi_oblik()
        ekran.fill(Boja.crna)
        for blok in polje: blok.nacrtaj()
        for blok in o.popuni(o.i, o.j): blok.nacrtaj()
        if score > 10_000 and not cheat_code_activated:
            print('Cheat code activated!')
            print('Press CAPS LOCK...')
            cheat_code_activated = True
        ...  # crtanje
        G.display.flip()
        for događaj in G.event.get():
            if događaj.type == G.QUIT:
                kraj()
            elif događaj.type == G.USEREVENT:
                opolje = o.popuni(o.i+1, o.j)
                if opolje & polje:
                    polje |= o.popuni(o.i, o.j)
                    o = novi_oblik()
                else: o.i += 1
            elif događaj.type == G.KEYDOWN:
                if događaj.key == G.K_ESCAPE:
                    kraj()
                elif događaj.key == G.K_LEFT:
                    opolje = o.popuni(o.i, o.j-1)
                    if opolje.isdisjoint(polje): o.j -= 1
                elif događaj.key == G.K_RIGHT:
                    opolje = o.popuni(o.i, o.j+1)
                    if opolje.isdisjoint(polje): o.j += 1
                elif događaj.key == G.K_DOWN:
                    opolje = o.popuni(o.i+1, o.j)
                    if opolje.isdisjoint(polje): o.i += 1
                elif događaj.key == G.K_SPACE:
                    while ...:
                        bodovi += 5
                        opolje = o.popuni(o.i+1, o.j)
                        if opolje.isdisjoint(polje): o.i += 1
                        else:
                            polje |= o.popuni(o.i, o.j)
                            o = novi_oblik()
                            break
                elif događaj.key == G.K_CAPSLOCK and cheat_code_activated:
                    o.i = 0
kraj()
