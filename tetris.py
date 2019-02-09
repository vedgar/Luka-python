import pygame as G, random, enum, os, time, collections

os.environ['SDL_VIDEO_WINDOW_POS'] = '200,35'

širina, visina = 10, 15
q = 40
cheat_code_activated = False

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
# G.font.init()
# font = G.font.SysFont('Arial', 24, bold=True)
polje = {Blok(i, 0, Boja.siva) for i in range(16)}
polje |= {Blok(15, i, Boja.siva) for i in range(1, 11)}
polje |= {Blok(i, 11, Boja.siva) for i in range(16)}

def kraj():
    G.quit()
    raise SystemExit    

o = None
score = 0
G.time.set_timer(G.USEREVENT, 500)

while ...:
    if o is None:
        o = random.choice(oblici)
        o.i, o.j = 0, 3
        print(*o.value, sep='\n')
        print()
        o.boja = Boja.slučajna()
        o.popuni(o.i, o.j)
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
                o = None
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
            elif događaj.key == G.K_CAPSLOCK and cheat_code_activated:
                o.i = 0
