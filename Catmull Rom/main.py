import math
from app import App, Point
import numpy as np


#daraus eine Klasse "Kreis" machen
KreismittelpunktListe = [Point(100,700), Point(400,700), Point(700,700)]# daraus in der Klasse nur einen Punkt statt eine Liste machen
RoterKreisradius = 20
wurdeMausGeklickt = [False, False, False]# daraus in der Klasse nur ein boolean statt eine Liste machen
#----
#VektorMittelpunktMaus = (Point(0,0))# mit random Werten initialisiert; für später, dass die Punkt beim anklicken nicht springen


#--- application loop ---#
def loop(t:float): #global, damit in der Funktion auch damit gearbeitet werden kann, nicht nur zum ablesen
    global KreismittelpunktListe 
    ##global VektorMittelpunktMaus
    global wurdeMausGeklickt
    app.clearCanvas()
    
    for i in range(len(KreismittelpunktListe)):
        Abstand = math.sqrt((KreismittelpunktListe[i].x-app.mousePos.x)**2 + (KreismittelpunktListe[i].y-app.mousePos.y)**2)
        
        if app.isMouseButton1Pressed and Abstand <= RoterKreisradius:
                # if not wurdeMausGeklickt: #wenn die Maus davor noch nicht geklickt wurde
                #     VektorMittelpunktMaus = KreismittelpunktListe[i]-app.mousePos
                #     wurdeMausGeklickt[i] = True #updaten, dass Maus geklickt wurde
                KreismittelpunktListe[i] = app.mousePos# - VektorMittelpunktMaus
        # else:
        #     wurdeMausGeklickt[i] = False
        app.drawCircle(KreismittelpunktListe[i],RoterKreisradius,"black","red")

#--- main ---#
app = App("My App", 800, 800)
app.start(loop)