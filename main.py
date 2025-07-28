import random
import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedTk
from wheel import Wheel, PWIF

def wheel_spin():
    bookWheel.spin()


root = ThemedTk(theme="equilux")
color = ttk.Style().lookup(root.get_themes(), "background", default="white")
canvas = tk.Canvas(root, width=800, height=800, bg=color)
canvas.pack()

root.configure(background=color)
root.title("Book Club")

wheel_canvas = tk.Canvas(root, width=510, height=500, bg=color)
wheel_canvas.pack()

bookList = PWIF('Wheels/BookWheel')
bookWheel = Wheel(wheel_canvas, bookList.slices, bookList.weights, 'Wheels/BookWheel')
bookWheel.color = color
bookWheel.angle = random.randint(0,360)
bookWheel.draw(bookWheel.angle)
ttk.Button(canvas, text="Spin Wheel", command=wheel_spin).pack()

root.mainloop()