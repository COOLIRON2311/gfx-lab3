import tkinter as tk
from tkinter import colorchooser
from dataclasses import dataclass

import pyjion
pyjion.enable()

TkColor = str
Color = tuple[int, int, int]

DIM = 500


@dataclass
class Point:
    x: int
    y: int
    col: tuple[int, int, int]

    def __init__(self, x, y, col: TkColor | Color) -> None:
        self.x = x
        self.y = y
        if isinstance(col, str):
            self.col = col
        elif isinstance(col, tuple):
            self.col = f'#{col[0]:02x}{col[1]:02x}{col[2]:02x}'

    def to_rgb(self):
        return tuple(int(self.col[i:i+2], 16) for i in (1, 3, 5))


class LineEq:
    p1: Point
    p2: Point

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def get_x(self, y: int) -> int:
        if self.p1.x == self.p2.x:
            return self.p1.x
        return (y - self.p1.y) * (self.p2.x - self.p1.x) // (self.p2.y - self.p1.y) + self.p1.x

    def get_y(self, x: int) -> int:
        if self.p1.y == self.p2.y:
            return self.p1.y
        return (x - self.p1.x) * (self.p2.y - self.p1.y) // (self.p2.x - self.p1.x) + self.p1.y

    def __repr__(self) -> str:
        return f'LineEq({self.p1}, {self.p2})'


class App(tk.Tk):
    canvas: tk.Canvas
    button: tk.Button
    p1: Point
    p2: Point
    p3: Point
    R: int = 5  # radius
    cpoint: str

    def __init__(self):
        super().__init__()
        self.title('Task 3')
        self.geometry(f'{DIM}x{DIM}')
        self.resizable(False, False)
        self.p1 = Point(100, 100, (255, 0, 0))
        self.p2 = Point(300, 150, (0, 255, 0))
        self.p3 = Point(100, 300, (0, 0, 255))
        self.cpoint = None
        self.create_widgets()
        self.draw_points()
        self.mainloop()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=DIM, height=DIM)
        self.button = tk.Button(self, text='Gradient', command=self.gradient)
        self.canvas.pack()
        self.button.pack()
        self.canvas.config(height=self.canvas.winfo_reqheight() - self.button.winfo_reqheight() - 20)
        self.canvas.bind('<B1-Motion>', self.move_point)
        self.canvas.bind('<ButtonPress-1>', self.select_point)
        self.canvas.bind('<ButtonRelease-1>', self.release_point)
        self.canvas.bind('<Button-3>', self.choose_color)

    def gradient_pixel(self, x: int, y: int, col: TkColor):
        self.canvas.create_line(x, y, x + 1, y, fill=col)

    def draw_points(self):
        self.canvas.create_oval(self.p1.x - self.R, self.p1.y - self.R, self.p1.x + self.R, self.p1.y + self.R, fill=self.p1.col)
        self.canvas.create_oval(self.p2.x - self.R, self.p2.y - self.R, self.p2.x + self.R, self.p2.y + self.R, fill=self.p2.col)
        self.canvas.create_oval(self.p3.x - self.R, self.p3.y - self.R, self.p3.x + self.R, self.p3.y + self.R, fill=self.p3.col)

    def in_point(self, p: Point, x: int, y: int) -> bool:
        return (x - p.x) ** 2 + (y - p.y) ** 2 <= self.R ** 2

    def select_point(self, event: tk.Event):
        if self.in_point(self.p1, event.x, event.y):
            self.cpoint = 'p1'
        elif self.in_point(self.p2, event.x, event.y):
            self.cpoint = 'p2'
        elif self.in_point(self.p3, event.x, event.y):
            self.cpoint = 'p3'
        # print(self.cpoint, event.x, event.y)

    def release_point(self, _):
        self.cpoint = None

    def move_point(self, event: tk.Event):
        if event.x < 0 or event.x > DIM or event.y < 0 or event.y > DIM:
            return
        if self.cpoint == 'p1':
            self.p1 = Point(event.x, event.y, self.p1.col)
        elif self.cpoint == 'p2':
            self.p2 = Point(event.x, event.y, self.p2.col)
        elif self.cpoint == 'p3':
            self.p3 = Point(event.x, event.y, self.p3.col)

        self.canvas.delete('all')
        self.draw_points()

    def choose_color(self, event: tk.Event):
        if self.in_point(self.p1, event.x, event.y):
            self.p1.col = colorchooser.askcolor()[1]
        elif self.in_point(self.p2, event.x, event.y):
            self.p2.col = colorchooser.askcolor()[1]
        elif self.in_point(self.p3, event.x, event.y):
            self.p3.col = colorchooser.askcolor()[1]

        self.canvas.delete('all')
        self.draw_points()

    def lin_col_interp(self, c1: Color, c2: Color, t: float) -> Color:
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        return (r, g, b)

    def gradient(self):
        def rgb2str(col: Color) -> TkColor:
            return f'#{col[0]:02x}{col[1]:02x}{col[2]:02x}'

        p1, p2, p3 = sorted([self.p1, self.p2, self.p3], key=lambda p: p.y)
        l1 = LineEq(p1, p3)
        l2 = LineEq(p1, p2)

        c1 = p1.to_rgb()
        c2 = p2.to_rgb()
        c3 = p3.to_rgb()

        hleft = p3.y - p1.y
        hright = p2.y - p1.y
        for y in range(p1.y, p2.y + 1):
            tl = 0 if hleft == 0 else (y - p1.y) / hleft
            tr = 0 if hright == 0 else (y - p1.y) / hright
            cl = self.lin_col_interp(c1, c3, tl)
            cr = self.lin_col_interp(c1, c2, tr)
            xl, xr = l1.get_x(y), l2.get_x(y)
            if xl > xr:
                xl, xr = xr, xl
                cl, cr = cr, cl
            for x in range(xl, xr + 1):
                t = 0 if xl == xr else (x - xl) / (xr - xl)
                cx = self.lin_col_interp(cl, cr, t)
                self.gradient_pixel(x, y, rgb2str(cx))

        l1 = LineEq(p1, p3)
        l2 = LineEq(p2, p3)
        hleft = p3.y - p1.y
        hright = p3.y - p2.y
        for y in range(p2.y, p3.y + 1):
            tl = 0 if hleft == 0 else (y - p1.y) / hleft
            tr = 0 if hright == 0 else (y - p2.y) / hright
            cl = self.lin_col_interp(c1, c3, tl)
            cr = self.lin_col_interp(c2, c3, tr)
            xl, xr = l1.get_x(y), l2.get_x(y)
            if xl > xr:
                xl, xr = xr, xl
                cl, cr = cr, cl
            for x in range(xl, xr + 1):
                t = 0 if xl == xr else (x - xl) / (xr - xl)
                cx = self.lin_col_interp(cl, cr, t)
                self.gradient_pixel(x, y, rgb2str(cx))
                # self.gradient_pixel(x, y, 'black')


if __name__ == '__main__':
    App()
