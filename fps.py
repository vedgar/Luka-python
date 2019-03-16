import pygame as G
from math import sin, cos, pi
stup = pi/180

x0, y0, z0 = 0, 0, 0
alfa, beta = 0, 180*stup
d = 1

objekti = [(-3, 0, 0)]

def kraj():
    G.quit()
    raise SystemExit

class Boja:
    crvena = G.Color('red')

ekran = G.display.set_mode([800, 600], G.FULLSCREEN)
try:
    while True:
        for događaj in G.event.get():
            if događaj.type == G.KEYDOWN and događaj.key == G.K_ESCAPE:
                kraj()
        ekran.fill(Boja.crvena)
        for x, y, z in objekti:
            
        G.display.flip()
except:
    G.quit()
    raise
