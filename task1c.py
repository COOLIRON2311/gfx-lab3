import tkinter as tk
from dataclasses import dataclass
from queue import Queue
from tkinter import filedialog
from PIL import Image, ImageTk

Color = tuple[int, int, int]


@dataclass
class Point:
    x: int
    y: int
    flag: bool

    def get_col(self, img: Image.Image) -> Color:
        return img.getpixel((self.x, self.y))

    def compare(self, img, col2: Color) -> float:
        col1 = self.get_col(img)
        return sum((col1[i] - col2[i]) ** 2 for i in range(3)) ** 0.5


class App(tk.Tk):
    TOLERANCE = 0.1
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
        self.button_open = tk.Button(self, text='Open image', command=self.open_image)
        self.canvas.pack()
        self.button_open.pack(padx=10, pady=10)
        self.canvas.bind('<Button-1>', self.select_color)
        self.canvas.bind('<Button-3>', self.select_point)

    def open_image(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        self.img = Image.open(path).convert('RGB')
        self.imgtk = ImageTk.PhotoImage(self.img)
        self.canvas.config(width=self.img.width, height=self.img.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imgtk)

    def select_color(self, event: tk.Event):
        self.color = self.img.getpixel((event.x, event.y))

    def select_point(self, event: tk.Event):
        if self.color and self.img:
            points = self.select_region(event.x, event.y)
            for p in points:
                self.canvas.create_rectangle(p.x, p.y, p.x + 1, p.y + 1, fill='red')

    def select_region(self, x, y) -> list[Point]:
        # q: Queue[Point] = Queue()
        st = Point(x, y, False)
        points = []

        while st.compare(self.img, self.color) < self.TOLERANCE:
            st = Point(st.x, st.y+1, False)
        st = Point(st.x, st.y-1, False)

        points.append(st)
        return points


if __name__ == '__main__':
    App()
