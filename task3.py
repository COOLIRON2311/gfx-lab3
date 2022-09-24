import tkinter as tk
from tkinter import colorchooser

Point = tuple[int, int]
TkColor = str

DIM = 500

class App(tk.Tk):
    canvas: tk.Canvas
    r1: Point
    r2: Point
    r3: Point
    c1: TkColor = 'red'
    c2: TkColor = 'green'
    c3: TkColor = 'blue'
    R: int = 10 # radius

    def __init__(self):
        super().__init__()
        self.title("Task 3")
        self.geometry(f"{DIM}x{DIM}")
        self.resizable(False, False)
        self.canvas = tk.Canvas(self, width=DIM, height=DIM)
        self.r1 = (100, 100)
        self.r2 = (300, 100)
        self.r3 = (100, 300)
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.move_point)
        self.canvas.bind("<Button-3>", self.choose_color)
        self.draw_points()
        self.mainloop()

    def draw_points(self):
        self.canvas.create_oval(self.r1[0], self.r1[1], self.r1[0] + self.R, self.r1[1] + self.R, fill=self.c1)
        self.canvas.create_oval(self.r2[0], self.r2[1], self.r2[0] + self.R, self.r2[1] + self.R, fill=self.c2)
        self.canvas.create_oval(self.r3[0], self.r3[1], self.r3[0] + self.R, self.r3[1] + self.R, fill=self.c3)

    def in_point(self, p: Point, x: int, y: int) -> bool:
        return (x - p[0]) ** 2 + (y - p[1]) ** 2 <= self.R ** 2

    def move_point(self, event: tk.Event):
        if self.in_point(self.r1, event.x, event.y):
            self.r1 = (event.x, event.y)
        elif self.in_point(self.r2, event.x, event.y):
            self.r2 = (event.x, event.y)
        elif self.in_point(self.r3, event.x, event.y):
            self.r3 = (event.x, event.y)

        self.canvas.delete("all")
        self.draw_points()

    def choose_color(self, event: tk.Event):
        if self.in_point(self.r1, event.x, event.y):
            self.c1 = colorchooser.askcolor()[1]
        elif self.in_point(self.r2, event.x, event.y):
            self.c2 = colorchooser.askcolor()[1]
        elif self.in_point(self.r3, event.x, event.y):
            self.c3 = colorchooser.askcolor()[1]

        self.canvas.delete("all")
        self.draw_points()

if __name__ == "__main__":
    App()
