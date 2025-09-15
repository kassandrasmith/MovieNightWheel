import math
import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedTk
from wheel import Wheel, PWIF

def enter_data():
    for name, var in checklist_names.items():
        if var.get():
            index = attendance.slices.index(name)
            #if attendance.weights[index] < 10:
            attendance.weights[index] += 1
            print(attendance.slices[index] + ',' + str(attendance.weights[index]))
    attendance.write_list_to_file()
    name_wheel.draw(0)

def launch_wheel():
    name_wheel.draw(0)

def spin_wheel():
    name_wheel.spin()

def winner_wheel_spin():
    filename = "Wheels/" + name_wheel.winner  # str()? tostring?
    print(filename)
    winnerPWIF = PWIF(filename)
    winners_movies = winnerPWIF.slices
    winners_weights = winnerPWIF.weights
    # canvas2 = tk.Canvas(root, width=500, height=500)
    global winner_wheel
    winner_wheel = Wheel(wheel_canvas, winners_movies, winners_weights, filename)
    winner_wheel.draw(0)
    winner_wheel.spin()
    index = attendance.slices.index(name_wheel.winner)
    attendance.weights[index] = 1
    attendance.write_list_to_file()



def override_click():
    new_winner = entry.get()
    filename = "Wheels/" + new_winner
    new_winner_PWIF = PWIF(filename)
    new_winner_weights = new_winner_PWIF.weights
    new_winner_movies = new_winner_PWIF.slices

    new_winner_pwif = PWIF(filename)
    new_winner_weights = new_winner_pwif.weights
    new_winner_movies = new_winner_pwif.slices

    new_winner_wheel = Wheel(wheel_canvas, new_winner_movies, new_winner_weights, filename)
    new_winner_wheel.draw(0)
    new_winner_wheel.spin()

def add_movie():
    print(winner_wheel.winner)
    Big_Wheel = PWIF("movies.pwif")
    Big_Wheel.slices.append(winner_wheel.winner)

    Big_Wheel.increment_weights()
    Big_Wheel.weights.append(10)
    Big_Wheel.write_list_to_file()

#WHERE DID THE CHANGE OF WEIGHT TO ONE GO PLEASE

def remove_movie():
    ##CURRENT SPOT
    filename = "Wheels/" + name_wheel.winner  # str()? tostring?
    print(filename)
    winnerPWIF = PWIF(filename)
    winners_movies = winnerPWIF.slices

    global winner_wheel
    index = winners_movies.index(winner_wheel.winner)
    winnerPWIF.slices.remove(winner_wheel.winner)

    del winnerPWIF.weights[index]
    winnerPWIF.write_list_to_file()

root = ThemedTk(theme="equilux")
color = ttk.Style().lookup(root.get_themes(), "background", default="white")

root.configure(background=color)
root.title("Attendance")

canvas = tk.Canvas(root, width=700, height=700, bg=color)
canvas.grid(sticky='NSEW')

wheel_canvas = tk.Canvas(root, width=510, height=500, bg=color)
wheel_canvas.grid(sticky='NSEW')

rowvar = 0
winner = ""
attendance = PWIF("Wheels/Whose Wheel.pwif")
names = attendance.slices
weights = attendance.weights
checklist_names = {}

ttk.Label(canvas, text="Select attendees:").grid(row=rowvar, pady=5)
# Checkboxes
for name in names:
    #three columns
    colvar = rowvar % 3
    rowvar += 1

    half = round(len(names) / 2)

    var = tk.BooleanVar()
    checklist_names[name] = var

    ttk.Checkbutton(canvas, text=name, variable=var).grid(row=math.ceil(rowvar/3), column=colvar, padx=5, pady=5, sticky=tk.W)
    # if rowvar > half:
    #     rowvar = 1
    # if names.index(name) < half:
    #     ttk.Checkbutton(canvas, text=name, variable=var).grid(row=rowvar, column=0, padx=5, pady=5, sticky=tk.W)
    # else:
    #     ttk.Checkbutton(canvas, text=name, variable=var).grid(row=rowvar, column=1, padx=5, pady=5, sticky=tk.W)

name_wheel = Wheel(wheel_canvas, names, weights, 'Wheels/Whose Wheel.pwif')
winner_wheel = Wheel(wheel_canvas, "", "", "")

# Buttons
ttk.Button(canvas, text="Enter Data", command= enter_data).grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
ttk.Button(canvas, text="Spin Wheel", command= lambda: spin_wheel()).grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)
ttk.Button(canvas, text="Manual Override:", command= override_click).grid(row=11, column=0, padx=5, pady=5, sticky=tk.W)
entry = ttk.Entry(canvas)
entry.grid(row=12, column=0, padx=5, pady=5, sticky=tk.W)
ttk.Button(canvas, text="Launch Winner's Wheel", command= winner_wheel_spin).grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)
ttk.Button(canvas, text="Add movie to main wheel", command= add_movie).grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
ttk.Button(canvas, text="Remove movie from personal wheel", command= remove_movie).grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
root.mainloop()