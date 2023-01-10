import math as mth
from pyglet import *
from pyglet.gl import *
from pyglet import shapes
import numpy as np
from sympy import cos
from inputSection import processInput 

def srediste(v):
    maxVs = v.max(axis=0)
    minVs = v.min(axis=0)
    return [(minVs[0]+maxVs[0]) / 2, (minVs[1]+maxVs[1]) / 2, (minVs[2]+maxVs[2]) / 2]

def scale(point, maxVcoord,sredisteOfPoint):
    return 2*(point-sredisteOfPoint)/(maxVcoord)

def makeSpiral(Vspir):
    spiral = []
    for i in range(0, 10):
        if i == 8:
            r = Vspir [i:]
            break
        else:
            r = Vspir [i:i+4]
        
        p_t = lambda t : np.matmul(T3(t), np.matmul(B3, r))/6
        for t in range(0, 11):
            spiral.append(list(p_t(t/10)))
    return spiral

def makeSpiralRotation(Vspir):
    osLista = []
    kuteviLista = []
    for i in range(0, 10):
        if i == 8:
            r = Vspir [i:]
            break
        else:
            r = Vspir [i:i+4]
        
        p_t_derivatev = lambda t : np.matmul(T2(t), np.matmul(B2, r))/2
        for t in range(0, 11):
            startOrientation = p_t_derivatev(t/10)
            if t == 10: endOrientation = p_t_derivatev(0)
            else: endOrientation = p_t_derivatev(t/10)
            osLista.append(list((np.cross(startOrientation, endOrientation))))
            cosiunsKuta = np.matmul(startOrientation,endOrientation) / (np.linalg.norm(startOrientation)*np.linalg.norm(endOrientation))
            if cosiunsKuta < -1: cosiunsKuta = -1
            if cosiunsKuta > 1: cosiunsKuta = 1
            kuteviLista.append(mth.acos(cosiunsKuta) * 180/mth.pi)
    return osLista, kuteviLista
    

def drawPoligon(f, v, tockaSpirale, osRotacije, kutRotacije):
    for i in f:
        glBegin(gl.GL_LINE_LOOP)
        firstPoint = [v[int(i[0]) - 1][0], v[int(i[0]) - 1][1], v[int(i[0]) - 1][2]]
        secondPoint = [v[int(i[1]) - 1][0], v[int(i[1]) - 1][1], v[int(i[1]) - 1][2]]
        thirdPoint = [v[int(i[2]) - 1][0], v[int(i[2]) - 1][1], v[int(i[2]) - 1][2]]
        glVertex2f(firstPoint[0]*125 + 525 + tockaSpirale[0]*5, firstPoint[1]*125+325+ tockaSpirale[1]*5)
        glVertex2f(secondPoint[0]*125+525+ tockaSpirale[0]*5, secondPoint[1]*125+325+ tockaSpirale[1]*5)
        glVertex2f(thirdPoint[0]*125+525+ tockaSpirale[0]*5, thirdPoint[1]*125+325+ tockaSpirale[1]*5)
        glEnd()
        #glRotatef(kutRotacije, osRotacije[0], osRotacije[1], osRotacije[2])

def drawTrajectory(spirala):
    for tockaSpirale in spirala:
        pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,('v2i', (int(tockaSpirale[0])*5 + 525, int(tockaSpirale[1])*5+ 325)))


width = 1000
height = 720
title = "Title"
window = pyglet.window.Window(width, height, title)
batch = pyglet.graphics.Batch()
#Konstante
B3 = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
B2 = np.array([[-1, 3, -3, 1], [2, -4, 2, 0], [-1, 0, 1, 0]])
T3 = lambda t : np.array([t*t*t, t*t, t, 1])
T2 = lambda t : np.array([t*t, t, 1])

"izvlacenje parametara iz fileova"
v, f =  processInput.getVF('bird.obj')
vSpir, fSpir = processInput.getVF('spiralaNew.obj')

#racunanje sredista i max kordinata
sredisteLista = srediste(v)
maxVcoord = np.amax(v)
for point in v:
    for p in range(len(point)):
        v[p] = scale(v[p], maxVcoord, sredisteLista[p])

sredisteListaSpirala = srediste(vSpir)
maxVcoordSpirala = np.amax(vSpir)
for point in vSpir:
    for p in range(len(point)):
        vSpir[p] = scale(vSpir[p], maxVcoordSpirala, sredisteListaSpirala[p])


putanjaSPirale = makeSpiral(vSpir)
osLista, kuteviLista = makeSpiralRotation(vSpir)




pom = 0
@window.event
def on_key_press(symbol, modifer):
    if symbol == pyglet.window.key.A:
        window.clear()
        drawTrajectory(putanjaSPirale)
        global pom
        drawPoligon(f, v, putanjaSPirale[pom], osLista[pom], kuteviLista[pom])        
        pom = pom + 1
        

    

def scale(x, M,vs):
    return 2*(x-vs)/(M)

pyglet.app.run()
