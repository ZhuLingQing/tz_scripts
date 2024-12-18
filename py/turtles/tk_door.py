import turtle

# 设置画布和画笔
turtle.setup(width=400, height=400)
door_turtle = turtle.Turtle()
door_turtle.speed(100)
door_turtle.penup()

# 画门的外框并填充黄色
door_turtle.goto(-100, -150)
door_turtle.pendown()
door_turtle.begin_fill()
door_turtle.fillcolor("yellow")
door_turtle.forward(200)
door_turtle.left(90)
door_turtle.forward(300)
door_turtle.left(90)
door_turtle.forward(200)
door_turtle.left(90)
door_turtle.forward(300)
door_turtle.end_fill()
door_turtle.penup()

# 画门把手，放在中间位置
door_turtle.goto(50, 0)
door_turtle.pendown()
door_turtle.begin_fill()
door_turtle.fillcolor("brown")
door_turtle.circle(20)
door_turtle.end_fill()
door_turtle.penup()

# 在门中间显示数字1
door_turtle.goto(-20, 50)
door_turtle.pendown()
door_turtle.write("1", font=("Arial", 50, "bold"))
door_turtle.penup()

# 隐藏画笔
door_turtle.hideturtle()

# 显示结果
# turtle.done()


def door_clicked(x, y):
    # 检查点击位置是否在门的范围内
    if -100 <= x <= 100 and -150 <= y <= 150:
        print("门被点击了")
        # 在点击位置显示一个小笑脸
        door_turtle.goto(x, y)
        door_turtle.write(":)", font=("Arial", 16, "bold"))

# 绑定点击事件
turtle.onscreenclick(door_clicked)

# 隐藏画笔
# door_turtle.hideturtle()

# 开始事件循环
turtle.mainloop()
