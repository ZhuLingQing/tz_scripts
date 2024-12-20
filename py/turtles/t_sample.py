import turtle, time

# 创建一个画布和一个画笔
screen = turtle.Screen()
pen = turtle.Turtle()

# 设置画笔的速度
# pen.speed(0)
turtle.tracer(0, 0)
pen.hideturtle()

# 绘制一个正方形的函数
def draw_square(color, size):
    for _ in range(4):
        pen.pencolor(color)
        pen.forward(size)  # 向前移动
        pen.right(90)      # 向右转90度
    turtle.update()

# 移动画笔到一个起始位置
pen.penup()
pen.goto(-100, -100)
pen.pendown()
print("Start",end='>')
# 绘制并移动正方形
for _ in range(10):  # 绘制4个正方形，使其看起来像是在移动
    pen.pendown()     # 放下画笔，准备绘制
    draw_square(color='black', size=100)
    print("Move",end='>')
    time.sleep(0.5)
    draw_square(color='white', size=100)
    pen.penup()       # 提起画笔，移动时不绘制
    pen.forward(10)  # 向前移动画笔，准备绘制下一个正方形
print('Done')
# 结束绘图
turtle.done()
