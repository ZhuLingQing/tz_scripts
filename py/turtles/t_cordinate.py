import turtle, math, time
from t_object import *

class tCordinate(tObject):
    def __init__(self, color = 'black', bgColor = 'white', size = Vec2D(400, 400), tick:int = 10):
        super().__init__(color = color, bgColor = bgColor, size = size)
        self.tick = tick
        self.arrow_size = 4
        self.Update()
        
    def _axis(self):
        x_size = self.size[0]
        y_size = self.size[1]
        # 绘制x轴
        self.penup()
        self.goto(-x_size, 0)
        self.pendown()
        self.goto(x_size, 0)
        # 绘制x箭头
        self.begin_fill()
        self.fillcolor(self.color)
        self.goto(x_size - self.arrow_size, self.arrow_size / -2)
        self.goto(x_size - self.arrow_size, self.arrow_size / 2)
        self.goto(x_size, 0)
        self.end_fill()
        # 绘制x刻度
        for x in range(-x_size, x_size, self.tick):
            self.penup()
            self.goto(x, 0)
            self.pendown()
            self.goto(x, 2)
            
        # 绘制y轴
        self.penup()
        self.goto(0, -y_size)
        self.pendown()
        self.goto(0, y_size)
        # 绘制y箭头
        self.begin_fill()
        self.fillcolor(self.color)
        self.goto(self.arrow_size / -2, y_size - self.arrow_size)
        self.goto(self.arrow_size / 2, y_size - self.arrow_size)
        self.goto(0, y_size)
        self.end_fill()
        # 绘制y刻度
        for y in range(-y_size, y_size, self.tick):
            self.penup()
            self.goto(0, y)
            self.pendown()
            self.goto(2, y)
        super().Update()
        
    def Update(self):
        self._axis()

if __name__ == '__main__':
    cor = tCordinate(size=Vec2D(800, 600), tick = 20)
    # cor.Update()
    cor.Done()