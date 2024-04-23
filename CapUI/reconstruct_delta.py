import tkinter as tk
import numpy as np
import rdp_tmp

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

def load_and_reconstruct_drawing(canvas):
    try:
        #deltas = np.load("mouse_deltas.npy")
        deltas = np.load('mouse_deltas.npy')
        print(deltas)
        reconstruct_drawing(canvas, deltas)
        #simplified = rdp_tmp.rdp(deltas, 2.0)

    except FileNotFoundError:
        print("No saved deltas file found.")

def main():
    root = tk.Tk()
    root.title("Reconstruct Drawing")

    canvas = tk.Canvas(root, width=256, height=256, bg="white")
    canvas.pack()

    load_button = tk.Button(root, text="Load and Reconstruct Drawing", command=lambda: load_and_reconstruct_drawing(canvas))
    load_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
