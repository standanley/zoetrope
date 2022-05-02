from tkinter import *
import math
N = 21
M = 21-13

root = Tk()
root.title("Paint Application")
SIZE = 800
root.geometry(f'{SIZE}x{SIZE}')
# create canvas
wn=Canvas(root, width=SIZE, height=SIZE, bg='white')
BRUSH_RADIUS = 8


class Point:
    angle_offset = 0

    def __init__(self, pos):
        if pos == None:
            self.cursor = True
            self.pos = (0, 0)
        else:
            self.cursor = False
            self.pos = self.rotate(*pos, -self.angle_offset)

        self.circles = []
        self.create_circles()

    def create_circles(self):
        #colors = ['blue', 'purple', 'black', 'red', 'orange']
        sat = 0.5 if self.cursor else 1
        colors = [
            rainbow(4/6, sat),
            rainbow(5/6, sat),
            'gray' if self.cursor else 'black',
            rainbow(1/12, sat),
            rainbow(2/12, sat)
        ]
        for i in range(5):
            circle = wn.create_oval(0, 0, BRUSH_RADIUS*2, BRUSH_RADIUS*2, fill=colors[i], outline=colors[i])
            self.circles.append(circle)
        self.move_circles()

    def move_circles(self):
        assert len(self.circles) == 5
        points = self.get_copies()
        for i, point in enumerate(points):
            x1, y1 = (point[0] - BRUSH_RADIUS), (point[1] - BRUSH_RADIUS)
            wn.moveto(self.circles[i], x1, y1)

    def set_pos(self, new_pos):
        self.pos = new_pos
        self.move_circles()

    def rotate(self, x_corner, y_corner, angle):
        x = x_corner - SIZE / 2
        y = y_corner - SIZE / 2
        r = (x ** 2 + y ** 2) ** .5
        a = math.atan2(y, x)

        xx = r * math.cos(a + angle)
        yy = r * math.sin(a + angle)
        xx_corner = xx + SIZE / 2
        yy_corner = yy + SIZE / 2
        return xx_corner, yy_corner

    def get_copies(self):
        offset = 0 if self.cursor else self.angle_offset
        ans = []
        step = 2 * math.pi * M / N
        for i in range(-2, 3):
            ans.append(self.rotate(*self.pos, i*step + offset))
        return ans

    def set_copies_hide(self):
        for i in [0, 1, 3, 4]:
            wn.itemconfigure(self.circles[i], state='hidden')
    def set_copies_show(self):
        for i in [0, 1, 3, 4]:
            wn.itemconfigure(self.circles[i], state='normal')

    def delete(self):
        # I don't actually know how to delete, so I just hide?
        for i in range(5):
            wn.itemconfigure(self.circles[i], state='hidden')





def rainbow(x, sat):
    def a(y):
        y = (1/6+y)%1
        if y < 2/6:
            return 1
        elif y < 3/6:
            return 1-(y-2/6)*6
        elif y < 5/6:
            return 0
        else:
            return (y-5/6)*6
    def b(z):
        i = int((1-(1-a(z))*sat) * 256)
        if i == 256:
            i -= 1
        h = hex(i)[2:]
        return '0'*(2-len(h))+h

    c = f'#{b(x)}{b(x+2/3)}{b(x+1/3)}'
    #print(c)
    return c


points = []
cursor = Point(None)

for i in range(13):
    wn.create_oval(10+i*10, 10, 20+i*10, 20, fill=rainbow(i/(13), 1))
    wn.create_oval(10+i*10, 20, 20+i*10, 30, fill=rainbow(i/(13), .5))


def mouse_move(event):
    cursor.set_pos((event.x, event.y))

#brush_colors = [
#    rainbow(0.70, .5),
#    rainbow(0.85, .5),
#    'gray',
#    rainbow(0.15, .5),
#    rainbow(0.30, .5),
#]
#brush_ovals = [wn.create_oval(0, 0, BRUSH_RADIUS*2, BRUSH_RADIUS*2,
#                              fill=brush_colors[i])
#               for i in range(5)]
def mouse_click(event):
    point = Point((event.x, event.y))
    points.append(point)

def arrow_left(event):
    Point.angle_offset += 2*math.pi * M/N
    for point in points:
        point.move_circles()

def arrow_right(event):
    #print('arrowing')
    Point.angle_offset -= 2*math.pi * M/N
    #print(Point.angle_offset)
    for point in points:
        point.move_circles()

def show(event):
    cursor.set_copies_show()
    for point in points:
        point.set_copies_show()

def hide(event):
    cursor.set_copies_hide()
    for point in points:
        point.set_copies_hide()

def save(event):
    print('[')
    for point in points:
        print(f'\t{point.pos},')
    print(']')

def backspace(event):
    points[-1].delete()
    points.pop()



# bind mouse event with canvas(wn)
wn.bind('<Button-1>', mouse_click)
wn.bind('<Motion>', mouse_move)
wn.bind('<Right>', arrow_right)
wn.bind('<space>', arrow_right)
wn.bind('<Left>', arrow_left)
wn.bind('<h>', hide)
wn.bind('<u>', show)
wn.bind('<s>', save)
wn.bind('<BackSpace>', backspace)
wn.focus_set()
wn.pack()


wn.create_oval(0, 0, SIZE, SIZE, width=3)
for i in range(N):
    a = i*2*math.pi / N - math.pi/2
    wn.create_line(SIZE/2, SIZE/2, SIZE/2+SIZE/2*math.cos(a), SIZE/2+SIZE/2*math.sin(a))


root.mainloop()
