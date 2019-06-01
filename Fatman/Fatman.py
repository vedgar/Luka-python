import pygame as G, dataclasses, pathlib, enum, collections

visina, širina = 40, 30
q = 16
ekran = G.display.set_mode([visina * q, širina * q])
sat = G.time.Clock()

def kraj():
    G.quit()
    raise SystemExit

@dataclasses.dataclass

class Tile(enum.Enum):
    TOČKICA = '.'
    ZID = '#'
    TOČKA = '0'
    VRATA = '_'
    PRAZNO = '\\'

    def __repr__(self):
        return self.name + self.value

@dataclasses.dataclass
class Karta:
    poz = (int, int)
    Pacman: poz
    duhovi: {str: {poz}}
    na: {poz: Tile}

    @classmethod
    def iz_datoteke(cls, ime):
        duhovi = collections.defaultdict(set)
        na, Pacman = {}, set()
        datoteka = pathlib.Path(ime)
        for i, linija in enumerate(open(datoteka)):
            for j, znak in enumerate(linija.strip('\n')):
                poz = i, j
                if znak in r'\.0#_': na[poz] = Tile(znak)
                elif znak == 'C': duhovi['Blinky'].add(poz)
                elif znak == 'P': duhovi['Inky'].add(poz)
                elif znak == 'R': duhovi['Pinky'].add(poz)
                elif znak == 'N': duhovi['Clyde'].add(poz)
                elif znak == '%': Pacman.add(poz)
                else: print('Nepoznat znak', znak)
        return cls(Pacman, duhovi, na)

karta = Karta.iz_datoteke('Fatman.txt')
galerija = {}

for slika in pathlib.Path('Sprites').iterdir():
    galerija[slika.stem] = G.image.load(str(slika))

nemaih = set()

while ...:
    sat.tick(20)

    for (i, j), tile in karta.na.items():
        ime = tile.name.lower()
        if ime in galerija:
            ekran.blit(galerija[ime], G.Rect(j * q, i * q, q, q))
        else: nemaih.add(ime)
    G.display.flip()
    
    for događaj in G.event.get():
        if događaj.type == G.QUIT: kraj()
        elif događaj.type == G.KEYDOWN and događaj.key == G.K_ESCAPE: kraj()
        else: print(događaj)
