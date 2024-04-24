import tkinter as tk
import numpy as np
import argparse

class MousePainter:
    def __init__(self, args):
        self.root = tk.Tk()
        # drawing frame, RDP frame, AI frame
        self.frame_draw = tk.Frame(self.root)
        self.frame_RDP = tk.Frame(self.root)
        self.frame_AI = tk.Frame(self.root)
        # --savefile_name to change the name of the stroke npy file
        self.save_file_name = 'mouse_deltas.npy'
        self.rdp_file_name = 'rdp_deltas.npy'
        self.ai_file_name = 'ai_deltas.npy'

        self.last_x = 0
        self.last_y = 0
        self.is_pressed = False

        # ( dx, dy, penstate )
        self.deltas = []

        # initialize canvas
        self.frame_draw_init()
        self.frame_RDP_init()
        self.frame_AI_init()

    # initialize last_x, last_y, is_pressed, deltas
    def init_drawing_vars(self):
        # initialize all drawings
        self.last_x = 0
        self.last_y = 0
        self.is_pressed = False
        self.deltas = []

    # Initialize for stroke drawing
    # button !!!!!!
    def frame_draw_init(self):
        self.frame_draw.root = self.root
        self.frame_draw.root.title("Drawing with Mouse")

        self.frame_draw.canvas = tk.Canvas(self.frame_draw.root, width=256, height=256, bg="white")
        self.frame_draw.canvas.pack()

        self.frame_draw.canvas.bind("<Button-1>", self.start_paint)
        self.frame_draw.canvas.bind("<ButtonRelease-1>", self.stop_paint)
        self.frame_draw.canvas.bind("<B1-Motion>", self.paint)

        self.frame_draw.erase_button = tk.Button(self.frame_draw.root, text="Erase", command=self.init_drawing_vars)
        self.frame_draw.erase_button.pack(side="left")

        self.frame_draw.exit_button = tk.Button(self.frame_draw.root, text="Exit", command=self.exit_application)
        self.frame_draw.exit_button.pack(side="left")

        self.frame_draw.save_button = tk.Button(self.frame_draw.root, text="Save Deltas", command=self.save_deltas)
        self.frame_draw.save_button.pack(side="left")

    # button Implementation!!!!!!
    def frame_RDP_init(self):
        self.frame_RDP.root = self.root
        self.frame_RDP.root.title("Drawing after RDP")

        self.frame_RDP.canvas = tk.Canvas(self.frame_RDP.root, width=256, height=256, bg="white")
        self.frame_RDP.canvas.pack()

        self.frame_RDP.next_button = tk.Button(self.frame_RDP.root, text="Next", command=self.init_drawing_vars)
        self.frame_RDP.next_button.pack(side="left")

        self.frame_RDP.exit_button = tk.Button(self.frame_RDP.root, text="Exit", command=self.exit_application)
        self.frame_RDP.exit_button.pack(side="left")

        self.load_and_reconstruct()

    # load npy file and draw
    def load_and_reconstruct(self, filename='mouse_deltas.npy'):
        try:
            self.deltas = np.load(filename)
            self.reconstruct_drawing()
        except FileNotFoundError:
            print("No saved data file found.")


    def reconstruct_drawing(self, framename=''):
        data = self.deltas
        if len(data) == 0:
            print("No input data.")
            return

        for i in range(len(data) - 1):
            x1, y1, pen_state1 = data[i]
            x2, y2, pen_state2 = data[i + 1]
            if pen_state1 == 0:
                self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

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

    def exit_application(self):
        self.root.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Evaluation input filepaths
    parser.add_argument('--savefile_name', type=str, help='set output file name', default='mouse_deltas.npy')
    args = parser.parse_args()

    painter = MousePainter(args)
    painter.run()

