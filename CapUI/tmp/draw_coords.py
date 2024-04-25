import tkinter as tk
import numpy as np

def start_paint(event):
    global last_x, last_y, is_pressed
    coords.append((last_x, last_y, not is_pressed))
    last_x, last_y = event.x, event.y
    is_pressed = True

def stop_paint(event):
    global is_pressed
    is_pressed = False

def paint(event):
    global last_x, last_y, is_pressed
    x, y = event.x, event.y
    coords.append((x, y, not is_pressed))
    if is_pressed:
        canvas.create_line((last_x, last_y, x, y), fill="black", width=2)
    last_x, last_y = x, y

def save_coords():
    np.save("../mouse_coords.npy", np.array(coords))

def main():
    global root, canvas, coords, last_x, last_y, is_pressed
    root = tk.Tk()
    root.title("Drawing with Mouse")

    last_x = last_y = 0
    is_pressed = False
    coords = []

    canvas = tk.Canvas(root, width=400, height=400, bg="white")
    canvas.pack()

    canvas.bind("<Button-1>", start_paint)
    canvas.bind("<ButtonRelease-1>", stop_paint)
    canvas.bind("<B1-Motion>", paint)

    save_button = tk.Button(root, text="Save Coordinates", command=save_coords)
    save_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
