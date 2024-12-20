import turtle, sys, os
from turtle import *

class tObject(Turtle):
    initiated = False
    on_click_event = []
    def __init__(self, color:str = 'black', bgColor:str = 'white', origin = Vec2D(0, 0), size = None):
        super().__init__()
        self.Factory()
        self.color = color
        self.bgColor = bgColor
        self.origin = origin
        self.Resize(size)
        self.topLeft = self.origin + Vec2D(0, self.size[1])
        self.btmRight = self.origin + Vec2D(self.size[0], 0)
        turtle.onscreenclick(tObject.OnClickEvent)
    
    def Factory(self):
        if tObject.initiated is False:
            tObject.initiated = True
            turtle.setup(width=1200, height=800)
            turtle.tracer(0, 0)
        self.hideturtle()
        self.speed(0)
        self.penup()
        
    def Resize(self, size):
        if isinstance(size, int) or isinstance(size, float):
            self.size = Vec2D(size, size)
        elif isinstance(size, Vec2D):
            self.size = size
        elif size == None:
            self.size = None
        else:
            assert False, f'Invalid size'
    
    def GetSize(self):
        return self.btmRight - self.topLeft
    
    def GotoOrigin(self, penUp:bool = True):
        if penUp == True: self.up()
        self.goto(self.origin)
        
    def Update(self):
        self.penup()
        turtle.update()
    
    def Erase(self):
        if self.GetSize() == Vec2D(0, 0): return
        self.GotoOrigin()
        self.down()
        self.color(self.bgColor)
        self.begin_fill()
        self.fillcolor(self.bgColor)
        self.goto(self.topLeft[0], self.topLeft[1])
        self.goto(self.topLeft[0], self.btmRight[1])
        self.goto(self.btmRight[0], self.btmRight[1])
        self.goto(self.btmRight[0], self.topLeft[1])
        self.goto(self.topLeft)
        self.end_fill()
        self.up()
        turtle.update()
        self.color(self.color)

    @staticmethod
    def RegistEventObj(obj):
        tObject.on_click_event.append(obj)
        
    @staticmethod
    def OnClickEvent(x, y):
        for obj in tObject.on_click_event:
            if obj.topLeft[0] <= x <= obj.btmRight[0] and obj.btmRight[1] <= y <= obj.topLeft[1]:
                obj.OnClicked()
        
    @staticmethod
    def Done():
        # turtle.done()
        turtle.mainloop()
        
class tPolyGon(tObject):
    def __init__(self, color:str = 'black', bgColor:str = 'white', origin = Vec2D(0, 0)):
        super().__init__(color, bgColor, origin)
        
    def Tops(self, l:tuple[Vec2D], close:bool = True):
        self.GotoOrigin()
        self.down()
        if close is True:
            self.begin_fill()
            self.fillcolor(self.bgColor)
        for v in l:
            self.goto(v[0], v[1])
        if close is True:
            self.GotoOrigin(False)
            self.end_fill()
        self.up()
        turtle.update()
        
    def Regular(self, len:float, angle:float, close:bool = True):
        self.GotoOrigin()
        self.down()
        v = Vec2D(self.pos())
        
# class tTriangle(tObject):
#     def __init__(self, color:str = 'black', bgColor:str = 'white', origin = Vec2D(0, 0), size = Vec2D(0, 0)):
#         super().__init__(color, bgColor, origin, size)
        
#     def Update(self, vertex:list):
#         assert len(vertex) == 3, 'len(vertex) of tTriangle must be 3'
        
if __name__ == '__main__':
    rect = tPolyGon(bgColor='yellow')
    rect.Tops((Vec2D(0,200), Vec2D(100,200), Vec2D(100,0)))
    rect.Done()