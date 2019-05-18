from turtle import *
import random

class par:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        return
    def __eq__(self, p):
        if self.x != p.x:
            return False
        if self.y != p.y:
            return False
        else:
            return True
    def daj_x(self):
        return self.x
    def daj_y(self):
        return self.y

    
ZMIJA = [par(0,0)]
SMJER = [0]
HRANA = [par(0,0)]


def ranking():
    ime = None
    pozicija = 0
    datoteka = open('ranking.txt','r')
    Lista = datoteka.readlines()
    ljestvica = ""
    for i in range(5):
        ljestvica = ljestvica + Lista[i]
    datoteka.close()
    for i in range(5):
        pom = Lista[i].split()
        Lista[i] = [pom[0], int(pom[1])]
    for i in range(5):
        if Lista[i][1] <len(ZMIJA):
            ime = textinput("cestitke",ljestvica + "\nTvoj rezultat je :" + str(len(ZMIJA)) + "\nUpisi se na ljestvicu: ")
            pozicija = i
            break
    if(ime == None):
        return
    datoteka = open('ranking.txt', 'w')
    for i in range(pozicija):
        datoteka.write(Lista[i][0] + " " + str(Lista[i][1])+"\n")
    datoteka.write(ime+" "+str(len(ZMIJA))+"\n")
    for i in range(pozicija+1,5):
        datoteka.write(Lista[i][0] + " " + str(Lista[i][1])+"\n")
    datoteka.close()
    return
    

def plus(x):
    if x<=50:
        return 50
    else:
        return x

def kvadrat():
    tracer(False)
    pendown()
    pensize(1)
    begin_fill()
    setheading(0)
    for i in range(4):
        fd(40)
        left(90)
    end_fill()
    penup()
    return
    
def okvir():
    tracer(False)
    pensize(5)
    pencolor('red')
    goto(-320,-240)
    setheading(0)
    pendown()
    for i in range(2):
        fd(640)
        left(90)
        fd(480)
        left(90)
    tracer(True)
    pensize(1)
    pencolor('black')
    penup()
    return


def postavi_hranu():
    dobar = False
    while (not dobar):
        i = random.randint(-8,7)
        j = random.randint(-6,5)
        dobar = True
        for p in ZMIJA:
            if par(i,j) == p:
                dobar = False
    HRANA[0] = par(i,j)
    goto(i*40, j*40)
    color('red')
    kvadrat()
    return


def sudar(a,b):
    if a == -9 or a == 8 or b == -7 or b == 6:
        return True
    for p in range(len(ZMIJA)-2):
        if ZMIJA[p] == par(a,b):
            return True
        return False


def gore():
    SMJER[0] = 90
    return
def dolje():
    SMJER[0] = 270
    return
def lijevo():
    SMJER[0] = 180
    return
def desno():
    SMJER[0] = 0
    return


def pomakni():
    polozaj = ZMIJA[len(ZMIJA)-1]
    x = polozaj.daj_x()
    y = polozaj.daj_y()
    
    if SMJER[0] == 0:
        x += 1 
    if SMJER[0] == 180:
        x -= 1
    if SMJER[0] == 90:
        y += 1
    if SMJER[0] == 270:
        y -= 1
    
    ZMIJA.append(par(x, y))
    goto(40*x, 40*y)
    color('green')
    kvadrat()

    if par(x,y) == HRANA[0]:
        postavi_hranu()
    elif sudar(x,y):
        goto(-100, 0)
        color('green')
        write("GAME OVER", font = ('Arial', 50))
        ranking()
        exit()
    else:
        goto(ZMIJA[0].daj_x()*40, ZMIJA[0].daj_y()*40)
        color('black')
        kvadrat()
        ZMIJA.pop(0)
        
    ontimer(pomakni,plus(350 - 50*len(ZMIJA)))
    return
    


    
def igra():
    reset()
    screensize(800,600)
    title('Snake')
    bgcolor('black')
    hideturtle()
    penup()

    okvir()
    postavi_hranu()
    
    ontimer(pomakni,plus(350-50*len(ZMIJA)))
    onkey(gore,"Up")
    onkey(desno, "Right")
    onkey(lijevo, "Left")
    onkey(dolje, "Down")
    listen()
    mainloop()

igra()    
    
    

    
    
