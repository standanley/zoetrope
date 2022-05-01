from tkinter import *
import math
N = 34
M = 34-21

root = Tk()
root.title("Paint Application")
SIZE = 800
root.geometry(f'{SIZE}x{SIZE}')
# create canvas
wn=Canvas(root, width=SIZE, height=SIZE, bg='white')
BRUSH_RADIUS = 8

def rotate(x_corner, y_corner):
    x = x_corner-SIZE/2
    y = y_corner-SIZE/2
    r = (x**2+y**2)**.5
    a = math.atan2(y, x)

    ans = []
    step = 2*math.pi * M/N
    for i in range(N):
        xx = r*math.cos(a+step*i)
        yy = r*math.sin(a+step*i)
        xx_corner = xx + SIZE/2
        yy_corner = yy + SIZE/2
        ans.append((xx_corner, yy_corner))
    return ans

def rotate2(x_corner, y_corner, sat):
    points = rotate(x_corner, y_corner)
    m2 = (points[-2], rainbow(0.7, sat))
    m1 = (points[-1], rainbow(0.85, sat))
    p0 = (points[0], 'black' if sat==1 else 'gray')
    p1 = (points[1], rainbow(0.15, sat))
    p2 = (points[2], rainbow(0.3, sat))
    return [m2, m1, p0, p1, p2]


def rainbow(x, sat):
    def a(y):
        y = y%1
        if y < 1/4:
            return y*4
        elif y < 1/2:
            return 1
        elif y < 3/4:
            return 3-y*4
        else:
            return 0
    def b(z):
        i = int((1-(1-a(z))*sat) * 256)
        if i == 256:
            i -= 1
        h = hex(i)[2:]
        return '0'*(2-len(h))+h

    c = f'#{b(x)}{b(x+1/3)}{b(x+2/3)}'
    #print(c)
    return c
for i in range(13):
    wn.create_oval(10+i*10, 10, 20+i*10, 20, fill=rainbow(i/(13), 1))
    wn.create_oval(10+i*10, 20, 20+i*10, 30, fill=rainbow(i/(13), .5))


def paint(event):
    # get x1, y1, x2, y2 co-ordinates
    color = "black"
    # display the mouse movement inside canvas
    move_brush(event)
    points = rotate2(event.x, event.y, 1)
    for i, (point, color) in enumerate(points):
        x1, y1 = (point[0] - BRUSH_RADIUS), (point[1] - BRUSH_RADIUS)
        x2, y2 = (point[0] + BRUSH_RADIUS), (point[1] + BRUSH_RADIUS)
        #color = 'black' if i==0 else rainbow(i/N, 1)
        wn.create_oval(x1, y1, x2, y2, fill=color, outline=color)

brush_colors = [
    rainbow(0.70, .5),
    rainbow(0.85, .5),
    'gray',
    rainbow(0.15, .5),
    rainbow(0.30, .5),
]
brush_ovals = [wn.create_oval(0, 0, BRUSH_RADIUS*2, BRUSH_RADIUS*2,
                              fill=brush_colors[i])
               for i in range(5)]
def brush(event):
    move_brush(event)

def move_brush(event):
    points = rotate2(event.x, event.y, 0.5)
    #for i, (point, color) in zip([N-2, N-1, 0, 1, 2], points):
    for i, (point, color) in enumerate(points):
        wn.moveto(brush_ovals[i], point[0]-BRUSH_RADIUS, point[1]-BRUSH_RADIUS)


# bind mouse event with canvas(wn)
wn.bind('<Button-1>', paint)
wn.bind('<Motion>', brush)
wn.pack()


wn.create_oval(0, 0, SIZE, SIZE, width=3)
for i in range(N):
    a = i*2*math.pi / N - math.pi/2
    wn.create_line(SIZE/2, SIZE/2, SIZE/2+SIZE/2*math.cos(a), SIZE/2+SIZE/2*math.sin(a))


root.mainloop()
