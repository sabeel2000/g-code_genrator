from turtle import *
a=open('g_code', 'w')
a.write('%\nO 2000;\nGOO G40 G80 G71 G90 ; (Rapid, Cancel Tool Compensation and Canned Cycle )\nM06 T01;\nG43 Z0.0 H01 ;')

screen = Screen()
screen.setworldcoordinates(-100, -100, 500, 500)
CURSOR_SIZE = 20
FONT_SIZE = 12
FONT = ('Arial', FONT_SIZE, 'bold')

t = Turtle()
t.goto(0, 0)
t.speed(50)
screen.bgcolor('#E6E6FA')


def button(name, x, y, shape, fun, title):
    name = Turtle()
    name.hideturtle()
    name.shape(shape)
    name.fillcolor('red')
    name.pencolor('black')
    name.pensize('500')
    name.penup()
    name.goto(x, y)
    name.write(title, align='center', font=FONT)
    name.sety(y + CURSOR_SIZE + FONT_SIZE)
    name.onclick(fun)
    name.showturtle()

def close(x,y):
    a.write('\nG00 G40 X0.0 Y0.0 M09;\nG00 Z0.0 M06;\nM30;\n%')
    print('Press the code button on the top and \nclick on g_code to view your code')
    screen.bye()


def drill(x, y):
    d = Turtle()

    d.penup()
    d.ht()
    d.shape('circle')

    x, y = float(input('enter coordinates for drilling :\n')), float(input())
    d.setpos(x, y)
    s = float(input('drill size :'))
    dep, feed = float(input('enter depth for drilling :')), float(input('enter feed rate : '))
    r = float(input('enter height of reference plane :'))
    d.dot(s, "sandybrown")
    a.write('\n(turning on canned cycle.....drill size' + str(s) + ')\nG81 G99 M07 X' + str(x) + ' Y' + str(y) + ' Z' + str(dep) + ' R' + str(r) + ' F' + str(feed) + ';')

    while (1):
        b = int(input('drill another hole(1 for yes 0 for no) :'))
        if (b == 0):
            print('turned off drilling cycle.')
            a.write('\nG80 M09                                                 (turned off canned cycle)')
            break
        else:
            x, y = float(input('enter coordinates for next hole :')), float(input())
            d.setpos(x, y)
            d.dot(s, "#E6E6FA")
            a.write('\n x' + str(x) + 'y' + str(y))


def pen(x, y):
    t.color("blue")
    t.setpos(x, y)
    t.dot()
    t.write('(' + str(x) + ',' + str(y) + ')')


def end_mill(x, y):
    d = float(input('enter end mill diameter:'))
    a.write('\n(end milling--end mill diameter=' + str(d) + ')')
    print('\ndefine the path of milling\n[if inner surface is to be cut press 1\nif outer surface to cut press 0]:')
    o = int(input())
    if o == 0:
        o = float(-d / 2)
        set = 41
    else:
        o = float(d / 2)
        set = 42

    a.write('\nM06 TO2;')
    s = int(input('enter spindle speed : '))
    feed = int(input('enter feed rate for milling : '))

    xy = []

    i, f = 0, 1
    while (f == 1):
        print('enter coordinated of', i + 1, 'point :')
        print('(enter c and radius to draw circle) :')
        x, y = input(), float(input())

        if (x == 'c'):
            w = int(input('draw circle on x-axis(0) or y-axis(1) :\n'))
            if w == 1:
                t.right(90)
            angle = int(input('enter angle (anti-clockwise) : \n'))
            t.color('red')
            t.circle(y,
                     extent=angle)

            t.dot()

            u, v = t.pos()
            u, v = "{:.2f}".format(u), "{:.2f}".format(v)
            t.write('(' + str(u) + ',' + str(v) + ')\n')
            xy.append(('c', y, u, v))
            if angle > 0:
                a.write('\nG03 X' + str(u) + ' Y' + str(v) + ' R' + str(y) + ';')
            else:
                a.write('\nG02 X' + str(u) + ' Y' + str(v) + ' R' + str(y) + ';')
        else:
            if (i == 0):
                t.penup()

                x = float(x)
                a.write('\nG01 Z' + str(-th - 5) + ' F' + str(feed) + ';')
                a.write('\nGOO G' + str(set) + ' X' + str(x) + ' Y' + str(y) + ' S' + str(s) + ' MO3')


            else:
                t.pendown()

            xy.append((x, y))
            x = float(x)

            pen(int(x), int(y))

            a.write('\nG00 X' + str(x) + ' Y' + str(y) + ';\n')

        if (i > 0 and x == xy[0][0] and y == xy[0][1]):
            f = 0
            print('milling done---choose next operation')
        i += 1
    print('drawing completed')


# menu

ui_turtle = Turtle()
ui_turtle.ht()
ui_turtle.penup()
ui_turtle.goto(10, 450)
ui_turtle.write("Milling- G-Code Genrator", align="left", font=("Courier", 15, "bold"))

menu = Turtle()
menu.shape('circle')
menu.ht()
menu.penup()
menu.speed(50)
menu.goto(450, 450)
menu.write('menu', align='center', font=FONT)
# menu
p, q = 250, 80
menu.goto(410, 480)
menu.pendown()
menu.width(2)
menu.fd(q)
menu.right(90)
menu.fd(p)
menu.rt(90)
menu.fd(q)
menu.right(90)
menu.fd(p)
menu.rt(90)

button('drill', 450, 390, 'circle', drill, 'drill')
button('mill', 450, 330, 'triangle', end_mill, 'end mill')
button('close', 450, 270, 'square', close, 'close')

# taking input for the side of the workpiece
l = int(input("Enter the length of workpiece   : "))
b = int(input("Enter the breadth of workpiece  : "))
th = int(input("Enter the thickness of workpiece: "))

# set the fillcolor
t.fillcolor('GREY')

# start the filling color
t.begin_fill()

# drawing the square of side s
for _ in range(2):
    t.forward(l)
    t.left(90)
    t.forward(b)
    t.left(90)

# ending the filling of the color
t.end_fill()
t.left(90)

print('select operation to be performed from the menu.')

screen.mainloop()
