import tkinter as tk
from tkinter import colorchooser
from dataclasses import dataclass
# import pyjion
# pyjion.enable()

TkColor = str

DIM = 500

@dataclass
class Point:
    x: int
    y: int

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
    c1: TkColor
    c2: TkColor
    c3: TkColor
    R: int = 5  # radius
    cpoint: str

    def __init__(self):
        super().__init__()
        self.title('Task 3')
        self.geometry(f'{DIM}x{DIM}')
        self.resizable(False, False)
        self.p1 = Point(100, 100)
        self.p2 = Point(300, 150)
        self.p3 = Point(100, 300)
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
        self.canvas.create_oval(self.p1.x - self.R, self.p1.y - self.R, self.p1.x + self.R, self.p1.y + self.R, fill=self.c1)
        self.canvas.create_oval(self.p2.x - self.R, self.p2.y - self.R, self.p2.x + self.R, self.p2.y + self.R, fill=self.c2)
        self.canvas.create_oval(self.p3.x - self.R, self.p3.y - self.R, self.p3.x + self.R, self.p3.y + self.R, fill=self.c3)

    def in_point(self, p: Point, x: int, y: int) -> bool:
        return (x - p.x) ** 2 + (y - p.y) ** 2 <= self.R ** 2

    def select_point(self, event: tk.Event):
        if self.in_point(self.p1, event.x, event.y):
            self.cpoint = 'p1'
        elif self.in_point(self.p2, event.x, event.y):
            self.cpoint = 'p2'
        elif self.in_point(self.p3, event.x, event.y):
            self.cpoint = 'p3'
        print(self.cpoint, event.x, event.y)

    def release_point(self, _):
        self.cpoint = None

    def move_point(self, event: tk.Event):
        if event.x < 0 or event.x > DIM or event.y < 0 or event.y > DIM:
            return
        if self.cpoint == 'p1':
            self.p1 = Point(event.x, event.y)
        elif self.cpoint == 'p2':
            self.p2 = Point(event.x, event.y)
        elif self.cpoint == 'p3':
            self.p3 = Point(event.x, event.y)

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
        ...


if __name__ == '__main__':
    App()
