import tkinter as tk
import numpy as np
import argparse

class ReconstructorRDP:
    def __init__(self, args):
        self.root = tk.Tk()
        self.root.title("Reconstruct Drawing")

        self.data_name = args.data_name

        self.canvas_init()

    def canvas_init(self):
        self.canvas = tk.Canvas(self.root, width=256, height=256, bg="white")
        self.canvas.pack()

        if args.from_file :
            self.load_button = tk.Button(self.root, text="Load and Reconstruct Drawing", command=self.load_and_reconstruct_from_file)
            self.load_button.pack()
        else :
            self.load_button = tk.Button(self.root, text="Load and Reconstruct Drawing", command=self.load_and_reconstruct_from_data)
            self.load_button.pack()

    def reconstruct_drawing(self, data):
        if len(data) == 0:
            print("No input data.")
            return

        for i in range(len(data) - 1):
            x1, y1, pen_state1 = data[i]
            x2, y2, pen_state2 = data[i + 1]
            if pen_state1 == 0:
                self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    def load_and_reconstruct_from_data(self):
        try:
            data = np.load(data_var_name)
            self.reconstruct_drawing(data)
        except FileNotFoundError:
            print("No saved data file found.")

    def load_and_reconstruct_from_file(self):
        try:
            data = np.load(self.data_name)
            self.reconstruct_drawing(data)
        except FileNotFoundError:
            print("No saved data file found.")

    def run(self):
        self.root.mainloop()
        root = tk.Tk()
        root.title("Reconstruct Drawing")
        root.mainloop()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    # Evaluation input filepaths
    parser.add_argument("--from_file", type=bool, default=True)
    parser.add_argument("--data_name", type=str, default="")
    parser.add_argument('--savefile_name', type=str, help='set output file name', default='extracted_array.npy')
    args = parser.parse_args()

    reconstructor = ReconstructorRDP(args)
    reconstructor.run()