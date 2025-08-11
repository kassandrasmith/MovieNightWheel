import tkinter as tk
import math
import random


###############################################################################


# Function to create a wheel
def create_wheel(canvas, slices, weights, rotation_angle=0):
    canvas.delete("all")  # Clear canvas
    winner = ""
    total_weight = sum(weights)  # Total weight to normalize the slices
    angle_per_weight = 360 / total_weight  # Angle per weight unit
    start_angle = rotation_angle  # Set the start angle based on rotation_angle

    slice_colors = ['#EE7EA0', '#FF9797', '#D20000', '#FD5E00', '#FFA07A', '#FFCC80', '#EEB649', '#F7CE15', '#BCC07B', '#C1DB9E', '#669E63', '#007D75', '#ADD2CA', '#D5EDf8', '#ABCDDE', '#B5BEF5', '#CDBDEB', '#F6E7FF']
    color_count = len(slice_colors)  # Number of colors available


    for i, weight in enumerate(weights):
        end_angle = start_angle + (weight * angle_per_weight)    #calculate the angle for this slice
        fill_color = slice_colors[i % color_count - 1] #cycle through the colors
        # Draw each slice as a wedge (arc)
        canvas.create_arc(0, 500, 500, 0, start=start_angle, extent=(end_angle - start_angle), fill=fill_color, outline=fill_color, width=2)
        start_angle = end_angle  # Update the start angle for the next slice

    # Create labels that move with the slices
    start_angle = rotation_angle
    for i, weight in enumerate(weights):
        end_angle = start_angle + (weight * angle_per_weight)
        mid_angle = (start_angle + end_angle) / 2  # Get the center angle of the slice

        start_unit_circle = start_angle % 360
        end_unit_circle = end_angle % 360

        # Calculate label position based on the mid-angle
        label_y = 250 + 125 * math.cos(math.radians(mid_angle + 90))
        label_x = 250 + 125 * math.sin(math.radians(mid_angle + 90))

        # Draw the label at the correct position
        canvas.create_text(label_x, label_y, text=f'{slices[i] + " " + str(weights[i])}', fill='#000042', font=('Roboto', 10, 'normal'), angle=mid_angle)
        start_angle = end_angle
        if (start_unit_circle > 220) and (end_unit_circle < 90):
            winner = slices[i]

    # Draw the stationary marker at the center of the wheel (0,0 position)
    canvas.create_line(500, 250, 480, 250, fill='black', width=2, arrow='last')
    #canvas.create_oval(240, 240, 260, 260, fill='#EE7EA0')
    return winner


def increment_weights(arr):
    for i in range(len(arr)):
        if arr[i] > 5:
            arr[i] += 1
    return arr


def write_new_movie_list(slices, weights):
    with open("movies.pwif", "w") as file:
        for i in range(len(slices)):
            if weights[i] < 9:
                file.write(slices[i] + ',' + "1" + "\n")
            else:
                file.write(slices[i] + ',' + str(weights[i]) + "\n")


# Function to spin the wheel
def spin_wheel(canvas, slices, weights):
    total_weight = sum(weights)
    spin_angle = random.randint(0, 360)  # Random starting angle
    rotation_duration = 2000  # Duration of the spin in ms
    frame_count = 60  # Number of frames for the animation

    # Animation loop
    def animate_spin(frame):
        # Calculate the rotation angle at this frame (counterclockwise direction)
        rotation_angle = 360 + ((spin_angle + (frame / frame_count) * 360) % 360)
        winner = create_wheel(canvas, slices, weights, rotation_angle)  # Draw the wheel with the updated angle

        if frame < frame_count:
            canvas.after(rotation_duration // frame_count, animate_spin, frame + 1)
        elif frame == frame_count:
            final_angle = (spin_angle - 360) % 360  # Final angle after the full spin
            canvas.create_rectangle(500, 500, 0, 460, fill='#bfd7ed')
            canvas.create_text(250, 480, text=winner, font=('Roboto', 14, 'bold'), fill='#000042', activefill='#0074b7')

    animate_spin(0)  # Start the animation from frame 0


# Function to handle button click and spin the wheel
def on_spin_button_click(canvas, slices, weights):
    spin_wheel(canvas, slices, weights)


def on_add_button_click(canvas, slices, weights):
    new_movie = entry.get()
    slices.append(new_movie)
    weights = increment_weights(weights)
    weights.append(10)
    create_wheel(canvas, slices, weights)
    write_new_movie_list(slices, weights)


def get_slices():
    movies = []
    weights = []
    with open("movies.pwif", "r") as file:
        for line in file:
            movie, weight = line.split(',')
            movies.append(movie)
            weights.append(int(weight))
    return movies, weights


# Function to get the input text
def get_text():
    text = entry.get()
    print("Input:", text)


##############################################################################################################################
# Setup the main window
root = tk.Tk()
root.title("Spinning Wheel")

# Create a canvas widget
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

slices, weights = get_slices()

# Draw the wheel initially
create_wheel(canvas, slices, weights)
#canvas.create_oval(220, 220, 280, 280, fill='#bfd7ed')

# Add a Spin button
spin_button = tk.Button(root, text="Spin Wheel", command=lambda: on_spin_button_click(canvas, slices, weights))
spin_button.pack()

# Create an Entry widget
entry = tk.Entry(root, width=30)
entry.pack()

add_button = tk.Button(root, text="Add Movie", command=lambda: on_add_button_click(canvas, slices, weights))
add_button.pack()

# Run the application
root.mainloop()