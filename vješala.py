import contextlib, textwrap, random
import pygame as G

G.init()
crna = G.Color('black')
crvena = G.Color('red')
smeđa = G.Color('brown')
siva = G.Color('gray')
tamnoplava = G.Color('darkblue')
narančasta = G.Color('orange')
žuta = G.Color('yellow')
abeceda = 'abcčćdǆđefghijklǉmnǌoprsštuvzž'.upper()
zamjene = str.maketrans('qwx', 'ǉǌǆ')
raspored = textwrap.TextWrapper(width=10, max_lines=7)

ekran = G.display.set_mode((800, 500))
filename = G.font.match_font('microsoftsansserif')
printer = G.font.Font(filename, 30)
zvukok = G.mixer.Sound('ok.wav')

def crtaj_slovo(slovo, i, j, boja=crna):
    površina = printer.render(slovo.upper(), True, boja)
    pravokutnik = površina.get_rect(center=(325+50*j, 25+50*i))
    ekran.blit(površina, pravokutnik)
    G.display.flip()

def crtaj_vješala(p):
    if p == 0:
        plist = (50, 480), (50, 50), (200, 50), (200, 100)
        G.draw.lines(ekran, smeđa, False, plist, 15)
    if p == 1:
        G.draw.circle(ekran, siva, (200, 150), 50, 5)
    if p == 2:
        G.draw.line(ekran, tamnoplava, (200, 200), (200, 400), 20)
    if p == 3:
        G.draw.line(ekran, tamnoplava, (200, 200), (270, 250), 10)
    if p == 4:
        G.draw.line(ekran, tamnoplava, (200, 200), (130, 250), 10)
    if p == 5:
        G.draw.line(ekran, tamnoplava, (200, 400), (270, 450), 10)
    if p == 6:
        G.draw.line(ekran, tamnoplava, (200, 400), (130, 450), 10)
    G.display.flip()

def inicijaliziraj():
    ekran.fill(narančasta, G.Rect((0, 0), (300, 500)))
    ekran.fill(žuta, G.Rect((300, 0), (500, 350)))
    ekran.fill(crvena, G.Rect((300, 350), (500, 150)))

def crtaj_dolje(slovo):
    slovo = slovo.upper()
    indeks = abeceda.index(slovo)
    i, j = divmod(indeks, 10)
    crtaj_slovo(slovo, i + raspored.max_lines, j)

def obiđi(linije):
    for i, linija in enumerate(linije, (raspored.max_lines - len(linije)) // 2):
        for j, znak in enumerate(linija.center(raspored.width)):
            yield i, j, znak
    
def kraj():
    G.quit()
    print(bodovi, odigrano, sep='/')
    raise SystemExit

def igra(riječ):
    linije = raspored.wrap(riječ.upper())
    inicijaliziraj()
    za_pogađanje = 0
    for i, j, znak in obiđi(linije):
        if znak in abeceda:
            znak = '_'
            za_pogađanje += 1
        crtaj_slovo(znak, i, j)

    upotrijebljena = set()
    promašaji = 0
    crtaj_vješala(promašaji)
    G.display.flip()

    while True:
        for događaj in G.event.get():
            if događaj.type == G.QUIT:
                kraj()
            if događaj.type == G.KEYDOWN:
                if događaj.key == G.K_ESCAPE:
                    kraj()
                slovo = događaj.unicode.lower().translate(zamjene).upper()
                if slovo in set(abeceda) - upotrijebljena:
                    upotrijebljena.add(slovo)
                    crtaj_dolje(slovo)
                    pogođeno = False
                    for i, j, znak in obiđi(linije):
                        if znak == slovo:
                            crtaj_slovo(slovo, i, j)
                            za_pogađanje -= 1
                            pogođeno = True
                    if not za_pogađanje:
                        zvukok.play()
                        G.time.wait(2000)
                        return True
                    if not pogođeno:
                        promašaji += 1
                        crtaj_vješala(promašaji)
                        if promašaji > 5:
                            for i, j, znak in obiđi(linije):
                                crtaj_slovo(znak, i, j, boja=crvena)
                            G.time.wait(2000)
                            return False
        G.time.wait(100)

riječi = []
with open('životinje.txt', encoding='utf-8-sig') as ulaz:
    for linija in ulaz:
        linija = linija.strip()
        if linija:
            riječi.append(linija)

#igra(random.choice(riječi))
#igra('''
#
#                                 bijela roda
#
#'''.strip().lower().translate(zamjene))

random.shuffle(riječi)
bodovi = odigrano = 0
for riječ in riječi:
    bodovi += igra(riječ)
    odigrano += 1
kraj()
