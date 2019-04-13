KINO = []

def slika():
    for i in range(10):
        for j in range(10):
            print(KINO[i][j],end=' ')
        print()




    
for i in range(10):
    LISTA = []
    for j in range(10):
        LISTA = LISTA + [None]
    KINO = KINO + [LISTA]

ex = True
while ex:
    redak = int(input('Unesite red: '))
    if redak == 0:
        ex = False
    else:
        stupac = int(input('Unesite sjedalo: '))
        ime = input('Ime: ')
        KINO[redak-1][stupac-1] = ime
        slika()
    
                     
    
        
