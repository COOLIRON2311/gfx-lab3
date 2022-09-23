import tkinter as tk
from dataclasses import dataclass
from enum import Enum
from tkinter import filedialog
from PIL import Image, ImageTk
Color = tuple[int, int, int]


class Direction(Enum):
    Down = 0
    DownRight = 1
    Right = 2
    UpRight = 3
    Up = 4
    UpLeft = 5
    Left = 6
    DownLeft = 7

    def apply_to(self, point: 'Point') -> 'Point':
        match self:
            case Direction.Down:
                return Point(point.x, point.y + 1)
            case Direction.DownRight:
                return Point(point.x + 1, point.y + 1)
            case Direction.Right:
                return Point(point.x + 1, point.y)
            case Direction.UpRight:
                return Point(point.x + 1, point.y - 1)
            case Direction.Up:
                return Point(point.x, point.y - 1)
            case Direction.UpLeft:
                return Point(point.x - 1, point.y - 1)
            case Direction.Left:
                return Point(point.x - 1, point.y)
            case Direction.DownLeft:
                return Point(point.x - 1, point.y + 1)

    def counter_clockwise90(self):
        return Direction((self.value - 2) % 8)

    def next(self):
        return Direction((self.value + 1) % 8)

@dataclass
class Point:
    TOLERANCE = 10
    x: int
    y: int
    # flag: bool

    def get_col(self, img: Image.Image) -> Color:
        return img.getpixel((self.x, self.y))

    def compare(self, img, col2: Color) -> float:
        col1 = self.get_col(img)
        return sum((col1[i] - col2[i]) ** 2 for i in range(3)) ** 0.5

    def neighborhood(self, direction: 'Direction'):
        yield (direction, direction.apply_to(self))
        i = direction.next()
        while i != direction:
            yield (i, i.apply_to(self))
            i = i.next()

    def next_point(self, img: Image.Image, direction: 'Direction', col: Color):
        for d, p in self.neighborhood(direction):
            if p.x < 0 or p.y < 0 or p.x >= img.width or p.y >= img.height:
                continue
            if p.compare(img, col) < self.TOLERANCE:
                return (d, p)
        return (direction, None)

    def in_bounds(self, img: Image.Image):
        return 0 <= self.x < img.width and 0 <= self.y < img.height

    def init_outline(self, img: Image.Image, col: Color):
        st = self
        while st.in_bounds(img) and st.compare(img, col) < self.TOLERANCE:
            st = Point(st.x+1, st.y)
        st = Point(st.x-1, st.y)

        while st.in_bounds(img) and st.compare(img, col) < self.TOLERANCE:
            st = Point(st.x, st.y-1)
        st = Point(st.x, st.y+1)
        return st


class App(tk.Tk):
    canvas: tk.Canvas
    img: Image.Image
    imgtk: ImageTk.PhotoImage
    color: Color = None

    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.create_widgets()
        self.mainloop()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=100, height=10)
        self.scale = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL,
                              label='Tolerance', command=self.set_tolerance)
        self.button_open = tk.Button(self, text='Open image', command=self.open_image)
        self.canvas.pack()
        self.scale.pack(padx=10, pady=10)
        self.button_open.pack(padx=10, pady=10)
        self.scale.set(Point.TOLERANCE)
        self.canvas.bind('<Button-1>', self.select_color)
        self.canvas.bind('<Button-3>', self.select_point)
        self.bind('<Escape>', self.clear)

    def open_image(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        self.img = Image.open(path).convert('RGB')
        self.imgtk = ImageTk.PhotoImage(self.img)
        self.canvas.config(width=self.img.width, height=self.img.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imgtk)
        self.scale.config(length=self.img.width - 20)

    def set_tolerance(self, value):
        Point.TOLERANCE = int(value)

    def select_color(self, event: tk.Event):
        self.color = self.img.getpixel((event.x, event.y))

    def select_point(self, event: tk.Event):
        if self.color and self.img:
            points = self.select_region(event.x, event.y)
            for p in points:
                self.canvas.create_line(p.x, p.y, p.x+1, p.y, fill='black')

    def select_region(self, x, y) -> list[Point]:
        st = Point(x, y).init_outline(self.img, self.color)
        d = Direction.Down
        p = st
        points = [st]
        while True:
            d, np = p.next_point(self.img, d.counter_clockwise90(), self.color)
            if np is None or np == st:
                break
            points.append(np)
            p = np
        return points

    def clear(self, _):
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imgtk)


if __name__ == '__main__':
    App()
