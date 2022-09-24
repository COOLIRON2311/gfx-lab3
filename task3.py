import tkinter as tk
from tkinter import colorchooser

Point = tuple[int, int]
TkColor = str

DIM = 500


class App(tk.Tk):
    canvas: tk.Canvas
    p1: Point
    p2: Point
    p3: Point
    c1: TkColor = 'red'
    c2: TkColor = 'green'
    c3: TkColor = 'blue'
    R: int = 10  # radius
    cpoint: str

    def __init__(self):
        super().__init__()
        self.title("Task 3")
        self.geometry(f"{DIM}x{DIM}")
        self.resizable(False, False)
        self.canvas = tk.Canvas(self, width=DIM, height=DIM)
        self.p1 = (100, 100)
        self.p2 = (300, 100)
        self.p3 = (100, 300)
        self.cpoint = None
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.move_point)
        self.canvas.bind("<ButtonPress-1>", self.select_point)
        self.canvas.bind("<ButtonRelease-1>", self.release_point)
        self.canvas.bind("<Button-3>", self.choose_color)
        self.draw_points()
        self.mainloop()

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

    def release_point(self, _):
        self.cpoint = None

    def move_point(self, event: tk.Event):
        if self.cpoint == 'p1':
            self.p1 = (event.x, event.y)
        elif self.cpoint == 'p2':
            self.p2 = (event.x, event.y)
        elif self.cpoint == 'p3':
            self.p3 = (event.x, event.y)

        self.canvas.delete("all")
        self.draw_points()

    def choose_color(self, event: tk.Event):
        if self.in_point(self.p1, event.x, event.y):
            self.c1 = colorchooser.askcolor()[1]
        elif self.in_point(self.p2, event.x, event.y):
            self.c2 = colorchooser.askcolor()[1]
        elif self.in_point(self.p3, event.x, event.y):
            self.c3 = colorchooser.askcolor()[1]

        self.canvas.delete("all")
        self.draw_points()


if __name__ == "__main__":
    App()
