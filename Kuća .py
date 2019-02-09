from turtle import *
reset()

penup()
goto(-100, -100)
pendown()
dot(20, 'red')
penup()
goto(100, -100)
pendown()
dot(20, 'yellow')
penup()
goto(100, 100)
pendown()
dot(20, 'black')
penup()
goto(0, 200)
pendown()
dot(20, 'green')
penup()
goto(-100, 100)
pendown()
dot(20, 'blue')
penup()

check = 1
while check == 1:
    garm = input()
    if garm == 'green':
        goto(0, 200)
        check = 0
    elif garm == 'red':
        goto(-100, -100)
        check = 0
    elif garm == 'black':
        goto(100, 100)
        check = 0
    elif garm == 'yellow':
        goto(100, -100)
        check = 0 
    elif garm == 'blue':
        goto(-100, 100)
        check = 0

pendown()    
pokusaj = 8
while pokusaj > 0:
    garm = input()
    if garm == 'green':
        goto(0, 200)
        pokusaj = pokusaj -1
    elif garm == 'red':
        goto(-100, -100)
        pokusaj = pokusaj -1
    elif garm == 'black':
        goto(100, 100)
        pokusaj = pokusaj -1
    elif garm == 'yellow':
        goto(100, -100)
        pokusaj = pokusaj -1
    elif garm == 'blue':
        goto(-100, 100)
        pokusaj = pokusaj -1
        
print('Odu svi pokušaji bolan!')  
