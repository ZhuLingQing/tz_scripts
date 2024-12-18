import turtle

class cordinate_point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __init__(self, point:tuple):
        assert len(point) == 2, "len(point) not 2"
        self.x = point[0]
        self.y = point[1]

class tObject:
    def __init__(self, origin = cordinate_point(0, 0), size = cordinate_point(0, 0)):
        self.origin = origin
        self.size = size
        self.pen = turtle.Turtle()

    def Width(self):
        return self.size.x - self.origin.x
    
    def Height(self):
        return self.size.y - self.origin.y
    
    def Clear(self):

    def Reset(self):
        self.pen.up()
        self.pen.goto(x = self.origin.x, y = self.origin.y)

    def Done(self):
        self.pen.hideturtle()
        turtle.done()