import tkinter as tk
import numpy as np

def reconstruct_drawing(canvas, data):
    if len(data) == 0:
        print("No input data.")
        return
    
    for i in range(len(data) - 1):
        x1, y1, pen_state1 = data[i]
        x2, y2, pen_state2 = data[i + 1]
        if pen_state1 == 0:
            canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

def load_and_reconstruct_drawing(canvas, data_name):
    try:
        data = np.load(data_name)
        reconstruct_drawing(canvas, data)
    except FileNotFoundError:
        print("No saved data file found.")

def main():
    root = tk.Tk()
    root.title("Reconstruct Drawing")

    canvas = tk.Canvas(root, width=256, height=256, bg="white")
    canvas.pack()
    
    #data_name = "mouse_coords.npy"
    data_name = "extracted_array.npy"
    load_button = tk.Button(root, text="Load and Reconstruct Drawing", command=lambda: load_and_reconstruct_drawing(canvas, data_name))
    load_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
