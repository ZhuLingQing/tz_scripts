import turtle

class tGhost:
    def __init__(self, size = 100):
        self.size = size
        self.pen = turtle.Turtle()
        self.pen.speed(100)
        self.pen.penup()
        self.pen.goto(0, 0)
        
    def Body(self):
        # head
        self.pen.pendown()
        self.pen.right(90)
        self.pen.circle(1 * self.size, -180)
        self.pen.penup()

        # body
        self.pen.goto(self.size * 2, 0)
        self.pen.pendown()
        self.pen.goto(self.size * 2, -1 * self.size)
        self.pen.penup()
        #
        self.pen.goto(0, 0)
        self.pen.pendown()
        self.pen.goto(0, -1 * self.size)
        self.pen.penup()
        
        # tail
        self.pen.pendown()
        self.pen.goto(self.size / 2 * 1, -0.75 * self.size)
        self.pen.goto(self.size / 2 * 2, -1 * self.size)
        self.pen.goto(self.size / 2 * 3, -0.75 * self.size)
        self.pen.goto(self.size / 2 * 4, -1 * self.size)
        self.pen.penup()
        
        # eyes
        self.pen.goto(self.size / 4 * 3, 0)
        self.pen.pendown()
        self.pen.circle(self.size / 4)
        self.pen.penup()
        #
        self.pen.goto(self.size / 4 * 7, 0)
        self.pen.pendown()
        self.pen.circle(self.size / 4)
        self.pen.penup()
        #
        self.pen.goto(self.size / 8 * 6, 0)
        self.pen.pendown()
        self.pen.begin_fill()
        self.pen.fillcolor("black")
        self.pen.circle(self.size / 8)
        self.pen.end_fill()
        self.pen.penup()
        #
        self.pen.goto(self.size / 8 * 14, 0)
        self.pen.pendown()
        self.pen.begin_fill()
        self.pen.fillcolor("black")
        self.pen.circle(self.size / 8)
        self.pen.end_fill()
        self.pen.penup()

    def Done(self):
        # 隐藏画笔
        self.pen.hideturtle()

        # 显示结果
        turtle.done()

g = tGhost()
g.Body()
g.Done()
