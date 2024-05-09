import tkinter as tk
import numpy as np


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


def load_and_reconstruct_drawing(canvas, filename="/Users/yoonjiwon/PycharmProjects/demo_1st/CapUI/airplane.npz"):
    try:
        canvas.delete("all")
        #deltas = np.load("mouse_deltas.npy")
        #deltas = np.load('../mouse_deltas.npy')
        #deltas = np.load('../rdp_deltas.npy')
        #deltas = np.load('../ai_deltas.npy')
        deltas = np.load(filename, encoding='latin1', allow_pickle=True)
        print(deltas["test"][1])
        deltas = deltas["test"][1]

        # Calculate the sum of each column
        column_sums = np.sum(deltas, axis=0)

        # Find the minimum and maximum sums for each column
        min_column_sum = np.min(column_sums, axis=1)
        max_column_sum = np.max(column_sums, axis=1)

        print("Minimum sum for each column:", min_column_sum)
        print("Maximum sum for each column:", max_column_sum)

        # reconstruct_drawing(canvas, deltas)
        # simplified = rdp_tmp.rdp(deltas, 2.0)

    except FileNotFoundError:
        print("No saved deltas file found.")


def main():
    root = tk.Tk()
    root.title("Reconstruct Drawing")

    canvas = tk.Canvas(root, width=256, height=256, bg="white")
    canvas.pack()

    load_button = tk.Button(root, text="Load and Reconstruct Drawing",
                            command=lambda: load_and_reconstruct_drawing(canvas))
    load_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
