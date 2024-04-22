import tkinter as tk
import numpy as np

def start_paint(event):
    global last_x, last_y, is_pressed
    dx = event.x - last_x
    dy = event.y - last_y
    deltas.append((dx, dy, not is_pressed))
    last_x, last_y = event.x, event.y
    is_pressed = True

def stop_paint(event):
    global is_pressed
    last_x, last_y = event.x, event.y
    is_pressed = False

def paint(event):
    global last_x, last_y, is_pressed
    x, y = event.x, event.y
    dx = x - last_x
    dy = y - last_y
    deltas.append((dx, dy, not is_pressed))
    if is_pressed:
        canvas.create_line((last_x, last_y, x, y), fill="black", width=2)
    last_x, last_y = x, y

def save_deltas():
    np.save("mouse_deltas.npy", np.array(deltas))

def main():
    global root, canvas, deltas, last_x, last_y, is_pressed
    root = tk.Tk()
    root.title("Drawing with Mouse")

    last_x = last_y = 0
    is_pressed = False
    deltas = []

    canvas = tk.Canvas(root, width=400, height=400, bg="white")
    canvas.pack()

    canvas.bind("<Button-1>", start_paint)
    canvas.bind("<ButtonRelease-1>", stop_paint)
    canvas.bind("<B1-Motion>", paint)

    save_button = tk.Button(root, text="Save Deltas", command=save_deltas)
    save_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
