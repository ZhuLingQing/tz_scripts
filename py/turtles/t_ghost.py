import turtle, math, time
from turtle import *
from t_object import *
from t_cordinate import tCordinate

class tGhost(tObject):
    def __init__(self, color = (.9,.9,.9), bgColor = 'white', origin=Vec2D(0, 0), size = 100, autoUpdate:bool = True):
        super().__init__(color = color, bgColor=bgColor, origin=origin, size = size/2)
        # self.topLeft = Vec2D(0, size[1]) if isinstance(size, Vec2D) else Vec2D(0, size)
        # self.btmRight = Vec2D(size[0], 0) if isinstance(size, Vec2D) else Vec2D(size, 0)
        if autoUpdate is True: self.Update()
        
    def _body(self, size, fillColor, penColor = 'black'):
        self.pendown()
        self.pencolor(penColor)
        self.begin_fill()
        self.fillcolor(fillColor)
        self.setheading(90)
        self.forward(size)
        self.circle( -size, 180)
        self.forward(size)
        self.setheading(150)
        self.forward(size/2/math.sin(math.radians(60)))
        self.setheading(210)
        self.forward(size/2/math.sin(math.radians(60)))
        self.setheading(150)
        self.forward(size/2/math.sin(math.radians(60)))
        self.setheading(210)
        self.forward(size/2/math.sin(math.radians(60)))
        self.end_fill()
        self.penup()
        
    def _eyes(self, size, left:bool):
        # eyes
        if left is True:
            self.goto(Vec2D(size / 4 * 3, size) + self.origin)
        else:
            self.goto(Vec2D(size / 4 * 3 + size, size) + self.origin)
        self.setheading(90)
        self.pendown()
        self.begin_fill()
        self.fillcolor(self.bgColor)
        self.circle(size / 4)
        self.end_fill()
        #
        self.begin_fill()
        self.fillcolor("black")
        self.circle(size / 8)
        self.end_fill()
        self.penup()
        
    def Update(self):
        self.GotoOrigin()
        self._body(fillColor = self.color, size = self.size[0])
        self._eyes(left = True, size = self.size[0])
        self._eyes(left = False, size = self.size[0])
        super().Update()
        
    def Erase(self):
        if self.GetSize() == Vec2D(0, 0): return
        self.GotoOrigin()
        self._body(fillColor = self.bgColor, penColor = self.bgColor, size = self.size[0])
        super().Update()

if __name__ == '__main__':
    ghosts = [
        tGhost(color=(1,1,1), origin=Vec2D(-300,-100), size = 200, autoUpdate = False),
        tGhost(color=(1,1,1), origin=Vec2D(0,0), size = 100, autoUpdate = False),
        tGhost(color=(1,1,1), origin=Vec2D(300,0), size = 150, autoUpdate = False),
    ]
    cor = tCordinate(size=Vec2D(800, 600), tick = 20)
    for g in ghosts:
        g.Update()
        time.sleep(0.5)
    # time.sleep(1)
    for g in ghosts:
        g.Erase()
        time.sleep(0.5)
    cor.Update()
    tGhost.Done()