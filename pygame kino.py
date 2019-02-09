import pygame as G, string
G.init()
ekran = G.display.set_mode([600, 100])
sat = G.time.Clock()

zauzeto = [None] * 10
def zauzmi(sjedalo):
        zauzeto[pozicija] = True
        if all(zauzeto):
           kraj() 
     
    
def kraj():
    G.quit()
    raise SystemExit
    

while True:
    sat.tick(10)
    ekran.fill(G.Color('purple'))
    for sjedalo in range(10):
        boja = G.Color('red' if zauzeto[sjedalo] else 'green')
        G.draw.circle(ekran,boja,((sjedalo + 1) * 50, 50), 10)
    G.display.flip()    
    for događaj in G.event.get():
        if događaj.type == G.QUIT:
            G.quit()
            raise SystemExit
        elif događaj.type == G.MOUSEBUTTONUP:
            pozicija = round(događaj.pos[0] / 50) - 1
            zauzmi(pozicija)
        elif događaj.type == G.KEYUP:
             if događaj.key == G.K_ESCAPE:
                     kraj()
             znamenka = chr(događaj.key)
             if znamenka in string.digits:
                pozicija = int(znamenka) - 1
                zauzmi(pozicija)
                  
