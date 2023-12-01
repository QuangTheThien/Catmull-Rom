from tkinter import Tk, Frame, Canvas, Label, Entry, Button, Scale, PhotoImage, StringVar, NW, ARC, BOTH, HORIZONTAL, ROUND, END
#from PIL import ImageTk, Image, ImageGrab
from dataclasses import dataclass, field
from collections.abc import Callable
from typing import Any, Union, Optional, Tuple
import time
import io

@dataclass
class Point:
    x:float
    y:float
    handleDx:float = field(default=0)
    handleDy:float = field(default=0)

    def fromTuple(point_tuple):
        x, y = point_tuple
        return Point(x, y)
    def toTuple(self): return (self.x, self.y)
    
    def __repr__(self):
        return f"Point({self.x},{self.y})"
    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def dist(self, other):
        return dist(self.toTuple(), other.toTuple())
    def handle(self, pos:int):
        if pos==-1: return Point(self.x-self.handleDx, self.y-self.handleDy)
        else:      return Point(self.x+self.handleDx, self.y+self.handleDy)
    def m(self):
        if (self.handleDx==0): return float("inf")
        return sign(self.handleDx)*self.handleDy/self.handleDx
    
def dist(p1:Tuple[int,int], p2:Tuple[int,int]) -> float:
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
def sign(x):
    if x>=0: return 1
    else: return -1

class App():

    def __init__(self, title:str, w:int, h:int, x:int=0, y:int=0):
        self.startTime = time.time()
        t = 0.0
        self.window = Tk()
        self.window.title(title)
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        self.loop:Optional[Callable[[float], None]] = None
        self.keyPressed:Optional[str] = None
        self.mousePos:Point= Point(0,0)
        self.isMouseButton1Pressed:bool = False

        self.setupGUI()
        self.update()

    def setupGUI(self):
        self.canvas = Canvas(self.window, bg="white")
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.focus_set()
        self.canvas.bind("<Key>", lambda ev:  self.keyDown(ev))
        self.canvas.bind("<KeyRelease>", lambda ev:  self.keyUp(ev))
        self.canvas.bind("<Button-1>", lambda ev: self.mouseDown(ev))
        self.canvas.bind("<ButtonRelease-1>", lambda ev: self.mouseUp(ev))
        self.canvas.bind("<Motion>", lambda ev: self.mouseMove(ev))

    def clearCanvas(self):
        self.canvas.delete("all")

    def addLabel(self, text:str, fontSize=80, x=0, y=0):
        label = Label(self.window, text=text, font=("Arial", fontSize))
        label.place(x=x, y=y)
        return label

    def addSlider(self, text:str, min:int, max:int, handler:Optional[Callable[[int], None]]=None):
        frame = Frame(self.window)
        label = Label(frame, text=text)
        slider = Scale(frame, from_=min, to=max, orient=HORIZONTAL, command=handler)
        label.grid(row=0, column=0)
        slider.grid(row=0, column=1)
        frame.pack()
        return slider
    
    def addButton(self, text:str, handler:Optional[Callable[[str], None]]=None):
        button = Button(self.window, text=text, command=handler)
        button.pack()
        return button
    
    def addInput(self, text:str, handler:Optional[Callable[[str], None]]=None):
        frame = Frame(self.window)
        label = Label(frame, text=text)
        entry = Entry(frame)
        if handler!=None: entry.bind("<KeyRelease>", lambda ev: handler(entry.get()))
        label.grid(row=0, column=0)
        entry.grid(row=0, column=1)
        frame.pack()
        return entry

    def update(self):
        self.t = time.time()-self.startTime
        if self.loop!=None: self.loop(self.t)
        self.window.after(16, self.update)

    def start(self, loop):
        self.loop = loop
        self.window.mainloop()

    def drawText(self, text:str, pos:Point, size=12):
        self.canvas.create_text(pos.x, pos.y, text=text, font=("Arial", size))

    def drawLine(self, start:Point, end:Point, width=3, fill="black"):
        self.canvas.create_line(start.x, start.y, end.x, end.y, width=width, fill=fill)

    def drawRect(self, pos:Point, w:int, h:int, fill=None, outline="black"):
        self.canvas.create_rectangle(pos.x, pos.y, pos.x+w, pos.y+h, fill=fill, outline=outline)

    def drawPolygon(self, points:list[Point], outline="black", fill=None):
        tuples = [(point.x,point.y) for point in points]
        self.canvas.create_polygon(tuples, fill=fill)

    def drawPath(self, points:list[Point], width=3, fill="black"):
        coords = []
        for point in points:
            coords.append(point.x)
            coords.append(point.y)
        if len(coords)>=4: self.canvas.create_line(*coords, capstyle=ROUND, joinstyle=ROUND, width=width, fill=fill)

    def drawArc(self, pos:Point, w:int, h:int, start:int, extent:int, outline="black", fill=None, width=3):
        self.canvas.create_arc(pos.x, pos.y, pos.x+w, pos.y+h, start=start, extent=extent, fill=fill, outline=outline, style=ARC, width=width)

    def drawCircle(self, pos:Point, r:int, outline="black", fill=None):
        self.canvas.create_oval(pos.x-r, pos.y-r, pos.x+r, pos.y+r, outline=outline, fill=fill)

    def loadImage(self, file:str):
        img = PhotoImage(file=file)
        return img
    
    def drawImage(self, image:Any, x = 0, y = 0):
        self.canvas.create_image(x, y, image=image, anchor=NW)

#    def grabCanvas(self):
#        x1=self.window.winfo_rootx()+self.canvas.winfo_x()
#        y1=self.window.winfo_rooty()+self.canvas.winfo_y()
#        x2=x1+self.canvas.winfo_width()
#        y2=y1+self.canvas.winfo_height()
#        return ImageGrab.grab().crop((x1,y1,x2,y2))
#    
#    def imageFromCanvas(self):
#        postscript_data = self.canvas.postscript(colormode='color')
#        image = Image.open(io.BytesIO(postscript_data.encode()))
#        return image
    
    def hasKey(self): return self.keyPressed!=None
    def consumeKey(self):
        key = self.keyPressed
        self.keyPressed = None
        return key

    def keyDown(self, ev):
        #print(ev.keysym)
        self.keyPressed = ev.keysym
    def keyUp(self, ev):
        #print(ev.keysym)
        self.keyPressed = None
    def mouseDown(self, ev):
        #print("down", ev.x, ev.y)
        self.isMouseButton1Pressed = True
    def mouseUp(self, ev):
        #print("up", ev.x, ev.y)
        self.isMouseButton1Pressed = False
    def mouseMove(self, ev):
        #print("move", ev.x, ev.y)
        self.mousePos = Point(ev.x, ev.y)
