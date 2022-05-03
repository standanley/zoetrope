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

    def dist(self, x, y):
        # use copies just to get rotation
        c = self.get_copies()[2]
        return ((x-c[0])**2 + (y-c[1])**2)**0.5






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

def nearest_point(x, y):
    if len(points) == 0:
        return None, float('inf')
    dist, point = min((p.dist(x, y), p) for p in points)
    return point, dist



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
    x, y = event.x, event.y
    p, dist = nearest_point(x, y)
    if dist < BRUSH_RADIUS:
        # delete
        p.delete()
        points.pop(points.index(p))
    else:
        # create
        point = Point((x, y))
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


def load(ps):
    for xy in ps:
        points.append(Point(xy))


wn.create_oval(0, 0, SIZE, SIZE, width=3)
for i in range(N):
    a = i*2*math.pi / N - math.pi/2
    wn.create_line(SIZE/2, SIZE/2, SIZE/2+SIZE/2*math.cos(a), SIZE/2+SIZE/2*math.sin(a))


ps = [
    (398.0, 216.99999999999997),
    (539.2384067167926, 517.7185885702384),
    (215.29551488880895, 429.2788862460616),
    (506.1407982219533, 234.77551345878965),
    (448.21460480738205, 603.4584770494166),
    (206.25214062763158, 279.1415415098101),
    (647.7678062199457, 357.0568491962283),
    (228.99364905388984, 603.8083117443836),
    (404.3788745640529, 131.35557802635788),
    (560.7271291177301, 600.0769601067861),
    (165.57004739631338, 359.5574812575521),
    (583.6975098620157, 279.5623610722353),
    (362.2430520030032, 598.250883675085),
    (284.53708105552647, 246.20040848941784),
    (582.2602170282169, 416.3160439085975),
    (265.7657529973841, 521.9268917492802),
    (399.00000000000045, 191.99999999999997),
    (534.9842208779982, 555.7698947613428),
    (202.4532054839826, 373.1622658101248),
    (557.1184972143416, 293.88789968572416),
    (359.5322678243157, 567.8432681180782),
    (323.9523324987556, 261.83071156143205),
    (534.12702160829, 445.999370370575),
    (275.58657048909805, 454.50961894322717),
    (459.0555452705065, 269.6142547177677),
    (443.8931917770805, 546.4595087920904),
    (257.7314032290724, 310.861644771562),
    (579.743635509049, 373.500462381578),
    (272.5136461725277, 549.4898979455686),
    (400.98442703529906, 149.14539887932656),
    (577.6108622074214, 577.5172713454563),
    (145.075907656362, 406.3013603906077),
    (578.2375196014425, 205.43282238176607),
    (219.76326216380744, 576.5324852092883),
    (655.8557158515243, 406.8449007373424),
    (232.30853501673326, 205.80017360521197),
    (375.2195657674978, 658.8859402888628),
    (404.9847397979937, 675.439925154554),
    (204.80131945233842, 191.26218571506507),
    (610.2775479024028, 218.64026673996054),
    (694.4170388700521, 431.29867765561687),
    (148.09430265399462, 569.686533480482),
    (104.92658893715924, 392.47124952334),
    (628.0396719436887, 609.0237020526973),
    (486.30148486282974, 103.2542271396764),
    (526.328836537144, 687.6769456511445),
    (114.77722933711135, 259.05330406360974),
    (710.4313013432866, 323.2835927176359),
    (215.10818705142222, 659.4745026097711),
    (368.16616506448344, 86.45318219873724),
]
load(ps)

root.mainloop()


