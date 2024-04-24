import tkinter as tk
import numpy as np
import argparse

class MousePainter:
    def __init__(self, args):
        self.root = None
        # --savefile_name to change the name of the stroke npy file
        self.save_file_name = args.savefile_name

        self.last_x = 0
        self.last_y = 0

        self.is_pressed = False

        # ( dx, dy, penstate )
        self.deltas = []

        # initialize canvas
        self.canvas_draw_init()

    # Initialize for stroke drawing
    def canvas_draw_init(self):
        self.root = tk.Tk()
        self.root.title("Drawing with Mouse")

        # initialize all drawings
        self.last_x = 0
        self.last_y = 0
        self.is_pressed = False
        self.deltas = []

        self.canvas = tk.Canvas(self.root, width=256, height=256, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.start_paint)
        self.canvas.bind("<ButtonRelease-1>", self.stop_paint)
        self.canvas.bind("<B1-Motion>", self.paint)

        self.erase_button = tk.Button(self.root, text="Erase", command=self.canvas_draw_init)
        self.erase_button.pack(side="left")

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_application)
        self.exit_button.pack(side="left")

        self.save_button = tk.Button(self.root, text="Save Deltas", command=self.save_deltas)
        self.save_button.pack(side="left")

    # Use deltas[] if it's length > 0. Or load the saved data.
    def get_data(self):
        if len(self.deltas) > 0 :
            data = self.deltas
        else :
            data = np.load(self.save_file_name)
        return data

    def canvas_reconstruct_init(self):
        self.root = tk.Tk()
        self.root.title("Reconstruct Drawing")

        self.canvas = tk.Canvas(self.root, width=256, height=256, bg="white")
        self.canvas.pack()

        self.load_and_reconstruct()

    def load_and_reconstruct(self):
        try:
            data = self.get_data()
            self.reconstruct_drawing(data)
        except FileNotFoundError:
            print("No saved data file found.")

    def reconstruct_drawing(self, data):
        if len(data) == 0:
            print("No input data.")
            return

        for i in range(len(data) - 1):
            x1, y1, pen_state1 = data[i]
            x2, y2, pen_state2 = data[i + 1]
            if pen_state1 == 0:
                self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    def exit_application(self):
        self.root.quit()

    def start_paint(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.deltas.append((dx, dy, not self.is_pressed))
        self.last_x, self.last_y = event.x, event.y
        self.is_pressed = True

    def stop_paint(self, event):
        self.is_pressed = False

    def paint(self, event):
        x, y = event.x, event.y
        dx = x - self.last_x
        dy = y - self.last_y
        self.deltas.append((dx, dy, not self.is_pressed))
        if self.is_pressed:
            self.canvas.create_line((self.last_x, self.last_y, x, y), fill="black", width=2)
        self.last_x, self.last_y = x, y

    def save_deltas(self):
        np.save( self.save_file_name, np.array(self.deltas))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Evaluation input filepaths
    parser.add_argument('--savefile_name', type=str, help='set output file name', default='mouse_deltas.npy')
    args = parser.parse_args()

    painter = MousePainter(args)
    painter.run()

