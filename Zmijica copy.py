from turtle import *
import random

ZMIJA, SMJER, HRANA = [(0, 0)], [0], [(0, 0)]
šmrk_boost = 0

def ranking():
    ime = None
    pozicija = 0
    with open('ranking.txt') as datoteka:
        Lista = datoteka.readlines()
        ljestvica = ""
        for i in range(5): ljestvica += Lista[i]
    for i in range(5):
        ime, bodovi = Lista[i].rsplit(maxsplit=1)
        Lista[i] = ime, int(bodovi)
    for i in range(5):
        if Lista[i][1] <len(ZMIJA):
            ime = textinput("cestitke",ljestvica + "\nTvoj rezultat je :" + str(len(ZMIJA)) + "\nUpisi se na ljestvicu: ")
            pozicija = i
            break
    if not ime: return
    with open('ranking.txt', 'w') as datoteka:
        for i in range(pozicija):
            datoteka.write(Lista[i][0] + " " + str(Lista[i][1])+"\n")
        datoteka.write(ime+" "+str(len(ZMIJA))+"\n")
        for i in range(pozicija+1,5):
            datoteka.write(Lista[i][0] + " " + str(Lista[i][1])+"\n")
    
def kvadrat():
    tracer(False)
    pendown()
    pensize(1)
    begin_fill()
    setheading(0)
    for i in range(4): fd(40), left(90)
    end_fill()
    penup()
    
def okvir():
    tracer(False), pensize(5), pencolor('white'), goto(-320, -240)
    setheading(0), pendown()
    for i in range(2): fd(640), left(90), fd(480), left(90)
    tracer(True), pensize(1), pencolor('black'), penup()

def postavi_hranu():
    dobar = False
    while not dobar:
        i, j = random.randint(-8, 7), random.randint(-6, 5)
        dobar = (i, j) not in ZMIJA
    HRANA[0] = i, j
    goto(i*40, j*40)
    color('red')
    kvadrat()

def sudar(a,b):
    global šmrk_boost
    if a == -9 or a == 8 or b == -7 or b == 6: return True
    if a == -8 or a == 7 or b == -6 or b == 5: šmrk_boost += 10
    for p in range(len(ZMIJA)-2):
        if ZMIJA[p] == (a, b): return True
        return False

def brzina(): ontimer(pomakni, max(50, 100 - šmrk_boost + 200//len(ZMIJA)))

def gore(): SMJER[0] = 90
def dolje(): SMJER[0] = 270
def lijevo(): SMJER[0] = 180
def desno(): SMJER[0] = 0

def pomakni():
    polozaj = ZMIJA[len(ZMIJA)-1]
    x, y = polozaj
    if SMJER[0] == 0: x += 1 
    if SMJER[0] == 180: x -= 1
    if SMJER[0] == 90: y += 1
    if SMJER[0] == 270: y -= 1
    ZMIJA.append((x, y)), goto(40*x, 40*y), color('green'), kvadrat()

    if (x, y) == HRANA[0]: postavi_hranu()
    elif sudar(x,y):
        goto(-100, 0)
        color('green')
        write('GAME OVER', font = ('Arial', 50))
        ranking()
        raise SystemExit
    else:
        goto(ZMIJA[0][0]*40, ZMIJA[0][1]*40)
        color('black')
        kvadrat()
        ZMIJA.pop(0)
        
    brzina()

reset(), screensize(800, 600), title('Snake'), bgcolor('black')
hideturtle(), penup()

okvir(), postavi_hranu()

brzina()
onkey(gore, 'Up'), onkey(desno, 'Right'),
onkey(lijevo, 'Left'), onkey(dolje, 'Down')
listen(), mainloop()
