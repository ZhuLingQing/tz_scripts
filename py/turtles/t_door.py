import turtle, math, time
from turtle import *
from t_object import *
from t_cordinate import tCordinate

class tDoor(tObject):
    def __init__(self, color = 'yellow', handleColor = 'brown', bgColor = 'white', origin=Vec2D(0, 0), size = (100, 200), autoUpdate:bool = True, handleLeft:bool = False):
        super().__init__(color = color, bgColor=bgColor, origin=origin, size = size if isinstance(size,Vec2D) or isinstance(size,tuple) else Vec2D(size, size *2))
        self.handleColor = handleColor
        self.handleLeft = handleLeft
        self._isOpen = False
        self.frame_width = self.size[0] / 16
        super().RegistEventObj(self)
        if autoUpdate is True: self.Update()
        
    def _door(self, fillColor, penColor = 'black'):
        self.pendown()
        self.pencolor(penColor)
        self.begin_fill()
        self.fillcolor(fillColor)
        self.setheading(0)
        self.forward(self.size[0])
        self.setheading(90)
        self.forward(self.size[1])
        self.setheading(180)
        self.forward(self.size[0])
        self.setheading(-90)
        self.forward(self.size[1])
        self.end_fill()
        self.penup()
        
    def _frame(self, penColor = 'black'):
        fillColor = self.bgColor
        self.setheading(0)
        self.forward(self.frame_width)
        self.pendown()
        self.pencolor(penColor)
        self.begin_fill()
        self.fillcolor(fillColor)
        self.setheading(0)
        self.forward(self.size[0] - 2 * self.frame_width)
        self.setheading(90)
        self.forward(self.size[1] - self.frame_width)
        self.setheading(180)
        self.forward(self.size[0] - 2 * self.frame_width)
        self.setheading(-90)
        self.forward(self.size[1] - self.frame_width)
        self.end_fill()
        self.penup()
        
    def _handle(self, left:bool):
        if left is True:
            self.goto(self.origin + Vec2D(self.size[0]/8*1, self.size[1]/2))
            self.setheading(-90)
        else:
            self.goto(self.origin + Vec2D(self.size[0]/8*7, self.size[1]/2))
            self.setheading(90)
        self.pendown()
        self.begin_fill()
        self.fillcolor(self.handleColor)
        self.circle(self.size[0]/8)
        self.end_fill()
        self.penup()
        
    def Update(self):
        self.GotoOrigin()
        self._door(fillColor = self.color)
        if self._isOpen is True:
            self._frame()
        else:
            self._handle(left = self.handleLeft)
        super().Update()
        
    def Open(self, autoUpdate:bool = True):
        self._isOpen = True
        if autoUpdate is True: self.Update()
        
    def Close(self, autoUpdate:bool = True):
        self._isOpen = False
        if autoUpdate is True: self.Update()
        
    def isOpen(self):
        return self._isOpen
        
    def Erase(self):
        if self.size == Vec2D(0, 0): return
        self.GotoOrigin()
        self._door(fillColor = self.bgColor)
        super().Update()
        
    def OnClicked(self):
        self._isOpen = not self._isOpen
        self.Update()
        return True

if __name__ == '__main__':
    cor = tCordinate(size=Vec2D(800, 600), tick = 20)
    doors = [
        tDoor(origin=Vec2D(-300,-100), size = 200, autoUpdate = True),
        tDoor(origin=Vec2D(0,0), size = 100, autoUpdate = True),
        tDoor(origin=Vec2D(300,0), size = 150, autoUpdate = True),
    ]
    tObject.Done()