import tkinter as tk
import numpy as np
import sys

def reconstruct_drawing(canvas, deltas):
    if len(deltas) == 0:
        print("no input strokes")
        return
        
    start_x = start_y = current_x = current_y = 0
    for dx, dy, mouse_button_pressed in deltas:
        # Update current coordinates
        current_x += dx
        current_y += dy

        # If the mouse button was pressed, draw a line
        if not mouse_button_pressed:
            canvas.create_line(start_x, start_y, current_x, current_y, fill="black", width=2)
        
        start_x, start_y = current_x, current_y

def load_and_reconstruct_drawing(canvas, filename):
    try:
        deltas = np.load(filename)
        reconstruct_drawing(canvas, deltas)
    except FileNotFoundError:
        print("No saved deltas file found.")

def main(filename):
    root = tk.Tk()
    root.title("Reconstruct Drawing")

    canvas = tk.Canvas(root, width=400, height=400, bg="white")
    canvas.pack()

    load_button = tk.Button(root, text="Load and Reconstruct Drawing", command=lambda: load_and_reconstruct_drawing(canvas, filename))
    load_button.pack()

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    main(filename)
