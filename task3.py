import tkinter as tk
from tkinter import colorchooser
import heapq
# import pyjion
# pyjion.enable()

Point = tuple[int, int]
TkColor = str

DIM = 500

class LineEq:
    p1: Point
    p2: Point

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def get_x(self, y: int) -> int:
        if self.p1[1] == self.p2[1]:
            return self.p1[0]
        return (y - self.p1[1]) * (self.p2[0] - self.p1[0]) // (self.p2[1] - self.p1[1]) + self.p1[0]

    def get_y(self, x: int) -> int:
        if self.p1[0] == self.p2[0]:
            return self.p1[1]
        return (x - self.p1[0]) * (self.p2[1] - self.p1[1]) // (self.p2[0] - self.p1[0]) + self.p1[1]

    def __repr__(self) -> str:
        return f'LineEq({self.p1}, {self.p2})'


class App(tk.Tk):
    canvas: tk.Canvas
    button: tk.Button
    p1: Point
    p2: Point
    p3: Point
    c1: TkColor
    c2: TkColor
    c3: TkColor
    R: int = 10  # radius
    cpoint: str

    def __init__(self):
        super().__init__()
        self.title('Task 3')
        self.geometry(f'{DIM}x{DIM}')
        self.resizable(False, False)
        self.p1 = (100, 100)
        self.p2 = (300, 150)
        self.p3 = (100, 300)
        self.c1 = 'red'
        self.c2 = 'green'
        self.c3 = 'blue'
        self.cpoint = None
        self.create_widgets()
        self.draw_points()
        self.mainloop()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=DIM, height=DIM - 40)
        self.button = tk.Button(self, text='Gradient', command=self.gradient)
        self.canvas.pack()
        self.button.pack()
        # self.canvas.config(height=self.winfo_height() - self.button.winfo_height())
        self.canvas.bind('<B1-Motion>', self.move_point)
        self.canvas.bind('<ButtonPress-1>', self.select_point)
        self.canvas.bind('<ButtonRelease-1>', self.release_point)
        self.canvas.bind('<Button-3>', self.choose_color)

    def draw_points(self):
        self.canvas.create_oval(self.p1[0] - self.R // 2, self.p1[1] - self.R // 2, self.p1[0] + self.R // 2, self.p1[1] + self.R // 2, fill=self.c1)
        self.canvas.create_oval(self.p2[0] - self.R // 2, self.p2[1] - self.R // 2, self.p2[0] + self.R // 2, self.p2[1] + self.R // 2, fill=self.c2)
        self.canvas.create_oval(self.p3[0] - self.R // 2, self.p3[1] - self.R // 2, self.p3[0] + self.R // 2, self.p3[1] + self.R // 2, fill=self.c3)

    def in_point(self, p: Point, x: int, y: int) -> bool:
        return (x - p[0]) ** 2 + (y - p[1]) ** 2 <= self.R ** 2

    def select_point(self, event: tk.Event):
        if self.in_point(self.p1, event.x, event.y):
            self.cpoint = 'p1'
        elif self.in_point(self.p2, event.x, event.y):
            self.cpoint = 'p2'
        elif self.in_point(self.p3, event.x, event.y):
            self.cpoint = 'p3'
        # print(self.cpoint)

    def release_point(self, _):
        self.cpoint = None

    def move_point(self, event: tk.Event):
        if event.x < 0 or event.x > DIM or event.y < 0 or event.y > DIM:
            return
        if self.cpoint == 'p1':
            self.p1 = (event.x, event.y)
        elif self.cpoint == 'p2':
            self.p2 = (event.x, event.y)
        elif self.cpoint == 'p3':
            self.p3 = (event.x, event.y)

        self.canvas.delete('all')
        self.draw_points()

    def choose_color(self, event: tk.Event):
        if self.in_point(self.p1, event.x, event.y):
            self.c1 = colorchooser.askcolor()[1]
        elif self.in_point(self.p2, event.x, event.y):
            self.c2 = colorchooser.askcolor()[1]
        elif self.in_point(self.p3, event.x, event.y):
            self.c3 = colorchooser.askcolor()[1]

        self.canvas.delete('all')
        self.draw_points()

    def gradient(self):
        p1 = min(self.p1, self.p2, self.p3, key=lambda p: p[1])
        p2, p3 = (p for p in (self.p1, self.p2, self.p3) if p != p1)
        if p2[0] > p3[0]:
            p2, p3 = p3, p2
        l1 = LineEq(p1, p2)
        l2 = LineEq(p1, p3)
        print(l1, l2)

        q = [p1[1], p2[1], p3[1]]
        heapq.heapify(q)
        a = heapq.heappop(q)
        b = heapq.heappop(q)

        for y in range(a, b + 1):
            xleft = l1.get_x(y)
            xright = l2.get_x(y)
            for x in range(xleft, xright + 1):
                self.canvas.create_line(x, y, x+1, y, fill='black')

        # TODO: implement gradient
        # 1. get line equations
        # 2. get xleft and xright for each y
        # 3. get color for each x (linear interpolation)
        # 4. draw line with color
        ...


if __name__ == '__main__':
    App()
